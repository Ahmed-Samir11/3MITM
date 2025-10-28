"""
Jira Integration Module
Handles creation of Jira tickets for detected vulnerabilities
"""

from jira import JIRA
import config

# Initialize Jira client
jira_client = JIRA(
    server=config.JIRA_SERVER,
    basic_auth=(config.JIRA_EMAIL, config.JIRA_API_TOKEN)
)


def create_jira_ticket(vulnerability_data, code_fix):
    """
    Create a Jira ticket for a detected vulnerability
    
    Args:
        vulnerability_data (dict): Dictionary containing vulnerability analysis results
        code_fix (str): Generated secure code to fix the vulnerability
        
    Returns:
        Issue: Created Jira issue object
    """
    # Format summary
    summary = f"[AI-Detected] {vulnerability_data['vulnerability_type']} - {vulnerability_data['severity']} Severity"
    
    # Format description using Jira markup
    description = f"""h2. Vulnerability Details
*Type:* {vulnerability_data['vulnerability_type']}
*Severity:* {vulnerability_data['severity']}
*Affected Parameter:* {vulnerability_data['affected_parameter']}

h3. Description
{vulnerability_data['description']}

h3. Recommendation
{vulnerability_data['recommendation']}

h2. AI-Generated Secure Code Fix
{{code:java}}
{code_fix}
{{code}}

---
_This ticket was automatically created by the DevSecOps AI Agent._
"""
    
    # Create the issue
    # Note: Using 'Task' as default issue type (most common in Jira)
    # If your project uses different issue types, update this accordingly
    issue_dict = {
        'project': {'key': config.JIRA_PROJECT_KEY},
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Task'}  # Changed from 'Bug' to 'Task'
    }
    
    # Don't include priority as it's not available in all Jira configurations
    # Priority can be set manually in Jira if needed
    
    new_issue = jira_client.create_issue(fields=issue_dict)
    
    return new_issue


def _map_severity_to_priority(severity):
    """
    Map vulnerability severity to Jira priority
    
    Args:
        severity (str): Vulnerability severity (Critical/High/Medium/Low)
        
    Returns:
        str: Jira priority name
    """
    severity_map = {
        'Critical': 'Highest',
        'High': 'High',
        'Medium': 'Medium',
        'Low': 'Low'
    }
    return severity_map.get(severity, 'Medium')
