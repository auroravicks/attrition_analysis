from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re


# Load API key from environment variables
load_dotenv(".env")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables")

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Enable CORS (Allowing all origins for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input model
class FeedbackRequest(BaseModel):
    feedback: dict | str  # Accepting free text, structured data, or JSON


def extract_json_from_gemini_response(response_text: str):
    """Extracts and parses JSON embedded inside a string."""
    # Use a regular expression to match JSON inside the ```json and ``` tags
    json_pattern = r'```json\n({.*?})\n```'
    
    match = re.search(json_pattern, response_text, re.DOTALL)  # re.DOTALL allows the pattern to match across newlines
    
    if match:
        json_string = match.group(1)  # Extract the JSON string from the match
        try:
            # Parse the JSON string into a Python dictionary
            response_json = json.loads(json_string)
            return response_json
        except json.JSONDecodeError:
            raise ValueError("Error decoding JSON from Gemini response")
    else:
        raise ValueError("No embedded JSON found in Gemini response")


def analyze_feedback_with_gemini(feedback):
    """Formats input data and queries Gemini API."""
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    You are an HR analytics assistant analyzing employee sentiment and attrition risk.  
    The input format may be:  
    - Free text (single-line or paragraph feedback).  
    - Lists of key points from surveys or meeting minutes.  
    - Structured dialogue (transcripts from exit interviews).  
    - Nested JSON objects with summaries and detailed feedback.  

    Normalize the input and analyze it.

    ### **Your Response Should Include:**  
    1. **Attrition Probability (0-1 scale)**  
    2. **Sentiment (Positive, Neutral, Negative)**  
    3. **Key Issues Extracted**  
    4. **Engagement Strategies to reduce attrition risk**  

    ### **Input Data:**  
    {feedback}

    ### **Response Format (JSON)**  
    ```json
    {{
      "attrition_probability": 0.XX,
      "sentiment": "Positive/Neutral/Negative",
      "key_issues": ["Issue 1", "Issue 2"],
      "recommendations": ["Strategy 1", "Strategy 2"]
    }}
    ```
    """
    
    response = model.generate_content(prompt)
    
    # Extract JSON from Gemini response
    try:
        analysis_result = extract_json_from_gemini_response(response.text)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return analysis_result


@app.post("/analyze_feedback/")
async def analyze_feedback(request: FeedbackRequest):
    try:
        analysis_result = analyze_feedback_with_gemini(request.feedback)
        print(request.feedback)
        print(analysis_result)
        return {"feedback": request.feedback, "analysis": analysis_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
