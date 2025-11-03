# 3MITM Setup Instructions

## Prerequisites

- Python 3.9+
- Git
- API credentials for: IBM watsonx.ai, Jira Cloud, Slack

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ahmed-Samir11/3MITM.git
cd 3MITM
```

### 2. Create Virtual Environment

```bash
python -m venv ibm
ibm\Scripts\Activate.ps1  # On PowerShell
# or
source ibm/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your API credentials:

```
IBM_API_KEY=your_ibm_watsonx_api_key
IBM_PROJECT_ID=your_ibm_project_id
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your_email@example.com
JIRA_API_TOKEN=your_jira_api_token
JIRA_PROJECT_KEY=YOUR_PROJECT_KEY
SLACK_WEBHOOK_URL=your_slack_webhook_url
```

### 5. Verify Configuration

```bash
python config.py
```

If successful, you'll see no errors. If credentials are missing, the script will tell you what's needed.

## Getting Your API Credentials

### IBM watsonx.ai

1. Visit [IBM Cloud Console](https://cloud.ibm.com)
2. Create an API key in **Manage > Access (IAM) > API keys**
3. Create a watsonx.ai project and get the Project ID

### Jira Cloud

1. Go to [Jira Cloud](https://www.atlassian.com/software/jira)
2. Create API token in **Account settings > Security > Create API token**
3. Get your Jira server URL and project key

### Slack

1. Go to [Slack API](https://api.slack.com)
2. Create an incoming webhook in **Your Apps > Create New App**
3. Copy the webhook URL

## Running the Project

### Terminal 1: Start Defense System

```bash
.\ibm\Scripts\Activate.ps1
python ingestion_api.py
```

### Terminal 2: Run Advanced Test

```bash
.\ibm\Scripts\Activate.ps1
python advanced_3mitm_test.py
```

## Security Notes

- **Never commit `.env` file** - it's in `.gitignore`
- Always use `.env.example` as template for credentials
- Rotate API keys regularly
- Use different credentials for development/production
- Keep `.env` in local machine only

## Troubleshooting

**Missing environment variables error?**
- Ensure `.env` file exists in project root
- Verify all required variables are set
- Check for typos in variable names

**API authentication fails?**
- Verify credentials in `.env` are correct
- Check if API keys have expired
- Regenerate tokens if needed

**Connection errors?**
- Ensure APIs are accessible from your network
- Check firewall/proxy settings
- Verify URLs in `.env` are correct

