# Use lightweight Python image
FROM python:3.12.1
# FROM python:3.11
# FROM python:3.9-slim-buster
# FROM python:3.10


# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Streamlit port
EXPOSE 8080

# Run Streamlit in Cloud Run (port must be 8080)
CMD ["streamlit", "run", "enhanced_ui.py", "--server.port=8080", "--server.address=0.0.0.0"]
