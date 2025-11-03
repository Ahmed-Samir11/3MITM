"""
Jira Authentication and Permissions Diagnostic Tool
Helps troubleshoot Jira integration issues
"""

import config
from jira import JIRA

def test_jira_connection():
    """Test Jira authentication and permissions"""
    
    print("=" * 80)
    print("JIRA AUTHENTICATION & PERMISSIONS DIAGNOSTIC")
    print("=" * 80)
    
    # Check if credentials are loaded
    print("\n1️⃣  Checking Jira credentials...")
    if not config.JIRA_SERVER:
        print("❌ JIRA_SERVER is empty!")
        return False
    if not config.JIRA_EMAIL:
        print("❌ JIRA_EMAIL is empty!")
        return False
    if not config.JIRA_API_TOKEN:
        print("❌ JIRA_API_TOKEN is empty!")
        return False
    if not config.JIRA_PROJECT_KEY:
        print("❌ JIRA_PROJECT_KEY is empty!")
        return False
    
    print(f"✅ JIRA_SERVER: {config.JIRA_SERVER}")
    print(f"✅ JIRA_EMAIL: {config.JIRA_EMAIL}")
    print(f"✅ JIRA_API_TOKEN: {config.JIRA_API_TOKEN[:30]}...")
    print(f"✅ JIRA_PROJECT_KEY: {config.JIRA_PROJECT_KEY}")
    
    # Test Jira connection
    print("\n2️⃣  Testing Jira Cloud connection...")
    try:
        jira_client = JIRA(
            server=config.JIRA_SERVER,
            basic_auth=(config.JIRA_EMAIL, config.JIRA_API_TOKEN)
        )
        print("✅ Successfully connected to Jira Cloud")
        
        # Get current user
        print("\n3️⃣  Checking authenticated user...")
        try:
            current_user = jira_client.current_user()
            print(f"✅ Authenticated as: {current_user}")
        except Exception as e:
            print(f"⚠️  Could not retrieve current user: {e}")
        
        # Check project permissions
        print(f"\n4️⃣  Checking permissions for project '{config.JIRA_PROJECT_KEY}'...")
        try:
            project = jira_client.project(config.JIRA_PROJECT_KEY)
            print(f"✅ Project found: {project.name}")
            print(f"   Project Key: {project.key}")
            print(f"   Project ID: {project.id}")
            
            # Try to get available issue types
            print("\n5️⃣  Checking available issue types...")
            try:
                issue_types = project.issueTypes
                print(f"✅ Available issue types:")
                for issue_type in issue_types:
                    print(f"   - {issue_type.name} (ID: {issue_type.id})")
            except Exception as e:
                print(f"⚠️  Could not retrieve issue types: {e}")
            
            # Try to list custom fields
            print("\n6️⃣  Checking project fields...")
            try:
                fields = jira_client.fields()
                print(f"✅ Available fields:")
                for field in fields[:10]:  # Show first 10
                    print(f"   - {field['name']} (ID: {field['id']})")
                print(f"   ... and {len(fields) - 10} more fields")
            except Exception as e:
                print(f"⚠️  Could not retrieve fields: {e}")
            
            # Try to create a test issue (in a safe way)
            print("\n7️⃣  Attempting to create a test issue...")
            try:
                issue_dict = {
                    'project': {'key': config.JIRA_PROJECT_KEY},
                    'summary': '[TEST] 3MITM Permission Check',
                    'description': 'This is a test issue to verify create permissions.',
                    'issuetype': {'name': 'Bug'},
                }
                
                test_issue = jira_client.create_issue(fields=issue_dict)
                print(f"✅ Successfully created test issue: {test_issue.key}")
                print(f"   You have permission to create issues!")
                
                # Clean up - delete the test issue
                try:
                    test_issue.delete()
                    print(f"✅ Cleaned up test issue")
                except Exception as e:
                    print(f"⚠️  Could not delete test issue (but it was created): {e}")
                
                return True
                
            except Exception as create_error:
                print(f"❌ Cannot create issues in this project")
                print(f"   Error: {str(create_error)}")
                
                # Provide troubleshooting suggestions
                error_msg = str(create_error).lower()
                if "permission" in error_msg or "401" in error_msg:
                    print("\n💡 TROUBLESHOOTING TIPS:")
                    print("   1. Check your API token has 'write' scope")
                    print("   2. Verify your account has 'Create Issues' permission")
                    print("   3. Try regenerating the API token in Jira settings")
                    print("   4. Ensure your Jira account is not locked")
                    print("   5. Check project settings - may restrict issue creation")
                elif "project" in error_msg:
                    print("\n💡 TROUBLESHOOTING TIPS:")
                    print("   1. Verify JIRA_PROJECT_KEY is correct")
                    print("   2. Check if project exists and is accessible")
                    print("   3. Try listing projects you have access to")
                elif "issue type" in error_msg:
                    print("\n💡 TROUBLESHOOTING TIPS:")
                    print("   1. Project may not have 'Bug' issue type")
                    print("   2. Try using 'Task' or 'Story' instead")
                    print("   3. Check available issue types above")
                
                return False
                
        except Exception as project_error:
            print(f"❌ Could not access project {config.JIRA_PROJECT_KEY}")
            print(f"   Error: {str(project_error)}")
            return False
        
    except Exception as e:
        print(f"❌ Failed to connect to Jira")
        print(f"   Error: {str(e)}")
        print("\n💡 TROUBLESHOOTING TIPS:")
        print("   1. Verify JIRA_SERVER URL is correct (include https://)")
        print("   2. Check JIRA_EMAIL and JIRA_API_TOKEN are valid")
        print("   3. Ensure your API token has not expired")
        print("   4. Check network connection to Jira")
        return False

if __name__ == "__main__":
    success = test_jira_connection()
    print("\n" + "=" * 80)
    if success:
        print("✅ Jira is configured correctly and you have create permissions!")
    else:
        print("❌ Jira configuration has issues - see above for details")
    print("=" * 80)
