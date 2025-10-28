"""
mitmproxy Script - Traffic Forwarder
Intercepts HTTP/HTTPS traffic and forwards it to the Ingestion API for analysis
"""

from mitmproxy import http
import requests
import json

# Ingestion API endpoint
INGESTION_API_ENDPOINT = "http://127.0.0.1:5000/api/traffic"


def request(flow: http.HTTPFlow) -> None:
    """
    Intercept HTTP request and response, then forward to ingestion API
    
    Args:
        flow: mitmproxy HTTPFlow object containing request/response data
    """
    # Only process completed flows (with responses)
    if flow.response:
        try:
            # Extract request data
            request_headers = dict(flow.request.headers)
            request_body = flow.request.text if flow.request.text else ""
            
            # Extract response data
            response_headers = dict(flow.response.headers)
            response_body = flow.response.text if flow.response.text else ""
            
            # Prepare payload for ingestion API
            payload = {
                "method": flow.request.method,
                "url": flow.request.pretty_url,
                "headers": request_headers,
                "body": request_body,
                "response_status": flow.response.status_code,
                "response_headers": response_headers,
                "response_body": response_body
            }
            
            # Forward to ingestion API
            response = requests.post(
                INGESTION_API_ENDPOINT,
                json=payload,
                timeout=5
            )
            
            if response.status_code == 202:
                print(f"✓ Traffic forwarded: {flow.request.method} {flow.request.pretty_url}")
            else:
                print(f"✗ Failed to forward traffic: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Error forwarding traffic: {str(e)}")
        except Exception as e:
            print(f"✗ Unexpected error: {str(e)}")


def response(flow: http.HTTPFlow) -> None:
    """
    Called when response is received - trigger the request analysis
    
    Args:
        flow: mitmproxy HTTPFlow object containing request/response data
    """
    # Call the request function to process the complete flow
    request(flow)
