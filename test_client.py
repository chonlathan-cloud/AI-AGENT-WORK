import requests
import sys
import mimetypes

def test_api(file_path):
    url = "http://localhost:8000/analyze-concept"
    
    # เดาประเภทของไฟล์ (MIME type) จากนามสกุลไฟล์
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"
        
    print(f"Uploading file: {file_path} (MIME type: {mime_type})")
    print("Sending request to Gemini... This might take a minute...")

    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, mime_type)}
            response = requests.post(url, files=files)
            
        response.raise_for_status() # Check for HTTP errors
        
        result = response.json()
        print("\n=== SUCCESS ===")
        print(f"Filename: {result.get('filename')}")
        print("\n=== BUSINESS LOGIC ===")
        print(result.get('business_logic'))
        
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the API: {e}")
        if response is not None:
             print(f"Response Content: {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_client.py <path_to_audio_or_video_file>")
        print("Example: python test_client.py my_meeting.mp3")
        sys.exit(1)
        
    test_api(sys.argv[1])