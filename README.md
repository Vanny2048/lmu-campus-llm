# 🦁 LMU Campus LLM - Bring Back the Roar!

> **Your personal AI buddy for everything LMU - from the best food spots to study hacks!**

## 🚀 Quick Start

### Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Deploy to Streamlit Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy!

## ✨ Features

### 🤖 **LMU Buddy AI Chatbot**
- **Mirrors your tone** - If you're formal, it's formal. If you're casual, it's casual!
- **Intimate LMU knowledge** - Knows every detail about campus life
- **Better than ChatGPT** for LMU-specific questions
- **GenZ personality** with emojis and campus slang
- **RAG-powered responses** using comprehensive LMU knowledge base

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
├── app.py                 # Main Streamlit application
├── enhanced_lmu_buddy.py  # AI chatbot with tone mirroring
├── requirements.txt      # Python dependencies
├── waitlist.json        # Waitlist data (auto-generated)
└── lmu_embeddings.pkl   # AI embeddings (auto-generated)
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

## 📞 Support

- **Issues**: GitHub Issues
- **Email**: [your-email@lmu.edu]

---

**🦁 Ready to Bring Back the Roar? Deploy now and start building the LMU community!**

*Built with ❤️ for the LMU community*
