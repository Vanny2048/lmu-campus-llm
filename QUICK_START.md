# 🦁 Enhanced LMU Buddy - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. **Setup Environment**
```bash
# Create virtual environment
python3 -m venv lmu_env
source lmu_env/bin/activate  # On Windows: lmu_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Generate Data** (First time only)
```bash
python run_scraper.py
```
This creates `lmu_data.json` and `lmu_embeddings.pkl` files.

### 3. **Run the Application**
```bash
streamlit run app.py
```

### 4. **Open Your Browser**
Navigate to `http://localhost:8501`

## 🎯 Try These Queries

### **Academic**
- "Who is Dr. Sarah Johnson?"
- "Tell me about CS 150"
- "What are the best professors?"

### **Campus Life**
- "Where should I eat on campus?"
- "What housing options are available?"
- "Tell me about Greek life"

### **Events & Activities**
- "What events are coming up?"
- "What's the latest LMU news?"

## 🔧 Troubleshooting

### **Common Issues**

**Import Error**: Make sure you're in the virtual environment
```bash
source lmu_env/bin/activate
```

**Missing Data**: Regenerate the data files
```bash
python run_scraper.py
```

**Port Already in Use**: Use a different port
```bash
streamlit run app.py --server.port 8502
```

### **Test the System**
```bash
python test_lmu_buddy.py
```

## 📊 What You Get

- **🤖 Advanced AI Chat**: Semantic search and intelligent responses
- **📚 30+ Data Points**: Professors, courses, dining, housing, events, news
- **🎨 Beautiful UI**: Modern, responsive interface
- **⚡ Fast Performance**: Sub-second response times
- **🦁 GenZ Personality**: Engaging, relatable communication

## 🎉 Ready to Roar!

Your Enhanced LMU Buddy is now ready to help with everything LMU! 🦁✨