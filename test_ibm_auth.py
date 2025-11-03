"""
IBM Cloud Authentication Diagnostic Tool
Helps troubleshoot IBM watsonx.ai authentication issues
"""

import requests
import json
import config

def test_ibm_connection():
    """Test IBM Cloud IAM authentication"""
    
    print("=" * 80)
    print("IBM CLOUD AUTHENTICATION DIAGNOSTIC")
    print("=" * 80)
    
    # Check if credentials are loaded
    print("\n1️⃣  Checking credentials...")
    if not config.IBM_API_KEY:
        print("❌ IBM_API_KEY is empty!")
        return False
    if not config.IBM_PROJECT_ID:
        print("❌ IBM_PROJECT_ID is empty!")
        return False
    
    print(f"✅ IBM_API_KEY loaded: {config.IBM_API_KEY[:30]}...")
    print(f"✅ IBM_PROJECT_ID loaded: {config.IBM_PROJECT_ID}")
    
    # Test IAM token endpoint
    print("\n2️⃣  Testing IBM Cloud IAM token endpoint...")
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": config.IBM_API_KEY
    }
    
    try:
        print(f"   POST {url}")
        print(f"   Headers: {headers}")
        print(f"   Data: grant_type=..., apikey={config.IBM_API_KEY[:30]}...")
        
        response = requests.post(url, headers=headers, data=data, timeout=10)
        
        print(f"\n   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        print(f"   Response Body: {response.text[:200]}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token", "")
            print(f"\n✅ Successfully obtained access token!")
            print(f"   Token (first 50 chars): {access_token[:50]}...")
            return True
        else:
            print(f"\n❌ Failed to get token")
            print(f"   Error: {response.text}")
            
            # Provide troubleshooting suggestions
            if response.status_code == 400:
                print("\n💡 TROUBLESHOOTING TIPS for 400 Error:")
                print("   - API key may be invalid or expired")
                print("   - API key format might be incorrect")
                print("   - Try regenerating the API key in IBM Cloud console")
                print("   - Verify the API key has no extra whitespace")
            elif response.status_code == 401:
                print("\n💡 TROUBLESHOOTING TIPS for 401 Error:")
                print("   - API key is not valid")
                print("   - Service might be disabled")
                print("   - Check IBM Cloud account status")
            elif response.status_code == 429:
                print("\n💡 TROUBLESHOOTING TIPS for 429 Error:")
                print("   - Rate limit exceeded")
                print("   - Wait a moment and try again")
            
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ Connection Error: {e}")
        print("   Cannot reach IBM Cloud. Check:")
        print("   - Internet connection")
        print("   - Firewall/Proxy settings")
        print("   - IBM Cloud service status")
        return False
    except requests.exceptions.Timeout as e:
        print(f"\n❌ Timeout Error: {e}")
        print("   Request took too long. Check network connection.")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = test_ibm_connection()
    print("\n" + "=" * 80)
    if success:
        print("✅ IBM Cloud authentication is working!")
    else:
        print("❌ IBM Cloud authentication failed - see above for details")
    print("=" * 80)
