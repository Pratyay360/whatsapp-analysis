# ====================================================================================
# BUILD STAGE
# ====================================================================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gcc \
        libfreetype6-dev libpng-dev libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Only remove Python cache files, preserve ALL metadata
RUN find /opt/venv -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -type f -name '*.pyc' -delete

# ====================================================================================
# PRODUCTION STAGE
# ====================================================================================
FROM python:3.12-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        libfreetype6 libpng16-16 libjpeg62-turbo zlib1g \
        wget fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Create user BEFORE setting workdir
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -m -d /home/appuser appuser

# Set working directory and ensure ownership
WORKDIR /app
RUN chown appuser:appgroup /app

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set Streamlit environment variables to avoid permission issues
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_CONFIG_DIR=/tmp/.streamlit
ENV STREAMLIT_CREDENTIALS_DIR=/tmp/.streamlit

# Create Streamlit config directory
RUN mkdir -p /tmp/.streamlit && chmod 755 /tmp/.streamlit

# Switch to non-root user
USER appuser

# Copy application code
COPY --chown=appuser:appgroup . .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=2 \
    CMD wget -nv -t1 --spider http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.headless=true"]
