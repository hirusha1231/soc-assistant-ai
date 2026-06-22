# load_data.py
from playbooks import PLAYBOOKS
from vectordb import db
import json

def load_playbooks():
    """Load all playbooks into vector database"""
    for key, playbook in PLAYBOOKS.items():
        # Create searchable text content
        content = f"""
        Alert Type: {', '.join(playbook['alert_types'])}
        Description: {playbook['description']}
        MITRE Technique: {playbook['mitre_technique']}
        Response Steps: {'; '.join(playbook['response_steps'])}
        Severity: {playbook['severity']}
        """
        db.add_playbook(key, content)
    print(f"✅ Loaded {len(PLAYBOOKS)} playbooks into database")

if __name__ == "__main__":
    load_playbooks()