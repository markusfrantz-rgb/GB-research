FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy all project files
COPY . .

# Index documents at build time (no API key needed for build, will re-index at start)
# Create chroma_db directory
RUN mkdir -p chroma_db

EXPOSE 8080

# Start script: ingest documents then run server
CMD ["sh", "start.sh"]
