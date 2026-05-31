#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

echo "Installing dependencies..."
npm install

echo "Starting the development server..."
npm run dev 