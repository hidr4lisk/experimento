#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create static files
python manage.py collectstatic --no-input

# Apply migrations
echo "==> Running migrations..."
python manage.py makemigrations --no-input
python manage.py migrate --no-input

# Initialize default users and agents
echo "==> Initializing users and agents..."
python init_users.py
python manage.py populate_agents
