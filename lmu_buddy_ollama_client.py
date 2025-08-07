#!/usr/bin/env python3
"""
LMU Buddy Ollama Client
Integration script for using the fine-tuned Ollama model with the Streamlit app
"""

import subprocess
import json
import logging
from typing import Dict, Any, Optional, List
import time
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LMUBuddyOllamaClient:
    def __init__(self, model_name: str = "lmu-buddy", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        
    def check_model_availability(self) -> bool:
        """Check if the fine-tuned model is available"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                models = result.stdout
                return self.model_name in models
            return False
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False
    
    def get_response_via_cli(self, prompt: str, timeout: int = 30) -> Optional[str]:
        """Get response using Ollama CLI"""
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"CLI error: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout getting response for prompt: {prompt}")
            return None
        except Exception as e:
            logger.error(f"Error getting response via CLI: {e}")
            return None
    
    def get_response_via_api_with_system_prompt(self, prompt: str, timeout: int = 30) -> Optional[str]:
        """Get response using Ollama API with LMU Buddy system prompt"""
        try:
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
            
            # Combine system prompt with user prompt
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
            
            payload = {
                "model": "llama2:7b",  # Use base model
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(
                f"{self.api_url}/generate",
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"API timeout for prompt: {prompt}")
            return None
        except Exception as e:
            logger.error(f"Error getting response via API: {e}")
            return None

    def get_response_via_cli_with_system_prompt(self, prompt: str, timeout: int = 30) -> Optional[str]:
        """Get response using Ollama CLI with LMU Buddy system prompt"""
        try:
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
            
            # Combine system prompt with user prompt
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
            
            result = subprocess.run(
                ['ollama', 'run', 'llama2:7b', full_prompt],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"CLI error: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout getting response for prompt: {prompt}")
            return None
        except Exception as e:
            logger.error(f"Error getting response via CLI: {e}")
            return None
    
    def get_response(self, prompt: str, use_api: bool = True, timeout: int = 30) -> Optional[str]:
        """Get response from the base model with LMU Buddy system prompt"""
        # Use the base model with system prompt instead of custom model
        if use_api:
            return self.get_response_via_api_with_system_prompt(prompt, timeout)
        else:
            return self.get_response_via_cli_with_system_prompt(prompt, timeout)
    
    def get_enhanced_response(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Get enhanced response with context and fallback logic"""
        
        # Try to get response from fine-tuned model
        response = self.get_response(user_input)
        
        if response:
            return response
        
        # Fallback to basic responses if model is not available
        fallback_responses = {
            "hi": "Hey! Welcome to LMU Buddy! 🦁 How can I help you today?",
            "hello": "What's up! Ready to explore LMU?",
            "help": "I can help you with campus info, food spots, study locations, and more! Just ask away!",
            "food": "The Bluff has amazing sunset views, The Lair is great for quick meals, and Lion's Den has the best coffee!",
            "study": "Library 3rd floor is quiet, UHall balcony has fresh air, or try the Lion's Den for a caffeine boost!",
            "coffee": "Lion's Den is the spot! Great coffee and vibes.",
            "events": "Check out the LMU events calendar or ask me about specific events!",
            "parking": "Parking can be tricky! Get here early or prepare for a walk from overflow lots.",
            "weather": "LA weather is pretty much perfect year-round, but bring a jacket for those windy bluff nights!"
        }
        
        # Simple keyword matching for fallback
        user_input_lower = user_input.lower()
        for keyword, fallback_response in fallback_responses.items():
            if keyword in user_input_lower:
                return fallback_response
        
        return "I'm still learning about that! But I can help with campus food, study spots, events, and more. What would you like to know?"

def integrate_with_streamlit():
    """Integration function for Streamlit app"""
    
    # Initialize the client
    client = LMUBuddyOllamaClient()
    
    # Test the integration
    test_prompts = [
        "Where should I eat on campus?",
        "What's a good coffee spot?",
        "Where can I study?",
        "Tell me a fun fact about LMU"
    ]
    
    print("Testing LMU Buddy Ollama Integration...")
    print("=" * 50)
    
    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        response = client.get_enhanced_response(prompt)
        print(f"Response: {response}")
        print("-" * 30)
    
    return client

# Example usage for Streamlit integration
def get_lmu_buddy_response_for_streamlit(user_input: str, user_context: Dict[str, Any] = None) -> str:
    """
    Function to be used in your Streamlit app
    Replace the existing get_lmu_buddy_response function with this
    """
    client = LMUBuddyOllamaClient()
    return client.get_enhanced_response(user_input, user_context)

if __name__ == "__main__":
    # Test the integration
    client = integrate_with_streamlit()
    
    # Interactive testing
    print("\n" + "=" * 50)
    print("Interactive Testing Mode")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        response = client.get_enhanced_response(user_input)
        print(f"LMU Buddy: {response}")