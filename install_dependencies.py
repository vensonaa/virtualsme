#!/usr/bin/env python3
"""
Install dependencies for Virtual SME with Groq LLM and HuggingFace embeddings
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Install all required dependencies"""
    print("🔧 Installing Virtual SME Dependencies")
    print("=" * 50)
    
    # Core dependencies
    packages = [
        "numpy>=1.21.0",
        "groq>=0.4.0",
        "langchain>=0.1.0", 
        "langchain-groq>=0.1.0",
        "langchain-community>=0.1.0",
        "sentence-transformers>=2.2.0",
        "torch>=1.9.0",
        "chromadb>=0.4.0",
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "sqlalchemy>=2.0.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0"
    ]
    
    print("📦 Installing packages...")
    failed_packages = []
    
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed successfully")
        else:
            print(f"❌ Failed to install {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️  Failed to install {len(failed_packages)} packages:")
        for package in failed_packages:
            print(f"  - {package}")
        print("\nPlease try installing them manually:")
        for package in failed_packages:
            print(f"  pip install {package}")
    else:
        print("\n🎉 All dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Setup your Groq API key: python setup_groq.py")
        print("2. Test the integration: python test_groq_complete.py")
        print("3. Add sample data: python add_sample_data.py")
        print("4. Start the server: python virtual_sme_solution.py")

if __name__ == "__main__":
    main()
