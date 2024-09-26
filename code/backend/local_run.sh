#!/bin/bash

# Check if .env file exists
if [ -d ".env" ]; then
    # Activate virtual environment
    source .env/bin/activate

    # Start Python Flask app
    python3 app.py

    deactivate
else
    echo ".env file not found"
fi
