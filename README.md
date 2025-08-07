# 🦁 LMU Campus LLM - Bring Back the Roar!

> **Your personal AI buddy for everything LMU - from the best food spots to study hacks!**

## 🚀 Quick Start

### Option 1: Basic Setup (No Fine-tuning)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Option 2: Full Setup with Fine-tuned AI (Recommended)
```bash
# Automated setup with Ollama fine-tuning
python3 setup_fine_tuning.py

# Or manual setup:
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 3. Start Ollama service
ollama serve &

# 4. Pull base model
ollama pull llama2:7b

# 5. Test integration
python3 quick_test.py

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
```dockerfile
# Dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy application files
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose ports
EXPOSE 8501 11434

# Start services
CMD ["sh", "-c", "ollama serve & sleep 10 && ollama pull llama2:7b && streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
```

### Deploy to Railway/Heroku
1. **Add Ollama buildpack** (if supported)
2. **Set environment variables**:
   ```
   OLLAMA_HOST=0.0.0.0
   OLLAMA_ORIGINS=*
   ```
3. **Deploy with Procfile**:
   ```
   web: ollama serve & sleep 10 && ollama pull llama2:7b && streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```

## 🔧 Fine-tuning Your LMU Buddy

### Quick Fine-tuning Setup
```bash
# Run automated fine-tuning
python3 setup_fine_tuning.py
```

### Manual Fine-tuning Process
1. **Create training data**:
   ```bash
   python3 fine_tune_lmu_buddy.py
   ```

2. **Test the model**:
   ```bash
   python3 test_fine_tuned_model.py
   ```

3. **Use in your app**:
   The app automatically integrates with the fine-tuned model!

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
- **AI/ML**: Sentence Transformers, FAISS
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
├── setup_fine_tuning.py            # Automated setup script
├── test_fine_tuned_model.py        # Model testing suite
├── create_simple_modelfile.py      # Modelfile generator
├── create_model_via_api.py         # API-based model creation
├── quick_test.py                   # Quick integration test
├── FINE_TUNING_README.md           # Fine-tuning documentation
│
├── 📄 Generated Files (after fine-tuning)
├── Modelfile                       # Ollama model configuration
├── lmu_buddy_training_data.json    # Training data
├── minimal_modelfile.txt           # Minimal test modelfile
├── test_modelfile.txt              # Test modelfile
└── Dockerfile                      # Docker deployment (optional)
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
# Test the integration
python3 quick_test.py

# Check model availability
python3 test_fine_tuned_model.py

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
- **Email**: [your-email@lmu.edu]
- **Documentation**: See `FINE_TUNING_README.md` for detailed fine-tuning guide

---

**🦁 Ready to Bring Back the Roar? Deploy now and start building the LMU community!**

*Built with ❤️ for the LMU community*
