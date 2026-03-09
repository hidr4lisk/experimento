# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Collect static files (optional, but good practice for production with whitenoise)
# We handle this conditionally in a startup script if needed, or inline.
# For now, let's just make sure the project directory is copied.
# If STATIC_ROOT is set in settings, we could run collectstatic here:
RUN python manage.py collectstatic --noinput || true

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application using Gunicorn
CMD ["gunicorn", "experimento.wsgi:application", "--bind", "0.0.0.0:8000"]
