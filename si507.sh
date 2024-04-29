#!/bin/bash

# Ensure script is run with correct privileges and environment is provided
if [ "$EUID" -ne 0 ]
  then echo "Please run as root or use sudo"
  exit
fi

if [ -z "$1" ]
  then echo "No environment name supplied. Usage: ./setup_and_run.sh <env_name>"
  exit
fi

ENV_NAME=$1

# Step 1: Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv $ENV_NAME

# Step 2: Activate the virtual environment
echo "Activating the virtual environment..."
source $ENV_NAME/bin/activate

# Step 3: Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Step 4: Run the Flask application or a specific Python script
echo "Running the Flask application..."
# Replace 'your_flask_app.py' with the name of your Flask application script
export FLASK_APP=your_flask_app.py
export FLASK_ENV=development
flask run

# Optional: Deactivate the virtual environment when done
echo "Deactivating the virtual environment..."
deactivate