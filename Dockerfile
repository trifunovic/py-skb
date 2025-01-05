# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libffi-dev g++ curl libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y gcc build-essential g++ \
    && apt-get autoremove -y \
    && rm -rf /root/.cache

# Stage 2: Runtime Image
FROM python:3.11-slim

WORKDIR /app

# Install minimal required packages for runtime (Redis + Python runtime essentials)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for Python behavior
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1         
ENV PYTHONPATH=/app            

# Copy dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app source code
COPY ./src /app/src

# Redis dependency (redundant but safe if omitted in requirements.txt)
RUN pip install --no-cache-dir redis

# Expose the port and run the application
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
