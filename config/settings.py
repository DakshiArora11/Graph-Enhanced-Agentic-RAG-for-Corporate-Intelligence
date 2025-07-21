"""
Configuration settings for Graph-Enhanced RAG System
This file manages all environment variables and system settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Central configuration class for all system settings"""
    
    # ===== API Configuration =====
    # OpenAI API key for LLM operations
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Alternative LLM providers (for flexibility)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    
    # ===== Database Configuration =====
    # Neo4j Graph Database settings
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    
    # ChromaDB Vector Database settings
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    VECTOR_COLLECTION_NAME = os.getenv("VECTOR_COLLECTION_NAME", "corporate_documents")
    
    # ===== File Path Configuration =====
    # Base project directory
    BASE_DIR = Path(__file__).parent.parent
    
    # Data directories
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    
    # Logging directory
    LOG_DIR = BASE_DIR / "logs"
    
    # ===== Processing Configuration =====
    # Text chunking parameters
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Entity extraction parameters
    MAX_ENTITIES_PER_CHUNK = int(os.getenv("MAX_ENTITIES_PER_CHUNK", "20"))
    MIN_ENTITY_CONFIDENCE = float(os.getenv("MIN_ENTITY_CONFIDENCE", "0.7"))
    
    # Query processing parameters
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    
    # ===== Model Configuration =====
    # Embedding model for vector search
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # LLM model for entity extraction and query processing
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    # Temperature for LLM operations (lower = more deterministic)
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    
    # ===== Validation Methods =====
    @classmethod
    def validate_required_settings(cls):
        """Validate that all required settings are present"""
        required_settings = [
            ("OPENAI_API_KEY", cls.OPENAI_API_KEY),
        ]
        
        missing_settings = []
        for setting_name, setting_value in required_settings:
            if not setting_value or setting_value == "your_api_key_here":
                missing_settings.append(setting_name)
        
        if missing_settings:
            raise ValueError(
                f"Missing required settings: {', '.join(missing_settings)}. "
                f"Please check your .env file."
            )
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.DATA_DIR,
            cls.RAW_DATA_DIR,
            cls.PROCESSED_DATA_DIR,
            cls.LOG_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

# Create a global settings instance
settings = Settings()