# Use lightweight Python image
FROM python:3.12.1-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PDF processing and OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libpoppler-cpp-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies first (caches layers)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . /app

# Ensure /app is in Python path (for agent imports)
ENV PYTHONPATH="/app"

# Set environment variables for better cloud compatibility
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

# Fix asyncio event loop policy for cloud environments
ENV PYTHONIOENCODING=utf-8
ENV PYTHONASYNCIODEBUG=0

# Expose Streamlit port
EXPOSE 8080

# Health check for Cloud Run
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/_stcore/health || exit 1

# Run Streamlit in Cloud Run (port must be 8080)
CMD ["streamlit", "run", "enhanced_ui_improved.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
