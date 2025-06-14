# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libffi-dev g++ curl libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Copy the requirements and install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt \
    && apt-get purge -y gcc build-essential g++ \
    && apt-get autoremove -y \
    && rm -rf /root/.cache

# Stage 2: Runtime Image
FROM python:3.11-slim

WORKDIR /app

# Install minimal required packages for runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev openssh-server \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose port for SSH and application
EXPOSE 80 2222 8000

# Declare and pass build argument
ARG ENVIRONMENT
ENV ENVIRONMENT=${ENVIRONMENT}

# Set other environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copy dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app source code
COPY ./src /app/src

# Install runtime Redis client
RUN pip install redis

# Debug output
RUN echo "Environment: $ENVIRONMENT"

# Start FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
