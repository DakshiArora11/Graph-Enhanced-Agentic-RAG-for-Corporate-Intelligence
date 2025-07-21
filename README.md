Graph-Enhanced-Agentic-RAG-for-Corporate-Intelligence

An application designed for corporate intelligence, utilizing Retrieval-Augmented Generation (RAG) enhanced with agentic capabilities and graph-based reasoning. The tool enables users to query PDF documents, leveraging vector search (via ChromaDB) and graph queries (via Neo4j) to extract insights, with responses synthesized using advanced natural language processing techniques. Data is persistently stored in a MongoDB Atlas database, making it ideal for enterprise use cases such as market analysis, competitor tracking, or internal knowledge management.

Features
Query Analysis: Classifies and processes user queries for optimal response generation.
Vector Search: Retrieves relevant document chunks using ChromaDB for semantic similarity.
Graph Queries: Executes relational queries via Neo4j to uncover connections in data.
Response Synthesis: Integrates vector and graph results with NLP models (e.g., Transformers) for coherent answers.
Conversation History: Stores and displays past interactions in a searchable sidebar, powered by MongoDB.
Interactive UI: Features a responsive design with progress bars and a clean layout, built with Streamlit.
Scalable Deployment: Optimized for Render’s free tier with Docker, supporting future scaling.

Prerequisites
Python: Version 3.9 or higher.
Git: For version control and deployment.
MongoDB Atlas: A free-tier cluster for database storage.
GitHub Account: To host the repository.
Render Account: For cloud deployment.
API Keys: Gemmini API Key and Hugging Face Token (for NLP features, if enabled).

Installation
Dependencies:
pip install -r requirements.txt
Create a .env file (not tracked by Git) with:
MONGODB_URI=your_mongodb_atlas_connection_string
GEMINI_API_KEY=your_gemini_api_key
HUGGINGFACE_TOKEN=your_huggingface_token
Alternatively, set these as environment variables in your shell.
Run the Application:
streamlit run app.py

Access it at http://localhost:8501 in your browser.

Example Usage
Query: "What products does Netflix offer?"
Result: The app retrieves relevant PDF text, queries a graph for related entities (e.g., streaming services), and synthesizes a response like: "Netflix offers streaming services for movies and TV shows, with additional features like Netflix Originals and interactive content."

Deployment
This app is deployed on Render using Docker for a seamless cloud experience. Follow these steps:

Push to GitHub: Ensure all changes are committed and pushed.

Render Deployment:
-Sign up at render.com.
-Create a Web Service:

Repository: Graph-Enhanced-Agentic-RAG-for-Corporate-Intelligence.
Instance Type: Free.
Runtime: Docker.
Build Command: docker build -t my-app .
Start Command: docker run -p 8501:8501 my-app
Port: 8501

Environment Variables:
MONGODB_URI: Your Atlas connection string.
GEMINI_API_KEY: Your Gemini key.
HUGGINGFACE_TOKEN: Your Hugging Face token.
Deploy and note the provided URL (e.g., https://yourapp.onrender.com).
Test: Enter queries and verify responses.