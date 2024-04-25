# Use Python slim image for a balance between size and functionality.
FROM python:3.12.2-slim

# Combine ENV statements
# Set environment variables:
# 1. PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (facilitates logging in Docker containers).
# 2. PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disk (reduces container size).
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory to /app. This is where the application code will live within the container.
WORKDIR /app

# Copy the Python requirements file first to leverage Docker cache layers.
# The requirements file is copied to the current directory (/app) instead of /tmp to simplify paths.
COPY ./requirements.txt .
COPY ./requirements.dev.txt .

# Copy the application code and entrypoint script into the container.
COPY ./ /app
# Add entrypoint script to /usr/local/bin
COPY ./entrypoint/entrypoint.sh /usr/local/bin/
COPY entrypoint entrypoint

ARG DEV=false

# Install dependencies in a virtual environment for isolation and cleanup in one layer to reduce image size.
# Also, correct the command to create a new user with a specified UID for better security practices.
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt && \
    if [ $DEV = "true" ]; \
        then /venv/bin/pip install -r requirements.dev.txt ; \
    fi && \
    adduser --uid 1001 --disabled-password --no-create-home django-user && \
    # Change ownership to non-root user
    chown -R django-user:django-user /app

# Adds the virtual environment binaries to the PATH, making it possible to run Python commands from anywhere in the container.
ENV PATH="/venv/bin:$PATH"

# Use the newly created user to run the application.
USER django-user

# Expose the port the app runs on.
EXPOSE 8000

# Use the entrypoint script to start the application.
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
