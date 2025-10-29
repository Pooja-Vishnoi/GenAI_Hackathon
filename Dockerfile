# Use lightweight Python image
FROM python:3.12.1

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies first (caches layers)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Ensure /app is in Python path (for agent imports)
ENV PYTHONPATH="/app"

# Expose Streamlit port
EXPOSE 8080

# Run Streamlit in Cloud Run (port must be 8080)
CMD ["streamlit", "run", "enhanced_ui_improved.py", "--server.port=8080", "--server.address=0.0.0.0"]
