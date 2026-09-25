FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install CPU PyTorch
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

# Expose ports for cloud hosting (7860 for Hugging Face Spaces, 8000 for standard)
EXPOSE 7860
EXPOSE 8000

ENV PORT=7860
ENV HOST=0.0.0.0

CMD ["python", "main.py"]
