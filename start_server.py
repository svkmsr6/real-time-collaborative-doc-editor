#!/usr/bin/env python3
"""
Start the Redis Document Management Flask Server

This script starts the Flask server for the rdoc_module with proper error handling.
"""

import sys

# Import and run the Flask app at the top-level
try:
    from rdoc_module import app
except ImportError as e:
    print(f"❌ Failed to import rdoc_module: {e}")
    print("💡 Make sure you're in the correct directory and Flask is installed")
    print("   Try: pip install flask redis")
    sys.exit(1)

def main():
    """Start the Flask server."""
    print("🚀 Starting Redis Document Management Server")
    print("=" * 50)

    print("✅ Flask app imported successfully")
    print("🌐 Starting server on http://localhost:5000")
    print("📋 Available endpoints:")
    print("   POST   /docs              - Create document")
    print("   PUT    /docs/<id>         - Update document")
    print("   GET    /docs/search?q=... - Search documents")
    print("   GET    /docs/<id>/audit   - Get document history")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 50)

    try:
        # Start the Flask app
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()