# ============================================================================
=====================================================================
# Build:   docker build -t neo-judge:latest .
# Run:     docker run --env-file .env -v ./service-account.json:/app/service-account.json neo-judge:latest
# Compose: docker-compose up -d
# ============================================================================

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for multi-language compilation
=======
# Dockerfile for NEO ONLINE JUDGE
# ============================================================================
# Build: docker build -t neo-judge:latest .
# Run: docker run -e OPENAI_API_KEY=xxx -v ./service-account.json:/app/service-account.json neo-judge:latest
# ============================================================================

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (g++ for C++ compilation)
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    gcc \

    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY judge.py .
COPY .env .env

# Create logs directory
RUN mkdir -p logs


# Expose if needed (Judge runs in background)
# EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Run judge server
CMD ["python", "-u", "judge.py"]

