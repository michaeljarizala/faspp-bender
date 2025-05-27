# == Official System Specification ==
# Ensure we are using Ubuntu 22.04 or higher
FROM ubuntu:22.04

# == Official Python Image==
# Here we use 3.11 as base version so
# so all developers must have at least this verion
# in order to proceed with local development.
FROM python:3.11-slim-bullseye

# == PYTHONPATH Specification ==
ENV PYTHONPATH=/ukiran

# == Working Directory ==
# Specify our entry point for Arko.
# In this case, we set it to the "app" directory.
WORKDIR /ukiran

# == System Dependencies Installation ==
# Install the required system packages,
# in this case for Ubuntu Linux.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# == Copy Dependecies File ==
# Copy requirements.txt
COPY requirements.txt .

# == Project Dependencies Installation ==
# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# == Copy Application Files ==
COPY . .

# == Port Specification ==
# Expore FastAPI port
EXPOSE 40002

# == Running App ==
# Run the application
# CMD ["sh", "-c", "uvicorn app.main:app --host $HOST --port $PORT --reload"]
CMD uvicorn ukiran.main:app --host $HOST --port $PORT --reload