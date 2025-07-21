# 🚀 Graph-Enhanced Agentic RAG for Corporate Intelligence

An enterprise-grade application that combines **graph reasoning**, **semantic search**, and **agentic RAG (Retrieval-Augmented Generation)** to extract deep insights from corporate documents such as PDFs. It integrates **Neo4j**, **ChromaDB**, and **MongoDB Atlas** to support rich, multi-modal knowledge retrieval. Designed for use cases like **market analysis**, **competitor tracking**, and **internal knowledge management**, this tool provides context-aware, accurate answers in natural language.

---

## 🌟 Key Features

* **🔍 Intelligent Query Analysis:**
  Dynamically classifies incoming user queries as vector-based, graph-based, or hybrid, ensuring optimal routing for precise answers.

* **🧠 Vector Search with ChromaDB:**
  Uses sentence-transformer embeddings to find semantically relevant chunks from indexed PDF documents.

* **🔸 Graph Query Engine (Neo4j):**
  Executes relationship-aware graph queries to uncover inter-entity connections such as companies, products, locations, and competitors.

* **🔣 NLP-Powered Response Synthesis:**
  Combines graph and vector results using Transformer-based language models (Gemini, HuggingFace) for coherent, context-rich answers.

* **🕘 Persistent Conversation History (MongoDB Atlas):**
  Stores and indexes user interactions, allowing users to revisit and search through previous queries and responses.

* **📄 PDF Parsing Pipeline:**
  Automatically ingests and processes uploaded PDF files to extract and structure content into the vector store and graph database.

* **💬 Interactive Streamlit UI:**
  User-friendly interface featuring a responsive layout, progress bars, and a searchable chat history sidebar.

* **🛆 Dockerized for Deployment:**
  Easily deployable via Render’s free tier or any Docker-compatible platform. Ready for scale in production environments.

---

## 📋 Prerequisites

* **Python 3.9+**
* **Git** (for version control)
* **MongoDB Atlas** (Free-tier cluster for storing chat and document metadata)
* **Neo4j** (Self-hosted or cloud version for graph storage)
* **ChromaDB** (Local or persistent vector DB)
* **GitHub Account** (to host and deploy repository)
* **Render Account** (for cloud deployment)

### 🔐 Required API Keys

* `GEMINI_API_KEY` – For Google Gemini NLP features (optional).
* `HUGGINGFACE_TOKEN` – For Hugging Face models (optional).
* `MONGODB_URI` – MongoDB Atlas connection string.

---

## ⚙️ Installation & Local Development

### 📁 Clone the Repository

```bash
git clone https://github.com/yourusername/graph-enhanced-rag.git
cd graph-enhanced-rag
```

### 📆 Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔐 Create a `.env` File

```bash
MONGODB_URI=your_mongodb_atlas_connection_string
GEMINI_API_KEY=your_gemini_api_key
HUGGINGFACE_TOKEN=your_huggingface_token
```

### ▶️ Run the App

```bash
streamlit run app.py
```

Visit **[http://localhost:8501](http://localhost:8501)** to interact with the interface.

---

## 🔪 Example Usage

**User Query:**

> “What products does Netflix offer?”

**System Response:**
The system fetches relevant PDF content from ChromaDB, identifies related nodes like *“Netflix Originals”* and *“Streaming Services”* from Neo4j, and synthesizes a natural language response:

> “Netflix offers streaming services for movies and TV shows, including original content like Netflix Originals, documentaries, and interactive series.”

---

## ☁️ Deployment on Render (Free Tier)

### 🚳️ Docker-Based Setup

#### Step 1: Push Code to GitHub

Ensure your latest changes are committed and pushed to a public/private repo.

#### Step 2: Create a Render Web Service

* **Sign in:** [https://render.com](https://render.com)
* **New Web Service** → Connect your GitHub repo
* **Runtime:** Docker
* **Instance Type:** Free
* **Build Command:**

  ```bash
  docker build -t corporate-intel-rag .
  ```
* **Start Command:**

  ```bash
  docker run -p 8501:8501 corporate-intel-rag
  ```
* **Port:** `8501`

#### Step 3: Set Environment Variables on Render

* `MONGODB_URI`
* `GEMINI_API_KEY`
* `HUGGINGFACE_TOKEN`

#### Step 4: Deploy & Access

After deployment, access the app at:

```
https://yourappname.onrender.com
```
