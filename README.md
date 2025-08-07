# 🦁 LMU Campus LLM - Bring Back the Roar!

> **Your personal AI buddy for everything LMU - from the best food spots to study hacks!**

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

### Full Setup with Fine-tuned AI (Recommended)
```bash
# 1. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 3. Start Ollama service
ollama serve &

# 4. Pull base model
ollama pull llama2:7b

# 5. Run fine-tuning (optional)
python3 fine_tune_lmu_buddy.py

# 6. Run the app
streamlit run app.py
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

### 🤖 **LMU Buddy AI Chatbot**
- **Fine-tuned with Ollama** - Custom LMU Buddy personality and responses
- **Mirrors your tone** - If you're formal, it's formal. If you're casual, it's casual!
- **Intimate LMU knowledge** - Knows every detail about campus life
- **Better than ChatGPT** for LMU-specific questions
- **GenZ personality** with emojis and campus slang
- **RAG-powered responses** using comprehensive LMU knowledge base
- **Fallback support** - Works with or without Ollama fine-tuning

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
- **AI/ML**: Sentence Transformers, FAISS, Ollama
- **Data Storage**: JSON files
- **Styling**: Custom CSS with LMU branding

## 📁 Project Structure

```
lmu-campus-llm/
├── app.py                           # Main Streamlit application
├── enhanced_lmu_buddy.py            # AI chatbot with tone mirroring
├── requirements.txt                 # Python dependencies
├── waitlist.json                   # Waitlist data (auto-generated)
├── lmu_embeddings.pkl              # AI embeddings (auto-generated)
├── enhanced_lmu_data.json          # LMU campus data
├── enhanced_lmu_scraper.py         # Data scraper for LMU information
│
├── 🔧 Fine-tuning Files
├── fine_tune_lmu_buddy.py          # Main fine-tuning script
├── lmu_buddy_ollama_client.py      # Ollama integration client
├── Modelfile                       # Ollama model configuration
├── lmu_buddy_training_data.json    # Training data
│
├── 📄 Configuration Files
├── .streamlit/config.toml          # Streamlit configuration
├── Dockerfile                      # Docker deployment
├── .gitignore                      # Git ignore rules
└── .dockerignore                   # Docker ignore rules
```

## 🎯 What Makes This Special

1. **Tone Mirroring**: The chatbot analyzes your writing style and matches it
2. **Intimate Knowledge**: Knows campus secrets, hidden gems, and student gossip
3. **GenZ Voice**: Speaks like a real LMU student, not a boring FAQ
4. **Waitlist Growth**: Built-in viral features to grow the community

## 🔧 Customization

### Update AI Responses
Edit `enhanced_lmu_buddy.py` to modify:
- Tone detection logic
- Response generation
- Campus knowledge base

### Update Styling
Edit the CSS in `app.py` to change:
- Colors and branding
- Layout and design
- Mobile responsiveness

### Update Campus Data
Edit `enhanced_lmu_data.json` or run `enhanced_lmu_scraper.py` to:
- Add new professors
- Update course information
- Refresh dining options
- Add new events

## 🚨 Troubleshooting

### Ollama Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama service
ollama serve &

# Check available models
ollama list

# Pull base model if missing
ollama pull llama2:7b
```

### Fine-tuning Issues
```bash
# Check model availability
ollama list

# Recreate model if needed
ollama rm lmu-buddy
python3 fine_tune_lmu_buddy.py
```

### Deployment Issues
- **Streamlit Cloud**: Use basic setup (no Ollama)
- **VPS/Server**: Ensure Ollama service is running
- **Docker**: Check port mappings and service startup
- **Timeout errors**: Increase timeout values in client code

### Performance Optimization
- **Slow responses**: Use `llama2:7b` instead of `llama2:13b`
- **Memory issues**: Ensure 8GB+ RAM for Ollama
- **Storage**: Use SSD for faster model loading

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: See `FINE_TUNING_README.md` for detailed fine-tuning guide

---

**🦁 Ready to Bring Back the Roar? Deploy now and start building the LMU community!**

*Built with ❤️ for the LMU community*
