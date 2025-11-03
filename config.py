"""
Configuration file for DevSecOps AI Agent
All secrets are loaded from environment variables (.env file)
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# IBM watsonx.ai Configuration
IBM_API_KEY = os.getenv("IBM_API_KEY", "")
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID", "")

# Jira Configuration
JIRA_SERVER = os.getenv("JIRA_SERVER", "")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "")

# Slack Configuration
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# Ingestion API Configuration
INGESTION_API_ENDPOINT = os.getenv("INGESTION_API_ENDPOINT", "http://127.0.0.1:5000/api/traffic")

# Validation check
def validate_config():
    """Validate that all required environment variables are set"""
    required_vars = [
        "IBM_API_KEY",
        "IBM_PROJECT_ID",
        "JIRA_SERVER",
        "JIRA_EMAIL",
        "JIRA_API_TOKEN",
        "JIRA_PROJECT_KEY",
        "SLACK_WEBHOOK_URL"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(
            f"Missing environment variables: {', '.join(missing_vars)}\n"
            f"Please copy .env.example to .env and fill in your credentials"
        )
