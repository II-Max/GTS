# ============================================================================
# NEO ONLINE JUDGE v2.0 - Dockerfile
# ============================================================================
# Build:   docker build -t neo-judge:latest .
# Run:     docker run --env-file .env -v ./service-account.json:/app/service-account.json neo-judge:latest
# Compose: docker-compose up -d
# ============================================================================

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for multi-language compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    gcc \
    default-jdk \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (modular structure)
COPY judge.py .
COPY backend/ backend/
COPY config/ config/
COPY .env.example .env

# Create logs directory
RUN mkdir -p logs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from backend.app import JudgeApplication; print('OK')" || exit 1

# Run judge server
CMD ["python", "-u", "judge.py"]
