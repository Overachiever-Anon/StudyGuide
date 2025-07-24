FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Default to port 7860 for Hugging Face Spaces compatibility
EXPOSE 7860

# Change to the backend directory and run gunicorn
CMD cd backend && gunicorn "backend:create_app()" --bind 0.0.0.0:7860
