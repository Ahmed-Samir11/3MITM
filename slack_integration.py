"""
Slack Integration Module
Handles sending rich alerts to Slack using Block Kit
"""

from slack_sdk.webhook import WebhookClient
import config


def send_slack_alert(jira_issue_key, jira_server_url, vulnerability_data):
    """
    Send a richly formatted Slack alert for a detected vulnerability
    
    Args:
        jira_issue_key (str): The Jira issue key (e.g., "PROJ-125")
        jira_server_url (str): The Jira server URL
        vulnerability_data (dict): Dictionary containing vulnerability analysis results
    """
    webhook = WebhookClient(config.SLACK_WEBHOOK_URL)
    
    # Determine severity color
    color_map = {
        'Critical': '#FF0000',  # Red
        'High': '#FF6B00',      # Orange
        'Medium': '#FFD700',    # Gold
        'Low': '#36A64F'        # Green
    }
    severity_color = color_map.get(vulnerability_data.get('severity', 'Medium'), '#808080')
    
    # Construct Jira issue URL
    jira_issue_url = f"{jira_server_url}/browse/{jira_issue_key}"
    
    # Build Block Kit message
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🚨 Security Vulnerability Detected",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Type:*\n{vulnerability_data.get('vulnerability_type', 'Unknown')}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Severity:*\n{vulnerability_data.get('severity', 'Unknown')}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Affected Parameter:*\n{vulnerability_data.get('affected_parameter', 'N/A')}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Jira Ticket:*\n<{jira_issue_url}|{jira_issue_key}>"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Description:*\n{vulnerability_data.get('description', 'No description available')}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Recommendation:*\n{vulnerability_data.get('recommendation', 'No recommendation available')}"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View Jira Ticket",
                        "emoji": True
                    },
                    "url": jira_issue_url,
                    "style": "primary"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "🤖 _Automatically detected and remediated by DevSecOps AI Agent_"
                }
            ]
        }
    ]
    
    # Send the message
    response = webhook.send(
        text=f"Security Vulnerability Detected: {vulnerability_data.get('vulnerability_type', 'Unknown')}",
        blocks=blocks,
        attachments=[
            {
                "color": severity_color,
                "fallback": f"New vulnerability detected: {jira_issue_key}"
            }
        ]
    )
    
    return response
