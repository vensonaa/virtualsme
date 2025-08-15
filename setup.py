#!/usr/bin/env python3
"""
Setup script for Virtual SME Banking Solution
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_env_file():
    """Create .env file with required environment variables"""
    env_content = """# Virtual SME Configuration
OPENAI_API_KEY=your_openai_api_key_here

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
    
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env file - please update with your API keys")
    else:
        print("ℹ️  .env file already exists")

def create_sample_data():
    """Create sample knowledge documents for testing"""
    sample_docs = [
        {
            "title": "Distribution Finance Overview",
            "content": """
            Distribution Finance is a specialized banking service that provides financing solutions for supply chain and distribution networks. 
            
            Key components include:
            - Supply chain financing: Working capital solutions for suppliers and distributors
            - Inventory financing: Credit facilities secured by inventory
            - Trade credit insurance: Protection against non-payment
            - Distribution network financing: Support for channel partners
            
            Benefits:
            - Improved cash flow for all parties in the supply chain
            - Reduced payment delays
            - Enhanced supplier relationships
            - Risk mitigation through insurance products
            """,
            "domain": "distribution_finance",
            "source": "Bank Internal Documentation"
        },
        {
            "title": "Channel Finance Best Practices",
            "content": """
            Channel Finance enables banks to provide financing to channel partners, dealers, and franchisees.
            
            Key features:
            - Dealer financing programs
            - Franchise financing solutions
            - Channel credit programs
            - Partner relationship management
            
            Risk management considerations:
            - Credit assessment of channel partners
            - Collateral management
            - Monitoring of channel performance
            - Default risk mitigation strategies
            """,
            "domain": "channel_finance",
            "source": "Channel Finance Manual"
        },
        {
            "title": "Global Trade Finance Fundamentals",
            "content": """
            Global Trade Finance facilitates international trade through various financial instruments.
            
            Primary instruments:
            - Letters of Credit (LC): Payment guarantees for international transactions
            - Documentary Collections: Trade finance with document control
            - Trade guarantees: Performance and payment guarantees
            - Export/Import financing: Working capital for international trade
            
            Regulatory considerations:
            - International trade regulations
            - Sanctions compliance
            - Anti-money laundering (AML) requirements
            - Know Your Customer (KYC) procedures
            """,
            "domain": "global_trade_finance",
            "source": "Global Trade Finance Handbook"
        },
        {
            "title": "Risk Management Framework",
            "content": """
            Comprehensive risk management is essential for banking operations.
            
            Risk categories:
            - Credit risk: Default risk on loans and advances
            - Market risk: Interest rate, currency, and commodity price risks
            - Operational risk: Internal processes, systems, and external events
            - Liquidity risk: Ability to meet financial obligations
            
            Risk mitigation strategies:
            - Diversification of portfolio
            - Collateral management
            - Stress testing
            - Regular risk assessments
            """,
            "domain": "risk_management",
            "source": "Risk Management Policy"
        },
        {
            "title": "Banking Compliance Requirements",
            "content": """
            Banking compliance ensures adherence to regulatory requirements and industry standards.
            
            Key compliance areas:
            - Anti-Money Laundering (AML): Detection and prevention of money laundering
            - Know Your Customer (KYC): Customer identification and verification
            - Basel III: Capital adequacy and liquidity requirements
            - GDPR: Data protection and privacy regulations
            
            Compliance monitoring:
            - Regular audits and assessments
            - Automated monitoring systems
            - Staff training programs
            - Regulatory reporting
            """,
            "domain": "compliance",
            "source": "Compliance Manual"
        },
        {
            "title": "Customer Service Excellence",
            "content": """
            Exceptional customer service is crucial for banking success.
            
            Service principles:
            - Customer-centric approach
            - Personalized solutions
            - Proactive communication
            - Continuous improvement
            
            Digital transformation:
            - Online banking platforms
            - Mobile applications
            - AI-powered chatbots
            - Omnichannel experience
            
            Service metrics:
            - Customer satisfaction scores
            - Response times
            - Resolution rates
            - Net Promoter Score (NPS)
            """,
            "domain": "customer_service",
            "source": "Customer Service Standards"
        }
    ]
    
    # Create a script to add sample data
    sample_data_script = """
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from virtual_sme_solution import VirtualSMESystem, KnowledgeDocument, BankingDomain
from datetime import datetime

def add_sample_data():
    sme = VirtualSMESystem()
    
    sample_docs = """ + str(sample_docs) + """
    
    for doc in sample_docs:
        knowledge_doc = KnowledgeDocument(
            id=f"sample_{doc['domain']}_{datetime.utcnow().timestamp()}",
            title=doc['title'],
            content=doc['content'],
            domain=BankingDomain(doc['domain']),
            source=doc['source'],
            upload_date=datetime.utcnow(),
            metadata={"type": "sample", "category": "training"}
        )
        
        success = sme.add_knowledge_document(knowledge_doc)
        if success:
            print(f"✅ Added: {doc['title']}")
        else:
            print(f"❌ Failed to add: {doc['title']}")

if __name__ == "__main__":
    add_sample_data()
"""
    
    with open("add_sample_data.py", "w") as f:
        f.write(sample_data_script)
    
    print("✅ Created sample data script: add_sample_data.py")

def main():
    """Main setup function"""
    print("🚀 Setting up Virtual SME Banking Solution")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Create virtual environment
    if not run_command("python -m venv venv", "Creating virtual environment"):
        sys.exit(1)
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        sys.exit(1)
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Create sample data script
    create_sample_data()
    
    # Create directories
    os.makedirs("chroma_db", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("uploads", exist_ok=True)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your OpenAI API key")
    print("2. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Add sample data: python add_sample_data.py")
    print("4. Start the server: python virtual_sme_solution.py")
    print("5. Open virtual_sme_ui.html in your browser")
    print("\n🔗 API Documentation will be available at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
