#!/bin/bash

# Setup script for Auto Clicker project on macOS

echo "Setting up Auto Clicker project..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo ""
echo "To run the application:"
echo "1. source venv/bin/activate"
echo "2. python auto_clicker.py"
echo ""
echo "Note: On macOS, you may need to grant accessibility permissions:"
echo "System Preferences > Security & Privacy > Privacy > Accessibility"
