
#!/usr/bin/env python3
"""
Start the Redis Document Management Server
"""
import sys
import os

def main():
    print("🚀 Starting Redis Document Management Server")
    print("=" * 50)
    
    try:
        # Import the Flask app from the module
        from rdoc_module import app
        print("✅ Flask app imported successfully")
        
        # Start the server
        print("🌐 Starting server on http://0.0.0.0:5000")
        print("📋 Available endpoints:")
        print("   GET    /                  - Health check")
        print("   POST   /docs              - Create document")
        print("   GET    /docs/<id>         - Get document")
        print("   PUT    /docs/<id>         - Update document")
        print("   GET    /docs/search?q=... - Search documents")
        print("   GET    /docs/<id>/audit   - Get document history")
        print()
        print("💡 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run the Flask app
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except ImportError as e:
        print(f"❌ Failed to import Flask app: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
