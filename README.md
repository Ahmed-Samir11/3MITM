# 3MITM: DevSecOps AI Agent - Hackathon Project

A complete Python application demonstrating the **3MITM** concept: Detection, Defense, and Remediation of Man-in-the-Middle (MITM) attacks using agentic AI and IBM watsonx.ai.

The system automatically:
1. **Detects** MITM attacks and vulnerabilities in HTTP traffic
2. **Generates** secure code fixes using AI
3. **Remediates** by creating Jira tickets and Slack notifications

## 🚀 Quick Start

### 1. Setup (see [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for detailed steps)

```bash
# Clone repository
git clone https://github.com/Ahmed-Samir11/3MITM.git
cd 3MITM

# Create virtual environment
python -m venv ibm
.\ibm\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API credentials
```

### 2. Run the Application

#### Terminal 1: Start the Defense System
```powershell
python ingestion_api.py
```

#### Terminal 2: Run Attack Simulation
```powershell
python advanced_3mitm_test.py
```

## 🔐 Security

**All API credentials are stored in `.env` file (git-ignored)**

- Copy `.env.example` to `.env` 
- Add your credentials to `.env`
- Never commit `.env` to git
- See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for credential instructions

### Required Credentials

- IBM watsonx.ai API Key & Project ID
- Jira Cloud Email & API Token
- Slack Incoming Webhook URL

## 📋 Configuration

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
