"""
Script to check available issue types in your Jira project
"""

from jira import JIRA
import config

print("\n" + "="*80)
print("Checking Jira Project Configuration")
print("="*80)

# Initialize Jira client
try:
    print(f"\n[1/3] Connecting to Jira: {config.JIRA_SERVER}")
    jira_client = JIRA(
        server=config.JIRA_SERVER,
        basic_auth=(config.JIRA_EMAIL, config.JIRA_API_TOKEN)
    )
    print("✓ Connected successfully")
except Exception as e:
    print(f"✗ Failed to connect: {str(e)}")
    exit(1)

# Get project info
try:
    print(f"\n[2/3] Fetching project: {config.JIRA_PROJECT_KEY}")
    project = jira_client.project(config.JIRA_PROJECT_KEY)
    print(f"✓ Project found: {project.name}")
except Exception as e:
    print(f"✗ Failed to get project: {str(e)}")
    exit(1)

# Get available issue types
try:
    print(f"\n[3/3] Fetching available issue types...")
    # Use createmeta for Jira Cloud
    createmeta = jira_client.createmeta(
        projectKeys=config.JIRA_PROJECT_KEY,
        expand='projects.issuetypes'
    )
    
    if not createmeta or 'projects' not in createmeta or not createmeta['projects']:
        print("✗ No project metadata found")
        exit(1)
    
    project_meta = createmeta['projects'][0]
    issue_types = project_meta.get('issuetypes', [])
    
    print(f"\n✓ Available issue types in '{config.JIRA_PROJECT_KEY}' project:\n")
    
    for issue_type in issue_types:
        print(f"  • {issue_type['name']}")
        if 'description' in issue_type and issue_type['description']:
            print(f"    Description: {issue_type['description']}")
    
    # Recommend the best one for security issues
    print("\n" + "="*80)
    print("RECOMMENDATION:")
    
    # Priority order: Bug, Task, Story
    preferred_types = ['Bug', 'Task', 'Story', 'Issue']
    recommended = None
    
    for pref in preferred_types:
        for issue_type in issue_types:
            if issue_type['name'] == pref:
                recommended = pref
                break
        if recommended:
            break
    
    if not recommended and issue_types:
        recommended = issue_types[0]['name']
    
    if recommended:
        print(f"\n  Use issue type: '{recommended}'")
        print(f"\n  Update jira_integration.py line ~54 to:")
        print(f"    'issuetype': {{'name': '{recommended}'}}")
    
    print("="*80 + "\n")
    
except Exception as e:
    print(f"✗ Failed to get issue types: {str(e)}")
    exit(1)
