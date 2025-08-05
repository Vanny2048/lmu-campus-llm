#!/bin/bash

# LMU Campus LLM Deployment Script
# This script provides deployment options for different platforms

set -e

echo "🦁 LMU Campus LLM Deployment Script"
echo "=================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install dependencies
install_dependencies() {
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed successfully!"
}

# Function to run locally
run_local() {
    echo "🚀 Starting LMU Campus LLM locally..."
    streamlit run app.py
}

# Function to run with Docker
run_docker() {
    if ! command_exists docker; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    echo "🐳 Building and running with Docker..."
    docker-compose up --build
}

# Function to deploy to Streamlit Cloud
deploy_streamlit_cloud() {
    echo "☁️ Preparing for Streamlit Cloud deployment..."
    echo "1. Make sure your code is pushed to GitHub"
    echo "2. Go to https://share.streamlit.io/"
    echo "3. Connect your GitHub repository"
    echo "4. Set the main file path to: app.py"
    echo "5. Deploy!"
    echo ""
    echo "Your app will be available at: https://your-app-name.streamlit.app"
}

# Function to deploy to Heroku
deploy_heroku() {
    if ! command_exists heroku; then
        echo "❌ Heroku CLI is not installed. Please install it first."
        exit 1
    fi
    
    echo "🚀 Deploying to Heroku..."
    
    # Create Procfile if it doesn't exist
    if [ ! -f Procfile ]; then
        echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
    fi
    
    # Create runtime.txt if it doesn't exist
    if [ ! -f runtime.txt ]; then
        echo "python-3.9.18" > runtime.txt
    fi
    
    # Deploy to Heroku
    heroku create lmu-campus-llm-$(date +%s)
    git add .
    git commit -m "Deploy to Heroku"
    git push heroku main
    
    echo "✅ Deployed to Heroku!"
    echo "Your app URL: https://$(heroku info -s | grep web_url | cut -d= -f2)"
}

# Function to deploy to Railway
deploy_railway() {
    if ! command_exists railway; then
        echo "❌ Railway CLI is not installed. Please install it first."
        exit 1
    fi
    
    echo "🚂 Deploying to Railway..."
    railway login
    railway init
    railway up
    
    echo "✅ Deployed to Railway!"
}

# Function to run tests
run_tests() {
    echo "🧪 Running tests..."
    
    # Test the application
    python3 -c "
import streamlit as st
import sys
sys.path.append('.')
from app import load_waitlist, save_waitlist, get_lmu_buddy_response

# Test waitlist functions
test_data = [{'name': 'Test User', 'email': 'test@lmu.edu', 'timestamp': '2024-01-01T00:00:00'}]
save_waitlist(test_data)
loaded_data = load_waitlist()
assert len(loaded_data) == 1, 'Waitlist test failed'

# Test AI response
response = get_lmu_buddy_response('Best food on campus?')
assert 'Lair' in response, 'AI response test failed'

print('✅ All tests passed!')
"
}

# Main menu
show_menu() {
    echo ""
    echo "Choose a deployment option:"
    echo "1) Install dependencies only"
    echo "2) Run locally"
    echo "3) Run with Docker"
    echo "4) Deploy to Streamlit Cloud"
    echo "5) Deploy to Heroku"
    echo "6) Deploy to Railway"
    echo "7) Run tests"
    echo "8) Exit"
    echo ""
    read -p "Enter your choice (1-8): " choice
    
    case $choice in
        1) install_dependencies ;;
        2) run_local ;;
        3) run_docker ;;
        4) deploy_streamlit_cloud ;;
        5) deploy_heroku ;;
        6) deploy_railway ;;
        7) run_tests ;;
        8) echo "👋 Goodbye!"; exit 0 ;;
        *) echo "❌ Invalid choice. Please try again."; show_menu ;;
    esac
}

# Check if arguments were provided
if [ $# -eq 0 ]; then
    show_menu
else
    case $1 in
        "install") install_dependencies ;;
        "local") run_local ;;
        "docker") run_docker ;;
        "streamlit") deploy_streamlit_cloud ;;
        "heroku") deploy_heroku ;;
        "railway") deploy_railway ;;
        "test") run_tests ;;
        *) echo "❌ Invalid argument. Use: install, local, docker, streamlit, heroku, railway, or test"; exit 1 ;;
    esac
fi