# 🚀 LMU Campus LLM Deployment Guide

This guide provides comprehensive instructions for deploying the LMU Campus LLM application using various methods.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended for optimal performance)
- **Storage**: At least 2GB free space
- **Network**: Internet connection for downloading models and dependencies

### Required Software
- Python 3.8+
- pip (Python package installer)
- Git (for cloning the repository)

### Optional Software
- Docker (for containerized deployment)
- Docker Compose (for multi-service deployment)

## 🔧 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd lmu-campus-llm
```

### 2. Run the Deployment Script
The easiest way to deploy is using the provided deployment script:

```bash
# Make the script executable (if not already)
chmod +x deploy.sh

# Deploy locally
./deploy.sh local

# Or deploy with Docker
./deploy.sh docker

# Or deploy with Docker Compose
./deploy.sh compose
```

## 🐍 Local Deployment

### Step 1: Setup Python Environment
```bash
# Check Python version
python3 --version

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
```

### Step 2: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 3: Run Tests
```bash
python test_app.py
```

### Step 4: Start the Application
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

The application will be available at: **http://localhost:8501**

## 🐳 Docker Deployment

### Prerequisites
- Docker installed and running
- Docker daemon accessible

### Step 1: Build the Image
```bash
docker build -t lmu-campus-llm .
```

### Step 2: Run the Container
```bash
docker run -p 8501:8501 -p 11434:11434 --name lmu-campus-llm-container lmu-campus-llm
```

### Step 3: Access the Application
The application will be available at: **http://localhost:8501**

### Step 4: Stop the Container
```bash
docker stop lmu-campus-llm-container
docker rm lmu-campus-llm-container
```

## 🐙 Docker Compose Deployment

### Prerequisites
- Docker Compose installed
- Docker daemon running

### Step 1: Create docker-compose.yml
The deployment script will create this automatically, or you can create it manually:

```yaml
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
```

### Step 2: Start Services
```bash
docker-compose up --build
```

### Step 3: Stop Services
```bash
docker-compose down
```

## 🌐 Production Deployment

### Environment Variables
Set these environment variables for production:

```bash
export OLLAMA_HOST=0.0.0.0
export OLLAMA_ORIGINS=*
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
```

### Reverse Proxy (Nginx)
For production, use a reverse proxy like Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

### SSL/HTTPS
For HTTPS, use Let's Encrypt or your preferred SSL certificate provider.

## 🔍 Testing

### Run All Tests
```bash
python test_app.py
```

### Manual Testing
1. Open the application in your browser
2. Test the waitlist functionality
3. Test the LMU Buddy chat
4. Test the analytics dashboard
5. Verify all features work as expected

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port 8501
lsof -i :8501

# Kill the process
kill -9 <PID>
```

#### 2. Docker Permission Issues
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Restart Docker service
sudo systemctl restart docker
```

#### 3. Python Import Errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### 4. Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama manually if needed
ollama serve
```

#### 5. Memory Issues
- Increase Docker memory limit
- Use smaller models
- Optimize batch sizes

### Logs and Debugging

#### Streamlit Logs
```bash
streamlit run app.py --logger.level debug
```

#### Docker Logs
```bash
docker logs lmu-campus-llm-container
```

#### Docker Compose Logs
```bash
docker-compose logs -f
```

## 📊 Monitoring

### Health Checks
The application includes health checks for:
- Ollama service availability
- Streamlit application status
- Model loading status

### Metrics to Monitor
- Application response time
- Memory usage
- CPU usage
- Error rates
- User engagement metrics

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Rebuild Docker image
docker build -t lmu-campus-llm .

# Restart services
docker-compose down
docker-compose up --build
```

### Backup Data
```bash
# Backup waitlist data
cp waitlist.json backup/waitlist_$(date +%Y%m%d_%H%M%S).json

# Backup embeddings
cp lmu_embeddings.pkl backup/embeddings_$(date +%Y%m%d_%H%M%S).pkl
```

## 📞 Support

### Getting Help
1. Check the troubleshooting section above
2. Review the application logs
3. Check the GitHub issues page
4. Contact the development team

### Reporting Issues
When reporting issues, please include:
- Deployment method used
- Error messages
- System specifications
- Steps to reproduce the issue

## 🎯 Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] Tests passing
- [ ] Application starts successfully
- [ ] All features working
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] SSL certificate configured (production)
- [ ] Domain configured (production)

## 🚀 Quick Commands Reference

```bash
# Local deployment
./deploy.sh local

# Docker deployment
./deploy.sh docker

# Docker Compose deployment
./deploy.sh compose

# Run tests only
./deploy.sh test

# Setup environment only
./deploy.sh setup

# Stop Docker container
./deploy.sh stop

# Show help
./deploy.sh help
```

---

**Happy Deploying! 🎉**

For more information, check the main README.md file or contact the development team.