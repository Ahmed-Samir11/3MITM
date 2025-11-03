"""
IBM watsonx.ai Client Module
Handles all interactions with the watsonx.ai API for AI-powered vulnerability detection and code generation
"""

import requests
import json
import config

def get_iam_token():
    """
    Generate a temporary IAM access token using IBM API Key
    
    Returns:
        str: IBM Cloud IAM access token
    """
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": config.IBM_API_KEY
    }
    
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    
    return response.json()["access_token"]


def call_watsonx_ai(prompt, model_id, project_id, access_token):
    """
    Make an inference call to watsonx.ai API
    
    Args:
        prompt (str): The prompt to send to the AI model
        model_id (str): The watsonx.ai model identifier
        project_id (str): The IBM watsonx project ID
        access_token (str): IAM access token
        
    Returns:
        str: Generated text from the AI model
    """
    url = f"https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    body = {
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 900,
            "repetition_penalty": 1.05,
            "min_tokens": 10
        },
        "model_id": model_id,
        "project_id": project_id
    }
    
    response = requests.post(url, headers=headers, json=body)
    
    # Enhanced error handling
    if not response.ok:
        error_detail = response.text
        print(f"\n❌ watsonx.ai API Error:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Error Details: {error_detail}")
        print(f"   Model ID used: {model_id}")
        print(f"   Project ID used: {project_id}")
    
    response.raise_for_status()
    
    data = response.json()
    generated_text = data["results"][0]["generated_text"]
    
    # Clean up the response - extract only the first JSON object
    # Remove any text before the first { and after the last }
    json_start = generated_text.find('{')
    json_end = generated_text.rfind('}') + 1
    
    if json_start != -1 and json_end > json_start:
        generated_text = generated_text[json_start:json_end]
    
    return generated_text


# Prompt for vulnerability detection (Part 2.2)
PROMPT_VULNERABILITY_DETECTION = """You are a security analyst. Analyze the following HTTP request/response pair for potential security vulnerabilities.

HTTP Request:
Method: {method}
URL: {url}
Headers: {headers}
Body: {body}

HTTP Response:
Status: {response_status}
Headers: {response_headers}
Body: {response_body}

Provide your analysis in the following JSON format:
{{
  "vulnerability_detected": true/false,
  "vulnerability_type": "Type of vulnerability (e.g., SQL Injection, XSS, Hardcoded Credentials, etc.)",
  "severity": "Critical/High/Medium/Low",
  "description": "Detailed description of the vulnerability",
  "affected_parameter": "The specific parameter or field that is vulnerable",
  "recommendation": "Brief recommendation for remediation"
}}

If no vulnerability is detected, set vulnerability_detected to false and leave other fields empty or null.
"""

# Prompt for secure code generation (Part 2.3)
PROMPT_SECURE_CODE_GENERATION = """You are a secure coding expert. Based on the vulnerability analysis below, generate secure code that fixes the issue.

Vulnerability Analysis:
{vulnerability_analysis}

Detected Framework: {framework_detected}

Generate secure code that:
1. Addresses the identified vulnerability
2. Follows security best practices for the detected framework
3. Includes inline comments explaining the security improvements
4. Is production-ready and can be directly integrated

Provide only the code block without additional explanation. Use appropriate language syntax based on the framework.
"""
