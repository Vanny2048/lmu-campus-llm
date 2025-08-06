#!/usr/bin/env python3
"""
Create LMU Buddy model using Ollama API
"""

import requests
import json
import time

def create_lmu_buddy_model():
    """Create LMU Buddy model using Ollama API"""
    
    # Check if Ollama is running
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code != 200:
            print("❌ Ollama service is not running")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return False
    
    # Create a simple model using the base model with system prompt
    print("🦁 Creating LMU Buddy model...")
    
    # First, let's test if we can use the base model directly
    test_prompt = "You are LMU Buddy, a friendly AI assistant for LMU students. Where should I eat on campus?"
    
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama2:7b",
                "prompt": test_prompt,
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Base model test successful!")
            print(f"Response: {result.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ Base model test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing base model: {e}")
        return False

def test_lmu_buddy_responses():
    """Test LMU Buddy style responses"""
    
    print("\n🧪 Testing LMU Buddy responses...")
    
    # Define system prompt for LMU Buddy
    system_prompt = """You are LMU Buddy, a friendly and helpful AI assistant for Loyola Marymount University students. You have a casual, relatable personality with these characteristics:

- Use casual, student-friendly language with emojis and slang
- Be specific about LMU locations, events, and campus life
- Provide personalized, contextual responses
- Show personality and humor while being helpful
- Use LMU-specific references and insider knowledge
- Be interactive and engaging
- Collect feedback and ratings
- Suggest relevant campus resources and events

Key LMU locations you know:
- The Bluff (scenic dining with sunset views)
- The Lair (quick dining option)
- Lion's Den (coffee spot)
- University Hall (UHall)
- Doolan Hall
- Hilton Center
- Howard B. Fitzpatrick Pavilion
- Alumni Mall
- Lawton Plaza
- Career Center
- Library (3rd floor study spots)
- C-store (convenience store)

Always respond in a helpful, engaging way that reflects LMU campus culture and student life."""
    
    test_prompts = [
        "Where should I eat on campus?",
        "What's a good coffee spot?",
        "Where can I study?",
        "Tell me a fun fact about LMU"
    ]
    
    for prompt in test_prompts:
        print(f"\n📝 Testing: {prompt}")
        
        # Combine system prompt with user prompt
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        
        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    "model": "llama2:7b",
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                print(f"🤖 Response: {response_text}")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🦁 LMU Buddy Model Creation via API")
    print("=" * 50)
    
    # Test base model
    if not create_lmu_buddy_model():
        print("❌ Cannot proceed without base model")
        return
    
    # Test LMU Buddy responses
    test_lmu_buddy_responses()
    
    print("\n" + "🎉" * 20)
    print("🎉 LMU Buddy is ready to use! 🎉")
    print("🎉" * 20)
    print("\nTo use LMU Buddy in your Streamlit app:")
    print("1. The lmu_buddy_ollama_client.py will use the base model with system prompts")
    print("2. This provides the LMU Buddy personality without needing a custom model")
    print("3. You can still create a custom model later when Ollama Modelfile issues are resolved")

if __name__ == "__main__":
    main()