# 🎓 EduGenius - AI-Powered Educational Assistant

EduGenius is an intelligent educational platform that leverages multiple Large Language Models (LLMs) including **DeepSeek**, OpenAI, and Anthropic to provide personalized learning experiences.

## ✨ Features

- **🧠 Multiple LLM Support**: Use DeepSeek, OpenAI (GPT-4), or Anthropic (Claude) as your AI backend
- **📝 Quiz Generation**: Create custom quizzes on any topic with multiple difficulty levels
- **💡 Concept Explanations**: Get clear, level-appropriate explanations of complex concepts
- **📅 Study Plans**: Generate personalized study plans based on your goals and schedule
- **🤝 Homework Help**: Receive guided assistance without direct answers (Socratic method)
- **🎯 Practice Problems**: Generate practice problems with hints and solutions
- **🌐 Modern Web Interface**: Clean, responsive UI that works on all devices
- **🔄 Flexible Provider Selection**: Choose your preferred LLM for each request
- **✅ Content Validation System**: Advanced content verification with confidence scoring
- **📚 Wikipedia RAG Integration**: Retrieval-Augmented Generation using Wikipedia as reference
- **⚠️ Smart Warnings**: Automatic alerts about content reliability and factual accuracy
- **📊 Confidence Scoring**: Transparency about AI-generated content quality
- **📝 Content Logging**: Complete audit trail of all generated content for quality tracking

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API key for at least one LLM provider:
  - **DeepSeek** (recommended) - Get from [DeepSeek Platform](https://platform.deepseek.com/)
  - OpenAI - Get from [OpenAI Platform](https://platform.openai.com/)
  - Anthropic - Get from [Anthropic Console](https://console.anthropic.com/)

### Installation

1. **Clone or download the repository**:
   ```bash
   cd EduGenius
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

5. **Edit `.env` file and add your API keys**:
   ```env
   # Add at least one API key
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here

   # Set default provider (deepseek, openai, or anthropic)
   DEFAULT_LLM_PROVIDER=deepseek
   ```

6. **Run the application**:
   ```bash
   # Using Python directly
   python3 run.py

   # Or using the bash script (Linux/Mac)
   chmod +x run.sh
   ./run.sh
   ```

7. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

## 📖 Usage Guide

### Web Interface

The web interface provides five main features accessible via tabs:

#### 1. Generate Quiz
- Enter a topic (e.g., "Ancient Rome", "Python Programming")
- Select number of questions (1-20)
- Choose difficulty level (Easy, Medium, Hard)
- Select LLM provider (optional, uses default if not specified)
- Click "Generate Quiz" to create an interactive quiz

#### 2. Explain Concept
- Enter a concept to learn about
- Choose your level (Beginner, Intermediate, Advanced)
- Get a detailed, structured explanation with examples

#### 3. Study Plan
- Enter the subject you want to study
- Specify duration in weeks and hours per week
- Receive a week-by-week structured study plan with topics, activities, and goals

#### 4. Homework Help
- Paste your homework question
- Optionally specify the subject
- Get guided help that teaches you how to solve the problem

#### 5. Practice Problems
- Enter a topic to practice
- Select number of problems (1-10)
- Choose difficulty level
- Get problems with hints and detailed solutions

### API Endpoints

EduGenius also provides a REST API for integration:

#### Health Check
```bash
GET /api/health
```

#### Get Available Providers
```bash
GET /api/providers
```

#### Generate Quiz
```bash
POST /api/quiz
Content-Type: application/json

{
  "topic": "World War II",
  "num_questions": 5,
  "difficulty": "medium",
  "provider": "deepseek"  // optional
}
```

#### Explain Concept
```bash
POST /api/explain
Content-Type: application/json

{
  "concept": "Quantum Entanglement",
  "level": "intermediate",
  "provider": "deepseek"  // optional
}
```

#### Create Study Plan
```bash
POST /api/study-plan
Content-Type: application/json

{
  "subject": "Machine Learning",
  "duration_weeks": 8,
  "hours_per_week": 10,
  "provider": "deepseek"  // optional
}
```

#### Get Homework Help
```bash
POST /api/homework-help
Content-Type: application/json

{
  "question": "How do I solve this quadratic equation: x² + 5x + 6 = 0?",
  "subject": "Mathematics",
  "provider": "deepseek"  // optional
}
```

#### Generate Practice Problems
```bash
POST /api/practice
Content-Type: application/json

{
  "topic": "Algebra",
  "num_problems": 3,
  "difficulty": "medium",
  "provider": "deepseek"  // optional
}
```

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔧 Configuration

### Environment Variables

All configuration is done via the `.env` file:

```env
# Server Configuration
HOST=0.0.0.0              # Server host (0.0.0.0 for all interfaces)
PORT=8000                 # Server port
DEBUG=True                # Enable debug mode and auto-reload

# LLM API Keys
OPENAI_API_KEY=sk-...     # Your OpenAI API key
ANTHROPIC_API_KEY=sk-...  # Your Anthropic API key
DEEPSEEK_API_KEY=sk-...   # Your DeepSeek API key

# Default LLM Provider
DEFAULT_LLM_PROVIDER=deepseek  # Options: openai, anthropic, deepseek

# DeepSeek Configuration
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# OpenAI Configuration
OPENAI_MODEL=gpt-4o-mini

# Anthropic Configuration
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### Choosing an LLM Provider

**DeepSeek** (Recommended):
- Cost-effective
- Strong performance on educational tasks
- Fast response times
- API: https://platform.deepseek.com/

**OpenAI**:
- Industry-leading models
- Excellent for complex reasoning
- Wide language support
- API: https://platform.openai.com/

**Anthropic**:
- Long context windows
- Strong at following instructions
- Excellent safety features
- API: https://console.anthropic.com/

### Content Validation & Quality Assurance

EduGenius includes a comprehensive content validation system to ensure educational quality:

**How It Works:**
1. **Wikipedia RAG Integration**: When generating content, the system automatically searches Wikipedia for relevant reference material
2. **Reference-Augmented Prompts**: LLMs receive context from reliable sources to improve factual accuracy
3. **Confidence Scoring**: Each generated content receives a confidence score (High/Medium/Low) based on:
   - Availability of reference material
   - LLM provider reliability
   - Topic complexity
4. **Smart Warnings**: Users receive clear warnings about:
   - AI-generated content limitations
   - Missing reference materials
   - Recommended verification steps
5. **Content Logging**: All generated content is logged for quality tracking and auditing

**Confidence Levels:**
- **High (85%+)**: Content verified with reference material from reliable provider
- **Medium (70-85%)**: Good quality but limited references or less tested provider
- **Low (<70%)**: No references found or untested scenario - verify carefully

**Validation Settings** (configured in `.env`):
```env
ENABLE_CONTENT_VALIDATION=True       # Enable/disable validation system
ENABLE_WIKIPEDIA_REFERENCES=True     # Use Wikipedia for RAG
MIN_CONFIDENCE_THRESHOLD=0.60        # Minimum confidence threshold
ENABLE_CONTENT_LOGGING=True          # Log all content for auditing
```

**Content Logs:**
All generated content is logged to `logs/content_validation.log` and `logs/content_log_YYYYMMDD.jsonl` for:
- Quality tracking and improvement
- Auditing educational content
- Identifying problematic patterns
- Research and analysis

**Best Practices:**
- ✅ Always review AI-generated content for accuracy
- ✅ Cross-reference important facts with multiple sources
- ✅ Use high-confidence content as a starting point, not final authority
- ✅ Check reference sources when provided
- ⚠️ Be extra cautious with low-confidence content
- ⚠️ Verify specialized or controversial topics independently

## 🏗️ Project Structure

```
EduGenius/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── llm_providers.py     # LLM provider implementations
│   ├── services.py          # Educational services
│   ├── content_validation.py # Content validation & RAG system
│   └── main.py              # FastAPI application
├── static/
│   ├── index.html           # Web interface
│   ├── styles.css           # Styling
│   └── app.js               # Frontend logic
├── logs/                    # Content validation and audit logs
│   ├── content_validation.log
│   └── content_log_YYYYMMDD.jsonl
├── .env                     # Environment configuration (create from .env.example)
├── .env.example             # Example environment file
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── run.py                   # Application runner
├── run.sh                   # Startup script
└── README.md                # This file
```

## 🧪 Development

### Running in Development Mode

```bash
# With auto-reload enabled
python3 run.py

# Or directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Adding New Features

1. **New Educational Service**: Add methods to `app/services.py`
2. **New API Endpoint**: Add routes to `app/main.py`
3. **New Frontend Feature**: Update `static/index.html`, `static/styles.css`, and `static/app.js`
4. **New LLM Provider**: Implement in `app/llm_providers.py`

### Code Structure

- **app/config.py**: Manages all configuration using Pydantic settings
- **app/llm_providers.py**: Abstract base class and implementations for each LLM
- **app/content_validation.py**: Content validation system with Wikipedia RAG integration
- **app/services.py**: Educational features using LLM providers with validation
- **app/main.py**: FastAPI routes and request handling
- **static/**: Frontend files served by FastAPI
- **logs/**: Content validation and audit logs

## 🐛 Troubleshooting

### "API key not configured" error
- Make sure you've created the `.env` file from `.env.example`
- Add at least one valid API key
- Restart the application

### Port already in use
- Change the `PORT` in `.env` file
- Or stop the process using port 8000: `lsof -ti:8000 | xargs kill`

### Import errors
- Make sure you're in the virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Slow responses
- Some LLM providers may have rate limits
- Try using a different provider
- Reduce the `max_tokens` parameter in the code

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 🌟 Features Roadmap

- [ ] User authentication and session management
- [ ] Save and track learning progress
- [ ] Export quizzes and study plans to PDF
- [ ] Flashcard generation
- [ ] Spaced repetition system
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Integration with educational platforms (Khan Academy, Coursera, etc.)
- [ ] Mobile app (React Native or Flutter)

## 📧 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the API docs at `/docs`

## 🎉 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- LLM Support: [DeepSeek](https://www.deepseek.com/), [OpenAI](https://openai.com/), [Anthropic](https://www.anthropic.com/)
- Frontend: Vanilla JavaScript with modern CSS

---

**Made with ❤️ for learners everywhere**
