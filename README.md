# DevSecOps AI Agent - Hackathon Project

A complete Python application that automatically detects vulnerabilities in HTTP traffic using IBM watsonx.ai, generates secure code fixes, and integrates with Jira and Slack.

## 🚀 Setup Instructions

### 1. Activate Virtual Environment
```powershell
.\ibm\Scripts\Activate.ps1
```

### 2. Configure Credentials
Edit `config.py` and replace the placeholder values with your actual credentials:

- **IBM watsonx.ai**: `IBM_API_KEY`, `IBM_PROJECT_ID`
- **Jira**: `JIRA_SERVER`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY`
- **Slack**: `SLACK_WEBHOOK_URL`

### 3. Run the Application

#### Start the Flask Ingestion API
```powershell
python ingestion_api.py
```

The API will start on `http://127.0.0.1:5000`

#### Run mitmproxy (in a separate terminal)
```powershell
.\ibm\Scripts\Activate.ps1
mitmdump -s forward_traffic.py
```

This starts mitmproxy on `http://localhost:8080`

### 4. Configure Your Application
Set your browser or application to use the mitmproxy as its HTTP proxy:
- **Proxy Host**: `localhost`
- **Proxy Port**: `8080`

## 📁 Project Structure

```
3MITM/
├── requirements.txt              # Python dependencies
├── config.py                     # Configuration and secrets
├── openapi-trafficanalysis-skill.yaml  # API specification
├── ibm_watsonx_client.py        # IBM watsonx.ai integration
├── jira_integration.py          # Jira ticket creation
├── slack_integration.py         # Slack notifications
├── ingestion_api.py             # Main Flask orchestrator
├── forward_traffic.py           # mitmproxy script
└── ibm/                         # Virtual environment
```

## 🔄 How It Works

1. **Traffic Interception**: mitmproxy intercepts HTTP/HTTPS traffic and forwards it to the ingestion API
2. **AI Analysis**: watsonx.ai analyzes the traffic for security vulnerabilities
3. **Code Generation**: If a vulnerability is found, AI generates secure code to fix it
4. **Jira Integration**: Creates a detailed ticket with the vulnerability and fix
5. **Slack Notification**: Sends a rich alert to your Slack channel

## 🛠️ Key Features

- ✅ Asynchronous processing (non-blocking)
- ✅ AI-powered vulnerability detection
- ✅ Automated secure code generation
- ✅ Jira ticket creation with rich formatting
- ✅ Slack Block Kit alerts
- ✅ Framework detection
- ✅ Production-ready error handling

## 📝 API Endpoints

### POST /api/traffic
Receives intercepted HTTP traffic for analysis.

**Request Body:**
```json
{
  "method": "POST",
  "url": "https://api.example.com/login",
  "headers": {"Content-Type": "application/json"},
  "body": "{\"username\":\"admin\"}",
  "response_status": 200,
  "response_headers": {"Content-Type": "application/json"},
  "response_body": "{\"token\":\"abc123\"}"
}
```

**Response:** `202 Accepted`

## 🧪 Testing

You can test the API directly using curl:

```powershell
curl -X POST http://127.0.0.1:5000/api/traffic `
  -H "Content-Type: application/json" `
  -d '{\"method\":\"POST\",\"url\":\"https://example.com\",\"headers\":{},\"body\":\"test\"}'
```

## 📚 Technologies Used

- **Flask**: Web framework for the ingestion API
- **IBM watsonx.ai**: AI-powered vulnerability analysis
- **mitmproxy**: HTTP/HTTPS traffic interception
- **Jira**: Issue tracking and ticket management
- **Slack**: Real-time team notifications

## 🔐 Security Notes

- Never commit `config.py` with real credentials to version control
- Use environment variables for production deployments
- The mitmproxy certificate must be trusted by the client application

## 📄 License

This is a hackathon proof-of-concept project for educational purposes.
