# 🦁 LMU Campus LLM V2 - Enhanced with Authentic Campus Tea!

> **Your AI buddy for everything LMU - now with REAL student experiences from Reddit & RateMyProfessors!**

## 🚀 What's New in V2

### ✅ Phase 1: Advanced Tone Mirroring
- **Smart Tone Detection**: Analyzes your writing style using multiple indicators
- **Real-time Adaptation**: Mirrors your casual, formal, or academic tone
- **Gen-Z Personality**: Speaks like a real LMU student with authentic slang
- **Emoji Intelligence**: Uses appropriate emojis based on your style

### ✅ Phase 2: Authentic LMU Knowledge
- **Reddit Integration**: Real campus tea from r/LMU
- **RateMyProfessors Data**: Actual professor reviews and ratings
- **Campus Gossip**: Authentic dorm rumors and student experiences
- **Live Data Collection**: Scrapes fresh content automatically

### ✅ Phase 3: Enhanced LMU Buddy Personality
- **Authentic Voice**: Not a boring FAQ, but LMU's real voice
- **Campus Tea**: Knows the real tea about professors, dorms, food, events
- **Personalization**: Remembers your major, dorm, preferences over time
- **Context Awareness**: Adapts responses based on your situation

## 🎯 Key Features

### 🤖 **Enhanced LMU Buddy V2**
- **Advanced Tone Mirroring**: If you're casual, it's casual. If you're formal, it's formal!
- **Authentic Campus Tea**: Real student experiences from Reddit and RateMyProfessors
- **Gen-Z Voice**: Uses emojis, slang, and speaks like a real LMU student
- **Smart Context**: Remembers your major, dorm, and preferences
- **Real-time Data**: Fresh campus gossip and professor reviews

### 📱 **Data Collection System**
- **Reddit Scraper**: Collects authentic student posts from r/LMU
- **RateMyProfessors Scraper**: Gets real professor reviews and ratings
- **Automatic Updates**: Fresh data collection with one command
- **Categorized Tea**: Organized by dorm gossip, professor tea, food reviews, etc.

### 🎭 **Tone Analysis Dashboard**
- **Real-time Analysis**: Shows your detected tone (Casual/Formal/Academic)
- **Visual Metrics**: Percentage breakdown of tone indicators
- **Adaptive Responses**: LMU Buddy adjusts its personality to match yours

## 🛠️ Quick Start

### Prerequisites
- Python 3.8 or higher
- 8GB+ RAM (for embeddings)
- Internet connection

### 1. Basic Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### 2. Collect Authentic Data (Recommended)
```bash
# Collect Reddit and RateMyProfessors data
python3 collect_lmu_data.py

# This will create:
# - lmu_reddit_data.json (campus tea from Reddit)
# - lmu_rmp_data.json (professor reviews from RMP)
# - enhanced_lmu_data_v2.json (combined enhanced data)
# - data_collection_summary.json (collection report)
```

### 3. Run Enhanced App
```bash
# Start the enhanced app
streamlit run app.py

# Choose "V2 - Enhanced with Reddit/RMP Data" in the version selector
```

## 📊 Data Collection Details

### Reddit Data Collection
```bash
# Run Reddit scraper individually
python3 lmu_reddit_scraper.py
```

**Collects:**
- Campus tea and gossip
- Dorm rumors and experiences
- Professor tea and reviews
- Food reviews and recommendations
- Event opinions and TNL feedback
- Admin complaints and issues
- Campus slang and culture
- Student experiences

### RateMyProfessors Data Collection
```bash
# Run RMP scraper individually
python3 lmu_rmp_scraper.py
```

**Collects:**
- Professor profiles and ratings
- Course reviews and difficulty
- Student feedback and comments
- Department-specific insights
- "Would take again" percentages
- Professor tea and recommendations

## 🎭 Tone Mirroring Examples

### Casual User Input:
```
"Yo what's the best food on campus fr fr?"
```

**LMU Buddy V2 Response:**
```
"Hey bestie! The omelette guy is the only reason I wake up for breakfast! That pasta line better be worth it today. Pizza at the Lair is mid but the garlic knots? *chef's kiss* ✨ literally 🔥"
```

### Formal User Input:
```
"Could you please provide information about the dining facilities?"
```

**LMU Buddy V2 Response:**
```
"Certainly, the primary dining facility is the Lair, which offers a variety of meal options including pizza, pasta, and salad bars. The Lion's Den provides smoothie bowls and coffee beverages. Indeed, the dining experience is quite comprehensive."
```

### Academic User Input:
```
"What are the optimal study locations for academic pursuits?"
```

**LMU Buddy V2 Response:**
```
"Furthermore, the Hannon Library's 3rd floor provides the most conducive environment for academic work, offering quiet study spaces with minimal distractions. Additionally, the Burns Fine Arts rooftop offers excellent views and typically maintains a peaceful atmosphere suitable for focused study sessions."
```

## 🍵 Authentic Campus Tea Examples

### Professor Tea:
- "If you're taking Calc with Bro. Martin… godspeed"
- "Dr. Walsh is cool if you participate, mid if you don't"
- "The Film School professors are actually industry legends"

### Dorm Gossip:
- "Nobody uses the showers on 2nd floor Hannon because ghost"
- "McCarthy thinks they're better than Del Rey but ok 👀"
- "Doheny has the best views but the elevators are always broken"

### Food Reviews:
- "The omelette guy is the only reason I wake up for breakfast"
- "That pasta line better be worth it today"
- "Pizza at the Lair is mid but the garlic knots? *chef's kiss*"

### Admin Complaints:
- "They said cura personalis but my advising appointment is 3 weeks out???"
- "Parking is literally the worst, I'm always late to class"
- "The wifi in Malone is actually unusable"

## 🔧 Technical Architecture

### Core Components
```
enhanced_lmu_buddy_v2.py     # Main AI chatbot with tone mirroring
lmu_reddit_scraper.py        # Reddit data collection
lmu_rmp_scraper.py          # RateMyProfessors data collection
collect_lmu_data.py         # Combined data collection script
app.py                      # Streamlit interface with V1/V2 selection
```

### Data Flow
1. **Data Collection**: Reddit + RMP scrapers collect authentic content
2. **Data Processing**: Content categorized and enhanced with metadata
3. **Embedding Generation**: Semantic search vectors for intelligent responses
4. **Tone Analysis**: Real-time user input analysis for personality matching
5. **Response Generation**: Contextual, tone-matched responses with authentic tea

### Tone Detection Algorithm
- **Pattern Matching**: Regex patterns for casual, formal, academic indicators
- **Emoji Analysis**: Emoji usage patterns and frequency
- **Punctuation Analysis**: Exclamation marks, question marks, ALL CAPS
- **Vocabulary Analysis**: Slang, contractions, academic terms
- **Sentence Structure**: Formal connectors, casual fillers

## 🚀 Deployment Options

### Streamlit Cloud (Recommended)
```bash
# Push to GitHub
git add .
git commit -m "Enhanced LMU Buddy V2 with authentic campus tea"
git push origin main

# Deploy on share.streamlit.io
# Connect your GitHub repo and deploy!
```

### Local Development
```bash
# Run with data collection
python3 collect_lmu_data.py
streamlit run app.py

# Access at http://localhost:8501
```

### Docker Deployment
```bash
# Build and run
docker build -t lmu-buddy-v2 .
docker run -p 8501:8501 lmu-buddy-v2
```

## 📈 Analytics & Insights

### Data Collection Metrics
- **Reddit Posts**: 200+ authentic student posts
- **Professor Profiles**: 100+ RMP profiles with reviews
- **Campus Tea Categories**: 8 different types of authentic content
- **Tone Analysis**: Real-time personality matching
- **Response Quality**: Contextual and tone-appropriate

### User Engagement Features
- **Tone Analysis Dashboard**: Visual feedback on communication style
- **Personalization Tracking**: Remembers user preferences over time
- **Authentic Content**: Real student experiences, not generic responses
- **Interactive Quick Access**: One-click access to popular topics

## 🎯 What Makes This Special

### 1. **Authentic Voice**
- Not a boring FAQ, but LMU's real voice
- Uses actual student experiences and language
- Speaks like a real LMU student, not a corporate chatbot

### 2. **Smart Personalization**
- Mirrors your exact communication style
- Remembers your major, dorm, and preferences
- Adapts responses based on your situation

### 3. **Real-time Data**
- Fresh campus gossip from Reddit
- Current professor reviews from RateMyProfessors
- Always up-to-date with student experiences

### 4. **Advanced AI**
- Semantic search for intelligent responses
- Tone analysis for personality matching
- Context awareness for relevant answers

## 🔧 Customization

### Add More Campus Tea
Edit `enhanced_lmu_buddy_v2.py` and add to `lmu_tea` dictionary:
```python
'new_category': [
    "Your authentic campus tea here",
    "More real student experiences",
    "Additional LMU-specific content"
]
```

### Customize Tone Detection
Modify tone patterns in `tone_patterns` dictionary:
```python
'your_tone': {
    'indicators': [r'your_pattern_here'],
    'emoji_usage': ['your', 'emojis'],
    'sentence_endings': ['your', 'endings']
}
```

### Add New Data Sources
Create new scraper in `collect_lmu_data.py`:
```python
# Add your new scraper
from your_new_scraper import YourNewScraper
scraper = YourNewScraper()
data = scraper.run_scrape()
```

## 🚨 Troubleshooting

### Data Collection Issues
```bash
# Check if scrapers are working
python3 lmu_reddit_scraper.py
python3 lmu_rmp_scraper.py

# Verify data files exist
ls -la *.json
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

### Performance Issues
```bash
# Clear embeddings cache
rm lmu_embeddings.pkl

# Regenerate embeddings
python3 -c "
from enhanced_lmu_buddy_v2 import EnhancedLMUBuddyV2
buddy = EnhancedLMUBuddyV2()
buddy.compute_embeddings()
"
```

## 📞 Support & Community

### Getting Help
- **Issues**: GitHub Issues for technical problems
- **Feature Requests**: GitHub Discussions for new ideas
- **Data Updates**: Run `collect_lmu_data.py` for fresh content

### Contributing
1. **Add Campus Tea**: Submit authentic LMU experiences
2. **Improve Tone Detection**: Enhance personality matching
3. **New Data Sources**: Add more authentic content sources
4. **UI Improvements**: Enhance the Streamlit interface

### Community Guidelines
- **Respectful Scraping**: Be mindful of rate limits
- **Authentic Content**: Only use real student experiences
- **Privacy Conscious**: Don't collect personal information
- **LMU Spirit**: Keep the bluff vibes alive! 🦁

---

**🦁 Ready to experience the most authentic LMU AI? Deploy V2 and start chatting with real campus tea!**

*Built with ❤️ for the LMU community - Bringing Back the Roar!*