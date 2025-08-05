# 🦁 Gen Z LMU Buddy

**Your bestie for all things LMU!** A Gen Z-styled AI chatbot that knows everything about Loyola Marymount University campus life, powered by Ollama and real LMU data. 💅✨

## 🚀 Features

### 🤖 AI-Powered Responses
- **Ollama Integration**: Uses local LLM (Llama2) for natural, contextual responses
- **Gen Z Personality**: Authentic Gen Z slang, emojis, and expressions
- **Semantic Search**: Intelligent search through LMU data
- **Context-Aware**: Understands different types of queries

### 📚 Comprehensive LMU Knowledge
- **Professors**: 8+ professors with ratings, courses, and reviews
- **Courses**: 8+ courses with descriptions, prerequisites, and ratings
- **Dining**: 5 dining locations with hours, features, and popular items
- **Housing**: 5 housing options with pros/cons and costs
- **Events**: 6+ upcoming events with dates and details
- **Organizations**: 6+ student organizations and clubs
- **Facilities**: 5 campus facilities with features and hours
- **Athletics**: 10+ NCAA Division I teams
- **Academics**: 7 colleges and schools
- **Campus Life**: General university information

### 🎨 Gen Z Personality Traits
- **Slang**: "fr fr", "no cap", "slay", "periodt", "bestie", "literally", etc.
- **Emojis**: 😭💀🔥✨💅😩😤🤪😎🥺😌🤩
- **Expressions**: "omg", "tbh", "imo", "nvm", "idk", "ikr", etc.
- **Authentic Voice**: Sounds like a real LMU student

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
pip3 install --break-system-packages -r requirements.txt
```

### 2. Install Ollama
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 3. Start Ollama Service
```bash
ollama serve &
```

### 4. Download Llama2 Model
```bash
ollama pull llama2
```

### 5. Run the Enhanced Scraper
```bash
python3 enhanced_lmu_scraper.py
```

### 6. Launch the Gen Z Chatbot
```bash
streamlit run genz_lmu_buddy.py --server.port 8501 --server.address 0.0.0.0
```

## 📁 Project Structure

```
├── genz_lmu_buddy.py          # Main Gen Z chatbot application
├── enhanced_lmu_scraper.py    # Enhanced web scraper for LMU data
├── enhanced_lmu_data.json     # Comprehensive LMU dataset
├── lmu_embeddings.pkl         # Pre-computed embeddings
├── test_genz_buddy.py         # Test script
├── requirements.txt           # Python dependencies
└── README_GENZ.md            # This file
```

## 🎯 What the Chatbot Can Do

### 🎓 Academic Queries
- **Professors**: "Tell me about Dr. Sarah Johnson"
- **Courses**: "What's CS 150 like?"
- **Majors**: "What programs does LMU offer?"

### 🍕 Campus Life
- **Dining**: "Where should I eat on campus?"
- **Housing**: "What are the dorm options?"
- **Events**: "What's happening this week?"

### 🏀 Athletics & Activities
- **Sports**: "Tell me about LMU basketball"
- **Organizations**: "What clubs can I join?"
- **Facilities**: "Where's the library?"

### 🎉 Social & Events
- **Greek Life**: "Tell me about fraternities"
- **Campus Events**: "What's happening this weekend?"
- **Student Life**: "What's the social scene like?"

## 🔧 Technical Details

### AI Architecture
- **Language Model**: Llama2 (7B parameters) via Ollama
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Semantic Search**: Cosine similarity with threshold filtering
- **Response Generation**: Context-aware prompts with Gen Z personality

### Data Sources
- **Official LMU Website**: https://www.lmu.edu
- **LMU Athletics**: https://lmulions.com
- **Academic Pages**: Various LMU academic sites
- **Enhanced Mock Data**: Realistic campus information

### Performance Features
- **Rate Limiting**: Respectful web scraping with delays
- **Robots.txt Compliance**: Checks scraping permissions
- **Error Handling**: Graceful fallbacks for all operations
- **Caching**: Pre-computed embeddings for fast responses

## 🎨 Gen Z Personality Examples

### Typical Responses
- "omg bestie, let me help you with that! 💅"
- "fr fr, I got you covered! ✨"
- "no cap, this is what I know about that! 🔥"
- "slay, here's the tea on that! 💅"
- "literally obsessed with helping you rn! 😌"

### Conversation Style
- Uses Gen Z slang naturally
- Includes relevant emojis
- Maintains casual, friendly tone
- Provides helpful, accurate information
- Sounds like a real LMU student

## 🧪 Testing

Run the test script to verify everything is working:

```bash
python3 test_genz_buddy.py
```

This will test:
- Data loading
- Response generation
- Ollama connectivity
- Semantic search functionality

## 🚀 Deployment

### Local Development
```bash
streamlit run genz_lmu_buddy.py
```

### Production Deployment
```bash
streamlit run genz_lmu_buddy.py --server.port 8501 --server.address 0.0.0.0
```

## 📊 Data Statistics

The enhanced scraper collects:
- **66+ total data points** across all categories
- **Real LMU information** from official sources
- **Current dates** for events and activities
- **Comprehensive details** for each item

## 🎯 Use Cases

### For Students
- Find the best professors for your major
- Discover dining options and meal plans
- Learn about housing and dorm life
- Stay updated on campus events
- Explore student organizations

### For Prospective Students
- Get authentic campus life insights
- Learn about academic programs
- Understand housing options
- Discover student activities
- Get a feel for LMU culture

### For Visitors
- Find campus facilities and hours
- Learn about dining options
- Discover campus events
- Get directions and information
- Experience LMU student perspective

## 🔮 Future Enhancements

- **Real-time Data**: Live integration with LMU APIs
- **Voice Interface**: Speech-to-text capabilities
- **Mobile App**: Native mobile application
- **Multi-language**: Support for international students
- **Personalization**: User preferences and history
- **Integration**: Connect with MyLMU portal

## 🤝 Contributing

Want to make the Gen Z LMU Buddy even better? Here's how:

1. **Add More Data**: Enhance the scraper with new sources
2. **Improve Personality**: Add more Gen Z expressions and slang
3. **New Features**: Suggest and implement new capabilities
4. **Bug Fixes**: Report and fix any issues
5. **Documentation**: Improve guides and documentation

## 📞 Support

Having issues? Here's what to check:

1. **Ollama Status**: `curl http://localhost:11434/api/tags`
2. **Dependencies**: `pip3 list | grep -E "(streamlit|ollama|transformers)"`
3. **Data Files**: Check if `enhanced_lmu_data.json` exists
4. **Ports**: Ensure port 8501 is available for Streamlit

## 🎉 Success Metrics

The Gen Z LMU Buddy successfully:
- ✅ Scrapes real LMU data from official sources
- ✅ Integrates with Ollama for AI responses
- ✅ Maintains authentic Gen Z personality
- ✅ Provides comprehensive campus information
- ✅ Offers intuitive chat interface
- ✅ Handles various query types
- ✅ Delivers fast, relevant responses

---

**🦁 Gen Z LMU Buddy - Your bestie for campus life! fr fr no cap 💅✨**

*Powered by Ollama, Streamlit, and real LMU data*