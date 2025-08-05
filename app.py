import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px
from PIL import Image
import requests
from streamlit_option_menu import option_menu
import time

# Page configuration
st.set_page_config(
    page_title="LMU Campus LLM - Bring Back the Roar! 🦁",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for LMU branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .waitlist-counter {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    .chat-container {
        background: #f8fafc;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .user-message {
        background: #3b82f6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        text-align: right;
    }
    .bot-message {
        background: #e5e7eb;
        color: #374151;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
    .feature-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .cta-button {
        background: linear-gradient(90deg, #3b82f6 0%, #1e3a8a 100%);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        font-weight: bold;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'waitlist_data' not in st.session_state:
    st.session_state.waitlist_data = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

# Load or create waitlist data
def load_waitlist():
    try:
        with open('waitlist.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_waitlist(data):
    with open('waitlist.json', 'w') as f:
        json.dump(data, f)

# LMU Buddy AI responses
def get_lmu_buddy_response(user_input):
    responses = {
        "food": "🍕 The best food spots on campus? Hands down, it's the Lair! Their pizza is legendary, and the smoothie bowls at the Lion's Den are perfect for those early morning classes. Pro tip: avoid the rush by going 15 minutes before the lunch crowd hits! 🦁",
        "study": "📚 Best study spots? The Hannon Library is clutch, especially the quiet zones on the 3rd floor. But my secret spot? The rooftop of the Burns Fine Arts Center - amazing views and usually pretty quiet! Perfect for those late-night cram sessions. ✨",
        "weekend": "🎉 This weekend? Check out the LMU events calendar! There's always something happening - from Greek life mixers to cultural events. Plus, the farmers market on Sundays is a vibe. Don't forget to follow @lmu_events on Instagram for the latest! 🎊",
        "greek": "🏛️ Greek Life hacks? Rush season is intense but so worth it! Go to as many events as possible, be yourself, and don't stress about the perfect outfit. The connections you make last way beyond college. Plus, the parties are epic! 🎭",
        "parking": "🚗 Parking drama? Yeah, it's real. Get there early (like 8 AM early) or park at the Playa Vista shuttle lot. The shuttle runs every 15 minutes and it's free with your student ID. Saves you from the parking ticket stress! 🎫",
        "default": "🤔 That's a great question! As your LMU Buddy, I'm here to help with everything campus-related. Try asking me about food spots, study locations, weekend events, Greek life, or parking tips! I'm constantly learning more about our amazing campus. 🦁✨"
    }
    
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ['food', 'eat', 'restaurant', 'dining']):
        return responses["food"]
    elif any(word in user_input_lower for word in ['study', 'library', 'quiet', 'spot']):
        return responses["study"]
    elif any(word in user_input_lower for word in ['weekend', 'party', 'event', 'fun']):
        return responses["weekend"]
    elif any(word in user_input_lower for word in ['greek', 'sorority', 'fraternity', 'rush']):
        return responses["greek"]
    elif any(word in user_input_lower for word in ['parking', 'car', 'shuttle']):
        return responses["parking"]
    else:
        return responses["default"]

# Navigation
selected = option_menu(
    menu_title=None,
    options=["🏠 Home", "🤖 LMU Buddy", "📊 Waitlist", "📈 Analytics"],
    icons=["house", "robot", "people", "graph-up"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "#3b82f6", "font-size": "18px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "#3b82f6",
        },
        "nav-link-selected": {"background-color": "#3b82f6"},
    }
)

# Home Page
if selected == "🏠 Home":
    st.markdown("""
    <div class="main-header">
        <h1>🦁 Bring Back the Roar: LMU's GenZ AI Campus Guide</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Your personal AI buddy for everything LMU - from the best food spots to study hacks!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2>🎯 What Makes This Different?</h2>
            <ul>
                <li><strong>First-ever campus AI with GenZ persona</strong> - Not a boring FAQ, but LMU's voice—smart, quick, real</li>
                <li><strong>Built WITH student feedback</strong> - Every feature request, upvote, and meme steers the roadmap</li>
                <li><strong>Waitlist + referral growth loop</strong> - Top sharers get previews, rewards, and "founder's club" status</li>
                <li><strong>Branding and community</strong> - "LMU Roar is back" is easy to meme, photograph, and screenshot for socials</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h2>🚀 What You'll Get</h2>
            <ul>
                <li><strong>Instant Answers:</strong> Best food spots, study locations, weekend events, Greek life tips</li>
                <li><strong>Personalized Experience:</strong> LMU Buddy learns your preferences and campus routine</li>
                <li><strong>Exclusive Access:</strong> Early access to new features and campus insights</li>
                <li><strong>Community Rewards:</strong> Earn points, badges, and recognition for being an early adopter</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Waitlist Counter
        waitlist_data = load_waitlist()
        st.markdown(f"""
        <div class="waitlist-counter">
            <h3>🔥 Join the Movement!</h3>
            <h2 style="color: #3b82f6; font-size: 2rem;">{len(waitlist_data)}</h2>
            <p>students have already joined!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Waitlist Form
        st.markdown("### 📝 Join the Waitlist")
        with st.form("waitlist_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            org = st.text_input("Organization/House (Optional)")
            username = st.text_input("Reserve Username (Optional)")
            feedback = st.text_area("What's the MOST important thing you want this app to do for you/your org?")
            
            submitted = st.form_submit_button("🚀 Join Waitlist")
            
            if submitted and name and email:
                new_entry = {
                    "name": name,
                    "email": email,
                    "org": org,
                    "username": username,
                    "feedback": feedback,
                    "timestamp": datetime.now().isoformat(),
                    "referral_code": f"LMU{len(waitlist_data)+1:04d}"
                }
                waitlist_data.append(new_entry)
                save_waitlist(waitlist_data)
                st.success(f"🎉 Welcome to the LMU family, {name}! You're #{len(waitlist_data)} on the waitlist. Share your unique code: {new_entry['referral_code']}")
                st.session_state.user_name = name
                st.session_state.user_email = email

# LMU Buddy Chat
elif selected == "🤖 LMU Buddy":
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Meet LMU Buddy</h1>
        <p>Your AI campus companion - Ask anything about LMU!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat interface
    st.markdown("### 💬 Chat with LMU Buddy")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask LMU Buddy anything...", key="chat_input")
    
    if st.button("Send", key="send_button") and user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        ai_response = get_lmu_buddy_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
        st.rerun()
    
    # Suggested questions
    st.markdown("### 💡 Try asking about:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍕 Best food on campus?"):
            st.session_state.chat_history.append({"role": "user", "content": "Best food on campus?"})
            ai_response = get_lmu_buddy_response("Best food on campus?")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    with col2:
        if st.button("📚 Best study spots?"):
            st.session_state.chat_history.append({"role": "user", "content": "Best study spots?"})
            ai_response = get_lmu_buddy_response("Best study spots?")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    with col3:
        if st.button("🎉 What's up this weekend?"):
            st.session_state.chat_history.append({"role": "user", "content": "What's up this weekend?"})
            ai_response = get_lmu_buddy_response("What's up this weekend?")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()

# Waitlist Analytics
elif selected == "📊 Waitlist":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Waitlist Analytics</h1>
        <p>Track the growth of the LMU community!</p>
    </div>
    """, unsafe_allow_html=True)
    
    waitlist_data = load_waitlist()
    
    if waitlist_data:
        df = pd.DataFrame(waitlist_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Signups", len(waitlist_data))
        with col2:
            org_count = len([entry for entry in waitlist_data if entry.get('org')])
            st.metric("With Organization", org_count)
        with col3:
            feedback_count = len([entry for entry in waitlist_data if entry.get('feedback')])
            st.metric("With Feedback", feedback_count)
        
        # Growth chart
        df['date'] = df['timestamp'].dt.date
        daily_signups = df.groupby('date').size().reset_index(name='signups')
        daily_signups['cumulative'] = daily_signups['signups'].cumsum()
        
        fig = px.line(daily_signups, x='date', y='cumulative', 
                     title='Waitlist Growth Over Time',
                     labels={'cumulative': 'Total Signups', 'date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent signups
        st.markdown("### Recent Signups")
        recent_data = df.tail(10)[['name', 'email', 'org', 'timestamp']]
        st.dataframe(recent_data, use_container_width=True)
        
        # Feedback analysis
        if feedback_count > 0:
            st.markdown("### 💭 Recent Feedback")
            feedback_entries = [entry for entry in waitlist_data if entry.get('feedback')]
            for entry in feedback_entries[-5:]:
                st.markdown(f"**{entry['name']}:** {entry['feedback']}")
    else:
        st.info("No waitlist data yet. Share the app to start building the community!")

# Analytics Dashboard
elif selected == "📈 Analytics":
    st.markdown("""
    <div class="main-header">
        <h1>📈 Analytics Dashboard</h1>
        <p>Deep insights into user engagement and growth</p>
    </div>
    """, unsafe_allow_html=True)
    
    waitlist_data = load_waitlist()
    
    if waitlist_data:
        df = pd.DataFrame(waitlist_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Engagement metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", len(waitlist_data))
        with col2:
            chat_sessions = len(st.session_state.chat_history) // 2
            st.metric("Chat Sessions", chat_sessions)
        with col3:
            avg_session_length = len(st.session_state.chat_history) / max(chat_sessions, 1)
            st.metric("Avg Session Length", f"{avg_session_length:.1f} messages")
        with col4:
            completion_rate = len([entry for entry in waitlist_data if entry.get('feedback')]) / len(waitlist_data) * 100
            st.metric("Feedback Rate", f"{completion_rate:.1f}%")
        
        # Top organizations
        org_data = [entry.get('org') for entry in waitlist_data if entry.get('org')]
        if org_data:
            org_counts = pd.Series(org_data).value_counts()
            st.markdown("### 🏛️ Top Organizations")
            st.bar_chart(org_counts.head(10))
        
        # Referral tracking
        st.markdown("### 🔗 Referral Performance")
        referral_codes = [entry.get('referral_code') for entry in waitlist_data]
        if len(set(referral_codes)) > 1:
            st.info("Referral tracking will be implemented in the next version!")
    else:
        st.info("Start collecting data by sharing the app with your network!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 10px;">
    <h3>🦁 LMU Campus LLM - Bringing Back the Roar!</h3>
    <p>Built with ❤️ for the LMU community</p>
    <p>Share your unique link and climb the waitlist! #BringBackTheRoar</p>
</div>
""", unsafe_allow_html=True)