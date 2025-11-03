"""
Configuration for Demo/Fallback Mode
When real APIs are unavailable, use mock/demo data for demonstrations
"""

# Enable demo mode for presentations/videos when APIs are unavailable
DEMO_MODE = True

# Demo settings
DEMO_JIRA_TICKET_ID = "SMS-001"
DEMO_SLACK_WEBHOOK_SUCCESS = True
DEMO_AI_RESPONSE_DELAY = 1  # seconds
