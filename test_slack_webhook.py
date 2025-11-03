"""
Slack Webhook Diagnostic Tool
Helps troubleshoot Slack integration issues
"""

import requests
import json
import config

def test_slack_webhook():
    """Test Slack webhook connection and message delivery"""
    
    print("=" * 80)
    print("SLACK WEBHOOK DIAGNOSTIC")
    print("=" * 80)
    
    # Check if webhook URL is configured
    print("\n1️⃣  Checking Slack configuration...")
    if not config.SLACK_WEBHOOK_URL:
        print("❌ SLACK_WEBHOOK_URL is empty!")
        return False
    
    print(f"✅ SLACK_WEBHOOK_URL configured")
    print(f"   URL (masked): {config.SLACK_WEBHOOK_URL[:50]}...{config.SLACK_WEBHOOK_URL[-10:]}")
    
    # Validate URL format
    if not config.SLACK_WEBHOOK_URL.startswith('https://hooks.slack.com/'):
        print("⚠️  Warning: URL doesn't look like a valid Slack webhook")
    
    # Test webhook connection
    print("\n2️⃣  Testing webhook connection...")
    
    test_payload = {
        "text": "🧪 Test Message from 3MITM Diagnostic",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*3MITM Slack Webhook Test*\n✅ If you see this, the webhook is working!"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "_Test sent from diagnostic tool_"
                    }
                ]
            }
        ]
    }
    
    try:
        print(f"   Sending test message to {config.SLACK_WEBHOOK_URL[:50]}...")
        response = requests.post(
            config.SLACK_WEBHOOK_URL,
            json=test_payload,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Body: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ Slack webhook is working correctly!")
            print("   Message should appear in your Slack channel now.")
            return True
        else:
            print(f"\n❌ Webhook returned status {response.status_code}")
            
            if response.status_code == 404:
                print("   Error: Webhook URL not found (404)")
                print("   💡 The webhook may have been deleted or the URL is incorrect")
                print("   💡 Try regenerating the webhook in Slack")
            elif response.status_code == 410:
                print("   Error: Webhook has been deleted (410)")
                print("   💡 You need to create a new incoming webhook in Slack")
            elif response.status_code == 400:
                print("   Error: Bad request (400)")
                print("   💡 The message format may be invalid")
                print(f"   Response: {response.text}")
            
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        print("   Cannot reach Slack. Check:")
        print("   - Internet connection")
        print("   - Firewall/Proxy settings")
        print("   - Slack service status")
        return False
    except requests.exceptions.Timeout as e:
        print(f"❌ Timeout error: {e}")
        print("   Request took too long. Check network connection.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_slack_webhook()
    print("\n" + "=" * 80)
    if success:
        print("✅ Slack webhook is configured and working!")
    else:
        print("❌ Slack webhook has issues - see above for details")
    print("=" * 80)
