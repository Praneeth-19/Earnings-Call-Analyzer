# Earnings Call Analyzer (Mistral + Ollama)
An AI-powered assistant to analyze earnings call transcripts, summarize them,
## Features
- Summary in 3 lines
- Sentiment classification
- Extracted insights (guidance, risks, growth)
- Streamlit frontend + FastAPI backend

- Ollama-hosted LLMs (Mistral)
## Run Locally
1. Pull model: `ollama pull mistral`
2. Start backend: `uvicorn backend.main:app --reload`
3. Start frontend: `streamlit run frontend/app.py`