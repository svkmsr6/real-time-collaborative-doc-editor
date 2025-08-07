"""
Redis JSON Document Management with Full-Text Search and Real-Time Updates
This module provides a RESTful API for managing JSON documents in Redis
with full-text search capabilities using Redisearch.
It supports creating, updating, and searching documents, as well as real-time updates via Pub/Sub.
It also includes an example of real-time document editing using WebSockets.
It uses Redis Streams for auditing document changes.
It is designed to work with Redis Cloud and requires the redis-py and redisearch-py libraries.
"""
import os
import json
import threading
import redis
import dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Try multiple Redis Search import strategies
SEARCH_AVAILABLE = False
IndexDefinition = None
IndexType = None
field = None

# Strategy 1: Try modern redis-py with search (version 5.x)
try:
    from redis.commands.search.field import TextField
    from redis.commands.search import IndexDefinition, IndexType
    SEARCH_AVAILABLE = True
    print("✅ Redis Search modules imported successfully (redis-py 5.x)")
except ImportError:
    try:
        # Strategy 2: Try older redis-py search syntax
        from redis.commands.search.field import TextField
        from redis.commands.search.indexDefinition import IndexDefinition, IndexType
        SEARCH_AVAILABLE = True
        print("✅ Redis Search modules imported successfully (redis-py older)")
    except ImportError:
        try:
            # Strategy 3: Direct FT commands (fallback)
            SEARCH_AVAILABLE = True
            TextField = None
            IndexDefinition = None
            IndexType = None
            print("✅ Using direct FT commands for Redis Search")
        except ImportError as e:
            SEARCH_AVAILABLE = False
            TextField = None
            IndexDefinition = None
            IndexType = None
            print(f"⚠️  Redis Search not available: {e}")

app = Flask(__name__)
# Configure CORS for Replit and web access
CORS(app, 
     origins=["*"],  # Allow all origins for development
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

dotenv.load_dotenv()

RDS_HOST = os.environ.get("RDS_HOST", "localhost")
RDS_PORT = int(os.environ.get("RDS_PORT", 6379))
RDS_PASSWORD = os.environ.get("RDS_PASSWORD", "")

# Enhanced Redis connection for Redis Cloud with flexible SSL support
def create_redis_connection():
    """Create Redis connection with fallback for different SSL configurations."""
    connection_configs = [
        # First try: No SSL (many Redis Cloud instances don't use SSL on standard ports)
        {
            "host": RDS_HOST,
            "port": RDS_PORT, 
            "password": RDS_PASSWORD, 
            "decode_responses": False,  # Important: JSON module handles its own encoding
            "ssl": False
        },
        # Second try: SSL with no certificate verification
        {
            "host": RDS_HOST,
            "port": RDS_PORT, 
            "password": RDS_PASSWORD, 
            "decode_responses": False,  # Important: JSON module handles its own encoding
            "ssl": True,
            "ssl_cert_reqs": None,
            "ssl_check_hostname": False
        },
        # Third try: SSL with minimal verification
        {
            "host": RDS_HOST,
            "port": RDS_PORT, 
            "password": RDS_PASSWORD, 
            "decode_responses": False,  # Important: JSON module handles its own encoding
            "ssl": True,
            "ssl_cert_reqs": "none"
        }
    ]
    for i, config in enumerate(connection_configs, 1):
        try:
            print(f"🔄 Trying connection method {i}...")
            r = redis.Redis(**config)
            r.ping()  # Test the connection
            ssl_status = "with SSL" if config.get("ssl") else "without SSL"
            print(f"✅ Connected to Redis at {RDS_HOST}:{RDS_PORT} ({ssl_status})")
            return r
        except Exception as e:
            print(f"❌ Connection method {i} failed: {e}")
            continue

    # If all methods fail, raise the last exception
    raise redis.ConnectionError(f"Failed to connect to Redis. Host: {RDS_HOST}:{RDS_PORT}")

try:
    r = create_redis_connection()
except redis.ConnectionError as e:
    print(f"❌ Failed to connect to Redis: {e}")
    print(f"   Host: {RDS_HOST}")
    print(f"   Port: {RDS_PORT}")
    print("   Check your Redis Cloud connection details and network connectivity")
    raise
except Exception as e:
    print(f"❌ Unexpected error connecting to Redis: {e}")
    raise

# --- Full-text search: CONFIGURE Redisearch index on document fields
def create_search_index():
    """Create a Redisearch index for document fields."""
    global SEARCH_AVAILABLE
    if not SEARCH_AVAILABLE:
        print("⚠️  Skipping search index creation - Redis Search not available")
        return
        
    try:
        # Try to create index using raw Redis commands for maximum compatibility
        # This works with most Redis instances that support FT commands
        try:
            # Try to create JSON index using FT.CREATE command directly
            r.execute_command(
                'FT.CREATE', 'idx:docs',
                'ON', 'JSON',
                'PREFIX', '1', 'doc:',
                'SCHEMA',
                '$.title', 'AS', 'title', 'TEXT',
                '$.body', 'AS', 'body', 'TEXT'
            )
            print("✅ Search index created successfully using FT.CREATE")
        except redis.ResponseError as e:
            if "Index already exists" in str(e):
                print("ℹ️  Search index already exists")
            else:
                # Try alternative approach for Hash-based indexing
                print(f"JSON indexing failed, trying hash-based approach: {e}")
                r.execute_command(
                    'FT.CREATE', 'idx:docs_hash',
                    'ON', 'HASH',
                    'PREFIX', '1', 'doc:',
                    'SCHEMA',
                    'title', 'TEXT',
                    'body', 'TEXT'
                )
                print("✅ Search index created successfully using HASH indexing")
    except redis.ResponseError as e:
        if "Index already exists" in str(e):
            print("ℹ️  Search index already exists")
        else:
            print(f"❌ Error creating search index: {e}")
            print("⚠️  Continuing without search functionality")
            SEARCH_AVAILABLE = False
    except Exception as e:
        print(f"⚠️  Search index creation failed: {e}")
        print("⚠️  Continuing without search functionality")
        SEARCH_AVAILABLE = False

create_search_index()

# --- Health Check Endpoint for Replit
@app.route('/')
@app.route('/health')
def health_check():
    """Health check endpoint for Replit and monitoring."""
    try:
        # Test Redis connection
        r.ping()
        return jsonify({
            "status": "healthy",
            "service": "Redis Document Management API",
            "version": "1.0.0",
            "redis": "connected",
            "endpoints": {
                "create_document": "POST /docs",
                "update_document": "PUT /docs/<id>",
                "search_documents": "GET /docs/search?q=...",
                "get_audit_history": "GET /docs/<id>/audit"
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "redis": "disconnected"
        }), 503

# --- Create Document (Primary DB/NoSQL)
@app.route('/docs', methods=['POST'])
def create_doc():
    """Create a new document in Redis JSON store."""
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    body = request.json
    if not body:
        return jsonify({"error": "Empty request body"}), 400

    try:
        doc_id = r.incr("next_doc_id")
        doc_key = f'doc:{doc_id}'
        # Redis JSON should accept Python dict directly
        r.json().set(doc_key, '$', body)
        return jsonify({"doc_id": doc_id})
    except Exception as e:
        print(f"Error creating document: {e}")
        return jsonify({"error": "Failed to create document"}), 500

# --- Get Document
@app.route('/docs/<int:doc_id>', methods=['GET'])
def get_doc(doc_id):
    """Get a specific document by ID."""
    try:
        if doc_id <= 0:
            return jsonify({"error": "Invalid document ID"}), 400

        doc_key = f'doc:{doc_id}'
        if not r.exists(doc_key):
            return jsonify({"error": "Document not found"}), 404

        json_data = r.json().get(doc_key, '$')
        if json_data and len(json_data) > 0:
            doc = json_data[0] if isinstance(json_data, list) else json_data
            return jsonify(doc), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        print(f"Error getting document {doc_id}: {e}")
        return jsonify({"error": "Failed to get document"}), 500

# --- Edit Document and Broadcast to Pub/Sub, Store in Stream
@app.route('/docs/<int:doc_id>', methods=['PUT'])
def update_doc(doc_id):
    """Update an existing document and broadcast changes."""
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    changes = request.json
    if not changes:
        return jsonify({"error": "Empty request body"}), 400

    try:
        doc_key = f'doc:{doc_id}'
        # Check if document exists
        if not r.exists(doc_key):
            return jsonify({"error": "Document not found"}), 404

        # Redis JSON should accept Python dict directly
        r.json().set(doc_key, '$', changes)
        # Publish update for real-time frontends
        r.publish(f'docs:{doc_id}:updates', json.dumps(changes))
        # Append to stream for auditing - flatten the changes for stream storage
        stream_data = {}
        for key, value in changes.items():
            # Convert complex values to JSON strings for stream storage
            if isinstance(value, (dict, list)):
                stream_data[key] = json.dumps(value)
            else:
                stream_data[key] = str(value)
        r.xadd(f'doc:{doc_id}:stream', stream_data)
        return jsonify({"status": "updated"})
    except Exception as e:
        print(f"Error updating document {doc_id}: {e}")
        return jsonify({"error": "Failed to update document"}), 500

# --- Real-time editing: Example WebSocket/PubSub handling pseudocode

def listen_for_doc_updates(doc_id):
    """Listen for real-time updates on a document using Pub/Sub."""
    pubsub = r.pubsub()
    pubsub.subscribe(f'docs:{doc_id}:updates')
    for msg in pubsub.listen():
        print(f"Update: {msg['data']}") # In prod, emit to frontend via websocket

# --- Full-Text Search
@app.route('/docs/search', methods=['GET'])
def search_docs():
    """Search documents using Redisearch."""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify([]), 200

        if not SEARCH_AVAILABLE:
            return jsonify({"error": "Search functionality not available"}), 503

        # Use FT.SEARCH command directly for maximum compatibility
        search_query = f"*{query}*"  # Wildcard search
        
        try:
            # Try JSON index first
            results = r.execute_command('FT.SEARCH', 'idx:docs', search_query)
        except Exception as json_error:
            try:
                # Fallback to hash index
                results = r.execute_command('FT.SEARCH', 'idx:docs_hash', search_query)
            except Exception as hash_error:
                print(f"Both search methods failed - JSON: {json_error}, Hash: {hash_error}")
                return jsonify([]), 200
        
        docs = []
        if len(results) > 1:  # First element is count
            # Parse results (skip count at index 0)
            for i in range(1, len(results), 2):
                doc_id = results[i].decode('utf-8') if isinstance(results[i], bytes) else results[i]
                try:
                    # Get JSON data from Redis
                    json_data = r.json().get(doc_id, '$')
                    if json_data and len(json_data) > 0:
                        # json_data is a list, get the first element
                        parsed_doc = json_data[0] if isinstance(json_data, list) else json_data
                        docs.append(parsed_doc)
                except Exception as e:
                    print(f"Error parsing document {doc_id}: {e}")
                    continue
        
        return jsonify(docs), 200
    except Exception as e:
        print(f"Search endpoint error: {e}")
        return jsonify({"error": "Search failed"}), 500

# --- Get document edit history (Streams)
@app.route('/docs/<int:doc_id>/audit', methods=['GET'])
def get_audit(doc_id):
    """Get the edit history of a document."""
    try:
        # Validate doc_id
        if doc_id <= 0:
            return jsonify({"error": "Invalid document ID"}), 400

        events = r.xrange(f'doc:{doc_id}:stream')
        audit_log = []
        for event in events:
            # Decode the event ID
            event_id = event[0].decode('utf-8') if isinstance(event[0], bytes) else event[0]

            # Handle the event data dictionary
            event_values = {}
            for key, value in event[1].items():
                # Decode bytes keys and values
                decoded_key = key.decode('utf-8') if isinstance(key, bytes) else key

                # Handle different types of values
                if isinstance(value, bytes):
                    try:
                        # Try to decode as UTF-8 string
                        decoded_value = value.decode('utf-8')
                        # Try to parse as JSON if it looks like JSON
                        if decoded_value.startswith(('{', '[', '"')) or decoded_value in ('true', 'false', 'null'):
                            try:
                                decoded_value = json.loads(decoded_value)
                            except json.JSONDecodeError:
                                pass  # Keep as string if not valid JSON
                    except UnicodeDecodeError:
                        # If UTF-8 decoding fails, convert to string representation
                        decoded_value = str(value)
                else:
                    decoded_value = value

                event_values[decoded_key] = decoded_value

            audit_log.append({"id": event_id, "values": event_values})

        return jsonify(audit_log), 200
    except Exception as e:
        print(f"Error getting audit log for document {doc_id}: {e}")
        print(f"Error type: {type(e).__name__}")
        return jsonify({"error": "Failed to get audit log"}), 500

# Debug: Print registered routes
print("🔍 Registered Flask routes:")
for rule in app.url_map.iter_rules():
    methods = ','.join(rule.methods - {'OPTIONS', 'HEAD'})
    print(f"   {methods:<10} {rule.rule}")

# Export the app for external imports
__all__ = ['app']

if __name__ == '__main__':
    threading.Thread(target=listen_for_doc_updates, args=(1,)).start()
    app.run(host='0.0.0.0', port=5000, debug=True)
