"""
Setup validation script for Graph-Enhanced RAG System
Run this script to verify your environment is correctly configured
"""

import sys
import os
from pathlib import Path
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\nChecking dependencies...")
    
    required_packages = [
        "openai",
        "langchain", 
        "chromadb",
        "neo4j",
        "streamlit",
        "pymupdf",
        "spacy",
        "sentence_transformers",
        "python-dotenv",
        "pandas",
        "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not found")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def check_environment_variables():
    """Check if environment variables are set"""
    print("\nChecking environment variables...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ["OPENAI_API_KEY"]
    optional_vars = ["NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD"]
    
    missing_required = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == "your_api_key_here":
            print(f"❌ {var} not set")
            missing_required.append(var)
        else:
            print(f"✅ {var} configured")
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} configured")
        else:
            print(f"⚠️  {var} using default value")
    
    if missing_required:
        print(f"\nPlease set required environment variables in .env file")
        return False
    
    return True

def check_project_structure():
    """Check if project structure is correct"""
    print("\nChecking project structure...")
    
    required_dirs = [
        "src",
        "src/ingestion",
        "src/storage", 
        "src/agents",
        "src/utils",
        "config",
        "data",
        "data/raw",
        "data/processed",
        "tests",
        "logs"
    ]
    
    missing_dirs = []
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ not found")
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"\nMissing directories: {', '.join(missing_dirs)}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of key components"""
    print("\nTesting basic functionality...")
    
    try:
        # Test ChromaDB
        import chromadb
        client = chromadb.Client()
        print("✅ ChromaDB client created successfully")
        
        # Test sentence transformers
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        test_embedding = model.encode(["Test sentence"])
        print("✅ Sentence transformer working")
        
        # Test OpenAI connection (if API key is set)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "your_api_key_here":
            import openai
            client = openai.OpenAI(api_key=openai_key)
            print("✅ OpenAI client configured")
        else:
            print("⚠️  OpenAI API key not configured - skipping test")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Main validation function"""
    print("🔍 Validating Graph-Enhanced RAG System Setup")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_environment_variables(),
        check_project_structure(),
        test_basic_functionality()
    ]
    
    print("\n" + "=" * 50)
    
    if all(checks):
        print("🎉 All checks passed! Your environment is ready.")
        print("\nNext steps:")
        print("1. Add your OpenAI API key to .env file")
        print("2. Start Neo4j database (see instructions)")
        print("3. Begin implementing the system components")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()