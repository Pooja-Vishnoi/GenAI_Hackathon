pip install google-adk
pip install google-genai
pip install google-generativeai
pip install google-cloud-vision

instead of running it here in power shell, 
run it in command prompt as administrator, actovate virtual env, go to project path
and run command

you should be out of project folder to run this command
adk run <project folder>
or 
adk run ./adk-agent

if you want to run in browser or web UI
adk web

<!--  --> -----------------------------------------------------------------
🔑 Gemini API (via Google AI Studio / Vertex AI)

Uses API Key (string like AIza....).

Enough if you only want Gemini (LLMs, embeddings, etc.).

Easy to set in your ADK config as GEMINI_API_KEY.

🔑 Google Cloud Client Libraries (like Vision, BigQuery, Storage, etc.)

Use Service Account Credentials (JSON file).

This JSON file is called Google Cloud credentials.

It contains a private key + permissions so your code can access Cloud Vision, BigQuery, etc.


Summary

If digital PDF → use PyPDF2 or pdfplumber (fast, free, no API).

If scanned PDF → use Google Cloud Vision OCR (needs credentials + billing).
