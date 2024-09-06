# Use Debian Bookworm as the base image
FROM debian:bookworm

# Set environment variables to ensure non-interactive installations
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install essential packages
RUN apt-get update && \
     apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    wget \
    vim \
    git \
    build-essential \
    python3 \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Example: Add a file to the image (you can change this)
COPY emaker.py /app/emaker.py
COPY messages.py /app/messages.py
COPY requirements.txt /app/requirements.txt

# Install requirements for app
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install --upgrade pip \
    && /app/venv/bin/pip install -r requirements.txt

# Make sure the virtual environment's python and pip are used
ENV PATH="/app/venv/bin:$PATH"

CMD ["python3", "/app/emaker.py"]

