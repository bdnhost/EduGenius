# 🎓 EduGenius - עוזר הלימוד החכם

EduGenius is an intelligent educational platform that leverages multiple Large Language Models (LLMs) including **DeepSeek**, OpenAI, and Anthropic to provide personalized learning experiences.

**New in v2.0:**
- 🇮🇱 **Full Hebrew interface with RTL support**
- ⚡ **Simplified single-prompt interface** - Create complete learning units from one natural language request
- 🎯 **Unified Learning Units** - Get explanations, quizzes, practice problems, and study plans all at once

## ✨ Features

### Core Functionality
- **🚀 One-Prompt Learning Units**: Simply describe what you want to learn in natural language, and get:
  - 📖 Detailed explanations
  - ✍️ Interactive quizzes with answers
  - 🎯 Practice problems with hints and solutions
  - 📅 Structured study plans
- **🇮🇱 Hebrew Interface**: Full RTL (right-to-left) support with Hebrew UI
- **🌐 Natural Language Input**: No forms to fill - just tell us what you want to learn
- **🧠 Multiple LLM Support**: Use DeepSeek (recommended), OpenAI (GPT-4), or Anthropic (Claude)

### Quality & Validation
- **✅ Content Validation System**: Advanced content verification with confidence scoring
- **📚 Wikipedia RAG Integration**: Retrieval-Augmented Generation using Wikipedia as reference
- **⚠️ Smart Warnings**: Automatic alerts about content reliability and factual accuracy
- **📊 Confidence Scoring**: Transparency about AI-generated content quality (High/Medium/Low)
- **📝 Content Logging**: Complete audit trail of all generated content for quality tracking
- **🔗 Source Attribution**: Direct links to Wikipedia sources used for content generation

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

### Web Interface (Hebrew / עברית)

The new simplified interface allows you to create complete learning units with a single natural language prompt:

#### How to Use:
1. **Open the application** at `http://localhost:8000`
2. **Describe what you want to learn** in the text box - use natural language!
3. **Optionally select an LLM provider** (DeepSeek is recommended)
4. **Click "צור יחידת לימוד" (Create Learning Unit)**
5. **Wait for your complete learning unit** with:
   - 📖 Detailed explanation of the concept
   - ✍️ Interactive quiz with multiple-choice questions
   - 🎯 Practice problems with hints and solutions
   - 📅 Week-by-week study plan

#### Example Prompts:

**Hebrew:**
- `אני רוצה ללמוד על מלחמת העולם השנייה ברמה בסיסית`
- `תכין לי יחידת לימוד על אלגוריתמי מיון בפייתון לרמה מתקדמת`
- `אני צריך ללמוד על תהליך הפוטוסינתזה לכיתה ח׳`
- `תלמד אותי על מהפכת התעשייה עם דגש על השפעותיה החברתיות`

**English:**
- `I want to learn about World War II at a basic level`
- `Prepare me a learning unit on sorting algorithms in Python for advanced level`
- `I need to learn about photosynthesis for 8th grade`
- `Teach me about the Industrial Revolution with emphasis on social impacts`

#### What You'll Get:

Each learning unit includes:
1. **הסבר מפורט (Detailed Explanation)**: Comprehensive explanation with examples and key points
2. **מבחן (Quiz)**: 5 multiple-choice questions with answers and explanations
3. **תרגילי תרגול (Practice Problems)**: 3 practice problems with hints and full solutions
4. **תוכנית לימוד (Study Plan)**: 2+ week structured study plan with weekly topics, activities, and goals
5. **אימות תוכן (Content Validation)**: Confidence score, warnings, and Wikipedia reference links

### API Endpoints

EduGenius provides a REST API for integration:

#### Create Learning Unit (NEW - Recommended)
```bash
POST /api/learning-unit
Content-Type: application/json

{
  "prompt": "I want to learn about the Solar System at an intermediate level",
  "provider": "deepseek"  // optional
}
```

This single endpoint returns a complete learning unit with explanation, quiz, practice problems, and study plan.

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
