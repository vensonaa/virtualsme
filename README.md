# 🏦 Virtual SME - Banking Expert Assistant

A comprehensive GenAI solution that provides domain expertise across multiple banking businesses including Distribution Finance, Channel Finance, Global Trade Finance, Risk Management, Compliance, and Customer Service.

## 🎯 Overview

The Virtual SME (Subject Matter Expert) solution addresses the critical need for domain knowledge within banking organizations. Many banking departments lack comprehensive understanding of other business areas, leading to inefficiencies and missed opportunities. This AI-powered solution provides:

- **Multi-Domain Expertise**: Comprehensive knowledge across all banking domains
- **Intelligent Query Processing**: Context-aware responses using RAG (Retrieval-Augmented Generation)
- **Domain-Specific Prompts**: Specialized AI experts for each banking area
- **Comprehensive Responses**: Integration of insights from multiple domains
- **Audit Trail**: Complete logging of queries and responses
- **Modern Web Interface**: User-friendly chat interface

## 🏗️ Architecture

### Core Components

1. **Knowledge Base Management**
   - Document ingestion and processing
   - Multi-format support (PDF, Word, Excel, databases)
   - Automated knowledge extraction and structuring
   - Version control and audit trails

2. **AI Model Layer**
   - Large Language Model (LLM) integration
   - RAG (Retrieval-Augmented Generation) system
   - Multi-domain knowledge fusion
   - Context-aware responses

3. **Banking Domain Modules**
   - Distribution Finance
   - Channel Finance
   - Global Trade Finance
   - Risk Management
   - Compliance & Regulatory
   - Customer Service

4. **User Interface**
   - Web-based chat interface
   - API endpoints for integration
   - Role-based access control
   - Audit logging

### Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **AI/ML**: OpenAI GPT-4, LangChain, ChromaDB
- **Database**: SQLite (production: PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Vector Store**: ChromaDB for semantic search
- **Security**: JWT authentication, role-based access

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd virtual-sme-banking
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Update environment variables**
   ```bash
   # Edit .env file and add your OpenAI API key
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Activate virtual environment**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

5. **Add sample data**
   ```bash
   python add_sample_data.py
   ```

6. **Start the server**
   ```bash
   python virtual_sme_solution.py
   ```

7. **Open the web interface**
   - Open `virtual_sme_ui.html` in your browser
   - Or access the API documentation at `http://localhost:8000/docs`

## 📚 Usage

### Web Interface

1. **Open the chat interface** in your browser
2. **Select domains** you want to consult (all selected by default)
3. **Ask questions** about banking processes, regulations, or best practices
4. **Review comprehensive responses** with sources and confidence scores

### API Usage

#### Query the Virtual SME

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    headers={
        "Authorization": "Bearer your-token",
        "Content-Type": "application/json"
    },
    json={
        "query": "What are the key considerations for supply chain financing?",
        "user_id": "user123",
        "preferred_domains": ["distribution_finance", "risk_management"]
    }
)

result = response.json()
print(result["answer"])
```

#### Add Knowledge Documents

```python
response = requests.post(
    "http://localhost:8000/documents",
    headers={
        "Authorization": "Bearer your-token",
        "Content-Type": "application/json"
    },
    json={
        "title": "New Banking Policy",
        "content": "Policy content here...",
        "domain": "compliance",
        "source": "Internal Policy Document"
    }
)
```

### Example Queries

- "What are the risk factors in global trade finance?"
- "How does channel finance work for automotive dealers?"
- "What compliance requirements apply to distribution financing?"
- "What are the best practices for customer service in digital banking?"
- "How do we assess credit risk for supply chain partners?"

## 🏛️ Banking Domains

### Distribution Finance
- Supply chain financing
- Inventory financing
- Working capital solutions
- Trade credit insurance
- Distribution network financing

### Channel Finance
- Channel partner financing
- Dealer financing
- Franchise financing
- Channel credit programs
- Partner relationship management

### Global Trade Finance
- Letters of credit
- Trade guarantees
- Export/import financing
- Documentary collections
- Trade risk management
- International payment solutions

### Risk Management
- Credit risk assessment
- Market risk analysis
- Operational risk management
- Regulatory compliance
- Risk modeling and analytics

### Compliance
- Regulatory requirements
- Anti-money laundering (AML)
- Know Your Customer (KYC)
- Banking regulations
- Compliance monitoring and reporting

### Customer Service
- Customer relationship management
- Service delivery optimization
- Customer experience enhancement
- Digital banking solutions
- Customer support processes

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
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
```

### Customization

#### Adding New Domains

1. **Update the BankingDomain enum** in `virtual_sme_solution.py`
2. **Add domain-specific prompts** in the `_initialize_domain_experts` method
3. **Update the web interface** to include the new domain

#### Customizing Prompts

Modify the domain expert prompts in the `VirtualSMESystem._initialize_domain_experts()` method to tailor responses to your specific needs.

## 📊 Monitoring and Analytics

### Query Logging

All queries are automatically logged with:
- User ID
- Query text
- Response
- Domains consulted
- Confidence score
- Timestamp

### Knowledge Base Statistics

Monitor your knowledge base with:
- Total documents per domain
- Vector store status
- Query performance metrics

## 🔒 Security Features

- **JWT Authentication**: Secure API access
- **Role-based Access Control**: Different permissions for different user types
- **Query Logging**: Complete audit trail
- **Input Validation**: Protection against malicious inputs
- **Rate Limiting**: Prevent abuse

## 🚀 Deployment

### Production Deployment

1. **Use a production database**
   ```bash
   # PostgreSQL recommended for production
   DATABASE_URL=postgresql://user:password@localhost/virtual_sme
   ```

2. **Set up proper authentication**
   - Implement JWT token validation
   - Add user management system
   - Configure role-based access

3. **Use a production server**
   ```bash
   # Using Gunicorn with Uvicorn workers
   gunicorn virtual_sme_solution:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

4. **Set up monitoring**
   - Application performance monitoring
   - Error tracking
   - Usage analytics

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "virtual_sme_solution.py"]
```

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Sample Test Cases

- Query processing across multiple domains
- Document addition and retrieval
- Authentication and authorization
- API endpoint functionality

## 📈 Performance Optimization

### Vector Store Optimization

- **Chunk Size**: Optimize document chunking for better retrieval
- **Embedding Model**: Consider using domain-specific embeddings
- **Index Optimization**: Regular reindexing for large knowledge bases

### Response Generation

- **Caching**: Cache frequently asked questions
- **Parallel Processing**: Process multiple domains concurrently
- **Response Length**: Optimize for clarity and conciseness

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the API documentation at `http://localhost:8000/docs`
2. Review the logs in the `logs/` directory
3. Open an issue on GitHub

## 🔮 Future Enhancements

- **Multi-language Support**: Support for multiple languages
- **Voice Interface**: Speech-to-text and text-to-speech capabilities
- **Advanced Analytics**: Business intelligence and reporting
- **Integration APIs**: Connect with existing banking systems
- **Mobile App**: Native mobile application
- **Advanced Security**: Multi-factor authentication, encryption at rest

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

---

**Built with ❤️ for the banking industry**
