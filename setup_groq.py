#!/usr/bin/env python3
"""
Setup script for Groq integration
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def setup_groq_api_key():
    """Setup Groq API key in .env file"""
    env_file = Path(".env")
    
    # Load existing .env file if it exists
    if env_file.exists():
        load_dotenv()
        existing_key = os.getenv("GROQ_API_KEY")
        if existing_key and existing_key != "your_groq_api_key_here":
            print(f"✅ GROQ_API_KEY already configured: {existing_key[:10]}...")
            return True
    
    print("🔧 Setting up Groq API Key...")
    print("\nTo get your Groq API key:")
    print("1. Go to https://console.groq.com/")
    print("2. Sign up or log in to your account")
    print("3. Navigate to API Keys section")
    print("4. Create a new API key")
    print("5. Copy the API key")
    
    api_key = input("\nEnter your Groq API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return False
    
    # Update .env file
    if env_file.exists():
        # Read existing content
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace or add GROQ_API_KEY
        if "GROQ_API_KEY=" in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith("GROQ_API_KEY="):
                    lines[i] = f"GROQ_API_KEY={api_key}"
                    break
            content = '\n'.join(lines)
        else:
            content = f"GROQ_API_KEY={api_key}\n" + content
    else:
        content = f"""# Virtual SME Configuration
GROQ_API_KEY={api_key}

# Database Configuration
DATABASE_URL=sqlite:///virtual_sme.db

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO

# Vector Store Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
"""
    
    # Write updated content
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("✅ GROQ_API_KEY configured successfully!")
    return True

def test_groq_connection():
    """Test Groq connection"""
    try:
        from langchain_groq import ChatGroq
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            print("❌ GROQ_API_KEY not properly configured")
            return False
        
        llm = ChatGroq(
            model_name="llama3-8b-8192",
            temperature=0.1,
            api_key=api_key
        )
        
        response = llm.invoke("Hello! This is a test message.")
        print("✅ Groq connection successful!")
        print(f"Test response: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Groq connection: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Groq Setup for Virtual SME")
    print("=" * 40)
    
    # Setup API key
    if not setup_groq_api_key():
        sys.exit(1)
    
    # Test connection
    print("\n🧪 Testing Groq connection...")
    if test_groq_connection():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Add sample data: python add_sample_data.py")
        print("3. Start the server: python virtual_sme_solution.py")
        print("4. Test the integration: python test_groq_integration.py")
    else:
        print("\n❌ Setup failed. Please check your API key and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
