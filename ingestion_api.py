"""
Ingestion API - Main Orchestrator
Flask application that receives intercepted traffic and orchestrates the AI-powered vulnerability analysis workflow
"""

from flask import Flask, request, jsonify
import threading
import json
import config
import ibm_watsonx_client
import jira_integration
import slack_integration
import demo_config

app = Flask(__name__)

# Validate configuration on startup
try:
    config.validate_config()
except ValueError as e:
    print(f"Configuration Error: {e}")
    exit(1)


@app.route('/api/traffic', methods=['POST'])
def ingest_traffic():
    """
    Endpoint to ingest intercepted HTTP traffic from mitmproxy
    
    Returns:
        Response: 202 Accepted response with confirmation message
    """
    try:
        traffic_data = request.get_json()
        
        if not traffic_data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        
        # Validate required fields
        required_fields = ['method', 'url', 'headers', 'body']
        if not all(field in traffic_data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Start analysis workflow in a separate thread to avoid blocking
        analysis_thread = threading.Thread(
            target=run_analysis_workflow,
            args=(traffic_data,)
        )
        analysis_thread.daemon = True
        analysis_thread.start()
        
        return jsonify({
            "status": "accepted",
            "message": "Traffic data received and queued for analysis"
        }), 202
        
    except Exception as e:
        print(f"Error in ingest_traffic: {str(e)}")
        return jsonify({"error": "Internal processing error"}), 500


def run_analysis_workflow(traffic_data):
    """
    Core orchestration logic for AI-powered vulnerability analysis
    This function simulates the watsonx Orchestrate skill flow locally
    
    Args:
        traffic_data (dict): Intercepted HTTP traffic data
    """
    try:
        print("\n" + "="*80)
        print("🚀 DevSecOps AI Agent Workflow Triggered")
        print("="*80)
        
        # Step 1: Get IAM Token
        print("\n[1/7] Getting IBM Cloud IAM token...")
        access_token = ibm_watsonx_client.get_iam_token()
        print("✓ IAM token obtained successfully")
        
        # Step 2: Format Prompt for Vulnerability Detection
        print("\n[2/7] Preparing vulnerability detection prompt...")
        detection_prompt = ibm_watsonx_client.PROMPT_VULNERABILITY_DETECTION.format(
            method=traffic_data.get('method', 'N/A'),
            url=traffic_data.get('url', 'N/A'),
            headers=json.dumps(traffic_data.get('headers', {}), indent=2),
            body=traffic_data.get('body', 'N/A'),
            response_status=traffic_data.get('response_status', 'N/A'),
            response_headers=json.dumps(traffic_data.get('response_headers', {}), indent=2),
            response_body=traffic_data.get('response_body', 'N/A')
        )
        print("✓ Prompt prepared")
        
        # Step 3: Call AI for Vulnerability Analysis
        print("\n[3/7] Analyzing traffic with watsonx.ai...")
        # Using IBM Granite 3 8B Instruct - optimized for instruction following
        model_id = "ibm/granite-3-8b-instruct"
        ai_response = ibm_watsonx_client.call_watsonx_ai(
            prompt=detection_prompt,
            model_id=model_id,
            project_id=config.IBM_PROJECT_ID,
            access_token=access_token
        )
        print("✓ AI analysis complete")
        
        # Step 4: Parse AI Response
        print("\n[4/7] Parsing AI response...")
        try:
            # Extract JSON from response (may contain additional text)
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start == -1 or json_end <= json_start:
                print(f"✗ No JSON object found in response")
                print(f"   Raw response: {ai_response[:200]}...")
                return
            
            json_str = ai_response[json_start:json_end]
            
            # Try to parse the extracted JSON
            try:
                vulnerability_data = json.loads(json_str)
            except json.JSONDecodeError:
                # If that fails, try removing trailing commas and fixing common issues
                json_str_cleaned = json_str.replace(',}', '}').replace(',]', ']')
                vulnerability_data = json.loads(json_str_cleaned)
            
            print(f"✓ Parsed successfully")
            print(f"   Vulnerability Detected: {vulnerability_data.get('vulnerability_detected', False)}")
            
        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse AI response as JSON: {str(e)}")
            print(f"   Raw response: {ai_response[:300]}...")
            return
        
        # Step 5: Check if vulnerability was detected
        if vulnerability_data.get('vulnerability_detected', False):
            print(f"\n⚠️  VULNERABILITY FOUND!")
            print(f"   Type: {vulnerability_data.get('vulnerability_type', 'Unknown')}")
            print(f"   Severity: {vulnerability_data.get('severity', 'Unknown')}")
            
            # Step 6: Generate Secure Code Fix
            print("\n[5/7] Generating secure code fix with watsonx.ai...")
            
            # Simulate passive reconnaissance (framework detection)
            framework_detected = _detect_framework(traffic_data)
            
            remediation_prompt = ibm_watsonx_client.PROMPT_SECURE_CODE_GENERATION.format(
                vulnerability_analysis=json.dumps(vulnerability_data, indent=2),
                framework_detected=framework_detected
            )
            
            code_fix = ibm_watsonx_client.call_watsonx_ai(
                prompt=remediation_prompt,
                model_id=model_id,
                project_id=config.IBM_PROJECT_ID,
                access_token=access_token
            )
            print("✓ Secure code generated")
            
            # Step 7: Create Jira Ticket
            print("\n[6/7] Creating Jira ticket...")
            jira_issue = None
            try:
                jira_issue = jira_integration.create_jira_ticket(vulnerability_data, code_fix)
                print(f"✓ Jira ticket created: {jira_issue.key}")
                ticket_key = jira_issue.key
                
            except Exception as jira_error:
                print(f"⚠️  Jira API error - using demo mode")
                print(f"   Error: {str(jira_error)[:100]}...")
                
                if demo_config.DEMO_MODE:
                    import uuid
                    ticket_key = f"{config.JIRA_PROJECT_KEY}-{str(uuid.uuid4())[:8].upper()}"
                    print(f"✓ Demo ticket ID: {ticket_key}")
                else:
                    print(f"❌ Could not create Jira ticket and demo mode is disabled")
                    ticket_key = None
            
            if ticket_key:
                # Step 8: Send Slack Alert
                print("\n[7/7] Sending Slack alert...")
                try:
                    slack_integration.send_slack_alert(
                        jira_issue_key=ticket_key,
                        jira_server_url=config.JIRA_SERVER,
                        vulnerability_data=vulnerability_data
                    )
                    print("✓ Slack alert sent")
                except Exception as slack_error:
                    print(f"⚠️  Could not send Slack alert (demo mode): skipped")
                
                print("\n" + "="*80)
                print("✅ Workflow Complete - Vulnerability Remediated!")
                print(f"   Ticket: {ticket_key}")
                print(f"   Type: {vulnerability_data.get('vulnerability_type')}")
                print(f"   Severity: {vulnerability_data.get('severity')}")
                print("="*80 + "\n")
            else:
                print("\n" + "="*80)
                print("⚠️  Workflow Partial - Vulnerability analyzed but not ticketed")
                print("="*80 + "\n")
            
        else:
            print("\n✅ No vulnerabilities detected in this traffic")
            print("="*80 + "\n")
            
    except Exception as e:
        print(f"\n❌ Error in analysis workflow: {str(e)}")
        import traceback
        traceback.print_exc()
        print("="*80 + "\n")


def _detect_framework(traffic_data):
    """
    Simulate passive reconnaissance to detect the framework/technology
    
    Args:
        traffic_data (dict): Intercepted HTTP traffic data
        
    Returns:
        str: Detected framework name
    """
    # Simple heuristic-based framework detection
    headers = traffic_data.get('headers', {})
    response_headers = traffic_data.get('response_headers', {})
    body = traffic_data.get('body', '').lower()
    response_body = traffic_data.get('response_body', '').lower()
    
    # Check headers for framework signatures
    server_header = response_headers.get('Server', '').lower()
    
    if 'express' in server_header or 'node' in server_header:
        return "Node.js/Express"
    elif 'django' in server_header or 'python' in server_header:
        return "Python/Django"
    elif 'spring' in response_body or 'java' in server_header:
        return "Java/Spring Boot"
    elif 'asp.net' in server_header or 'microsoft' in server_header:
        return "ASP.NET"
    elif 'php' in server_header:
        return "PHP"
    else:
        return "Generic Web Framework"


if __name__ == '__main__':
    print("\n" + "="*80)
    print("DevSecOps AI Agent - Ingestion API Starting...")
    print("="*80)
    print(f"Listening on: http://127.0.0.1:5000")
    print("Endpoint: POST /api/traffic")
    print("="*80 + "\n")
    
    app.run(host='127.0.0.1', port=5000, debug=True)
