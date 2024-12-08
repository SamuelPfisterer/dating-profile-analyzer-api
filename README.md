# Dating Profile Analyzer API

This API analyzes dating profile photos using GPT-4 Vision and provides detailed feedback and improvement suggestions.

## Features

- Analyzes multiple profile photos
- Provides comprehensive scoring across multiple categories
- Identifies potential red flags
- Suggests specific improvements
- Estimates current and potential profile scores

## API Endpoints

### Health Check
```
GET /
```
Confirms if the API is running.

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

#### Response
JSON object containing:
- Overall score and potential score
- Category-specific scores (photo quality, authenticity, vibe, lifestyle, etc.)
- Red flags with severity levels
- Prioritized improvement actions

## Setup & Deployment

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up environment variables:
   - Create a `.env` file
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
4. Run locally:
```bash
uvicorn app.main:app --reload
```

## Example Usage

Using cURL:
```bash
curl -X POST "http://your-api-url/analyze-photos/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "photos=@photo1.jpg" \
  -F "photos=@photo2.jpg"
```

Using Python requests:
```python
import requests

url = "http://your-api-url/analyze-photos/"
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

## Requirements

- Python 3.11+
- FastAPI
- OpenAI API key with GPT-4 Vision access
- See `requirements.txt` for full list of dependencies

## Deployment

This API is configured for deployment on Render. Required configuration files (`render.yaml` and `runtime.txt`) are included in the repository.

## Rate Limits & Costs

- Be aware that GPT-4 Vision API has associated costs
- Monitor your OpenAI API usage
- Consider implementing rate limiting for production use 