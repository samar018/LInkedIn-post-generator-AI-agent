LinkedIn Post Generator Agent

An AI-powered LinkedIn post generator built with LangChain that creates professional, engaging LinkedIn posts based on user-specified topics and languages. This project supports both a Command Line Interface (CLI) for scripting and a Full Web Application for easy, interactive use.

🚀 Features

Topic-based Generation: Generate LinkedIn posts on any professional topic.

Multi-language Support: Create posts in different languages (English, Spanish, Bengali, etc.).

Professional Structure: Posts include title, content (2-4 paragraphs), hashtags, and call-to-action.

LangChain Integration: Built with LangChain for robust AI agent functionality.

Structured Output: Uses Pydantic models for consistent, well-formatted posts.

Web Interface: Optional FastAPI backend and HTML/JS frontend for a modern, accessible UI.

Error Handling: Robust error handling with graceful fallback options.

📋 Requirements

Python 3.8+

API key for your chosen LLM provider (e.g., OpenAI, custom endpoint).

Required packages (see requirements.txt).

Docker and Docker Compose (Optional, for web app distribution).

📂 Project Structure

This project supports two execution modes (CLI and Web), resulting in a comprehensive file structure:

/
├── App/
│   ├── main.py        # FastAPI application and Pydantic schema for the Web Interface
│   ├── requirements.txt # Python dependencies
│   └── Lnkedin_post_agent.py # The original CLI Agent script
├── index.html         # Frontend user interface (HTML, JS, CSS)
├── .env               # Environment file for API keys (crucial)
├── Dockerfile         # Docker build instructions for the FastAPI backend
├── docker-compose.yml # Orchestrates the backend and frontend (Nginx) containers
└── nginx.conf         # Nginx proxy configuration for Docker networking



🛠️ Installation & Configuration

1. Clone the Repository

git clone <repository-url>
cd linkedin-post-generator-agent


2. Install Dependencies

Install all required Python packages:

pip install -r requirements.txt
# If a requirements.txt doesn't exist, use:
# pip install "fastapi[all]" uvicorn pydantic python-dotenv openai langchain


3. Configure Environment Variables

Create a file named .env in the root directory and add your API credentials.

# Configuration for the LLM API (Flexible for various providers)
API_KEY="sk-YOUR_SECRET_API_KEY_HERE"
BASE_URL="[https://models.github.ai/inference](https://models.github.ai/inference)" # Custom or standard API endpoint URL
MODEL_NAME="gpt-4o-mini" # The specific model to be used



🎯 Usage: Command Line Interface (CLI)

This is the original, non-web-based agent mode, ideal for scripting or quick generation.

Running the Agent

python Lnkedin_post_agent.py


Input and Example Usage

Interactive Mode: Run the script and follow the prompts.

Enter your request: AI in Healthcare, English


Demo Mode: The script includes built-in demos that can be run directly.

🌐 Usage: Web Interface (FastAPI & HTML)

This method provides a graphical, browser-based interface for easy interaction.

💻 Option 1: Manual Local Setup (Development)

This requires running the frontend and backend in two separate terminal sessions.

Terminal 1 (Backend: Port 8000)

Terminal 2 (Frontend: Port 8080)

Start the FastAPI server:

Start the simple HTTP server to serve index.html:

uvicorn App.main:app --reload

python -m http.server 8080 --bind 127.0.0.1

Access the App: Open your browser and navigate to: http://127.0.0.1:8080

🐋 Option 2: Docker Setup (Distribution)

This uses Docker Compose to manage both services, simplifying the run process into a single command.

Build and Run Containers: Run the following command from the root of your project directory.

docker compose up --build


Access the App: Open your browser and navigate to: http://localhost:8080

Shutdown: To stop the containers when finished, press Ctrl+C and run:

docker compose down


📝 Output Structure

Each generated post, regardless of the usage method, adheres to the following structured format:

Title: Catchy headline for the post.

Content: 2-4 paragraphs of professional content.

Hashtags: Relevant professional hashtags.

Call-to-Action: Engaging prompt to encourage interaction.

💡 Troubleshooting

Problem

Likely Cause

Solution

"Failed to fetch" (Web App)

Frontend (8080) cannot connect to Backend (8000).

Ensure both Terminal 1 (uvicorn) and Terminal 2 (http.server) are running. If using Docker, ensure all containers are up.

"API Error: Status 401 Unauthorized"

The LLM API key is invalid or expired.

Check your .env file. Correct the API_KEY, stop the servers (or docker compose down), and restart them.

Loading Spinner Stuck

Backend crashed during the LLM call.

Crucially, check the Uvicorn terminal (Port 8000) for a Python Traceback—this will show the exact error (e.g., a connection timeout or model configuration issue).

🤝 Contributing & License

Feel free to submit issues, feature requests, or pull requests. This project is open source and available under the MIT License.