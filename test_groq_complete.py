#!/usr/bin/env python3
"""
Complete Groq Integration Test
Tests both LLM and embeddings functionality
"""

import os
import sys
from dotenv import load_dotenv

def test_groq_llm():
    """Test Groq LLM functionality"""
    try:
        from langchain_groq import ChatGroq
        from groq_config import DEFAULT_MODEL
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("❌ GROQ_API_KEY not found")
            return False
        
        llm = ChatGroq(
            model_name=DEFAULT_MODEL,
            temperature=0.1,
            api_key=api_key
        )
        
        response = llm.invoke("What is the capital of France?")
        print("✅ Groq LLM test successful!")
        print(f"Response: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Groq LLM test failed: {e}")
        return False

def test_embeddings():
    """Test HuggingFace embeddings functionality"""
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from groq_config import DEFAULT_EMBEDDING_MODEL
        
        embeddings = HuggingFaceEmbeddings(
            model_name=DEFAULT_EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        # Test embedding generation
        texts = ["Hello world", "This is a test", "Banking finance"]
        embeddings_result = embeddings.embed_documents(texts)
        
        print("✅ HuggingFace embeddings test successful!")
        print(f"Generated {len(embeddings_result)} embeddings")
        print(f"Embedding dimensions: {len(embeddings_result[0])}")
        return True
        
    except Exception as e:
        print(f"❌ HuggingFace embeddings test failed: {e}")
        return False

def test_vector_store():
    """Test vector store with HuggingFace embeddings"""
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma
        from groq_config import DEFAULT_EMBEDDING_MODEL
        
        embeddings = HuggingFaceEmbeddings(
            model_name=DEFAULT_EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        # Create a simple vector store
        texts = [
            "Distribution finance helps supply chain partners",
            "Channel finance supports dealers and franchisees",
            "Global trade finance facilitates international commerce"
        ]
        
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            collection_name="test_collection"
        )
        
        # Test similarity search
        results = vectorstore.similarity_search("supply chain", k=2)
        
        print("✅ Vector store test successful!")
        print(f"Found {len(results)} similar documents")
        return True
        
    except Exception as e:
        print(f"❌ Vector store test failed: {e}")
        return False

def test_virtual_sme_complete():
    """Test complete Virtual SME system"""
    try:
        from virtual_sme_solution import VirtualSMESystem
        
        sme = VirtualSMESystem()
        print("✅ Virtual SME system initialized successfully!")
        
        # Test query
        response = sme.query_knowledge_base(
            query="What is distribution finance?",
            user_id="test_user"
        )
        
        print("✅ Virtual SME query test successful!")
        print(f"Answer: {response.answer[:200]}...")
        print(f"Confidence: {response.confidence}")
        print(f"Sources: {len(response.sources)} documents found")
        
        return True
        
    except Exception as e:
        print(f"❌ Virtual SME test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Complete Groq Integration Test")
    print("=" * 50)
    
    load_dotenv()
    
    tests = [
        ("Groq LLM", test_groq_llm),
        ("HuggingFace Embeddings", test_embeddings),
        ("Vector Store", test_vector_store),
        ("Virtual SME System", test_virtual_sme_complete)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Complete Groq integration is working.")
        print("\n🚀 You can now:")
        print("1. Start the server: python virtual_sme_solution.py")
        print("2. Add sample data: python add_sample_data.py")
        print("3. Use the web interface: virtual_sme_ui.html")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
