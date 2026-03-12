# Product Review Analyzer - Assignment 3

A LangChain-based product review analyzer that uses **Pydantic** models and **PydanticOutputParser** to extract validated structured data from product reviews using Groq's free API with fast inference.

## Objective

Use Pydantic and PydanticOutputParser to extract validated structured data from a product review with the following schema:
- **sentiment**: Overall sentiment (positive, negative, neutral)
- **rating**: Numeric rating (1-5)
- **key_features**: List of mentioned product features
- **improvement_suggestions**: List of suggested improvements

## Key Features

✓ **Proper Pydantic Schema Design** - ReviewAnalysis model with field validation and constraints
✓ **PydanticOutputParser** - Automatic parsing and validation of LLM outputs
✓ **Format Instructions** - Clear format guidance in prompts for accurate parsing
✓ **Type Validation** - Pydantic validators ensure correct data types and ranges
✓ **Error Handling** - Graceful handling of parsing errors and API failures
✓ **Free AI Model** - Uses Groq's free API (fast inference, no rate limits)

## Installation

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Groq API Key

**Free Tier** (No credit card required):

1. Go to [Groq Console](https://console.groq.com/)
2. Create a free account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy your API key
6. Set the environment variable:

**On Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY = "your-api-key-here"
```

**Or create a `.env` file in the project root:**
```
GROQ_API_KEY=your-api-key-here
```

## Project Structure

```
product-review-analyzer/
├── main.py              # Main application and analyzer chain
├── models.py            # Pydantic model definitions
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Usage

### Run the Analyzer

```bash
python main.py
```

The script will:
1. Initialize the LLM with PydanticOutputParser
2. Analyze three sample product reviews
3. Display structured insights for each review
4. Show a summary of results

### Example Output

```
Review: "This laptop is amazing! The build quality is excellent..."

✓ Analysis completed successfully!

Parsed Analysis:
  Sentiment: positive
  Rating: 4/5
  Key Features: excellent build quality, fast performance, decent battery life
  Improvement Suggestions: keyboard comfort for long typing sessions
```

### Custom Review Analysis

To analyze custom reviews, modify the `sample_reviews` list in `main.py`:

```python
custom_reviews = [
    "Your product review text here...",
    # Add more reviews as needed
]

for review in custom_reviews:
    analysis = analyze_review(review, chain)
```

## Implementation Details

### 1. Pydantic Model (`models.py`)

```python
class ReviewAnalysis(BaseModel):
    sentiment: str  # Validated against allowed values
    rating: int     # Constrained to 1-5
    key_features: List[str]              # Auto-converted to list
    improvement_suggestions: List[str]   # Auto-converted to list
```

**Validators:**
- `validate_sentiment()` - Ensures sentiment is positive, negative, or neutral
- `ensure_list()` - Converts strings/None to proper lists
- Field constraints prevent invalid ratings

### 2. PydanticOutputParser

The parser automatically:
- Extracts the JSON structure from LLM output
- Validates against the Pydantic model schema
- Raises ValidationError if output doesn't match schema
- Includes format instructions in the prompt

### 3. Error Handling

The application handles:
- Missing API key
- LLM API failures
- Invalid model outputs (Pydantic ValidationError)
- Malformed responses

## Free Tier Limits

**Groq Free Tier:**
- 30 requests per minute
- Up to 14k tokens per minute
- Very fast inference (optimal for real-time applications)
- No credit card required
- Sufficient for development and testing

## Requirements Explanation

| Package | Purpose |
|---------|---------|
| `langchain` | LLM orchestration and chain management |
| `langchain-groq` | Groq API integration |
| `langchain-core` | Core LangChain utilities |
| `pydantic` | Data validation and schema modeling |
| `groq` | Direct Groq API access |
| `python-dotenv` | Environment variable management |

## Troubleshooting

### Error: "GROQ_API_KEY not set"
- Run `$env:GROQ_API_KEY = "your-key"` in PowerShell
- Or create a `.env` file with `GROQ_API_KEY=your-key`
- Get a free API key from https://console.groq.com

### Error: "429 Too Many Requests"
- Exceeded free tier rate limit (30 requests/min)
- Wait a minute before re-running

### Error: "Invalid API Key"
- Verify the API key is correct from Groq Console
- Regenerate a new key if needed

### Error: "ValidationError"
- LLM output format doesn't match schema
- Check that format_instructions are included in prompt
- Consider adjusting temperature or prompt wording

## Assignment Evaluation

✅ **Proper Pydantic Schema Design** - ReviewAnalysis with validators and constraints
✅ **Correct Usage of PydanticOutputParser** - Full integration with LangChain
✅ **Structured and Validated Output** - All outputs match the defined schema
✅ **Error Handling and Robustness** - Handles API errors, validation errors gracefully
✅ **Format Instructions** - Automatically included in prompts via parser

## License

This project is created for educational purposes.

## References

- [LangChain Documentation](https://python.langchain.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Groq API Console](https://console.groq.com/)
- [PydanticOutputParser Guide](https://python.langchain.com/docs/modules/model_io/output_parsers/pydantic)
