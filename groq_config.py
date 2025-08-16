"""
Groq Configuration for Virtual SME System
"""

# Available Groq models
GROQ_MODELS = {
    "llama3-8b-8192": {
        "name": "llama3-8b-8192",
        "description": "Fast and efficient 8B parameter model",
        "max_tokens": 8192,
        "recommended_for": "General queries, cost-effective inference"
    },
    "llama3-70b-8192": {
        "name": "llama3-70b-8192", 
        "description": "High-performance 70B parameter model",
        "max_tokens": 8192,
        "recommended_for": "Complex reasoning, high accuracy requirements"
    },
    "mixtral-8x7b-32768": {
        "name": "mixtral-8x7b-32768",
        "description": "Mixture of experts model with large context",
        "max_tokens": 32768,
        "recommended_for": "Long documents, extensive context analysis"
    },
    "gemma2-9b-it": {
        "name": "gemma2-9b-it",
        "description": "Google's Gemma2 instruction-tuned model",
        "max_tokens": 8192,
        "recommended_for": "Instruction following, structured outputs"
    }
}

# Available embedding models (HuggingFace)
EMBEDDING_MODELS = {
    "sentence-transformers/all-MiniLM-L6-v2": {
        "name": "sentence-transformers/all-MiniLM-L6-v2",
        "description": "Fast and efficient sentence embeddings",
        "dimensions": 384,
        "recommended_for": "General purpose embeddings, fast inference"
    },
    "sentence-transformers/all-mpnet-base-v2": {
        "name": "sentence-transformers/all-mpnet-base-v2",
        "description": "High-quality sentence embeddings",
        "dimensions": 768,
        "recommended_for": "High-accuracy semantic search"
    },
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2": {
        "name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "description": "Multilingual sentence embeddings",
        "dimensions": 384,
        "recommended_for": "Multilingual applications"
    }
}

# Default configuration
DEFAULT_MODEL = "llama3-8b-8192"
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_TEMPERATURE = 0.1
DEFAULT_MAX_TOKENS = 4096

def get_model_config(model_name: str = None):
    """Get configuration for a specific model"""
    model_name = model_name or DEFAULT_MODEL
    
    if model_name not in GROQ_MODELS:
        raise ValueError(f"Unknown model: {model_name}. Available models: {list(GROQ_MODELS.keys())}")
    
    return GROQ_MODELS[model_name]

def get_embedding_model_config(model_name: str = None):
    """Get configuration for a specific embedding model"""
    model_name = model_name or DEFAULT_EMBEDDING_MODEL
    
    if model_name not in EMBEDDING_MODELS:
        raise ValueError(f"Unknown embedding model: {model_name}. Available models: {list(EMBEDDING_MODELS.keys())}")
    
    return EMBEDDING_MODELS[model_name]

def list_available_models():
    """List all available models with descriptions"""
    print("Available Groq LLM Models:")
    print("=" * 50)
    
    for model_id, config in GROQ_MODELS.items():
        print(f"\nModel: {model_id}")
        print(f"Description: {config['description']}")
        print(f"Max Tokens: {config['max_tokens']:,}")
        print(f"Recommended for: {config['recommended_for']}")
        print("-" * 30)
    
    print("\n\nAvailable Embedding Models (HuggingFace):")
    print("=" * 50)
    
    for model_id, config in EMBEDDING_MODELS.items():
        print(f"\nModel: {model_id}")
        print(f"Description: {config['description']}")
        print(f"Dimensions: {config['dimensions']:,}")
        print(f"Recommended for: {config['recommended_for']}")
        print("-" * 30)

if __name__ == "__main__":
    list_available_models()
