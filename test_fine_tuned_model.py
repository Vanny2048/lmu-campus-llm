#!/usr/bin/env python3
"""
Test script for the fine-tuned LMU Buddy model
Verifies that the model is working correctly with various test cases
"""

import subprocess
import json
import time
from typing import List, Dict, Any

def test_model_availability():
    """Test if the fine-tuned model is available"""
    print("🔍 Testing model availability...")
    
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            if 'lmu-buddy' in result.stdout:
                print("✅ LMU Buddy model is available")
                return True
            else:
                print("❌ LMU Buddy model not found")
                return False
        else:
            print(f"❌ Error checking models: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_basic_responses():
    """Test basic response generation"""
    print("\n🧪 Testing basic responses...")
    
    test_cases = [
        "Where should I eat on campus?",
        "What's a good coffee spot?",
        "Where can I study?",
        "Tell me a fun fact about LMU"
    ]
    
    for prompt in test_cases:
        print(f"\n📝 Prompt: {prompt}")
        try:
            result = subprocess.run(
                ['ollama', 'run', 'lmu-buddy', prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                response = result.stdout.strip()
                print(f"🤖 Response: {response}")
                print(f"📏 Length: {len(response)} characters")
            else:
                print(f"❌ Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("⏰ Timeout - response took too long")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_response_variety():
    """Test that the model provides varied responses"""
    print("\n🎲 Testing response variety...")
    
    prompt = "Where should I eat on campus?"
    responses = []
    
    for i in range(3):
        print(f"\n🔄 Attempt {i+1}:")
        try:
            result = subprocess.run(
                ['ollama', 'run', 'lmu-buddy', prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                response = result.stdout.strip()
                responses.append(response)
                print(f"Response: {response[:100]}...")
            else:
                print(f"❌ Error: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Check for variety
    unique_responses = set(responses)
    print(f"\n📊 Response variety: {len(unique_responses)} unique responses out of {len(responses)} attempts")
    
    if len(unique_responses) > 1:
        print("✅ Good variety in responses!")
    else:
        print("⚠️ Responses are too similar")

def test_personality_consistency():
    """Test that the model maintains LMU Buddy personality"""
    print("\n🎭 Testing personality consistency...")
    
    personality_indicators = [
        "casual language",
        "LMU references",
        "emoji usage",
        "student-friendly tone"
    ]
    
    test_prompts = [
        "Hi",
        "What's the weather like?",
        "Where can I get help with my resume?"
    ]
    
    for prompt in test_prompts:
        print(f"\n📝 Testing: {prompt}")
        try:
            result = subprocess.run(
                ['ollama', 'run', 'lmu-buddy', prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                response = result.stdout.strip()
                print(f"Response: {response}")
                
                # Check personality indicators
                has_emoji = any(char in response for char in "🦁🍕📚🎉🏛️🚗✨")
                has_lmu_ref = any(word in response.lower() for word in ['lmu', 'bluff', 'lair', 'lions den', 'campus'])
                is_casual = any(word in response.lower() for word in ['hey', 'whats up', 'pro tip', 'clutch', 'vibe'])
                
                print(f"  🎨 Has emoji: {has_emoji}")
                print(f"  🏫 Has LMU reference: {has_lmu_ref}")
                print(f"  😎 Casual tone: {is_casual}")
                
            else:
                print(f"❌ Error: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_edge_cases():
    """Test how the model handles edge cases"""
    print("\n🔍 Testing edge cases...")
    
    edge_cases = [
        "What's the graduation rate for transfer students?",
        "How do I file a Title IX complaint?",
        "What's the meaning of life?",
        "",  # Empty prompt
        "x" * 1000,  # Very long prompt
    ]
    
    for prompt in edge_cases:
        print(f"\n📝 Edge case: {prompt[:50]}{'...' if len(prompt) > 50 else ''}")
        try:
            result = subprocess.run(
                ['ollama', 'run', 'lmu-buddy', prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                response = result.stdout.strip()
                print(f"Response: {response[:100]}{'...' if len(response) > 100 else ''}")
            else:
                print(f"❌ Error: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_integration():
    """Test integration with the client"""
    print("\n🔗 Testing integration...")
    
    try:
        from lmu_buddy_ollama_client import LMUBuddyOllamaClient
        
        client = LMUBuddyOllamaClient()
        
        # Test basic functionality
        response = client.get_enhanced_response("Where should I eat on campus?")
        print(f"✅ Integration test response: {response[:100]}...")
        
        # Test fallback
        if not client.check_model_availability():
            print("⚠️ Model not available, testing fallback...")
            fallback_response = client.get_enhanced_response("test")
            print(f"✅ Fallback response: {fallback_response[:100]}...")
        
        return True
        
    except ImportError:
        print("❌ Integration module not found")
        return False
    except Exception as e:
        print(f"❌ Integration error: {e}")
        return False

def run_performance_test():
    """Run a basic performance test"""
    print("\n⚡ Performance test...")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ['ollama', 'run', 'lmu-buddy', 'Hi'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Response time: {response_time:.2f} seconds")
            
            if response_time < 5:
                print("🚀 Fast response!")
            elif response_time < 15:
                print("⚡ Good response time")
            else:
                print("🐌 Slow response - consider using a smaller base model")
        else:
            print(f"❌ Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Performance test error: {e}")

def main():
    """Run all tests"""
    print("🦁 LMU Buddy Model Test Suite")
    print("=" * 50)
    
    # Test 1: Model availability
    if not test_model_availability():
        print("\n❌ Model not available. Please run the fine-tuning first:")
        print("python fine_tune_lmu_buddy.py")
        return
    
    # Test 2: Basic responses
    test_basic_responses()
    
    # Test 3: Response variety
    test_response_variety()
    
    # Test 4: Personality consistency
    test_personality_consistency()
    
    # Test 5: Edge cases
    test_edge_cases()
    
    # Test 6: Integration
    test_integration()
    
    # Test 7: Performance
    run_performance_test()
    
    print("\n" + "🎉" * 20)
    print("🎉 ALL TESTS COMPLETED! 🎉")
    print("🎉" * 20)
    print("\nYour LMU Buddy model is ready to roar! 🦁")

if __name__ == "__main__":
    main()