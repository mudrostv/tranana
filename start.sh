#!/bin/bash
# Start script for Tron Wallet Connection Analyzer

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies if needed
echo "Checking dependencies..."
pip install -q -r requirements.txt

# Start the Flask application
echo ""
echo "Starting Tron Wallet Connection Analyzer..."
echo "Server will be available at: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py


