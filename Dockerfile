# Use a fuller base image so building wheels works
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app

# Install OS-level build deps commonly required for Python packages
# libpq-dev for psycopg2, build-essential/gcc, curl/git, cmake, rust (cargo) for extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    python3-dev \
    curl \
    git \
    cmake \
    pkg-config \
    rustc \
    cargo \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip / setuptools / wheel / build — important for pyproject builds
RUN python -m pip install --upgrade pip setuptools wheel build

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create a non-root user (optional but recommended)
RUN useradd --create-home --shell /bin/bash papercargo || true
USER papercargo

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
