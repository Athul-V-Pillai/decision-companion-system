#!/bin/bash
# Decision Companion System - Quick Start Script for macOS/Linux

echo ""
echo "==================================="
echo "Decision Companion System Startup"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from python.org"
    exit 1
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Run Flask app
echo ""
echo "==================================="
echo "Starting Flask server..."
echo "==================================="
echo ""
echo "Open your browser and navigate to:"
echo "http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
