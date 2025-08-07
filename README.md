# 🦁 LMU Campus LLM V2 - Enhanced with Authentic Campus Tea!

> **Your AI buddy for everything LMU - now with REAL student experiences from Reddit & RateMyProfessors!**

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 8GB+ RAM (for Ollama models)
- Internet connection

### Basic Setup (No Fine-tuning)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Enhanced Setup with Authentic Data (Recommended)
```bash
# 1. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Collect authentic LMU data
python3 collect_lmu_data.py

# 3. Run the enhanced app
streamlit run app.py

# 4. Choose "V2 - Enhanced with Reddit/RMP Data" in the app
```

## 🌐 Deployment Options

### Deploy to Streamlit Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy!

**Note**: Streamlit Cloud doesn't support Ollama. The app will use fallback responses.

### Deploy to VPS/Server with Ollama
1. **Set up your server** (Ubuntu 20.04+ recommended)
2. **Install Ollama**:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```
3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Start Ollama service**:
   ```bash
   ollama serve &
   ```
5. **Pull the base model**:
   ```bash
   ollama pull llama2:7b
   ```
6. **Deploy with Streamlit**:
   ```bash
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   ```

### Deploy with Docker
```bash
# Build and run with Docker
docker build -t lmu-buddy .
docker run -p 8501:8501 -p 11434:11434 lmu-buddy
```

## 🔧 Fine-tuning Your LMU Buddy

### Quick Fine-tuning
```bash
# Run the fine-tuning script
python3 fine_tune_lmu_buddy.py
```

### Manual Fine-tuning Process
1. **Ensure Ollama is running**:
   ```bash
   ollama serve &
   ```

2. **Pull base model**:
   ```bash
   ollama pull llama2:7b
   ```

3. **Run fine-tuning**:
   ```bash
   python3 fine_tune_lmu_buddy.py
   ```

4. **Test the model**:
   ```bash
   ollama run lmu-buddy "Where should I eat on campus?"
   ```

### Customize Training Data
Edit `fine_tune_lmu_buddy.py` to add more conversational examples:
```python
conversations = [
    {
        "prompt": "Your new prompt",
        "response": "Your new response"
    }
]
```

### Available Base Models
- `llama2:7b` - Good balance of performance and speed (default)
- `llama2:13b` - Better performance, slower inference
- `mistral:7b` - Alternative base model
- `codellama:7b` - Good for technical questions

## ✨ Features

### 🤖 **Enhanced LMU Buddy V2**
- **Advanced Tone Mirroring** - Analyzes and mirrors your exact communication style
- **Authentic Campus Tea** - Real student experiences from Reddit & RateMyProfessors
- **Gen-Z Voice** - Speaks like a real LMU student with authentic slang and emojis
- **Smart Context** - Remembers your major, dorm, and preferences over time
- **Real-time Data** - Fresh campus gossip and professor reviews
- **Tone Analysis Dashboard** - Visual feedback on your communication style
- **Dual Version Support** - Choose between V1 (original) and V2 (enhanced)

### 🏠 **Landing Page + Waitlist**
- **Viral-ready landing page** with LMU branding
- **Waitlist system** with referral tracking
- **Real-time counter** showing community growth
- **Social proof** with user testimonials

### 📊 **Analytics Dashboard**
- **Waitlist growth tracking**
- **User engagement metrics**
- **Organization insights**
- **Real-time data visualization**

## 🛠️ Technical Stack

- **Frontend**: Streamlit (Python)
- **AI/ML**: Sentence Transformers, Semantic Search, Tone Analysis
- **Data Collection**: Reddit API, RateMyProfessors Scraping
- **Data Storage**: JSON files with real-time updates
- **Styling**: Custom CSS with LMU branding

## 📁 Project Structure

```
lmu-campus-llm/
├── app.py                           # Main Streamlit application with V1/V2 selection
├── enhanced_lmu_buddy.py            # Original AI chatbot (V1)
├── enhanced_lmu_buddy_v2.py         # Enhanced AI chatbot with tone mirroring (V2)
├── requirements.txt                 # Python dependencies
├── waitlist.json                   # Waitlist data (auto-generated)
├── lmu_embeddings.pkl              # AI embeddings (auto-generated)
├── enhanced_lmu_data.json          # Original LMU campus data
├── enhanced_lmu_data_v2.json       # Enhanced LMU data with Reddit/RMP content
│
├── 📱 Data Collection Files
├── lmu_reddit_scraper.py           # Reddit data collection for authentic campus tea
├── lmu_rmp_scraper.py              # RateMyProfessors data collection
├── collect_lmu_data.py             # Combined data collection script
├── lmu_reddit_data.json            # Reddit scraped data (auto-generated)
├── lmu_rmp_data.json               # RMP scraped data (auto-generated)
├── data_collection_summary.json    # Collection summary report
│
├── 📄 Configuration Files
├── .streamlit/config.toml          # Streamlit configuration
├── Dockerfile                      # Docker deployment
├── .gitignore                      # Git ignore rules
└── .dockerignore                   # Docker ignore rules
```

## 🎯 What Makes This Special

1. **Advanced Tone Mirroring**: Analyzes your writing style with multiple indicators and mirrors it perfectly
2. **Authentic Campus Tea**: Real student experiences from Reddit and RateMyProfessors, not generic responses
3. **Gen-Z Voice**: Speaks like a real LMU student with authentic slang, emojis, and campus culture
4. **Smart Personalization**: Remembers your major, dorm, and preferences over time
5. **Real-time Data**: Fresh campus gossip and professor reviews, always up-to-date
6. **Dual Version Support**: Choose between V1 (original) and V2 (enhanced) based on your needs

## 🔧 Customization

### Update AI Responses
Edit `enhanced_lmu_buddy_v2.py` to modify:
- Advanced tone detection logic
- Response generation with authentic tea
- Campus knowledge base with Reddit/RMP data

### Update Styling
Edit the CSS in `app.py` to change:
- Colors and branding
- Layout and design
- Mobile responsiveness

### Update Campus Data
Run `collect_lmu_data.py` to get fresh authentic data:
- Collect new Reddit posts for campus tea
- Update professor reviews from RateMyProfessors
- Refresh dining reviews and recommendations
- Get latest event opinions and TNL feedback

## 🚨 Troubleshooting

### Data Collection Issues
```bash
# Check if scrapers are working
python3 lmu_reddit_scraper.py
python3 lmu_rmp_scraper.py

# Verify data files exist
ls -la *.json

# Regenerate all data
python3 collect_lmu_data.py
```

### Tone Analysis Issues
```bash
# Test tone detection
python3 -c "
from enhanced_lmu_buddy_v2 import EnhancedLMUBuddyV2
buddy = EnhancedLMUBuddyV2()
scores = buddy.analyze_user_tone('Yo what\'s up?')
print(scores)
"
```

### Deployment Issues
- **Streamlit Cloud**: Use basic setup (no Ollama)
- **VPS/Server**: Ensure Ollama service is running
- **Docker**: Check port mappings and service startup
- **Timeout errors**: Increase timeout values in client code

### Performance Optimization
- **Slow responses**: Clear embeddings cache with `rm lmu_embeddings.pkl`
- **Memory issues**: Ensure 8GB+ RAM for embeddings
- **Storage**: Use SSD for faster data processing
- **Data freshness**: Run `collect_lmu_data.py` regularly for updated content

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: See `README_ENHANCED.md` for detailed V2 features
- **Data Updates**: Run `collect_lmu_data.py` for fresh campus tea

---

**🦁 Ready to experience the most authentic LMU AI? Deploy V2 and start chatting with real campus tea!**

*Built with ❤️ for the LMU community - Bringing Back the Roar!*
