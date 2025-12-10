#!/bin/bash

# Go to frontend and start dev server in background
echo "Starting frontend..."
cd frontend || exit
npm run dev &   # & runs it in the background
cd ..

# Go to backend and start backend in background
echo "Starting backend..."
cd backend || exit
source myenv/bin/activate
python backend.py &

# Wait for all background processes
wait
