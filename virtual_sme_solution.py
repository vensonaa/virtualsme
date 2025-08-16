"""
Virtual SME (Subject Matter Expert) Solution for Banking
A comprehensive GenAI solution to provide domain expertise across multiple banking businesses
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
from dataclasses import dataclass
from enum import Enum

# AI/ML Libraries
import groq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain.schema import Document

# FastAPI for web interface
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Database
import sqlite3
from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration
from dotenv import load_dotenv
from groq_config import DEFAULT_MODEL, DEFAULT_EMBEDDING_MODEL, DEFAULT_TEMPERATURE

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enums and Data Classes
class BankingDomain(Enum):
    DISTRIBUTION_FINANCE = "distribution_finance"
    CHANNEL_FINANCE = "channel_finance"
    GLOBAL_TRADE_FINANCE = "global_trade_finance"
    RISK_MANAGEMENT = "risk_management"
    COMPLIANCE = "compliance"
    CUSTOMER_SERVICE = "customer_service"

@dataclass
class KnowledgeDocument:
    id: str
    title: str
    content: str
    domain: BankingDomain
    source: str
    upload_date: datetime
    metadata: Dict[str, Any]

@dataclass
class QueryResponse:
    answer: str
    sources: List[str]
    confidence: float
    domains_consulted: List[BankingDomain]
    timestamp: datetime

# Database Models
Base = declarative_base()

class DocumentModel(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    domain = Column(String, nullable=False)
    source = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    document_metadata = Column(Text)  # JSON string

class QueryLog(Base):
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    domains_consulted = Column(Text)  # JSON string
    confidence = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Pydantic Models for API
class QueryRequest(BaseModel):
    query: str
    user_id: str
    preferred_domains: Optional[List[str]] = None
    context: Optional[str] = None

class QueryResponseModel(BaseModel):
    answer: str
    sources: List[str]
    confidence: float
    domains_consulted: List[str]
    timestamp: datetime

class DocumentUploadRequest(BaseModel):
    title: str
    content: str
    domain: str
    source: str
    metadata: Optional[Dict[str, Any]] = None

class VirtualSMESystem:
    def __init__(self):
        # Using HuggingFace embeddings (free, local) with Groq LLM
        # This provides a complete solution without requiring OpenAI API
        self.embeddings = HuggingFaceEmbeddings(
            model_name=DEFAULT_EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        # Using Groq's Llama3-8b model for fast, cost-effective inference
        # Alternative models: "mixtral-8x7b-32768", "llama3-70b-8192", "gemma2-9b-it"
        self.llm = ChatGroq(
            model_name=DEFAULT_MODEL,
            temperature=DEFAULT_TEMPERATURE,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Initialize vector stores for each domain
        self.vector_stores = {}
        self.document_processors = {}
        self.domain_experts = {}
        
        # Initialize database
        self.engine = create_engine("sqlite:///virtual_sme.db")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db_session = SessionLocal()
        
        self._initialize_domain_experts()
        self._load_existing_knowledge()
    
    def _initialize_domain_experts(self):
        """Initialize specialized prompts for each banking domain"""
        
        domain_prompts = {
            BankingDomain.DISTRIBUTION_FINANCE: """
            You are a Distribution Finance expert in banking. You specialize in:
            - Supply chain financing
            - Inventory financing
            - Working capital solutions
            - Trade credit insurance
            - Distribution network financing
            
            Provide comprehensive, accurate responses based on the retrieved knowledge.
            Always cite sources and explain complex concepts clearly.
            """,
            
            BankingDomain.CHANNEL_FINANCE: """
            You are a Channel Finance expert in banking. You specialize in:
            - Channel partner financing
            - Dealer financing
            - Franchise financing
            - Channel credit programs
            - Partner relationship management
            
            Provide comprehensive, accurate responses based on the retrieved knowledge.
            Always cite sources and explain complex concepts clearly.
            """,
            
            BankingDomain.GLOBAL_TRADE_FINANCE: """
            You are a Global Trade Finance expert in banking. You specialize in:
            - Letters of credit
            - Trade guarantees
            - Export/import financing
            - Documentary collections
            - Trade risk management
            - International payment solutions
            
            Provide comprehensive, accurate responses based on the retrieved knowledge.
            Always cite sources and explain complex concepts clearly.
            """,
            
            BankingDomain.RISK_MANAGEMENT: """
            You are a Risk Management expert in banking. You specialize in:
            - Credit risk assessment
            - Market risk analysis
            - Operational risk management
            - Regulatory compliance
            - Risk modeling and analytics
            
            Provide comprehensive, accurate responses based on the retrieved knowledge.
            Always cite sources and explain complex concepts clearly.
            """,
            
            BankingDomain.COMPLIANCE: """
            You are a Compliance expert in banking. You specialize in:
            - Regulatory requirements
            - Anti-money laundering (AML)
            - Know Your Customer (KYC)
            - Banking regulations
            - Compliance monitoring and reporting
            
            Provide comprehensive, accurate responses based on the retrieved knowledge.
            Always cite sources and explain complex concepts clearly.
            """,
            
            BankingDomain.CUSTOMER_SERVICE: """
            You are a Customer Service expert in banking. You specialize in:
            - Customer relationship management
            - Service delivery optimization
            - Customer experience enhancement
            - Digital banking solutions
            - Customer support processes
            
            Provide comprehensive, accurate responses based on the retrieved knowledge.
            Always cite sources and explain complex concepts clearly.
            """
        }
        
        for domain, prompt in domain_prompts.items():
            self.domain_experts[domain] = PromptTemplate(
                input_variables=["context", "question"],
                template=f"{prompt}\n\nContext: {{context}}\n\nQuestion: {{question}}\n\nAnswer:"
            )
    
    def _load_existing_knowledge(self):
        """Load existing knowledge documents from database into vector stores"""
        try:
            documents = self.db_session.query(DocumentModel).all()
            
            for doc in documents:
                domain = BankingDomain(doc.domain)
                if domain not in self.vector_stores:
                    self.vector_stores[domain] = Chroma(
                        embedding_function=self.embeddings,
                        collection_name=f"knowledge_{domain.value}"
                    )
                
                # Add document to vector store
                self.vector_stores[domain].add_documents([
                    Document(
                        page_content=doc.content,
                        metadata={
                            "title": doc.title,
                            "source": doc.source,
                            "domain": doc.domain,
                            "upload_date": doc.upload_date.isoformat()
                        }
                    )
                ])
            
            logger.info(f"Loaded {len(documents)} existing documents into vector stores")
            
        except Exception as e:
            logger.error(f"Error loading existing knowledge: {e}")
    
    def add_knowledge_document(self, document: KnowledgeDocument) -> bool:
        """Add a new knowledge document to the system"""
        try:
            # Save to database
            doc_model = DocumentModel(
                id=document.id,
                title=document.title,
                content=document.content,
                domain=document.domain.value,
                source=document.source,
                upload_date=document.upload_date,
                metadata=json.dumps(document.metadata)
            )
            
            self.db_session.add(doc_model)
            self.db_session.commit()
            
            # Add to vector store
            if document.domain not in self.vector_stores:
                self.vector_stores[document.domain] = Chroma(
                    embedding_function=self.embeddings,
                    collection_name=f"knowledge_{document.domain.value}"
                )
            
            self.vector_stores[document.domain].add_documents([
                Document(
                    page_content=document.content,
                    metadata={
                        "title": document.title,
                        "source": document.source,
                        "domain": document.domain.value,
                        "upload_date": document.upload_date.isoformat()
                    }
                )
            ])
            
            logger.info(f"Successfully added document: {document.title}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            self.db_session.rollback()
            return False
    
    def query_knowledge_base(self, query: str, user_id: str, 
                           preferred_domains: Optional[List[BankingDomain]] = None,
                           context: Optional[str] = None) -> QueryResponse:
        """Query the knowledge base across all domains"""
        
        # Determine which domains to search
        domains_to_search = preferred_domains or list(BankingDomain)
        
        # Collect relevant documents from all domains
        all_relevant_docs = []
        domains_consulted = []
        
        for domain in domains_to_search:
            if domain in self.vector_stores:
                try:
                    # Search for relevant documents
                    docs = self.vector_stores[domain].similarity_search(
                        query, k=5
                    )
                    
                    if docs:
                        all_relevant_docs.extend(docs)
                        domains_consulted.append(domain)
                        
                except Exception as e:
                    logger.error(f"Error searching domain {domain}: {e}")
        
        if not all_relevant_docs:
            return QueryResponse(
                answer="I don't have sufficient information to answer your question. Please try rephrasing or contact a human expert.",
                sources=[],
                confidence=0.0,
                domains_consulted=[],
                timestamp=datetime.utcnow()
            )
        
        # Create context from relevant documents
        context_text = "\n\n".join([
            f"Source: {doc.metadata.get('title', 'Unknown')}\n{doc.page_content}"
            for doc in all_relevant_docs
        ])
        
        # Generate response using domain experts
        responses = []
        for domain in domains_consulted:
            if domain in self.domain_experts:
                try:
                    chain = LLMChain(
                        llm=self.llm,
                        prompt=self.domain_experts[domain]
                    )
                    
                    response = chain.run({
                        "context": context_text,
                        "question": query
                    })
                    
                    responses.append({
                        "domain": domain,
                        "response": response
                    })
                    
                except Exception as e:
                    logger.error(f"Error generating response for domain {domain}: {e}")
        
        # Combine responses from multiple domains
        if responses:
            combined_response = self._combine_domain_responses(responses, query)
        else:
            combined_response = "I apologize, but I'm unable to generate a response at this time."
        
        # Calculate confidence based on number of sources and domain coverage
        confidence = min(0.9, len(all_relevant_docs) * 0.1 + len(domains_consulted) * 0.1)
        
        # Log the query
        self._log_query(user_id, query, combined_response, domains_consulted, confidence)
        
        return QueryResponse(
            answer=combined_response,
            sources=[doc.metadata.get('title', 'Unknown') for doc in all_relevant_docs],
            confidence=confidence,
            domains_consulted=domains_consulted,
            timestamp=datetime.utcnow()
        )
    
    def _combine_domain_responses(self, responses: List[Dict], original_query: str) -> str:
        """Combine responses from multiple domains into a comprehensive answer"""
        
        if len(responses) == 1:
            return responses[0]["response"]
        
        # Create a synthesis prompt
        synthesis_prompt = PromptTemplate(
            input_variables=["responses", "question"],
            template="""
            You are a banking expert synthesizing information from multiple domain specialists.
            
            Original Question: {question}
            
            Domain-specific responses:
            {responses}
            
            Please provide a comprehensive, well-structured answer that:
            1. Addresses the original question completely
            2. Integrates insights from all relevant domains
            3. Avoids redundancy while maintaining completeness
            4. Provides clear, actionable information
            5. Cites the relevant domains when appropriate
            
            Comprehensive Answer:
            """
        )
        
        # Format responses for synthesis
        formatted_responses = "\n\n".join([
            f"Domain: {resp['domain'].value.replace('_', ' ').title()}\nResponse: {resp['response']}"
            for resp in responses
        ])
        
        try:
            chain = LLMChain(llm=self.llm, prompt=synthesis_prompt)
            combined_response = chain.run({
                "responses": formatted_responses,
                "question": original_query
            })
            
            return combined_response
            
        except Exception as e:
            logger.error(f"Error combining responses: {e}")
            # Fallback to concatenating responses
            return "\n\n".join([resp["response"] for resp in responses])
    
    def _log_query(self, user_id: str, query: str, response: str, 
                   domains_consulted: List[BankingDomain], confidence: float):
        """Log the query for audit and improvement purposes"""
        try:
            log_entry = QueryLog(
                user_id=user_id,
                query=query,
                response=response,
                domains_consulted=json.dumps([d.value for d in domains_consulted]),
                confidence=str(confidence)
            )
            
            self.db_session.add(log_entry)
            self.db_session.commit()
            
        except Exception as e:
            logger.error(f"Error logging query: {e}")
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            total_docs = self.db_session.query(DocumentModel).count()
            
            domain_stats = {}
            for domain in BankingDomain:
                count = self.db_session.query(DocumentModel).filter(
                    DocumentModel.domain == domain.value
                ).count()
                domain_stats[domain.value] = count
            
            return {
                "total_documents": total_docs,
                "domains": domain_stats,
                "vector_stores_initialized": len(self.vector_stores)
            }
            
        except Exception as e:
            logger.error(f"Error getting knowledge stats: {e}")
            return {}

# FastAPI Application
app = FastAPI(
    title="Virtual SME Banking Solution",
    description="A comprehensive GenAI solution for banking domain expertise",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Global instance
virtual_sme = VirtualSMESystem()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple authentication - in production, implement proper JWT validation"""
    # This is a placeholder - implement proper authentication
    return credentials.credentials

@app.post("/query", response_model=QueryResponseModel)
async def query_knowledge_base(
    request: QueryRequest,
    current_user: str = Depends(get_current_user)
):
    """Query the Virtual SME system"""
    try:
        # Convert string domains to enum
        preferred_domains = None
        if request.preferred_domains:
            preferred_domains = [BankingDomain(domain) for domain in request.preferred_domains]
        
        response = virtual_sme.query_knowledge_base(
            query=request.query,
            user_id=request.user_id,
            preferred_domains=preferred_domains,
            context=request.context
        )
        
        return QueryResponseModel(
            answer=response.answer,
            sources=response.sources,
            confidence=response.confidence,
            domains_consulted=[d.value for d in response.domains_consulted],
            timestamp=response.timestamp
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing your query"
        )

@app.post("/documents")
async def add_document(
    request: DocumentUploadRequest,
    current_user: str = Depends(get_current_user)
):
    """Add a new knowledge document"""
    try:
        document = KnowledgeDocument(
            id=f"doc_{datetime.utcnow().timestamp()}",
            title=request.title,
            content=request.content,
            domain=BankingDomain(request.domain),
            source=request.source,
            upload_date=datetime.utcnow(),
            metadata=request.metadata or {}
        )
        
        success = virtual_sme.add_knowledge_document(document)
        
        if success:
            return {"message": "Document added successfully", "document_id": document.id}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add document"
            )
            
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid domain: {e}"
        )
    except Exception as e:
        logger.error(f"Error adding document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error adding document"
        )

@app.get("/stats")
async def get_knowledge_stats(current_user: str = Depends(get_current_user)):
    """Get knowledge base statistics"""
    return virtual_sme.get_knowledge_stats()

@app.get("/domains")
async def get_available_domains():
    """Get list of available banking domains"""
    return {
        "domains": [domain.value for domain in BankingDomain],
        "descriptions": {
            BankingDomain.DISTRIBUTION_FINANCE.value: "Supply chain and distribution financing solutions",
            BankingDomain.CHANNEL_FINANCE.value: "Channel partner and dealer financing",
            BankingDomain.GLOBAL_TRADE_FINANCE.value: "International trade and export/import financing",
            BankingDomain.RISK_MANAGEMENT.value: "Credit, market, and operational risk management",
            BankingDomain.COMPLIANCE.value: "Regulatory compliance and AML/KYC",
            BankingDomain.CUSTOMER_SERVICE.value: "Customer relationship and service optimization"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7000)
