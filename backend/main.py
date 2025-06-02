from fastapi import FastAPI, Form
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def query_model(prompt: str):
    try:
        logger.info(f"Querying model with prompt length: {len(prompt)}")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral","prompt": prompt,"stream": False},
            #json={"model": "tinyllama", "prompt": prompt, "stream": False},
            timeout=60  # Add a timeout for the request
        )
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()["response"].strip()
    except requests.exceptions.RequestException as e:
        error_msg = f"Error querying model: {e}"
        logger.error(error_msg)
        return f"Error: Could not get response from model. {e}"

@app.post("/analyze/")
def analyze_call(text: str = Form(...)):
    # Truncate text if it's too long
    max_length = 4000  # Adjust based on model capabilities
    if len(text) > max_length:
        logger.warning(f"Truncating input from {len(text)} to {max_length} characters")
        text = text[:max_length]
    
    prompts = {
        "summary": f"Summarize the following earnings call transcript in 3 sentences: {text}",
        "sentiment": f"What is the overall sentiment (Positive, Neutral, Negative) of the following earnings call transcript: {text}",
        "insights": f"Extract key financial insights (growth, risk, guidance, etc.) from the following earnings call transcript: {text}",
    }
    
    result = {}
    for k, p in prompts.items():
        response = query_model(p)
        # Check if the response is an error message
        if response.startswith("Error:"):
            result[k] = "Unable to analyze due to service error"
            logger.error(f"Error in {k} analysis: {response}")
        else:
            result[k] = response
            
    return result