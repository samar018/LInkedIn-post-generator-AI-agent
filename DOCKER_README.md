# LinkedIn Post Generator - Docker Setup

This guide will help you run the LinkedIn Post Generator application using Docker and Docker Compose.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

## Quick Start

### 1. Clone and Setup Environment

```bash
# Clone the repository (if not already done)
git clone <your-repo-url>
cd LangChain-powered_AI_agent

# Copy the environment template
cp env.example .env

# Edit the .env file with your API configuration
nano .env
```

### 2. Configure Environment Variables

Edit the `.env` file with your preferred AI model configuration:

#### Option A: OpenAI Configuration
```env
BASE_URL=https://api.openai.com/v1
API_KEY=sk-your-openai-api-key-here
MODEL_NAME=gpt-4o-mini
```

#### Option B: Local Ollama Configuration
```env
BASE_URL=http://localhost:11434
API_KEY=ollama
MODEL_NAME=llama2
```

#### Option C: Docker Ollama Service
```env
BASE_URL=http://ollama:11434
API_KEY=ollama
MODEL_NAME=mistral
```

### 3. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### 4. Access the Application

- **Frontend (Web Interface)**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Docker Services

### Backend Service
- **Container**: `linkedin-post-generator-api`
- **Port**: 8000
- **Health Check**: Automatic health monitoring
- **Restart Policy**: Unless stopped

### Frontend Service
- **Container**: `linkedin-post-generator-frontend`
- **Port**: 80 (HTTP), 443 (HTTPS)
- **Web Server**: Nginx
- **Dependencies**: Waits for backend to be healthy

### Optional: Ollama Service
Uncomment the Ollama service in `docker-compose.yml` if you want to run local AI models:

```yaml
ollama:
  image: ollama/ollama:latest
  container_name: ollama-server
  ports:
    - "11434:11434"
  volumes:
    - ollama_data:/root/.ollama
  # ... rest of configuration
```

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Rebuild Services
```bash
# Rebuild and restart
docker-compose up --build --force-recreate
```

### Access Container Shell
```bash
# Backend container
docker-compose exec backend bash

# Frontend container
docker-compose exec frontend sh
```

## Development Mode

For development, you can run the backend directly:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp env.example .env
# Edit .env with your configuration

# Run the backend
cd App
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Serve frontend separately (optional)
# Open frontend/index.html in browser
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   netstat -tulpn | grep :8000
   
   # Change ports in docker-compose.yml if needed
   ```

2. **API Key Not Working**
   - Verify your API key is correct
   - Check the BASE_URL matches your provider
   - For OpenAI, ensure you have sufficient credits

3. **Frontend Can't Connect to Backend**
   - Ensure backend is healthy: `docker-compose ps`
   - Check backend logs: `docker-compose logs backend`
   - Verify environment variables are set correctly

4. **Permission Issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

### Health Checks

Check service health:
```bash
# Backend health
curl http://localhost:8000/

# Frontend health
curl http://localhost/health
```

### Clean Restart

If you encounter issues:
```bash
# Stop everything
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Rebuild from scratch
docker-compose up --build
```

## Production Deployment

For production deployment:

1. **Use HTTPS**: Configure SSL certificates in nginx.conf
2. **Environment Variables**: Use Docker secrets or external configuration
3. **Resource Limits**: Add resource constraints in docker-compose.yml
4. **Monitoring**: Add logging and monitoring services
5. **Backup**: Regular backup of any persistent data

### Production docker-compose.yml additions:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs`
2. Verify your `.env` configuration
3. Ensure Docker and Docker Compose are up to date
4. Check that all required ports are available
