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
import requests
import random

class GenZLMUBuddy:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.data = self.load_lmu_data()
        self.embeddings = self.load_or_compute_embeddings()
        self.conversation_history = []
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Gen Z personality traits and responses
        self.genz_traits = {
            "slang": [
                "fr fr", "no cap", "slay", "periodt", "bestie", "literally", "ngl", 
                "lowkey", "highkey", "vibe", "mood", "squad", "flex", "bussin", 
                "cheugy", "stan", "tea", "spill", "main character energy", "it's giving"
            ],
            "emojis": ["😭", "💀", "🔥", "✨", "💅", "😩", "😤", "🤪", "😎", "🥺", "😌", "🤩"],
            "expressions": [
                "omg", "tbh", "imo", "nvm", "idk", "ikr", "ttyl", "brb", "afk",
                "irl", "fomo", "yolo", "fyp", "pov", "ngl", "lowkey", "highkey"
            ]
        }
        
    def load_lmu_data(self):
        """Load enhanced LMU data from JSON file"""
        try:
            with open('enhanced_lmu_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback to original data
            try:
                with open('lmu_data.json', 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
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
            'news': [],
            'athletics': [],
            'academics': [],
            'campus_life': []
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
        
        # Process all data types
        for data_type, items in self.data.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        text = " ".join([str(v) for v in item.values() if v])
                        all_texts.append(text)
                        text_mapping.append((data_type, item))
        
        if all_texts:
            embeddings = self.model.encode(all_texts)
            
            # Save embeddings
            with open('lmu_embeddings.pkl', 'wb') as f:
                pickle.dump((embeddings, text_mapping), f)
            
            return embeddings, text_mapping
        return None, []
    
    def semantic_search(self, query, top_k=3):
        """Perform semantic search on LMU data"""
        if not self.embeddings or not self.embeddings[1]:
            return []
        
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings[0])[0]
        
        # Get top k most similar items
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # Threshold for relevance
                data_type, item = self.embeddings[1][idx]
                results.append({
                    'type': data_type,
                    'item': item,
                    'similarity': similarities[idx]
                })
        
        return results
    
    def call_ollama(self, prompt, model="llama2"):
        """Call Ollama API for response generation"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()['response']
            else:
                return None
        except Exception as e:
            st.error(f"Error calling Ollama: {e}")
            return None
    
    def add_genz_flair(self, text):
        """Add Gen Z personality to responses"""
        # Add random emoji
        if random.random() < 0.3:
            emoji = random.choice(self.genz_traits["emojis"])
            text += f" {emoji}"
        
        # Add random slang
        if random.random() < 0.2:
            slang = random.choice(self.genz_traits["slang"])
            text = f"{slang}, {text}"
        
        # Add expressions
        if random.random() < 0.15:
            expr = random.choice(self.genz_traits["expressions"])
            text = f"{expr} {text}"
        
        return text
    
    def generate_genz_response(self, user_input, context_data):
        """Generate a Gen Z style response using Ollama"""
        
        # Create a Gen Z personality prompt
        genz_prompt = f"""You are a Gen Z college student at Loyola Marymount University (LMU) in Los Angeles. You're friendly, knowledgeable about campus life, and speak like a typical Gen Z student. Use Gen Z slang, emojis, and expressions naturally.

Context about LMU: {context_data}

User question: {user_input}

Respond as a helpful LMU student with Gen Z personality. Keep it casual, friendly, and informative. Use Gen Z expressions like "fr fr", "no cap", "slay", "bestie", etc. naturally. Include relevant emojis. Keep responses conversational and not too long."""

        # Get response from Ollama
        response = self.call_ollama(genz_prompt)
        
        if response:
            # Clean up the response
            response = response.strip()
            # Remove any system-like prefixes
            if response.startswith("Assistant:"):
                response = response[10:].strip()
            
            return response
        else:
            # Fallback response
            return self.generate_fallback_response(user_input, context_data)
    
    def generate_fallback_response(self, user_input, context_data):
        """Generate a fallback response without Ollama"""
        responses = [
            "omg bestie, let me help you with that! 💅",
            "fr fr, I got you covered! ✨",
            "no cap, this is what I know about that! 🔥",
            "slay, here's the tea on that! 💅",
            "literally obsessed with helping you rn! 😌"
        ]
        
        base_response = random.choice(responses)
        
        if context_data:
            return f"{base_response} {context_data}"
        else:
            return f"{base_response} I'm not totally sure about that, but I can help you find out! 🤪"
    
    def get_professor_info(self, query):
        """Get professor information"""
        professors = self.data.get('professors', [])
        for prof in professors:
            if query.lower() in prof.get('name', '').lower():
                return prof
        return None
    
    def get_course_info(self, query):
        """Get course information"""
        courses = self.data.get('courses', [])
        for course in courses:
            if query.lower() in course.get('code', '').lower() or query.lower() in course.get('name', '').lower():
                return course
        return None
    
    def get_upcoming_events(self, days=7):
        """Get upcoming events"""
        events = self.data.get('events', [])
        current_date = datetime.now()
        upcoming = []
        
        for event in events:
            try:
                event_date = datetime.strptime(event.get('date', ''), '%Y-%m-%d')
                if event_date >= current_date and event_date <= current_date + timedelta(days=days):
                    upcoming.append(event)
            except:
                continue
        
        return upcoming
    
    def handle_professor_query(self, query):
        """Handle professor-related queries"""
        prof = self.get_professor_info(query)
        if prof:
            context = f"Professor {prof['name']} teaches {prof['department']} and has a {prof['rating']}/5 rating. They're known for being {', '.join(prof['tags'][:3])}. They teach courses like {', '.join(prof['courses'][:2])}."
            return self.generate_genz_response(query, context)
        else:
            return self.generate_genz_response(query, "I couldn't find that specific professor, but I can help you find other great profs at LMU!")
    
    def handle_course_query(self, query):
        """Handle course-related queries"""
        course = self.get_course_info(query)
        if course:
            context = f"{course['code']} - {course['name']} is a {course['credits']}-credit course in {course['department']}. It's {course['description'][:100]}... and has a {course['rating']}/5 rating."
            return self.generate_genz_response(query, context)
        else:
            return self.generate_genz_response(query, "I couldn't find that specific course, but I can help you explore other courses at LMU!")
    
    def handle_dining_query(self, query):
        """Handle dining-related queries"""
        dining = self.data.get('dining', [])
        if dining:
            context = f"LMU has {len(dining)} dining locations including {', '.join([d['name'] for d in dining[:3]])}. The Lair is our main dining hall and Lion's Den has the best smoothie bowls fr fr!"
            return self.generate_genz_response(query, context)
        else:
            return self.generate_genz_response(query, "We have some amazing dining options on campus! The Lair is literally everything and Lion's Den has the best acai bowls! 💅")
    
    def handle_housing_query(self, query):
        """Handle housing-related queries"""
        housing = self.data.get('housing', [])
        if housing:
            context = f"LMU has {len(housing)} housing options. Freshmen usually live in Del Rey North/South (traditional dorms), while upperclassmen can live in apartment-style housing like Huesman Hall."
            return self.generate_genz_response(query, context)
        else:
            return self.generate_genz_response(query, "Housing at LMU is actually pretty nice! Freshmen get the traditional dorm experience and upperclassmen get apartment-style living. No cap, it's a vibe! ✨")
    
    def handle_event_query(self, query):
        """Handle event-related queries"""
        upcoming = self.get_upcoming_events()
        if upcoming:
            context = f"We have {len(upcoming)} upcoming events! Including {upcoming[0]['name']} on {upcoming[0]['date']} and {upcoming[1]['name'] if len(upcoming) > 1 else 'more fun stuff'}!"
            return self.generate_genz_response(query, context)
        else:
            return self.generate_genz_response(query, "There's always something happening on campus! Check out the student life office or follow LMU social media for the latest events! 🔥")
    
    def handle_organization_query(self, query):
        """Handle organization-related queries"""
        orgs = self.data.get('organizations', [])
        if orgs:
            context = f"LMU has {len(orgs)} major student organizations including Greek Life, Film Society, Service Organization, and more! There's literally something for everyone!"
            return self.generate_genz_response(query, context)
        else:
            return self.generate_genz_response(query, "We have so many amazing clubs and organizations! From Greek life to film society to service clubs, there's something for every vibe! 💅")
    
    def handle_facility_query(self, query):
        """Handle facility-related queries"""
        facilities = self.data.get('facilities', [])
        if facilities:
            context = f"LMU has {len(facilities)} main facilities including the Hannon Library (24/7 during finals!), Burns Fine Arts Center, Gersten Pavilion (basketball!), and Malone Student Center."
            return self.generate_genz_response(query, context)
        else:
            return self.generate_genz_response(query, "Our campus facilities are literally everything! The library is 24/7 during finals (bless), and Gersten is where all the basketball games happen! 🏀")
    
    def handle_athletics_query(self, query):
        """Handle athletics-related queries"""
        athletics = self.data.get('athletics', [])
        if athletics:
            context = f"LMU has {len(athletics)} NCAA Division I teams in the WCC conference! Our basketball teams are literally everything, and we also have soccer, baseball, volleyball, and more!"
            return self.generate_genz_response(query, context)
        else:
            return self.generate_genz_response(query, "LMU athletics are no cap amazing! We're in the WCC conference and our basketball games at Gersten are literally the best vibes! 🏀")
    
    def handle_academics_query(self, query):
        """Handle academics-related queries"""
        academics = self.data.get('academics', [])
        if academics:
            context = f"LMU has {len(academics)} colleges and schools including CBA (Business), CFA (Arts), CLA (Liberal Arts), CSE (Science & Engineering), and SFTV (Film & TV). SFTV is literally world-famous!"
            return self.generate_genz_response(query, context)
        else:
            return self.generate_genz_response(query, "LMU academics are slay! We have amazing programs in business, arts, sciences, and our film school is literally world-famous! ✨")
    
    def generate_response(self, user_input):
        """Generate a response based on user input"""
        # Add to conversation history
        self.conversation_history.append({"user": user_input, "timestamp": datetime.now()})
        
        # Perform semantic search
        search_results = self.semantic_search(user_input)
        
        # Determine the type of query and handle accordingly
        user_input_lower = user_input.lower()
        
        # Check for specific query types
        if any(word in user_input_lower for word in ['professor', 'prof', 'teacher', 'instructor']):
            return self.handle_professor_query(user_input)
        elif any(word in user_input_lower for word in ['course', 'class', 'cs', 'bus', 'psy', 'eng', 'ftv']):
            return self.handle_course_query(user_input)
        elif any(word in user_input_lower for word in ['dining', 'food', 'eat', 'lair', 'lions den', 'coffee']):
            return self.handle_dining_query(user_input)
        elif any(word in user_input_lower for word in ['housing', 'dorm', 'apartment', 'live', 'room']):
            return self.handle_housing_query(user_input)
        elif any(word in user_input_lower for word in ['event', 'activity', 'party', 'fair', 'week']):
            return self.handle_event_query(user_input)
        elif any(word in user_input_lower for word in ['organization', 'club', 'greek', 'society']):
            return self.handle_organization_query(user_input)
        elif any(word in user_input_lower for word in ['facility', 'library', 'gym', 'center', 'building']):
            return self.handle_facility_query(user_input)
        elif any(word in user_input_lower for word in ['athletics', 'sports', 'basketball', 'soccer', 'team']):
            return self.handle_athletics_query(user_input)
        elif any(word in user_input_lower for word in ['academic', 'college', 'school', 'major', 'degree']):
            return self.handle_academics_query(user_input)
        else:
            # General query - use search results for context
            context_data = ""
            if search_results:
                top_result = search_results[0]
                item = top_result['item']
                if isinstance(item, dict):
                    context_data = f"Based on what I know: {str(item)[:200]}..."
            
            return self.generate_genz_response(user_input, context_data)

def create_genz_chat_interface():
    """Create the Gen Z LMU Buddy chat interface"""
    st.set_page_config(
        page_title="Gen Z LMU Buddy",
        page_icon="🦁",
        layout="wide"
    )
    
    st.title("🦁 Gen Z LMU Buddy")
    st.markdown("**Your bestie for all things LMU! Ask me anything about campus life, professors, courses, events, and more!** 💅✨")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'lmu_buddy' not in st.session_state:
        st.session_state.lmu_buddy = GenZLMUBuddy()
    
    # Sidebar with information
    with st.sidebar:
        st.header("📚 Quick Info")
        st.markdown("""
        **What I can help with:**
        - 🎓 Professors & Courses
        - 🍕 Dining & Food
        - 🏠 Housing & Dorms
        - 🎉 Events & Activities
        - 🏀 Athletics & Sports
        - 🏛️ Campus Facilities
        - 👥 Student Organizations
        - 📰 Campus News
        
        **Just ask me anything!** 😌
        """)
        
        # Show some stats
        buddy = st.session_state.lmu_buddy
        st.markdown("**📊 Campus Stats:**")
        st.markdown(f"• {len(buddy.data.get('professors', []))} Professors")
        st.markdown(f"• {len(buddy.data.get('courses', []))} Courses")
        st.markdown(f"• {len(buddy.data.get('dining', []))} Dining Locations")
        st.markdown(f"• {len(buddy.data.get('housing', []))} Housing Options")
        st.markdown(f"• {len(buddy.data.get('organizations', []))} Student Orgs")
        
        # Ollama status
        st.markdown("**🤖 AI Status:**")
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                st.success("✅ Ollama Connected")
            else:
                st.error("❌ Ollama Error")
        except:
            st.warning("⚠️ Ollama Not Running")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about LMU! 💅"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking... 🤔"):
                    response = st.session_state.lmu_buddy.generate_response(prompt)
                st.markdown(response)
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🦁 <strong>Gen Z LMU Buddy</strong> - Your bestie for campus life! | Powered by Ollama & LMU Data</p>
        <p>Ask me about professors, courses, dining, housing, events, and more! fr fr no cap 💅✨</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    create_genz_chat_interface()