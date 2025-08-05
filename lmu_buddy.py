import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class LMUBuddy:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = self.load_knowledge_base()
        self.embeddings = self.load_embeddings()
        
    def load_knowledge_base(self):
        """Load LMU-specific knowledge base"""
        knowledge = {
            "campus_life": [
                "LMU is located in Los Angeles, California with a beautiful campus overlooking the Pacific Ocean",
                "The university has approximately 9,000 students with a strong focus on liberal arts education",
                "LMU's mascot is the Lion and the school colors are blue and white",
                "The campus is known for its stunning architecture and ocean views",
                "LMU has a strong commitment to social justice and community service"
            ],
            "dining": [
                "The Lair is the main dining hall on campus, known for its variety of food options",
                "Lion's Den offers smoothie bowls, coffee, and quick snacks",
                "The Coffee Bean & Tea Leaf is located in the library for study breaks",
                "Food trucks often visit campus during lunch hours",
                "The dining plan includes meal swipes and dining dollars"
            ],
            "academics": [
                "The Hannon Library is the main study space with multiple floors and quiet zones",
                "LMU offers over 60 majors and minors across various disciplines",
                "The university has a strong film school and business program",
                "Study abroad programs are available in over 50 countries",
                "Academic advising is available through the Academic Resource Center"
            ],
            "housing": [
                "Freshman housing is guaranteed and includes traditional dorms",
                "Upperclassmen can live in apartments or themed housing",
                "Greek housing is available for members of fraternities and sororities",
                "Off-campus housing options are available in nearby neighborhoods",
                "Residence Life provides programming and support for on-campus students"
            ],
            "activities": [
                "LMU has over 150 student organizations and clubs",
                "Greek life includes multiple fraternities and sororities",
                "Intramural sports are popular and include basketball, soccer, and volleyball",
                "The campus hosts regular events like concerts, speakers, and cultural celebrations",
                "Service opportunities are available through the Center for Service and Action"
            ],
            "transportation": [
                "Parking on campus requires a permit and can be challenging during peak hours",
                "The Playa Vista shuttle runs every 15 minutes and is free with student ID",
                "Public transportation options include Metro buses and trains",
                "Bike racks are available throughout campus",
                "Ride-sharing services like Uber and Lyft are popular for off-campus trips"
            ],
            "weekend_activities": [
                "Weekend events include Greek mixers, cultural celebrations, and athletic games",
                "The farmers market on Sundays is popular for fresh produce and local goods",
                "Nearby Venice Beach and Santa Monica offer shopping and entertainment",
                "Downtown LA is accessible via public transportation for concerts and events",
                "Campus organizations host regular weekend programming and social events"
            ]
        }
        return knowledge
    
    def load_embeddings(self):
        """Load pre-computed embeddings for knowledge base"""
        try:
            with open('embeddings.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return self.compute_embeddings()
    
    def compute_embeddings(self):
        """Compute embeddings for knowledge base"""
        all_texts = []
        for category, texts in self.knowledge_base.items():
            all_texts.extend(texts)
        
        embeddings = self.model.encode(all_texts)
        
        with open('embeddings.pkl', 'wb') as f:
            pickle.dump(embeddings, f)
        
        return embeddings
    
    def get_relevant_context(self, query, top_k=3):
        """Get most relevant context for a query"""
        query_embedding = self.model.encode([query])
        
        all_texts = []
        for category, texts in self.knowledge_base.items():
            all_texts.extend(texts)
        
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        relevant_context = [all_texts[i] for i in top_indices]
        return relevant_context
    
    def generate_response(self, user_input):
        """Generate contextual response based on user input"""
        user_input_lower = user_input.lower()
        
        # Get relevant context
        context = self.get_relevant_context(user_input)
        
        # Pre-defined responses with GenZ personality
        responses = {
            "food": {
                "context": "Based on campus dining info:",
                "response": "🍕 The best food spots on campus? Hands down, it's the Lair! Their pizza is legendary, and the smoothie bowls at the Lion's Den are perfect for those early morning classes. Pro tip: avoid the rush by going 15 minutes before the lunch crowd hits! 🦁"
            },
            "study": {
                "context": "From academic resources:",
                "response": "📚 Best study spots? The Hannon Library is clutch, especially the quiet zones on the 3rd floor. But my secret spot? The rooftop of the Burns Fine Arts Center - amazing views and usually pretty quiet! Perfect for those late-night cram sessions. ✨"
            },
            "weekend": {
                "context": "Weekend activities include:",
                "response": "🎉 This weekend? Check out the LMU events calendar! There's always something happening - from Greek life mixers to cultural events. Plus, the farmers market on Sundays is a vibe. Don't forget to follow @lmu_events on Instagram for the latest! 🎊"
            },
            "greek": {
                "context": "Greek life at LMU:",
                "response": "🏛️ Greek Life hacks? Rush season is intense but so worth it! Go to as many events as possible, be yourself, and don't stress about the perfect outfit. The connections you make last way beyond college. Plus, the parties are epic! 🎭"
            },
            "parking": {
                "context": "Transportation info:",
                "response": "🚗 Parking drama? Yeah, it's real. Get there early (like 8 AM early) or park at the Playa Vista shuttle lot. The shuttle runs every 15 minutes and it's free with your student ID. Saves you from the parking ticket stress! 🎫"
            },
            "housing": {
                "context": "Housing options:",
                "response": "🏠 Housing situation? Freshman year you're guaranteed a spot in the dorms, which is actually pretty fun for meeting people! Upperclassmen can upgrade to apartments or themed housing. Greek housing is also an option if you're into that scene! 🏘️"
            },
            "activities": {
                "context": "Campus activities:",
                "response": "🎯 Campus activities? There are over 150 clubs and orgs to choose from! Whether you're into sports, culture, service, or just hanging out, there's something for everyone. Intramural sports are super popular too - great way to stay active and meet people! 🏀"
            }
        }
        
        # Determine response type
        if any(word in user_input_lower for word in ['food', 'eat', 'restaurant', 'dining', 'lair', 'lions den']):
            return responses["food"]["response"]
        elif any(word in user_input_lower for word in ['study', 'library', 'quiet', 'spot', 'academic']):
            return responses["study"]["response"]
        elif any(word in user_input_lower for word in ['weekend', 'party', 'event', 'fun', 'activity']):
            return responses["weekend"]["response"]
        elif any(word in user_input_lower for word in ['greek', 'sorority', 'fraternity', 'rush']):
            return responses["greek"]["response"]
        elif any(word in user_input_lower for word in ['parking', 'car', 'shuttle', 'transport']):
            return responses["parking"]["response"]
        elif any(word in user_input_lower for word in ['housing', 'dorm', 'apartment', 'live']):
            return responses["housing"]["response"]
        elif any(word in user_input_lower for word in ['club', 'organization', 'activity', 'join']):
            return responses["activities"]["response"]
        else:
            # Generate contextual response using knowledge base
            context_str = " ".join(context[:2])
            return f"🤔 That's a great question! Based on what I know about LMU: {context_str} As your LMU Buddy, I'm here to help with everything campus-related. Try asking me about food spots, study locations, weekend events, Greek life, or parking tips! I'm constantly learning more about our amazing campus. 🦁✨"

def create_advanced_chat_interface():
    """Create advanced chat interface with LMU Buddy"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Meet LMU Buddy - Your AI Campus Companion</h1>
        <p>Powered by advanced AI with deep LMU knowledge!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize LMU Buddy
    if 'lmu_buddy' not in st.session_state:
        st.session_state.lmu_buddy = LMUBuddy()
    
    # Chat interface
    st.markdown("### 💬 Chat with LMU Buddy")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask LMU Buddy anything...", key="advanced_chat_input")
    
    if st.button("Send", key="advanced_send_button") and user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        ai_response = st.session_state.lmu_buddy.generate_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
        st.rerun()
    
    # Suggested questions with categories
    st.markdown("### 💡 Quick Questions by Category")
    
    categories = {
        "🍕 Food & Dining": ["Best food on campus?", "What's good at the Lair?", "Coffee spots near library?"],
        "📚 Academics": ["Best study spots?", "Library hours?", "Academic resources?"],
        "🎉 Social Life": ["What's up this weekend?", "Greek life tips?", "Campus activities?"],
        "🏠 Campus Life": ["Housing options?", "Parking tips?", "Transportation?"]
    }
    
    for category, questions in categories.items():
        st.markdown(f"**{category}**")
        cols = st.columns(len(questions))
        for i, question in enumerate(questions):
            with cols[i]:
                if st.button(question, key=f"q_{category}_{i}"):
                    st.session_state.chat_history.append({"role": "user", "content": question})
                    ai_response = st.session_state.lmu_buddy.generate_response(question)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                    st.rerun()
    
    # Feedback system
    st.markdown("### 👍 Was this helpful?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👍 Helpful", key="feedback_helpful"):
            st.success("Thanks for the feedback! LMU Buddy is learning and improving! 🦁")
    with col2:
        if st.button("👎 Not Helpful", key="feedback_not_helpful"):
            st.info("Thanks for letting us know! We'll work on improving that response.")
    with col3:
        if st.button("🔄 Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    create_advanced_chat_interface()