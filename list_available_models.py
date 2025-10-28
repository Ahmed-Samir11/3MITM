"""
Script to list all available foundation models in your watsonx.ai instance
"""

import requests
import config
import ibm_watsonx_client

print("\n" + "="*80)
print("Fetching Available Models from watsonx.ai")
print("="*80)

# Get IAM token
print("\n[1/2] Getting IBM Cloud IAM token...")
try:
    access_token = ibm_watsonx_client.get_iam_token()
    print("✓ Token obtained")
except Exception as e:
    print(f"✗ Failed: {str(e)}")
    exit(1)

# List foundation models
print("\n[2/2] Fetching available foundation models...")
url = f"https://us-south.ml.cloud.ibm.com/ml/v1/foundation_model_specs?version=2023-05-29"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if "resources" in data:
        models = data["resources"]
        print(f"\n✓ Found {len(models)} available models:\n")
        
        # Group models by provider
        providers = {}
        for model in models:
            model_id = model.get("model_id", "unknown")
            # Extract provider from model_id (e.g., "ibm/granite-13b-chat" -> "ibm")
            provider = model_id.split("/")[0] if "/" in model_id else "other"
            
            if provider not in providers:
                providers[provider] = []
            providers[provider].append(model_id)
        
        # Print organized by provider
        for provider, model_list in sorted(providers.items()):
            print(f"\n{provider.upper()} Models:")
            print("-" * 60)
            for model_id in sorted(model_list):
                print(f"  • {model_id}")
        
        # Recommend the first available model
        if models:
            first_model = models[0].get("model_id")
            print("\n" + "="*80)
            print(f"✓ RECOMMENDED: Use this model for your project:")
            print(f"\n  model_id = \"{first_model}\"")
            print(f"\nUpdate ingestion_api.py line ~97 with this model ID.")
            print("="*80 + "\n")
    else:
        print("✗ No models found in response")
        print(f"Response: {data}")
        
except Exception as e:
    print(f"\n✗ Error fetching models: {str(e)}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response: {e.response.text}")
