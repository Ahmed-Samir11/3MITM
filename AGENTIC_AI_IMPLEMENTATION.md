# Agentic AI and IBM watsonx.ai Implementation in 3MITM

## Executive Summary

The 3MITM framework demonstrates a sophisticated orchestration of three specialized autonomous agents powered by IBM watsonx.ai (specifically the Granite 3-8B model) to detect, analyze, and remediate Man-in-the-Middle (MITM) attacks in real-time.

## Agent Orchestration Architecture

**Agent 1 - Reconnaissance Agent**: Passively analyzes intercepted HTTP traffic to discover API endpoints, identify vulnerability indicators, map database schemas, and extract live API credentials. This agent establishes the attack surface without triggering detection systems.

**Agent 2 - Injection Agent**: Based on reconnaissance data, crafts coordinated multi-vector attack payloads including SQL Injection, IDOR, JWT escalation, parameter tampering, and CSV injection attacks. Each payload is intelligently tailored to exploit specific vulnerabilities identified by Agent 1.

**Agent 3 - Exfiltration Agent**: Executes injected payloads to systematically extract sensitive data including customer PII, payment records, admin credentials, and database backups. This agent optimizes data exfiltration to maximize impact while maintaining stealth.

## IBM watsonx.ai Integration

Each agent leverages IBM watsonx.ai's Granite 3-8B large language model through the Flask-based ingestion API. The system sends contextual prompts describing intercepted traffic to watsonx, which analyzes the HTTP requests/responses and generates vulnerability assessments and secure code fixes. This AI-powered analysis enables human-level reasoning about attack vectors and security remediation without hardcoded rule engines.

## Defense and Remediation

The orchestrated attack triggers an automated defense system that creates Jira tickets with AI-generated remediation code, sends Slack alerts, and initiates incident response workflows—demonstrating how agentic AI can be weaponized and, conversely, how it enables advanced defensive automation.

