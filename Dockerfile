# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Build argument for Azure Key Vault
ARG AZURE_KEY_VAULT_NAME
# Optional: Use build argument in the environment
ENV AZURE_KEY_VAULT_NAME=$AZURE_KEY_VAULT_NAME

# Install system dependencies and pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libffi-dev g++ curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final runtime image
FROM python:3.11-slim

WORKDIR /app

# Install tools required for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copy dependencies and application files
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . /app

# Expose the application port
EXPOSE 8000

# Health check for the container
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
     CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
