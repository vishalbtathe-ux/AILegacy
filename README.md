# AILegacy - Legacy System Modernization Advisor

An AI-powered assistant that helps teams modernize legacy systems by providing intelligent answers based on uploaded documentation.

---

## 📋 Problem Statement

Organizations struggle with modernizing legacy systems due to:
- **Scattered Documentation**: Architecture docs, database schemas, and runbooks are spread across multiple sources
- **Knowledge Loss**: Tribal knowledge from experienced developers is not documented
- **Complex Decision-Making**: Choosing the right modernization strategy requires understanding the entire system
- **Time-Consuming Research**: Developers spend hours searching through documentation to answer simple questions

**Solution**: AILegacy uses RAG (Retrieval-Augmented Generation) to provide instant, context-aware answers by searching through your uploaded documentation and generating intelligent responses using a local LLM.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface                          │
│              (Streamlit Web App / CLI)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Document   │  │     RAG      │  │ Conversation │     │
│  │   Upload     │  │    Agent     │  │   Manager    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer                                │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │   InMemoryDB         │  │   MongoDB            │        │
│  │   (Development)      │  │   (Production)       │        │
│  └──────────────────────┘  └──────────────────────┘        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI Layer                                  │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │   Ollama Server      │  │   LLM Model          │        │
│  │   (Local)            │  │   (llama3.2:1b)      │        │
│  └──────────────────────┘  └──────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### **1. AI Model**
- **Primary Model**: Llama 3.2 (1B parameters) via Ollama
  - **Why**: Fast inference, runs locally, no API costs
  - **Alternatives**: llama3 (8B), phi3:mini
- **Model Server**: Ollama (local LLM runtime)
- **API Interface**: OpenAI-compatible API

### **2. Interface/Frontend**
- **Primary**: Streamlit
  - Web-based UI with chat interface
  - File upload functionality
  - Real-time response streaming
- **Fallback**: CLI (Command Line Interface)
  - For environments without Streamlit
  - Supports batch document upload

### **3. Database**
- **Development**: InMemoryDB (Python class)
  - Fast, no setup required
  - Data lost on restart
- **Production**: MongoDB (optional)
  - Persistent storage
  - Scalable document storage
  - Conversation history tracking

### **4. AI Agent Architecture**
- **Type**: RAG (Retrieval-Augmented Generation)
- **Components**:
  1. **Document Retriever**: Token-based similarity search
  2. **Context Builder**: Assembles relevant document snippets
  3. **LLM Generator**: Generates answers using Ollama
  4. **Response Formatter**: Returns structured responses with sources

### **5. Programming Language & Frameworks**
- **Language**: Python 3.x
- **Web Framework**: Streamlit
- **LLM Client**: OpenAI Python SDK (for Ollama compatibility)
- **Database Driver**: PyMongo (optional)

### **6. Development Tools**
- **Version Control**: Git + GitHub
- **Environment Management**: Python venv
- **Configuration**: python-dotenv (.env files)
- **Testing**: Custom test scripts (pytest-compatible)

---

## 📦 Project Structure

```
AILegacy/
├── app/
│   └── app.py                 # Streamlit web interface + CLI fallback
├── agents/
│   └── rag_agent.py          # RAG agent implementation
├── database/
│   └── connector.py          # Database abstraction layer
├── tests/
│   └── test_cli.py           # Test scripts
├── sample_docs/              # Sample documentation for testing
│   ├── legacy_system.txt
│   └── database_schema.txt
├── requirements.txt          # Python dependencies
├── setup.sh                  # Automated setup script
├── .env                      # Environment configuration (gitignored)
├── SETUP_NEW_SYSTEM.md      # Comprehensive setup guide
├── PERFORMANCE.md           # Performance optimization tips
├── TESTING.md               # Testing guide
└── README.md                # This file
```

---

## 🔧 Core Components

### **1. RAG Agent (`agents/rag_agent.py`)**
**Purpose**: Retrieve relevant documents and generate AI-powered answers

**Key Features**:
- Token-based document similarity scoring
- Context window optimization (500 chars per doc)
- Configurable LLM parameters (temperature, max_tokens)
- Error handling and confidence scoring

**Algorithm**:
1. Tokenize user query
2. Score all documents by token overlap
3. Select top 3 most relevant documents
4. Build context from document snippets
5. Send to LLM with system prompt
6. Return answer with sources and confidence

### **2. Database Connector (`database/connector.py`)**
**Purpose**: Abstract database operations with fallback support

**Features**:
- Automatic fallback to InMemoryDB if MongoDB unavailable
- Unified interface for both database types
- Collections: documents, conversations, feedback

**Methods**:
- `insert_document(doc)`: Store uploaded documents
- `list_documents()`: Retrieve all documents
- `insert_conversation(conv)`: Save chat history
- `list_conversations()`: Retrieve chat history

### **3. Streamlit App (`app/app.py`)**
**Purpose**: User-facing web interface

**Features**:
- Document upload (sidebar)
- Chat interface with message history
- Loading spinner during processing
- Automatic page refresh after responses
- Conversation persistence

---

## 🚀 How It Works

### **User Flow**:
1. **Upload Documents**: User uploads `.txt` files via sidebar
2. **Ask Question**: User types a question in chat input
3. **Document Retrieval**: System searches uploaded docs for relevant content
4. **Context Building**: Top 3 documents are selected and truncated
5. **LLM Query**: Context + question sent to Ollama
6. **Response Generation**: LLM generates answer based on context
7. **Display**: Answer shown in chat with sources cited

### **RAG Pipeline**:
```
User Query → Tokenization → Document Scoring → Top-K Selection
     ↓
Context Assembly → System Prompt + User Prompt → Ollama API
     ↓
LLM Response → Answer Extraction → Display with Sources
```

---

## 📊 Technical Specifications

### **Performance**:
- **Response Time**: 1-5 seconds (with llama3.2:1b)
- **Context Size**: 500 chars per document, max 3 documents
- **Max Tokens**: 300 tokens per response
- **Temperature**: 0.3 (focused, deterministic responses)

### **Scalability**:
- **Documents**: Unlimited (limited by memory in InMemoryDB)
- **Concurrent Users**: Single-user (Streamlit default)
- **Storage**: In-memory or MongoDB

### **Requirements**:
- **RAM**: 4GB minimum (8GB recommended for llama3.2:1b)
- **Disk**: 2GB for model storage
- **CPU**: Multi-core recommended
- **GPU**: Optional (Metal on Mac, CUDA on Linux/Windows)

---

## 🔐 Security & Privacy

- **Local Processing**: All data stays on your machine
- **No Cloud APIs**: No data sent to external services
- **Gitignored Secrets**: `.env` file excluded from version control
- **No Authentication**: Currently single-user, local deployment

---

## 📈 Future Enhancements

- [ ] Vector database integration (ChromaDB, Pinecone)
- [ ] Multi-user authentication
- [ ] Support for PDF, DOCX, Markdown files
- [ ] Advanced chunking strategies
- [ ] Conversation memory and context
- [ ] Export chat history
- [ ] Model fine-tuning on domain-specific data
- [ ] API endpoint for programmatic access

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📞 Support

For setup instructions, see [SETUP_NEW_SYSTEM.md](SETUP_NEW_SYSTEM.md)

For performance tips, see [PERFORMANCE.md](PERFORMANCE.md)

For testing guide, see [TESTING.md](TESTING.md)

---

## 🙏 Acknowledgments

- **Ollama**: For providing an excellent local LLM runtime
- **Streamlit**: For the easy-to-use web framework
- **Meta**: For the Llama models
- **OpenAI**: For the API standard

---

**Built with ❤️ for modernizing legacy systems**
