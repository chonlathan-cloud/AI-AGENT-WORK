from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from app.services.ai_engine import transcribe_and_generate_logic
from app.services.db_manager import create_project_state, get_project_state
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Scaffolding AI Agent API",
    description="API for ingesting audio and generating architectural maps via Vertex AI.",
    version="1.0.0"
)

# Request Models (Pydantic validation)
class GcsEvent(BaseModel):
    bucket: str = Field(..., description="The name of the GCS bucket.")
    name: str = Field(..., description="The name of the object in the bucket.")

# Response Models
class WebhookResponse(BaseModel):
    message: str
    gcs_uri: str

async def process_audio_pipeline(gcs_uri: str):
    """
    The actual background pipeline that processes the audio.
    It calls Vertex AI asynchronously and saves the state to Firestore.
    """
    try:
        logging.info(f"Starting analysis for {gcs_uri}")
        # 1. Transcribe and generate business logic
        business_logic_md = await transcribe_and_generate_logic(gcs_uri)
        
        # 2. Save to database awaiting approval
        project_id = create_project_state(gcs_uri, business_logic_md)
        logging.info(f"Successfully processed project: {project_id}")
        
    except Exception as e:
        logging.error(f"Error processing {gcs_uri}: {str(e)}")

@app.post("/webhook/audio-ingested", response_model=WebhookResponse)
async def audio_ingested_webhook(event: GcsEvent, background_tasks: BackgroundTasks):
    """
    Endpoint triggered by Eventarc when a new audio file is uploaded to GCS.
    It immediately returns a 200 OK and processes the audio in the background.
    """
    gcs_uri = f"gs://{event.bucket}/{event.name}"
    logging.info(f"Received new audio file: {gcs_uri}")
    
    # Process in background to avoid Eventarc timeout
    background_tasks.add_task(process_audio_pipeline, gcs_uri)
    
    return WebhookResponse(message="Processing started", gcs_uri=gcs_uri)

@app.get("/api/projects/{project_id}")
async def review_business_logic(project_id: str):
    """
    Endpoint for Human-in-the-Loop review.
    Retrieve the generated Business Logic for inspection in VSCode/Postman.
    """
    data = get_project_state(project_id)
    if not data:
        raise HTTPException(status_code=404, detail="Project not found")
    return data

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    # The command to run should be: uvicorn app.main:app --reload