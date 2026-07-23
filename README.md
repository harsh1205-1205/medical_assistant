# Medical Assistant App

A Streamlit-based medical assistant chatbot that uses the Groq API for general health information responses.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set the environment variable:

```bash
set GROQ_API_KEY=your_api_key_here
```

4. Start the app:

```bash
streamlit run app.py
```

## Production notes

- Store secrets in environment variables, not in source files.
- Keep `.env` and secret files out of version control via `.gitignore`.
- Use a hosted environment or deployment platform to inject `GROQ_API_KEY` securely.
