from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from dotenv import load_dotenv
from app.schemas import ProfileAnalysis
from langchain_openai import ChatOpenAI
import base64
from PIL import Image
import io
import json

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Dating Profile Analyzer API",
    description="API for analyzing dating profile photos and providing feedback",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def compress_image(image_bytes, max_size=(768, 2000)):
    """Compress image from bytes to reduce token size"""
    with Image.open(io.BytesIO(image_bytes)) as img:
        # Keep aspect ratio
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        # Convert to buffer
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)
        return buffer.read()

def encode_image_to_base64(image_bytes):
    """Encode a compressed image to base64"""
    compressed = compress_image(image_bytes)
    return base64.b64encode(compressed).decode('utf-8')

def read_prompt_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def analyze_single_photo(llm, prompt_template, image_bytes, photo_number):
    """Analyze a single photo using the provided LLM and prompt template."""
    base64_image = encode_image_to_base64(image_bytes)
    
    # Add photo number to the prompt
    numbered_prompt = f"[Photo {photo_number}] {prompt_template}"
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": numbered_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]
    
    response = llm.invoke(messages)
    return f"[Photo {photo_number}] {response.content}"

def create_summary(llm, summary_prompt, individual_analyses):
    """Create a summary of all photo analyses."""
    # Combine all analyses into one text
    all_analyses = "\n\n===NEXT PHOTO===\n\n".join(individual_analyses)
    
    messages = [
        {
            "role": "user",
            "content": summary_prompt.format(analyses=all_analyses)
        }
    ]
    
    return llm.invoke(messages)

@app.get("/")
async def root():
    return {
        "message": "Dating Profile Analyzer API is running",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }

@app.post("/analyze-photos/", response_model=ProfileAnalysis)
async def analyze_photos(photos: List[UploadFile] = File(...)):
    try:
        print("Starting photo analysis...")
        
        # Initialize the LLMs
        try:
            print("Initializing LLM...")
            llm = ChatOpenAI(
                model_name="gpt-4o",
                temperature=0.7,
                max_tokens=4096
            )
            print("LLM initialized successfully")
        except Exception as e:
            print(f"Error initializing LLM: {str(e)}")
            raise HTTPException(status_code=500, detail=f"LLM initialization failed: {str(e)}")
        
        try:
            print("Creating structured LLM...")
            structured_llm = llm.with_structured_output(ProfileAnalysis)
            print("Structured LLM created successfully")
        except Exception as e:
            print(f"Error creating structured LLM: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Structured LLM creation failed: {str(e)}")
        
        # Read prompt templates
        try:
            print("Reading prompt templates...")
            single_photo_prompt = read_prompt_file("prompts/single_photo_prompt.txt")
            summary_prompt = read_prompt_file("prompts/all_photos_summary_prompt.txt")
            print("Prompt templates read successfully")
        except Exception as e:
            print(f"Error reading prompt files: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to read prompt files: {str(e)}")
        
        # Analyze each photo
        individual_analyses = []
        for idx, photo in enumerate(photos, 1):
            try:
                print(f"Processing photo {idx}...")
                content = await photo.read()
                print(f"Photo {idx} read successfully, size: {len(content)} bytes")
                analysis = analyze_single_photo(llm, single_photo_prompt, content, idx)
                individual_analyses.append(analysis)
                print(f"Photo {idx} analyzed successfully")
            except Exception as e:
                print(f"Error processing photo {idx}: {str(e)}")
                import traceback
                print(f"Traceback for photo {idx}: {traceback.format_exc()}")
                raise HTTPException(status_code=500, detail=f"Error processing photo {idx}: {str(e)}\nTraceback: {traceback.format_exc()}")
        
        # Generate structured summary
        try:
            print("Generating final summary...")
            structured_summary = create_summary(structured_llm, summary_prompt, individual_analyses)
            print("Summary generated successfully")
            return structured_summary
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")
        
    except Exception as e:
        import traceback
        error_detail = f"Unexpected error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=error_detail)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)