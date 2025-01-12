# Dating Profile Analyzer API

This API analyzes dating profile photos using GPT-4 Vision and provides detailed feedback and improvement suggestions.

## API Base URL
```
https://dating-profile-analyzer-api.onrender.com
```

## Features

- Analyzes multiple profile photos
- Provides comprehensive scoring across multiple categories
- Identifies potential red flags
- Suggests specific improvements
- Estimates current and potential profile scores

## Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd dating-profile-analyzer-api
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

5. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Version Requirements
- Python 3.9+
- OpenAI package >= 1.59.0
- LangChain OpenAI >= 0.3.0
- Other dependencies as specified in `requirements.txt`

### Troubleshooting
If you encounter package compatibility issues:
1. Make sure you're using a fresh virtual environment
2. Install packages with exact versions from requirements.txt
3. Update packages if needed:
```bash
pip install --upgrade langchain-openai openai
```

## API Endpoints

### Health Check
```
GET /
```
Confirms if the API is running.

### API Documentation
```
GET /docs
```
Interactive Swagger documentation to test the API directly in your browser.

### Analyze Photos
```
POST /analyze-photos/
```
Analyzes multiple dating profile photos and returns detailed feedback.

#### Request
- Method: POST
- Content-Type: multipart/form-data
- Body: 
  - `photos`: List of image files (supports multiple files)

## Example Usage

Using cURL:
```bash
curl -X POST "http://localhost:8000/analyze-photos/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "photos=@photo1.jpg" \
  -F "photos=@photo2.jpg"
```

Using Python requests:
```python
import requests

url = "http://localhost:8000/analyze-photos/"
files = [
    ('photos', ('photo1.jpg', open('photo1.jpg', 'rb'), 'image/jpeg')),
    ('photos', ('photo2.jpg', open('photo2.jpg', 'rb'), 'image/jpeg'))
]

response = requests.post(url, files=files)
print(response.json())
```

## Response Format

```json
{
    "overall_score": 75,
    "potential_score": 90,
    "photo_quality": {
        "score": 80,
        "potential_score": 95,
        "reasoning": {
            "positive_points": ["..."],
            "improvement_points": ["..."],
            "score": 80
        }
    },
    "no_catfish": { ... },
    "vibe": { ... },
    "lifestyle": { ... },
    "social_proof": { ... },
    "stand_out": { ... },
    "red_flags": [
        {
            "category": "Photo Quality",
            "description": "...",
            "severity": "low",
            "quick_fix": "..."
        }
    ],
    "improvement_actions": [
        {
            "category": "Photo Quality",
            "action": "...",
            "expected_impact": 85,
            "priority": 1,
            "reasoning": "..."
        }
    ]
}
```

## Important Notes

- Maximum file size: 2MB per image
- Supported image formats: JPEG, PNG
- First request might take 15-30 seconds as the model initializes
- Each request uses OpenAI API credits (GPT-4 Vision)
- Keep your API keys secure and never commit them to version control

## Production Deployment Notes
- The API is hosted on Render's free tier
- First request after inactivity might be slow (15-30 seconds)
- Service automatically spins down after 15 minutes of inactivity