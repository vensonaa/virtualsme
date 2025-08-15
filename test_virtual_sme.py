#!/usr/bin/env python3
"""
Test script for Virtual SME Banking Solution
Demonstrates the core functionality of the system
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from virtual_sme_solution import VirtualSMESystem, KnowledgeDocument, BankingDomain

def test_virtual_sme():
    """Test the Virtual SME system with sample queries"""
    
    print("🧪 Testing Virtual SME Banking Solution")
    print("=" * 50)
    
    # Initialize the system
    print("🔄 Initializing Virtual SME system...")
    try:
        sme = VirtualSMESystem()
        print("✅ System initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        return
    
    # Test queries
    test_queries = [
        {
            "query": "What are the key components of distribution finance?",
            "description": "Distribution Finance Overview",
            "expected_domains": [BankingDomain.DISTRIBUTION_FINANCE]
        },
        {
            "query": "How does channel finance work for automotive dealers?",
            "description": "Channel Finance for Automotive",
            "expected_domains": [BankingDomain.CHANNEL_FINANCE]
        },
        {
            "query": "What are the risk factors in global trade finance?",
            "description": "Global Trade Finance Risks",
            "expected_domains": [BankingDomain.GLOBAL_TRADE_FINANCE, BankingDomain.RISK_MANAGEMENT]
        },
        {
            "query": "What compliance requirements apply to supply chain financing?",
            "description": "Compliance in Supply Chain Finance",
            "expected_domains": [BankingDomain.DISTRIBUTION_FINANCE, BankingDomain.COMPLIANCE]
        },
        {
            "query": "How do we assess credit risk for channel partners?",
            "description": "Credit Risk Assessment",
            "expected_domains": [BankingDomain.CHANNEL_FINANCE, BankingDomain.RISK_MANAGEMENT]
        }
    ]
    
    print(f"\n📝 Testing {len(test_queries)} queries...")
    print("-" * 50)
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {test_case['description']}")
        print(f"Query: {test_case['query']}")
        
        try:
            # Query the system
            response = sme.query_knowledge_base(
                query=test_case['query'],
                user_id=f"test_user_{i}",
                preferred_domains=test_case['expected_domains']
            )
            
            # Display results
            print(f"✅ Response received (Confidence: {response.confidence:.2f})")
            print(f"📚 Domains consulted: {[d.value for d in response.domains_consulted]}")
            print(f"📖 Sources: {len(response.sources)} documents")
            
            # Show a preview of the response
            preview = response.answer[:200] + "..." if len(response.answer) > 200 else response.answer
            print(f"💬 Response preview: {preview}")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
    
    # Test knowledge base statistics
    print(f"\n📊 Knowledge Base Statistics")
    print("-" * 30)
    
    try:
        stats = sme.get_knowledge_stats()
        print(f"Total documents: {stats.get('total_documents', 0)}")
        print(f"Vector stores initialized: {stats.get('vector_stores_initialized', 0)}")
        
        if 'domains' in stats:
            print("Documents per domain:")
            for domain, count in stats['domains'].items():
                print(f"  - {domain}: {count}")
                
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
    
    # Test adding a new document
    print(f"\n📄 Testing Document Addition")
    print("-" * 30)
    
    try:
        new_doc = KnowledgeDocument(
            id=f"test_doc_{datetime.utcnow().timestamp()}",
            title="Test Banking Policy",
            content="""
            This is a test banking policy document that covers various aspects of banking operations.
            
            Key points:
            - Risk management procedures
            - Customer service standards
            - Compliance requirements
            - Operational guidelines
            
            This document serves as a test case for the Virtual SME system.
            """,
            domain=BankingDomain.COMPLIANCE,
            source="Test Document",
            upload_date=datetime.utcnow(),
            metadata={"type": "test", "category": "demo"}
        )
        
        success = sme.add_knowledge_document(new_doc)
        if success:
            print("✅ Test document added successfully")
        else:
            print("❌ Failed to add test document")
            
    except Exception as e:
        print(f"❌ Error adding test document: {e}")
    
    print(f"\n🎉 Testing completed!")
    print("=" * 50)

def test_api_endpoints():
    """Test the FastAPI endpoints"""
    
    print("\n🌐 Testing API Endpoints")
    print("=" * 30)
    
    import requests
    import json
    
    base_url = "http://localhost:8000"
    
    # Test endpoints
    endpoints = [
        {
            "method": "GET",
            "url": "/domains",
            "description": "Get available domains"
        },
        {
            "method": "GET", 
            "url": "/stats",
            "description": "Get knowledge base statistics"
        },
        {
            "method": "POST",
            "url": "/query",
            "description": "Query the Virtual SME",
            "data": {
                "query": "What is distribution finance?",
                "user_id": "test_user",
                "preferred_domains": ["distribution_finance"]
            }
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 Testing: {endpoint['description']}")
        
        try:
            headers = {
                "Authorization": "Bearer dummy-token",
                "Content-Type": "application/json"
            }
            
            if endpoint["method"] == "GET":
                response = requests.get(f"{base_url}{endpoint['url']}", headers=headers)
            else:
                response = requests.post(
                    f"{base_url}{endpoint['url']}", 
                    headers=headers,
                    json=endpoint.get("data", {})
                )
            
            if response.status_code == 200:
                print(f"✅ Success (Status: {response.status_code})")
                if endpoint["method"] == "POST":
                    result = response.json()
                    print(f"   Response length: {len(result.get('answer', ''))} characters")
            else:
                print(f"❌ Failed (Status: {response.status_code})")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Server not running. Start the server with: python virtual_sme_solution.py")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main test function"""
    
    print("🏦 Virtual SME Banking Solution - Test Suite")
    print("=" * 60)
    
    # Test core functionality
    test_virtual_sme()
    
    # Test API endpoints (if server is running)
    test_api_endpoints()
    
    print(f"\n📋 Test Summary")
    print("=" * 20)
    print("✅ Core functionality tested")
    print("✅ Knowledge base operations tested")
    print("✅ API endpoints tested (if server running)")
    print("\n🚀 To start the server: python virtual_sme_solution.py")
    print("🌐 Web interface: Open virtual_sme_ui.html in your browser")
    print("📚 API docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
