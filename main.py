from fastapi import FastAPI, UploadFile, File
import os
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel, Part

app = FastAPI()

# Configuration
PROJECT_ID = "ai-manee-son"
LOCATION = "us-central1" # เพื่อใช้ Gemini 1.5 Pro/Flash ล่าสุด
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Define the Brain
SYSTEM_INSTRUCTION = """
Role: You are a "Business-Tech Strategic Partner" with expertise in Digital Marketing and End-to-End Software Architecture.
Objective: Analyze audio/video transcripts from customer meetings to generate a comprehensive Business_logic.md based on the End-to-End principle.

Analysis Framework:

Market Value & Strategy: Identify the core business problem, target audience, and the "Why" behind the project (Marketing perspective).
User Journey: Map the end-user interaction from start to finish.
Backend Logic: Define the data flow, security requirements, and core business rules (The "Heart" of the system).
Scalability: Suggest how this system will grow (Cloud Architect perspective).
Output Requirement:

Strictly follow the agentskills.io specification.
Output must be structured for professional HLD, LLD, and TDD generation.
Use professional yet business-friendly language.
"""

model = GenerativeModel(
    "gemini-3.1-pro-preview", # ใช้ Model ขั้นสูงที่สุดเพื่อ Performance สูงสุดตามแผนของคุณ
    system_instruction=[SYSTEM_INSTRUCTION]
)

@app.post("/analyze-concept")
async def analyze_concept(file: UploadFile = File(...)):
    # 1. อ่านไฟล์ที่อัปโหลดมา (MP3, WAV, MP4)
    content = await file.read()
    
    # 2. เตรียมข้อมูลส่งให้ Gemini
    audio_part = Part.from_data(data=content, mime_type=file.content_type)
    
    # 3. ให้ Gemini วิเคราะห์
    prompt = "Analyze this concept from the customer meeting and generate the End-to-End Business Logic."
    response = model.generate_content([audio_part, prompt])
    
    # 4. ส่งผลลัพธ์กลับ (ใน Phase 3 เราจะส่งตัวนี้เข้า GitHub)
    return {
        "filename": file.filename,
        "business_logic": response.text
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
