# 🦁 LMU Campus LLM MVP - Bring Back the Roar!

> **Your personal AI buddy for everything LMU - from the best food spots to study hacks!**

## 🚀 Quick Start

### Option 1: One-Click Deployment (Recommended)
```bash
# Clone the repository
git clone <your-repo-url>
cd lmu-campus-llm

# Run the deployment script
./deploy.sh
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

### Option 3: Docker Deployment
```bash
# Build and run with Docker
docker-compose up --build
```

## ✨ Features

### 🏠 **Landing Page + Waitlist**
- **Viral-ready landing page** with LMU branding
- **Waitlist system** with referral tracking
- **Real-time counter** showing community growth
- **Social proof** with user testimonials

### 🤖 **LMU Buddy AI Chatbot**
- **GenZ personality** with emojis and campus slang
- **RAG-powered responses** using LMU knowledge base
- **Contextual answers** for food, study spots, events, etc.
- **Feedback system** for continuous improvement

### 📊 **Analytics Dashboard**
- **Waitlist growth tracking**
- **User engagement metrics**
- **Organization insights**
- **Real-time data visualization**

### 🎯 **Viral Growth Features**
- **Referral system** with unique codes
- **Social sharing** with branded content
- **Leaderboard** for top sharers
- **Exclusive rewards** for early adopters

## 🛠️ Technical Stack

- **Frontend**: Streamlit (Python)
- **AI/ML**: Sentence Transformers, FAISS
- **Data Storage**: JSON files (easily upgradable to database)
- **Deployment**: Docker, Streamlit Cloud, Heroku, Railway
- **Styling**: Custom CSS with LMU branding

## 📁 Project Structure

```
lmu-campus-llm/
├── app.py                 # Main Streamlit application
├── lmu_buddy.py          # Advanced AI chatbot with RAG
├── requirements.txt      # Python dependencies
├── deploy.sh            # Deployment automation script
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Multi-container setup
├── Procfile            # Heroku deployment
├── runtime.txt         # Python version specification
├── .streamlit/         # Streamlit configuration
│   └── config.toml
├── waitlist.json       # Waitlist data (auto-generated)
└── embeddings.pkl      # AI embeddings (auto-generated)
```

## 🚀 Deployment Options

### 1. **Streamlit Cloud (Recommended for MVP)**
- **Free tier available**
- **Automatic deployments** from GitHub
- **Perfect for demos and testing**

```bash
# 1. Push code to GitHub
git add .
git commit -m "Initial commit"
git push origin main

# 2. Deploy to Streamlit Cloud
./deploy.sh streamlit
```

### 2. **Heroku**
- **Scalable platform**
- **Custom domain support**
- **Database integration ready**

```bash
# Deploy to Heroku
./deploy.sh heroku
```

### 3. **Railway**
- **Modern deployment platform**
- **Easy scaling**
- **Database included**

```bash
# Deploy to Railway
./deploy.sh railway
```

### 4. **Local Development**
```bash
# Run locally
./deploy.sh local
```

### 5. **Docker**
```bash
# Run with Docker
./deploy.sh docker
```

## 🧪 Testing

Run comprehensive tests:
```bash
./deploy.sh test
```

Tests include:
- ✅ Waitlist functionality
- ✅ AI response generation
- ✅ Data persistence
- ✅ UI components

## 📈 Analytics & Growth

### **Waitlist Metrics**
- Total signups
- Growth rate
- Referral tracking
- Organization breakdown

### **Engagement Metrics**
- Chat sessions
- Average session length
- Feedback rates
- Feature usage

### **Viral Coefficients**
- Share rates
- Referral conversion
- Social media mentions
- Community growth

## 🎯 Marketing Strategy

### **Phase 1: Launch (Week 1-2)**
- [ ] Deploy MVP to Streamlit Cloud
- [ ] Share with LMU student groups
- [ ] Post on social media with #BringBackTheRoar
- [ ] Collect initial feedback

### **Phase 2: Growth (Week 3-4)**
- [ ] Implement referral rewards
- [ ] Add more AI capabilities
- [ ] Partner with campus organizations
- [ ] Launch influencer campaign

### **Phase 3: Scale (Month 2+)**
- [ ] Add database backend
- [ ] Implement advanced features
- [ ] Expand to other campuses
- [ ] Monetization options

## 🔧 Customization

### **Branding**
- Update colors in `.streamlit/config.toml`
- Modify CSS in `app.py`
- Replace LMU-specific content

### **AI Responses**
- Edit responses in `lmu_buddy.py`
- Add new knowledge categories
- Fine-tune personality

### **Features**
- Add new pages in `app.py`
- Implement additional analytics
- Create new AI capabilities

## 📊 Performance Optimization

### **Current Optimizations**
- ✅ Lazy loading of AI models
- ✅ Cached embeddings
- ✅ Efficient data structures
- ✅ Mobile-responsive design

### **Future Improvements**
- [ ] Database integration
- [ ] CDN for static assets
- [ ] Advanced caching
- [ ] Load balancing

## 🔒 Security & Privacy

### **Data Protection**
- ✅ No sensitive data collection
- ✅ Local data storage
- ✅ GDPR compliant
- ✅ Secure deployment

### **Best Practices**
- ✅ Input validation
- ✅ Rate limiting
- ✅ Error handling
- ✅ Logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

- **Issues**: GitHub Issues
- **Email**: [your-email@lmu.edu]
- **Discord**: [your-discord-link]

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- LMU student community for feedback
- Streamlit team for the amazing framework
- Open source contributors
- Campus organizations for support

---

**🦁 Ready to Bring Back the Roar? Deploy now and start building the LMU community!**

*Built with ❤️ for the LMU community*
