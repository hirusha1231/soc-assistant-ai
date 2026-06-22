# playbooks.py
PLAYBOOKS = {
    "brute_force": {
        "alert_types": ["brute force", "failed login", "password spraying"],
        "mitre_technique": "T1110.001",
        "description": "Multiple failed authentication attempts from a single source",
        "response_steps": [
            "Identify source IP address from logs",
            "Check if any authentication succeeded from this IP",
            "If malicious, block source IP at firewall/IDS",
            "Reset passwords for any compromised accounts",
            "Enable MFA for affected accounts",
            "Review logs for similar patterns from other IPs"
        ],
        "severity": "High"
    },
    "malware_detection": {
        "alert_types": ["malware", "virus", "ransomware", "trojan"],
        "mitre_technique": "T1204.002",
        "description": "Malicious file or process detected on endpoint",
        "response_steps": [
            "Isolate affected system from network immediately",
            "Identify the malware family using hash/IoC",
            "Check for lateral movement indicators",
            "Quarantine or remove malicious files",
            "Scan all systems in same network segment",
            "Update antivirus definitions",
            "File incident report"
        ],
        "severity": "Critical"
    },
    "phishing": {
        "alert_types": ["phishing", "suspicious email", "malicious link"],
        "mitre_technique": "T1566.001",
        "description": "Suspicious email with malicious intent detected",
        "response_steps": [
            "Extract email headers, sender info, and attachments",
            "Check if any users clicked links or opened attachments",
            "Block sender domain/IP at email gateway",
            "Remove phishing emails from all mailboxes",
            "Reset credentials if any user credentials were compromised",
            "Conduct user awareness training"
        ],
        "severity": "High"
    },
    "data_exfiltration": {
        "alert_types": ["data exfil", "data leak", "data transfer"],
        "mitre_technique": "T1048",
        "description": "Unusual large data transfer detected",
        "response_steps": [
            "Identify source system and data being transferred",
            "Determine destination IP/domain",
            "Check if transfer was authorized",
            "Block suspicious destination IPs",
            "Review user activity logs",
            "Engage legal/HR if insider threat suspected",
            "Update DLP policies"
        ],
        "severity": "Critical"
    }
}

def get_playbook_by_alert(alert_text):
    """Find matching playbook based on alert description"""
    alert_lower = alert_text.lower()
    for key, playbook in PLAYBOOKS.items():
        for alert_type in playbook["alert_types"]:
            if alert_type in alert_lower:
                return playbook
    return None