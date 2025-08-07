#!/usr/bin/env python3
"""
Quick test for LMU Buddy integration
"""

import requests
import json

def test_lmu_buddy():
    """Test LMU Buddy with base model"""
    
    # LMU Buddy system prompt
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
        "Where can I study?"
    ]
    
    print("🦁 Testing LMU Buddy Integration")
    print("=" * 40)
    
    for prompt in test_prompts:
        print(f"\n📝 Prompt: {prompt}")
        
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
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_lmu_buddy()