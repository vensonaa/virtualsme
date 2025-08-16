#!/usr/bin/env python3
"""
Test script to verify Groq integration
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

def test_groq_connection():
    """Test basic Groq connection and response"""
    load_dotenv()
    
    # Check if API key is set
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        return False
    
    try:
        # Initialize Groq client
        llm = ChatGroq(
            model_name="llama3-8b-8192",
            temperature=0.1,
            api_key=api_key
        )
        
        # Test simple query
        response = llm.invoke("Hello! Can you confirm you're working with Groq?")
        
        print("✅ Groq connection successful!")
        print(f"Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Groq: {e}")
        return False

def test_virtual_sme_integration():
    """Test Virtual SME system with Groq"""
    try:
        from virtual_sme_solution import VirtualSMESystem
        
        # Initialize the system
        sme = VirtualSMESystem()
        
        print("✅ Virtual SME system initialized with Groq successfully!")
        
        # Test a simple query
        response = sme.query_knowledge_base(
            query="What is distribution finance?",
            user_id="test_user"
        )
        
        print(f"✅ Query processed successfully!")
        print(f"Answer: {response.answer[:200]}...")
        print(f"Confidence: {response.confidence}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Virtual SME with Groq: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Groq Integration...")
    print("=" * 50)
    
    # Test basic connection
    print("\n1. Testing basic Groq connection...")
    connection_ok = test_groq_connection()
    
    if connection_ok:
        print("\n2. Testing Virtual SME integration...")
        sme_ok = test_virtual_sme_integration()
        
        if sme_ok:
            print("\n🎉 All tests passed! Groq integration is working correctly.")
        else:
            print("\n⚠️  Virtual SME integration failed. Check the logs above.")
    else:
        print("\n❌ Basic Groq connection failed. Please check your API key and internet connection.")
