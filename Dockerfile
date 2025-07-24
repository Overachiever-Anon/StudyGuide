# Stage 1: Build the React frontend
FROM node:18-alpine AS build-frontend
WORKDIR /app

# Copy package files and install dependencies
COPY frontend/package.json frontend/package-lock.json ./frontend/
RUN cd frontend && npm install

# Copy the rest of the frontend source code
COPY frontend/ ./frontend/

# Build the frontend for production
RUN cd frontend && npm run build

# Stage 2: Build the Python backend
FROM python:3.9-slim
WORKDIR /app

# Set environment variables for Flask
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=run:app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend and the root run.py file
COPY backend/ ./backend/
COPY backend/run.py .

# Copy the built frontend from the previous stage into a static folder
# that the Flask app can serve.
COPY --from=build-frontend /app/frontend/dist ./backend/static

# Expose the port Hugging Face uses
EXPOSE 7860

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "run:app"]
