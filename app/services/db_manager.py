from google.cloud import firestore
import uuid
import os
import logging
from typing import Optional, Dict, Any

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "ai-manee-son")

# Initialize Firestore client.
# In a highly asynchronous environment, consider initializing this client efficiently
# or using an async wrapper if Firestore I/O becomes a bottleneck, but the standard
# client is usually sufficient for these HITL state updates.
try:
    db = firestore.Client(project=PROJECT_ID)
except Exception as e:
    logging.warning(f"Could not initialize Firestore client explicitly: {e}")
    # Fallback to default if environment is already configured
    db = firestore.Client()

def create_project_state(gcs_uri: str, business_logic: str) -> str:
    """
    Saves a new project state to Firestore for the Human-in-the-Loop workflow.

    Args:
        gcs_uri: The URI of the uploaded audio file.
        business_logic: The generated markdown content.

    Returns:
        The generated unique project ID.
    """
    project_id = str(uuid.uuid4())
    doc_ref = db.collection("projects").document(project_id)
    doc_ref.set({
        "project_id": project_id,
        "audio_uri": gcs_uri,
        "business_logic_md": business_logic,
        "status": "pending_business_logic_review" # Awaiting human approval
    })
    return project_id

def get_project_state(project_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves the current state of a project from Firestore.

    Args:
        project_id: The unique identifier of the project.

    Returns:
        A dictionary containing the project data, or None if not found.
    """
    doc_ref = db.collection("projects").document(project_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None
