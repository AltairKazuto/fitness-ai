#!/bin/bash

# Go to frontend and start dev server in background
echo "Installing Javascript dependencies..."
cd frontend || exit
npm install   # & runs it in the background
cd ../

# Go to backend and start backend in background
echo "Installing Python dependencies..."
cd backend || exit
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt

deactivate
echo "Installation complete"
read -n 1 -s -r -p "Press any key to exit..."
