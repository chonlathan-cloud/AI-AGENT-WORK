import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# Initialize Vertex AI.
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "ai-manee-son")
# Remove REGION restriction for global efficiency if needed, 
# but vertexai.init usually requires a location for the SDK to route correctly.
# We will default to a broad location or allow the SDK to handle routing.
LOCATION = "us-central1" # Recommended for preview models and global availability

try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
except Exception as e:
    import logging
    logging.warning(f"Could not initialize Vertex AI explicitly: {e}")

async def transcribe_and_generate_logic(gcs_uri: str) -> str:
    """
    Receives a GCS URI of an audio file and uses Gemini 3.1 Pro Preview to analyze it
    and generate a comprehensive Business_logic.md.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., gs://bucket/file.m4a).

    Returns:
        The generated Business_logic.md content as a string.
    """
    # Using 'gemini-3.1-pro-preview' for maximum efficiency as requested.
    model = GenerativeModel("gemini-3.1-pro-preview")
    
    # Read the file directly from GCS.
    # We specify audio/mp4 as a safe default for .m4a.
    audio_file = Part.from_uri(gcs_uri, mime_type="audio/mp4")
    
    prompt = """
    คุณคือ Senior Business Analyst และ System Architect ระดับโลก
    จงฟังไฟล์เสียงนี้ ซึ่งเป็นการสรุป Concept Project จากลูกค้า
    และเขียนออกมาเป็นโครงสร้างไฟล์ `Business_logic.md` อย่างละเอียด
    
    รูปแบบที่ต้องการ (Markdown):
    # Business Logic & Core Concept
    ## 1. Project Overview (ภาพรวม)
    ## 2. Target Audience (กลุ่มเป้าหมาย)
    ## 3. Core Features (ฟีเจอร์หลัก)
    ## 4. Business Value / Monetization (คุณค่าทางธุรกิจและการทำเงิน)
    ## 5. Technical Constraints (ข้อจำกัดทางเทคนิคเบื้องต้นที่ตีความได้)
    """
    
    # Process asynchronously to maximize FastAPI performance
    responses = await model.generate_content_async(
        [audio_file, prompt],
        stream=False
    )
    return responses.text
