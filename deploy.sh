#!/bin/bash

# LMU Campus LLM Deployment Script
# This script provides multiple deployment options for the LMU Campus LLM application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        print_status "Python version: $PYTHON_VERSION"
        
        # Parse version numbers
        MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$MAJOR" -gt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 8 ]); then
            return 0
        else
            print_error "Python 3.8 or higher is required"
            return 1
        fi
    else
        print_error "Python 3 is not installed"
        return 1
    fi
}

# Function to setup virtual environment
setup_venv() {
    print_status "Setting up virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    source venv/bin/activate
    print_status "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Function to run tests
run_tests() {
    print_status "Running application tests..."
    
    if [ -f "test_app.py" ]; then
        python test_app.py
        if [ $? -eq 0 ]; then
            print_success "All tests passed"
        else
            print_error "Some tests failed"
            exit 1
        fi
    else
        print_warning "Test file not found, skipping tests"
    fi
}

# Function to deploy locally
deploy_local() {
    print_status "Deploying application locally..."
    
    check_python_version
    setup_venv
    run_tests
    
    print_status "Starting Streamlit application..."
    print_status "Application will be available at: http://localhost:8501"
    print_status "Press Ctrl+C to stop the application"
    
    source venv/bin/activate
    streamlit run app.py --server.port 8501 --server.address 0.0.0.0
}

# Function to deploy with Docker
deploy_docker() {
    print_status "Deploying application with Docker..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    
    print_status "Building Docker image..."
    docker build -t lmu-campus-llm .
    
    if [ $? -eq 0 ]; then
        print_success "Docker image built successfully"
        
        print_status "Starting Docker container..."
        print_status "Application will be available at: http://localhost:8501"
        print_status "Press Ctrl+C to stop the container"
        
        docker run -p 8501:8501 -p 11434:11434 --name lmu-campus-llm-container lmu-campus-llm
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Function to deploy with Docker Compose
deploy_docker_compose() {
    print_status "Deploying application with Docker Compose..."
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Create docker-compose.yml if it doesn't exist
    if [ ! -f "docker-compose.yml" ]; then
        cat > docker-compose.yml << EOF
version: '3.8'

services:
  lmu-campus-llm:
    build: .
    ports:
      - "8501:8501"
      - "11434:11434"
    environment:
      - OLLAMA_HOST=0.0.0.0
      - OLLAMA_ORIGINS=*
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
EOF
        print_success "Created docker-compose.yml"
    fi
    
    print_status "Starting services with Docker Compose..."
    docker-compose up --build
}

# Function to stop Docker container
stop_docker() {
    print_status "Stopping Docker container..."
    
    if docker ps -q --filter "name=lmu-campus-llm-container" | grep -q .; then
        docker stop lmu-campus-llm-container
        docker rm lmu-campus-llm-container
        print_success "Docker container stopped and removed"
    else
        print_warning "No running container found"
    fi
}

# Function to show help
show_help() {
    echo "LMU Campus LLM Deployment Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  local           Deploy application locally with Python virtual environment"
    echo "  docker          Deploy application with Docker"
    echo "  compose         Deploy application with Docker Compose"
    echo "  stop            Stop Docker container"
    echo "  test            Run application tests only"
    echo "  setup           Setup virtual environment and install dependencies"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 local        # Deploy locally"
    echo "  $0 docker       # Deploy with Docker"
    echo "  $0 compose      # Deploy with Docker Compose"
    echo "  $0 stop         # Stop Docker container"
}

# Main script logic
case "${1:-help}" in
    "local")
        deploy_local
        ;;
    "docker")
        deploy_docker
        ;;
    "compose")
        deploy_docker_compose
        ;;
    "stop")
        stop_docker
        ;;
    "test")
        check_python_version
        setup_venv
        run_tests
        ;;
    "setup")
        check_python_version
        setup_venv
        print_success "Setup completed successfully"
        ;;
    "help"|*)
        show_help
        ;;
esac