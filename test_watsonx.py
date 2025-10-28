"""
Test script to check available watsonx.ai models and validate configuration
"""

import config
import ibm_watsonx_client

print("\n" + "="*80)
print("watsonx.ai Configuration Test")
print("="*80)

# Step 1: Test IAM Token
print("\n[1/3] Testing IBM Cloud IAM authentication...")
try:
    access_token = ibm_watsonx_client.get_iam_token()
    print("✓ IAM token obtained successfully")
    print(f"   Token (first 20 chars): {access_token[:20]}...")
except Exception as e:
    print(f"✗ Failed to get IAM token: {str(e)}")
    exit(1)

# Step 2: Test simple prompt with different models
print("\n[2/3] Testing AI model inference...")
test_prompt = "Hello, please respond with 'OK' if you can read this message."

# List of common models to try (updated for 2025)
models_to_test = [
    # IBM Granite models (2024-2025)
    "ibm/granite-3-8b-instruct",
    "ibm/granite-13b-instruct-v2",
    "ibm/granite-13b-chat-v2",
    "ibm/granite-20b-multilingual",
    # Meta Llama models
    "meta-llama/llama-3-2-90b-vision-instruct",
    "meta-llama/llama-3-1-70b-instruct",
    "meta-llama/llama-3-70b-instruct",
    "meta-llama/llama-3-8b-instruct",
    # Mistral models
    "mistralai/mixtral-8x7b-instruct-v01",
    "mistralai/mistral-large",
    # Google models
    "google/flan-t5-xxl",
    "google/flan-ul2",
    # Other foundation models
    "bigscience/mt0-xxl",
]

successful_model = None

for model_id in models_to_test:
    print(f"\nTrying model: {model_id}")
    try:
        response = ibm_watsonx_client.call_watsonx_ai(
            prompt=test_prompt,
            model_id=model_id,
            project_id=config.IBM_PROJECT_ID,
            access_token=access_token
        )
        print(f"✓ SUCCESS! This model works.")
        print(f"   Response: {response[:100]}...")
        successful_model = model_id
        break  # Stop after first successful model
    except Exception as e:
        print(f"✗ Failed with this model")
        continue

# Step 3: Recommendation
print("\n" + "="*80)
if successful_model:
    print(f"✓ RECOMMENDATION: Use model: {successful_model}")
    print(f"\nUpdate ingestion_api.py line ~90 to:")
    print(f'   model_id = "{successful_model}"')
else:
    print("✗ None of the tested models worked.")
    print("\nPlease check:")
    print("1. Your IBM_PROJECT_ID in config.py is correct")
    print("2. You have access to watsonx.ai models in your IBM Cloud account")
    print("3. Your project has the necessary model deployments enabled")
    print("\nYou can check available models in your watsonx.ai project dashboard:")
    print("https://dataplatform.cloud.ibm.com/wx/home")

print("="*80 + "\n")
