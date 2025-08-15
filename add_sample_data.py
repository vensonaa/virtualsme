
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from virtual_sme_solution import VirtualSMESystem, KnowledgeDocument, BankingDomain
from datetime import datetime

def add_sample_data():
    sme = VirtualSMESystem()
    
    sample_docs = [{'title': 'Distribution Finance Overview', 'content': '\n            Distribution Finance is a specialized banking service that provides financing solutions for supply chain and distribution networks. \n            \n            Key components include:\n            - Supply chain financing: Working capital solutions for suppliers and distributors\n            - Inventory financing: Credit facilities secured by inventory\n            - Trade credit insurance: Protection against non-payment\n            - Distribution network financing: Support for channel partners\n            \n            Benefits:\n            - Improved cash flow for all parties in the supply chain\n            - Reduced payment delays\n            - Enhanced supplier relationships\n            - Risk mitigation through insurance products\n            ', 'domain': 'distribution_finance', 'source': 'Bank Internal Documentation'}, {'title': 'Channel Finance Best Practices', 'content': '\n            Channel Finance enables banks to provide financing to channel partners, dealers, and franchisees.\n            \n            Key features:\n            - Dealer financing programs\n            - Franchise financing solutions\n            - Channel credit programs\n            - Partner relationship management\n            \n            Risk management considerations:\n            - Credit assessment of channel partners\n            - Collateral management\n            - Monitoring of channel performance\n            - Default risk mitigation strategies\n            ', 'domain': 'channel_finance', 'source': 'Channel Finance Manual'}, {'title': 'Global Trade Finance Fundamentals', 'content': '\n            Global Trade Finance facilitates international trade through various financial instruments.\n            \n            Primary instruments:\n            - Letters of Credit (LC): Payment guarantees for international transactions\n            - Documentary Collections: Trade finance with document control\n            - Trade guarantees: Performance and payment guarantees\n            - Export/Import financing: Working capital for international trade\n            \n            Regulatory considerations:\n            - International trade regulations\n            - Sanctions compliance\n            - Anti-money laundering (AML) requirements\n            - Know Your Customer (KYC) procedures\n            ', 'domain': 'global_trade_finance', 'source': 'Global Trade Finance Handbook'}, {'title': 'Risk Management Framework', 'content': '\n            Comprehensive risk management is essential for banking operations.\n            \n            Risk categories:\n            - Credit risk: Default risk on loans and advances\n            - Market risk: Interest rate, currency, and commodity price risks\n            - Operational risk: Internal processes, systems, and external events\n            - Liquidity risk: Ability to meet financial obligations\n            \n            Risk mitigation strategies:\n            - Diversification of portfolio\n            - Collateral management\n            - Stress testing\n            - Regular risk assessments\n            ', 'domain': 'risk_management', 'source': 'Risk Management Policy'}, {'title': 'Banking Compliance Requirements', 'content': '\n            Banking compliance ensures adherence to regulatory requirements and industry standards.\n            \n            Key compliance areas:\n            - Anti-Money Laundering (AML): Detection and prevention of money laundering\n            - Know Your Customer (KYC): Customer identification and verification\n            - Basel III: Capital adequacy and liquidity requirements\n            - GDPR: Data protection and privacy regulations\n            \n            Compliance monitoring:\n            - Regular audits and assessments\n            - Automated monitoring systems\n            - Staff training programs\n            - Regulatory reporting\n            ', 'domain': 'compliance', 'source': 'Compliance Manual'}, {'title': 'Customer Service Excellence', 'content': '\n            Exceptional customer service is crucial for banking success.\n            \n            Service principles:\n            - Customer-centric approach\n            - Personalized solutions\n            - Proactive communication\n            - Continuous improvement\n            \n            Digital transformation:\n            - Online banking platforms\n            - Mobile applications\n            - AI-powered chatbots\n            - Omnichannel experience\n            \n            Service metrics:\n            - Customer satisfaction scores\n            - Response times\n            - Resolution rates\n            - Net Promoter Score (NPS)\n            ', 'domain': 'customer_service', 'source': 'Customer Service Standards'}]
    
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
