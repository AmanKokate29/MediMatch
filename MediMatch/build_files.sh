#!/bin/bash
# Build script for Vercel deployment
set -e

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt

echo "Collecting static files..."
mkdir -p staticfiles
python3 manage.py collectstatic --noinput --clear

echo "Vercel build complete!"
