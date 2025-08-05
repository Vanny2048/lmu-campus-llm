# 🚀 LMU Campus LLM - Complete Deployment Guide

## 📋 Prerequisites

Before deploying, ensure you have:

- ✅ Python 3.9+ installed
- ✅ Git installed
- ✅ GitHub account (for cloud deployments)
- ✅ Basic command line knowledge

## 🎯 Quick Deployment Options

### **Option A: Streamlit Cloud (Recommended for MVP)**
**Best for**: Quick launch, demos, testing
**Cost**: Free tier available
**Time**: 5 minutes

### **Option B: Heroku**
**Best for**: Production, custom domains
**Cost**: Free tier (limited), paid plans available
**Time**: 10 minutes

### **Option C: Railway**
**Best for**: Modern deployment, easy scaling
**Cost**: Free tier available
**Time**: 8 minutes

### **Option D: Local Development**
**Best for**: Development, testing
**Cost**: Free
**Time**: 3 minutes

---

## 🚀 Option A: Streamlit Cloud Deployment

### Step 1: Prepare Your Repository
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/lmu-campus-llm.git
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Fill in the details:
   - **Repository**: `yourusername/lmu-campus-llm`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click "Deploy!"

### Step 3: Configure (Optional)
- Add custom domain in app settings
- Configure environment variables if needed
- Set up monitoring

**✅ Your app is live at**: `https://your-app-name.streamlit.app`

---

## 🚀 Option B: Heroku Deployment

### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login and Deploy
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create lmu-campus-llm-$(date +%s)

# Deploy
git push heroku main

# Open the app
heroku open
```

### Step 3: Configure Environment (Optional)
```bash
# Set environment variables
heroku config:set STREAMLIT_SERVER_PORT=$PORT
heroku config:set STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Add custom domain
heroku domains:add yourdomain.com
```

**✅ Your app is live at**: `https://your-app-name.herokuapp.com`

---

## 🚀 Option C: Railway Deployment

### Step 1: Install Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Or download from https://railway.app/cli
```

### Step 2: Deploy
```bash
# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up

# Get deployment URL
railway status
```

### Step 3: Configure (Optional)
- Add custom domain in Railway dashboard
- Set environment variables
- Configure auto-deploy from GitHub

**✅ Your app is live at**: `https://your-app-name.railway.app`

---

## 🚀 Option D: Local Development

### Step 1: Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run Locally
```bash
# Start the application
streamlit run app.py

# Or use the deployment script
./deploy.sh local
```

**✅ Your app is live at**: `http://localhost:8501`

---

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)
```bash
# Build and run with docker-compose
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### Option 2: Docker Only
```bash
# Build the image
docker build -t lmu-campus-llm .

# Run the container
docker run -p 8501:8501 lmu-campus-llm
```

**✅ Your app is live at**: `http://localhost:8501`

---

## 🔧 Advanced Configuration

### Environment Variables
Create a `.env` file for local development:
```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Custom Domain Setup
1. **Streamlit Cloud**: Add in app settings
2. **Heroku**: `heroku domains:add yourdomain.com`
3. **Railway**: Add in project settings

### SSL/HTTPS
- **Streamlit Cloud**: Automatic
- **Heroku**: Automatic with paid plans
- **Railway**: Automatic
- **Local**: Use ngrok for testing

---

## 📊 Monitoring & Analytics

### Built-in Analytics
The app includes:
- ✅ Waitlist growth tracking
- ✅ User engagement metrics
- ✅ Chat session analytics
- ✅ Feedback collection

### External Monitoring
Consider adding:
- [ ] Google Analytics
- [ ] Sentry for error tracking
- [ ] Uptime monitoring
- [ ] Performance monitoring

---

## 🔒 Security Best Practices

### Data Protection
- ✅ No sensitive data collection
- ✅ Local data storage
- ✅ Input validation
- ✅ Rate limiting

### Deployment Security
- ✅ HTTPS enforcement
- ✅ Environment variable protection
- ✅ Regular dependency updates
- ✅ Security headers

---

## 🚨 Troubleshooting

### Common Issues

#### 1. **Port Already in Use**
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app.py --server.port=8502
```

#### 2. **Dependencies Not Found**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 3. **Docker Build Fails**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild
docker-compose build --no-cache
```

#### 4. **Heroku Deployment Fails**
```bash
# Check logs
heroku logs --tail

# Restart dyno
heroku restart
```

### Performance Issues
- Check memory usage
- Optimize image sizes
- Use CDN for static assets
- Implement caching

---

## 📈 Scaling Strategy

### Phase 1: MVP (0-100 users)
- ✅ Streamlit Cloud free tier
- ✅ JSON file storage
- ✅ Basic analytics

### Phase 2: Growth (100-1000 users)
- [ ] Upgrade to paid Streamlit plan
- [ ] Add database (PostgreSQL)
- [ ] Implement caching
- [ ] Add monitoring

### Phase 3: Scale (1000+ users)
- [ ] Microservices architecture
- [ ] Load balancing
- [ ] CDN integration
- [ ] Advanced analytics

---

## 🎯 Post-Deployment Checklist

### Technical
- [ ] App loads without errors
- [ ] All features working
- [ ] Mobile responsiveness
- [ ] Performance acceptable
- [ ] Analytics tracking

### Marketing
- [ ] Social media posts ready
- [ ] Email list building
- [ ] Influencer outreach
- [ ] Campus organization partnerships
- [ ] Press release prepared

### Growth
- [ ] Referral system active
- [ ] Feedback collection working
- [ ] User onboarding smooth
- [ ] Viral features enabled
- [ ] Community building started

---

## 📞 Support & Resources

### Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [Railway Documentation](https://docs.railway.app/)

### Community
- [Streamlit Community](https://discuss.streamlit.io/)
- [GitHub Issues](https://github.com/yourusername/lmu-campus-llm/issues)

### Tools
- [ngrok](https://ngrok.com/) - Local tunnel for testing
- [Postman](https://postman.com/) - API testing
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Performance testing

---

**🎉 Congratulations! Your LMU Campus LLM is now live and ready to Bring Back the Roar!**

*Need help? Check the troubleshooting section or reach out to the community.*