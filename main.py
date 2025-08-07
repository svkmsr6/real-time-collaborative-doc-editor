#!/usr/bin/env python3
"""
Main entry point for Replit deployment
Redis Document Management Flask Server
"""

import os
import sys

# Set environment variables for Replit
os.environ['FLASK_ENV'] = 'production'

# Import and configure the Flask app
try:
    from rdoc_module import app
    print("✅ Flask app imported successfully")
except ImportError as e:
    print(f"❌ Failed to import rdoc_module: {e}")
    print("💡 Make sure all dependencies are installed")
    sys.exit(1)

def main():
    """Start the Flask server for Replit."""
    print("🚀 Starting Redis Document Management Server on Replit")
    print("=" * 60)

    # Get port from environment (Replit sets this automatically)
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'  # Required for Replit

    print(f"🌐 Starting server on {host}:{port}")
    print("📋 Available endpoints:")
    print("   POST   /docs              - Create document")
    print("   PUT    /docs/<id>         - Update document") 
    print("   GET    /docs/search?q=... - Search documents")
    print("   GET    /docs/<id>/audit   - Get document history")
    print("=" * 60)

    try:
        # Start the Flask app (disable debug for production)
        app.run(host=host, port=port, debug=False)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()