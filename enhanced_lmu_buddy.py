import streamlit as st
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class EnhancedLMUBuddy:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.data = self.load_lmu_data()
        self.embeddings = self.load_or_compute_embeddings()
        self.conversation_history = []
        
    def load_lmu_data(self):
        """Load LMU data from JSON file"""
        try:
            with open('lmu_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default data if file doesn't exist
            return self.create_default_data()
    
    def create_default_data(self):
        """Create default LMU data structure"""
        return {
            'professors': [],
            'courses': [],
            'dining': [],
            'housing': [],
            'events': [],
            'organizations': [],
            'facilities': [],
            'news': []
        }
    
    def load_or_compute_embeddings(self):
        """Load pre-computed embeddings or compute new ones"""
        try:
            with open('lmu_embeddings.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return self.compute_embeddings()
    
    def compute_embeddings(self):
        """Compute embeddings for all LMU data"""
        all_texts = []
        text_mapping = []
        
        # Process professors
        for prof in self.data.get('professors', []):
            text = f"{prof.get('name', '')} {prof.get('department', '')} {' '.join(prof.get('tags', []))} {' '.join(prof.get('courses', []))}"
            all_texts.append(text)
            text_mapping.append(('professor', prof))
        
        # Process courses
        for course in self.data.get('courses', []):
            text = f"{course.get('code', '')} {course.get('name', '')} {course.get('department', '')} {course.get('description', '')}"
            all_texts.append(text)
            text_mapping.append(('course', course))
        
        # Process dining
        for dining in self.data.get('dining', []):
            text = f"{dining.get('name', '')} {dining.get('type', '')} {' '.join(dining.get('features', []))} {' '.join(dining.get('popular_items', []))}"
            all_texts.append(text)
            text_mapping.append(('dining', dining))
        
        # Process housing
        for housing in self.data.get('housing', []):
            text = f"{housing.get('name', '')} {housing.get('type', '')} {' '.join(housing.get('features', []))} {' '.join(housing.get('pros', []))}"
            all_texts.append(text)
            text_mapping.append(('housing', housing))
        
        # Process events
        for event in self.data.get('events', []):
            text = f"{event.get('name', '')} {event.get('type', '')} {event.get('description', '')} {event.get('location', '')}"
            all_texts.append(text)
            text_mapping.append(('event', event))
        
        # Process organizations
        for org in self.data.get('organizations', []):
            text = f"{org.get('name', '')} {org.get('type', '')} {org.get('description', '')} {' '.join(org.get('events', []))}"
            all_texts.append(text)
            text_mapping.append(('organization', org))
        
        # Process facilities
        for facility in self.data.get('facilities', []):
            text = f"{facility.get('name', '')} {facility.get('type', '')} {' '.join(facility.get('features', []))} {' '.join(facility.get('popular_spots', []))}"
            all_texts.append(text)
            text_mapping.append(('facility', facility))
        
        if all_texts:
            embeddings = self.model.encode(all_texts)
            
            # Save embeddings
            with open('lmu_embeddings.pkl', 'wb') as f:
                pickle.dump((embeddings, text_mapping), f)
            
            return embeddings, text_mapping
        else:
            return np.array([]), []
    
    def semantic_search(self, query, top_k=3):
        """Perform semantic search on LMU data"""
        if not self.embeddings[0].size:
            return []
        
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings[0])[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # Threshold for relevance
                category, data = self.embeddings[1][idx]
                results.append({
                    'category': category,
                    'data': data,
                    'similarity': similarities[idx]
                })
        
        return results
    
    def get_professor_info(self, query):
        """Get specific professor information"""
        query_lower = query.lower()
        
        for prof in self.data.get('professors', []):
            if prof['name'].lower() in query_lower or any(course.lower() in query_lower for course in prof.get('courses', [])):
                return prof
        
        return None
    
    def get_course_info(self, query):
        """Get specific course information"""
        query_lower = query.lower()
        
        for course in self.data.get('courses', []):
            if course['code'].lower() in query_lower or course['name'].lower() in query_lower:
                return course
        
        return None
    
    def get_upcoming_events(self, days=7):
        """Get upcoming events within specified days"""
        today = datetime.now()
        upcoming = []
        
        for event in self.data.get('events', []):
            try:
                event_date = datetime.strptime(event['date'], '%Y-%m-%d')
                if event_date >= today and event_date <= today + timedelta(days=days):
                    upcoming.append(event)
            except:
                continue
        
        return sorted(upcoming, key=lambda x: x['date'])
    
    def generate_response(self, user_input):
        """Generate intelligent response based on user input"""
        user_input_lower = user_input.lower()
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Check for specific query types
        if any(word in user_input_lower for word in ['professor', 'teacher', 'instructor']):
            return self.handle_professor_query(user_input)
        elif any(word in user_input_lower for word in ['course', 'class', 'subject']):
            return self.handle_course_query(user_input)
        elif any(word in user_input_lower for word in ['food', 'eat', 'dining', 'restaurant']):
            return self.handle_dining_query(user_input)
        elif any(word in user_input_lower for word in ['housing', 'dorm', 'apartment', 'live']):
            return self.handle_housing_query(user_input)
        elif any(word in user_input_lower for word in ['event', 'activity', 'weekend', 'party']):
            return self.handle_event_query(user_input)
        elif any(word in user_input_lower for word in ['organization', 'club', 'greek', 'sorority', 'fraternity']):
            return self.handle_organization_query(user_input)
        elif any(word in user_input_lower for word in ['facility', 'library', 'study', 'gym']):
            return self.handle_facility_query(user_input)
        elif any(word in user_input_lower for word in ['news', 'announcement', 'update']):
            return self.handle_news_query(user_input)
        else:
            return self.handle_general_query(user_input)
    
    def handle_professor_query(self, query):
        """Handle professor-related queries"""
        prof_info = self.get_professor_info(query)
        if prof_info:
            response = f"👨‍🏫 **{prof_info['name']}** ({prof_info['department']})\n\n"
            response += f"⭐ Rating: {prof_info['rating']}/5.0\n"
            response += f"📊 Difficulty: {prof_info['difficulty']}/5.0\n"
            response += f"💬 Reviews: {prof_info['reviews']}\n\n"
            response += f"🏷️ Tags: {', '.join(prof_info['tags'])}\n"
            response += f"📚 Courses: {', '.join(prof_info['courses'])}\n\n"
            response += "💡 Pro tip: Check Rate My Professor for detailed reviews and student experiences! 🦁"
            return response
        
        # Search for professors by department or other criteria
        search_results = self.semantic_search(query, top_k=3)
        if search_results:
            response = "🔍 Here are some professors that might match your query:\n\n"
            for result in search_results:
                if result['category'] == 'professor':
                    prof = result['data']
                    response += f"• **{prof['name']}** ({prof['department']}) - Rating: {prof['rating']}/5.0\n"
            response += "\n💡 Try asking about a specific professor by name!"
            return response
        
        return "🤔 I couldn't find specific professor information for that query. Try asking about a particular professor by name, or ask about courses in a specific department! 📚"
    
    def handle_course_query(self, query):
        """Handle course-related queries"""
        course_info = self.get_course_info(query)
        if course_info:
            response = f"📚 **{course_info['code']}: {course_info['name']}**\n\n"
            response += f"🏫 Department: {course_info['department']}\n"
            response += f"📝 Credits: {course_info['credits']}\n"
            response += f"⭐ Rating: {course_info['rating']}/5.0\n\n"
            response += f"📖 Description: {course_info['description']}\n\n"
            response += f"👨‍🏫 Professors: {', '.join(course_info['professors'])}\n"
            response += f"📋 Prerequisites: {course_info['prerequisites']}\n\n"
            response += "💡 Pro tip: Check the course catalog for current availability and schedules! 🦁"
            return response
        
        # Search for courses by department or topic
        search_results = self.semantic_search(query, top_k=3)
        if search_results:
            response = "🔍 Here are some courses that might interest you:\n\n"
            for result in search_results:
                if result['category'] == 'course':
                    course = result['data']
                    response += f"• **{course['code']}**: {course['name']} ({course['department']})\n"
            response += "\n💡 Ask about a specific course code for more details!"
            return response
        
        return "🤔 I couldn't find specific course information for that query. Try asking about a particular course code (like 'CS 150') or department! 📚"
    
    def handle_dining_query(self, query):
        """Handle dining-related queries"""
        search_results = self.semantic_search(query, top_k=3)
        
        if search_results:
            response = "🍕 Here are the best dining options on campus:\n\n"
            for result in search_results:
                if result['category'] == 'dining':
                    dining = result['data']
                    response += f"🏪 **{dining['name']}** ({dining['type']})\n"
                    response += f"🕐 Hours: {dining['hours']}\n"
                    response += f"⭐ Rating: {dining['rating']}/5.0\n"
                    response += f"🍽️ Popular: {', '.join(dining['popular_items'][:3])}\n"
                    response += f"✨ Features: {', '.join(dining['features'][:2])}\n\n"
            
            response += "💡 Pro tip: The Lair is always a safe bet for variety, and Lion's Den has the best smoothie bowls! 🦁"
            return response
        
        return "🍕 The best food spots on campus? Hands down, it's the Lair! Their pizza is legendary, and the smoothie bowls at the Lion's Den are perfect for those early morning classes. Pro tip: avoid the rush by going 15 minutes before the lunch crowd hits! 🦁"
    
    def handle_housing_query(self, query):
        """Handle housing-related queries"""
        search_results = self.semantic_search(query, top_k=3)
        
        if search_results:
            response = "🏠 Here's what you need to know about LMU housing:\n\n"
            for result in search_results:
                if result['category'] == 'housing':
                    housing = result['data']
                    response += f"🏢 **{housing['name']}** ({housing['type']})\n"
                    response += f"👥 Capacity: {housing['capacity']} students\n"
                    response += f"✅ Pros: {', '.join(housing['pros'][:2])}\n"
                    response += f"❌ Cons: {', '.join(housing['cons'][:2])}\n\n"
            
            response += "💡 Pro tip: Freshman year dorms are great for meeting people, but upperclassman apartments offer more privacy! 🦁"
            return response
        
        return "🏠 Housing situation? Freshman year you're guaranteed a spot in the dorms, which is actually pretty fun for meeting people! Upperclassmen can upgrade to apartments or themed housing. Greek housing is also an option if you're into that scene! 🏘️"
    
    def handle_event_query(self, query):
        """Handle event-related queries"""
        upcoming_events = self.get_upcoming_events(14)  # Next 2 weeks
        
        if upcoming_events:
            response = "🎉 Here's what's happening soon at LMU:\n\n"
            for event in upcoming_events[:5]:  # Show top 5
                response += f"📅 **{event['name']}**\n"
                response += f"📅 Date: {event['date']} at {event['time']}\n"
                response += f"📍 Location: {event['location']}\n"
                response += f"🎯 Type: {event['type']}\n"
                response += f"📝 {event['description']}\n\n"
            
            response += "💡 Pro tip: Follow @lmu_events on Instagram for real-time updates! 🦁"
            return response
        
        return "🎉 This weekend? Check out the LMU events calendar! There's always something happening - from Greek life mixers to cultural events. Plus, the farmers market on Sundays is a vibe. Don't forget to follow @lmu_events on Instagram for the latest! 🎊"
    
    def handle_organization_query(self, query):
        """Handle organization-related queries"""
        search_results = self.semantic_search(query, top_k=3)
        
        if search_results:
            response = "🏛️ Here are some great organizations to check out:\n\n"
            for result in search_results:
                if result['category'] == 'organization':
                    org = result['data']
                    response += f"👥 **{org['name']}** ({org['type']})\n"
                    response += f"👤 Members: {org['members']}\n"
                    response += f"📝 {org['description']}\n"
                    response += f"🎉 Events: {', '.join(org['events'][:3])}\n\n"
            
            response += "💡 Pro tip: Greek Life is huge here, but there are over 150 clubs to choose from! 🦁"
            return response
        
        return "🏛️ Greek Life hacks? Rush season is intense but so worth it! Go to as many events as possible, be yourself, and don't stress about the perfect outfit. The connections you make last way beyond college. Plus, the parties are epic! 🎭"
    
    def handle_facility_query(self, query):
        """Handle facility-related queries"""
        search_results = self.semantic_search(query, top_k=3)
        
        if search_results:
            response = "🏢 Here are the best facilities on campus:\n\n"
            for result in search_results:
                if result['category'] == 'facility':
                    facility = result['data']
                    response += f"🏛️ **{facility['name']}** ({facility['type']})\n"
                    response += f"🕐 Hours: {facility['hours']}\n"
                    response += f"✨ Features: {', '.join(facility['features'][:3])}\n"
                    response += f"⭐ Popular spots: {', '.join(facility['popular_spots'][:2])}\n\n"
            
            response += "💡 Pro tip: The Hannon Library is clutch for studying, especially the quiet zones on the 3rd floor! 🦁"
            return response
        
        return "📚 Best study spots? The Hannon Library is clutch, especially the quiet zones on the 3rd floor. But my secret spot? The rooftop of the Burns Fine Arts Center - amazing views and usually pretty quiet! Perfect for those late-night cram sessions. ✨"
    
    def handle_news_query(self, query):
        """Handle news-related queries"""
        recent_news = self.data.get('news', [])[:3]  # Latest 3 news items
        
        if recent_news:
            response = "📰 Here's the latest LMU news:\n\n"
            for news in recent_news:
                response += f"📅 **{news['title']}**\n"
                response += f"📅 Date: {news['date']}\n"
                response += f"🏷️ Category: {news['category']}\n"
                response += f"📝 {news['summary']}\n\n"
            
            response += "💡 Pro tip: Check the LMU website for the most up-to-date news and announcements! 🦁"
            return response
        
        return "📰 LMU is always making headlines! From academic achievements to campus developments, there's always something exciting happening. Check out the official LMU news website for the latest updates! 🦁"
    
    def handle_general_query(self, query):
        """Handle general queries with semantic search"""
        search_results = self.semantic_search(query, top_k=2)
        
        if search_results:
            # Use the most relevant result
            best_result = search_results[0]
            category = best_result['category']
            data = best_result['data']
            
            if category == 'professor':
                return self.handle_professor_query(query)
            elif category == 'course':
                return self.handle_course_query(query)
            elif category == 'dining':
                return self.handle_dining_query(query)
            elif category == 'housing':
                return self.handle_housing_query(query)
            elif category == 'event':
                return self.handle_event_query(query)
            elif category == 'organization':
                return self.handle_organization_query(query)
            elif category == 'facility':
                return self.handle_facility_query(query)
        
        # Default response with conversation memory
        if len(self.conversation_history) > 2:
            return "🤔 That's a great question! As your LMU Buddy, I'm here to help with everything campus-related. Try asking me about professors, courses, food spots, study locations, weekend events, Greek life, or parking tips! I'm constantly learning more about our amazing campus. 🦁✨"
        else:
            return "👋 Hey! I'm your LMU Buddy - your AI campus companion! I can help you with everything from finding the best professors and courses to discovering great food spots and upcoming events. What would you like to know about LMU? 🦁✨"

def create_enhanced_chat_interface():
    """Create the enhanced chat interface"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Enhanced LMU Buddy - Your AI Campus Companion</h1>
        <p>Powered by advanced AI with comprehensive LMU knowledge!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Enhanced LMU Buddy
    if 'enhanced_lmu_buddy' not in st.session_state:
        with st.spinner("Loading LMU Buddy... This may take a moment on first run."):
            st.session_state.enhanced_lmu_buddy = EnhancedLMUBuddy()
    
    # Chat interface
    st.markdown("### 💬 Chat with Enhanced LMU Buddy")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask Enhanced LMU Buddy anything...", key="enhanced_chat_input")
    
    if st.button("Send", key="enhanced_send_button") and user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("LMU Buddy is thinking..."):
            ai_response = st.session_state.enhanced_lmu_buddy.generate_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
        st.rerun()
    
    # Quick access buttons
    st.markdown("### 🚀 Quick Access")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📚 Academic**")
        if st.button("Find Professors", key="find_professors"):
            st.session_state.chat_history.append({"role": "user", "content": "Show me some good professors"})
            ai_response = st.session_state.enhanced_lmu_buddy.generate_response("Show me some good professors")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
        
        if st.button("Popular Courses", key="popular_courses"):
            st.session_state.chat_history.append({"role": "user", "content": "What are some popular courses?"})
            ai_response = st.session_state.enhanced_lmu_buddy.generate_response("What are some popular courses?")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    with col2:
        st.markdown("**🎉 Campus Life**")
        if st.button("Upcoming Events", key="upcoming_events"):
            st.session_state.chat_history.append({"role": "user", "content": "What events are coming up?"})
            ai_response = st.session_state.enhanced_lmu_buddy.generate_response("What events are coming up?")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
        
        if st.button("Best Food Spots", key="best_food"):
            st.session_state.chat_history.append({"role": "user", "content": "Where should I eat on campus?"})
            ai_response = st.session_state.enhanced_lmu_buddy.generate_response("Where should I eat on campus?")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    # Data insights
    st.markdown("### 📊 LMU Data Insights")
    
    buddy = st.session_state.enhanced_lmu_buddy
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Professors", len(buddy.data.get('professors', [])))
    with col2:
        st.metric("Courses", len(buddy.data.get('courses', [])))
    with col3:
        st.metric("Dining Options", len(buddy.data.get('dining', [])))
    with col4:
        st.metric("Organizations", len(buddy.data.get('organizations', [])))
    
    # Feedback system
    st.markdown("### 👍 How was your experience?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👍 Great!", key="feedback_great"):
            st.success("Thanks! LMU Buddy is learning and improving! 🦁")
    with col2:
        if st.button("👎 Could be better", key="feedback_better"):
            st.info("Thanks for the feedback! We're constantly working to improve.")
    with col3:
        if st.button("🔄 Clear Chat", key="clear_enhanced_chat"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    create_enhanced_chat_interface()