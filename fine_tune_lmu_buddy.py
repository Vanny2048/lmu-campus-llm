#!/usr/bin/env python3
"""
LMU Buddy Fine-tuning Script
Fine-tunes an Ollama model with LMU-specific conversational data
"""

import json
import os
import subprocess
import sys
from typing import List, Dict, Any
import logging
from datetime import datetime
import requests
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LMUBuddyFineTuner:
    def __init__(self, base_model: str = "llama2:7b", model_name: str = "lmu-buddy"):
        self.base_model = base_model
        self.model_name = model_name
        self.training_data = []
        self.system_prompt = self._get_system_prompt()
        
    def _get_system_prompt(self) -> str:
        """Define the system prompt for LMU Buddy personality"""
        return """You are LMU Buddy, a friendly and helpful AI assistant for Loyola Marymount University students. You have a casual, relatable personality with these characteristics:

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

    def create_training_data(self) -> List[Dict[str, Any]]:
        """Create training data from the provided conversational examples"""
        
        # Define the training conversations
        conversations = [
            # 1. Avoid Repetitive/Static Responses
            {
                "prompt": "Where should I eat on campus?",
                "responses": [
                    "Depends. Want cheap, vegan, or sunset vibes? Bluff = scenic, Lair = speed-run.",
                    "If you're post-class hungry, The Lair hits. But if you're tryna vibe with a view? Bluff, always.",
                    "Are we talking snack or full meal? Red Mango for sweet. Lair if you're in a rush.",
                    "Still deciding? Vegan = Iggy's. Views = Bluff. Broke? C-store microwave roulette.",
                    "How hungry are we talking? The Lair if you're late to class, The Bluff if you're early to life."
                ]
            },
            
            # 2. Deepen Personalization & Context
            {
                "prompt": "What's a good coffee spot?",
                "response": "Morning grind? Lion's Den. Late night hustle? Starbucks at the bookstore (don't expect miracles)."
            },
            {
                "prompt": "Where can I get food?",
                "response": "Hey Vanessa! You asked about sweets last time—how about Red Mango near the bookstore?"
            },
            {
                "prompt": "Where can I study near the business school?",
                "response": "If it's sunny, the UHall balcony slaps. Rainy? Try the quiet room in the library basement."
            },
            {
                "prompt": "What's open late?",
                "response": "Late-night = vending machines and bad choices. But the on-campus 24hr lounge has snacks & vibes."
            },
            
            # 3. Interactive Event Actions
            {
                "prompt": "What events are happening this week?",
                "response": "Greek Life Rush on Thursday at 7pm by Alumni Mall. Want a reminder or should I add it to your Google Cal?"
            },
            {
                "prompt": "Any career events soon?",
                "response": "Resume Bootcamp, Friday at 4pm @ Career Center. Want me to ping you day-of?"
            },
            {
                "prompt": "What's happening today?",
                "response": "Today: Sunset Yoga at 5pm on Lawton Plaza. LMU trivia night at 8pm. Want links or to RSVP?"
            },
            
            # 4. Enhanced Visual Feedback
            {
                "prompt": "Hi",
                "response": "[confetti:true] First question unlocked! Welcome to LMU Buddy, your new campus bestie."
            },
            {
                "prompt": "thanks!",
                "response": "Stoppp I'm blushing. Wanna leave a or so I know if I'm killing it?"
            },
            
            # 5. Feedback Collection
            {
                "prompt": "Cool, that helped.",
                "response": "Love that for us! Was it or mid? Tap below to rate me."
            },
            {
                "prompt": "That didn't help",
                "response": "Oof my bad! Tap below or tell me what sucked—I'll fix up."
            },
            
            # 6. Waitlist & Social Loop
            {
                "prompt": "What else can you do?",
                "response": "Still learning! Wanna try beta features before anyone else? Join the LMU Buddy Club here."
            },
            {
                "prompt": "How do I stay updated?",
                "response": "Easy—drop your email to join the waitlist or share your link for early-access perks"
            },
            
            # 7. Richer, More Dynamic Example Prompts
            {
                "prompt": "What can I ask?",
                "response": "Hit me with: Where to nap between classes? Best professor for psych majors? LMU's secret study corners?"
            },
            {
                "prompt": "Give me example questions",
                "response": "You can ask: Who's the GOAT CS prof? Where's a chill place to cry between finals? Any fire campus memes this week?"
            },
            
            # 8. Handle Edge Cases Gracefully
            {
                "prompt": "What's the graduation rate for transfer students?",
                "response": "Not sure yet! Want me to send you the official LMU page or submit it to my creators to add?"
            },
            {
                "prompt": "How do I file a Title IX complaint?",
                "response": "That's a big one. I'll link you straight to LMU's Title IX Office page for the most accurate info."
            },
            
            # 9. Boost LMU Buddy Personality
            {
                "prompt": "Where's the best food?",
                "response": "Didn't I already hype up The Bluff? Or you just testing me again?"
            },
            {
                "prompt": "Where can I nap?",
                "response": "Library. 3rd floor. Back corner behind the giant plant. Bring a hoodie and pretend you're studying."
            },
            {
                "prompt": "Tell me a fun fact",
                "response": "LMU's mascot is Iggy the Lion. But real ones know the bluff is the actual spiritual mascot (sunset vibes don't lie)."
            },
            {
                "prompt": "What's something nobody tells you about LMU?",
                "response": "Nobody warns you that the C-store closes EARLY. Like, what if I want instant ramen at 10pm?!"
            },
            
            # Additional LMU-specific conversations
            {
                "prompt": "Where's the best place to study?",
                "response": "Depends on your vibe! Library 3rd floor for quiet, UHall balcony for fresh air, or the Lion's Den if you need caffeine to survive."
            },
            {
                "prompt": "How do I find my classes?",
                "response": "First day chaos? Use the LMU app or just follow the crowd. Pro tip: Doolan Hall is NOT near Hilton Center (learned that the hard way)."
            },
            {
                "prompt": "What's the parking situation?",
                "response": "Parking at LMU is like finding a unicorn. Get here early or prepare for a hike from the overflow lot. Student parking pass is worth it!"
            },
            {
                "prompt": "Best professor recommendations?",
                "response": "For CS? Dr. Johnson is a legend. Business? Prof. Chen makes marketing actually interesting. Film? Prof. Kim has industry connections that'll blow your mind."
            },
            {
                "prompt": "Where can I get help with my resume?",
                "response": "Career Center is your bestie! They do resume workshops every week and the advisors there actually know what they're talking about."
            },
            {
                "prompt": "What's the social scene like?",
                "response": "Greek life is big, but there's something for everyone. Check out the 100+ clubs or just hang at the Lion's Den—you'll meet people either way."
            },
            {
                "prompt": "How do I get involved on campus?",
                "response": "Club fair is your golden ticket! Or just DM me and I'll hook you up with the right people. There's literally a club for everything here."
            },
            {
                "prompt": "What's the food like in the dining halls?",
                "response": "The Lair is hit or miss but the Bluff has those sunset views that make everything taste better. Pro tip: avoid the mystery meat on Mondays."
            },
            {
                "prompt": "How do I get to LA from campus?",
                "response": "Uber/Lyft is easiest, but the Metro bus is cheap if you're patient. Takes about 30-45 min depending on traffic (which is always terrible)."
            },
            {
                "prompt": "What's the weather like?",
                "response": "LA weather is basically perfect year-round. You'll forget what seasons are. But bring a jacket for those random cold nights—the bluff gets windy!"
            }
        ]
        
        training_data = []
        
        for conv in conversations:
            if "responses" in conv:
                # For conversations with multiple response variations
                for response in conv["responses"]:
                    training_data.append({
                        "prompt": conv["prompt"],
                        "response": response,
                        "system_prompt": self.system_prompt
                    })
            else:
                # For single response conversations
                training_data.append({
                    "prompt": conv["prompt"],
                    "response": conv["response"],
                    "system_prompt": self.system_prompt
                })
        
        return training_data

    def create_modelfile(self, training_data: List[Dict[str, Any]]) -> str:
        """Create a Modelfile for Ollama fine-tuning"""
        
        modelfile_content = f"""FROM {self.base_model}

# System prompt
SYSTEM \"\"\"
{self.system_prompt}
\"\"\"

# Training examples
"""
        
        # Add training examples
        for i, example in enumerate(training_data):
            modelfile_content += f"""
# Example {i+1}
PROMPT \"\"\"
{example['prompt']}
\"\"\"

RESPONSE \"\"\"
{example['response']}
\"\"\"
"""
        
        return modelfile_content

    def save_training_data(self, training_data: List[Dict[str, Any]], filename: str = "lmu_buddy_training_data.json"):
        """Save training data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(training_data, f, indent=2)
        logger.info(f"Training data saved to {filename}")

    def save_modelfile(self, modelfile_content: str, filename: str = "Modelfile"):
        """Save Modelfile for Ollama"""
        with open(filename, 'w') as f:
            f.write(modelfile_content)
        logger.info(f"Modelfile saved to {filename}")

    def check_ollama_installation(self) -> bool:
        """Check if Ollama is installed and running"""
        try:
            result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Ollama version: {result.stdout.strip()}")
                return True
            else:
                logger.error("Ollama is not properly installed")
                return False
        except FileNotFoundError:
            logger.error("Ollama is not installed. Please install Ollama first.")
            return False

    def check_base_model(self) -> bool:
        """Check if the base model is available"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                models = result.stdout
                if self.base_model.split(':')[0] in models:
                    logger.info(f"Base model {self.base_model} is available")
                    return True
                else:
                    logger.warning(f"Base model {self.base_model} not found. Available models: {models}")
                    return False
        except Exception as e:
            logger.error(f"Error checking base model: {e}")
            return False

    def pull_base_model(self):
        """Pull the base model if not available"""
        logger.info(f"Pulling base model {self.base_model}...")
        try:
            result = subprocess.run(['ollama', 'pull', self.base_model], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("Base model pulled successfully")
            else:
                logger.error(f"Failed to pull base model: {result.stderr}")
        except Exception as e:
            logger.error(f"Error pulling base model: {e}")

    def create_model(self):
        """Create the fine-tuned model using Ollama"""
        logger.info(f"Creating fine-tuned model {self.model_name}...")
        try:
            # First, try to remove the model if it exists
            subprocess.run(['ollama', 'rm', self.model_name], capture_output=True, text=True)
            
            # Create the model using the Modelfile
            result = subprocess.run(['ollama', 'create', self.model_name, '-f', 'Modelfile'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Model {self.model_name} created successfully!")
                return True
            else:
                logger.error(f"Failed to create model: {result.stderr}")
                logger.error(f"Full error output: {result.stdout}")
                return False
        except Exception as e:
            logger.error(f"Error creating model: {e}")
            return False

    def test_model(self, test_prompts: List[str] = None):
        """Test the fine-tuned model with sample prompts"""
        if test_prompts is None:
            test_prompts = [
                "Where should I eat on campus?",
                "What's a good coffee spot?",
                "Where can I study?",
                "Tell me a fun fact about LMU"
            ]
        
        logger.info("Testing the fine-tuned model...")
        
        for prompt in test_prompts:
            try:
                result = subprocess.run(['ollama', 'run', self.model_name, prompt], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    logger.info(f"Prompt: {prompt}")
                    logger.info(f"Response: {result.stdout.strip()}")
                    logger.info("-" * 50)
                else:
                    logger.error(f"Failed to get response for '{prompt}': {result.stderr}")
            except subprocess.TimeoutExpired:
                logger.error(f"Timeout getting response for '{prompt}'")
            except Exception as e:
                logger.error(f"Error testing model: {e}")

    def run_fine_tuning(self):
        """Run the complete fine-tuning process"""
        logger.info("Starting LMU Buddy fine-tuning process...")
        
        # Step 1: Check Ollama installation
        if not self.check_ollama_installation():
            logger.error("Please install Ollama first: https://ollama.ai/")
            return False
        
        # Step 2: Create training data
        logger.info("Creating training data...")
        training_data = self.create_training_data()
        self.save_training_data(training_data)
        
        # Step 3: Create Modelfile
        logger.info("Creating Modelfile...")
        modelfile_content = self.create_modelfile(training_data)
        self.save_modelfile(modelfile_content)
        
        # Step 4: Check and pull base model
        if not self.check_base_model():
            self.pull_base_model()
        
        # Step 5: Create fine-tuned model
        if self.create_model():
            logger.info("Fine-tuning completed successfully!")
            
            # Step 6: Test the model
            self.test_model()
            
            return True
        else:
            logger.error("Fine-tuning failed!")
            return False

def main():
    """Main function to run the fine-tuning process"""
    print("🦁 LMU Buddy Fine-tuning Script")
    print("=" * 50)
    
    # Initialize the fine-tuner
    fine_tuner = LMUBuddyFineTuner(
        base_model="llama2:7b",  # You can change this to other models
        model_name="lmu-buddy"
    )
    
    # Run the fine-tuning process
    success = fine_tuner.run_fine_tuning()
    
    if success:
        print("\n🎉 Fine-tuning completed successfully!")
        print(f"Your LMU Buddy model '{fine_tuner.model_name}' is ready to use!")
        print("\nTo use the model:")
        print(f"  ollama run {fine_tuner.model_name} 'Your question here'")
        print("\nTo integrate with your Streamlit app, update the model name in your code.")
    else:
        print("\n❌ Fine-tuning failed. Please check the logs above for details.")

if __name__ == "__main__":
    main()