
#!/usr/bin/env python3
"""
Test script to verify all API endpoints are working correctly.
"""

import requests
import json
import time

def test_endpoints(base_url="http://localhost:5000"):
    """Test all API endpoints."""
    print(f"🧪 Testing API endpoints at {base_url}")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print(f"   ❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: Create document
    print("\n2. Testing document creation...")
    test_doc = {
        "title": "Test Document",
        "body": "This is a test document for API verification",
        "author": "Test Script"
    }
    try:
        response = requests.post(f"{base_url}/docs", 
                               json=test_doc,
                               headers={"Content-Type": "application/json"})
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            doc_data = response.json()
            doc_id = doc_data.get('doc_id')
            print(f"   ✅ Document created with ID: {doc_id}")
            
            # Test 3: Get document
            print(f"\n3. Testing document retrieval...")
            get_response = requests.get(f"{base_url}/docs/{doc_id}")
            print(f"   Status: {get_response.status_code}")
            if get_response.status_code == 200:
                print("   ✅ Document retrieved successfully")
            else:
                print(f"   ❌ Document retrieval failed: {get_response.text}")
            
            # Test 4: Update document
            print(f"\n4. Testing document update...")
            updated_doc = {
                "title": "Updated Test Document",
                "body": "This document has been updated",
                "author": "Test Script",
                "status": "updated"
            }
            put_response = requests.put(f"{base_url}/docs/{doc_id}",
                                       json=updated_doc,
                                       headers={"Content-Type": "application/json"})
            print(f"   Status: {put_response.status_code}")
            if put_response.status_code == 200:
                print("   ✅ Document updated successfully")
            else:
                print(f"   ❌ Document update failed: {put_response.text}")
            
            # Test 5: Search documents
            print(f"\n5. Testing document search...")
            search_response = requests.get(f"{base_url}/docs/search?q=test")
            print(f"   Status: {search_response.status_code}")
            if search_response.status_code == 200:
                print("   ✅ Document search completed")
            else:
                print(f"   ❌ Document search failed: {search_response.text}")
            
            # Test 6: Get audit log
            print(f"\n6. Testing audit log...")
            audit_response = requests.get(f"{base_url}/docs/{doc_id}/audit")
            print(f"   Status: {audit_response.status_code}")
            if audit_response.status_code == 200:
                print("   ✅ Audit log retrieved successfully")
            else:
                print(f"   ❌ Audit log failed: {audit_response.text}")
        else:
            print(f"   ❌ Document creation failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Document creation error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Testing completed")

if __name__ == "__main__":
    test_endpoints()
