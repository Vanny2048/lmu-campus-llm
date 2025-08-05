#!/usr/bin/env python3
"""
Test script for Gen Z LMU Buddy
"""

from genz_lmu_buddy import GenZLMUBuddy
import json

def test_genz_buddy():
    """Test the Gen Z LMU Buddy functionality"""
    print("🦁 Testing Gen Z LMU Buddy...")
    
    # Initialize the buddy
    buddy = GenZLMUBuddy()
    
    # Test data loading
    print(f"✅ Loaded {len(buddy.data)} data categories")
    for category, items in buddy.data.items():
        if isinstance(items, list):
            print(f"   • {category}: {len(items)} items")
    
    # Test queries
    test_queries = [
        "Tell me about professors",
        "What dining options are available?",
        "Tell me about housing",
        "What events are happening?",
        "Tell me about LMU athletics"
    ]
    
    print("\n🧪 Testing responses...")
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = buddy.generate_response(query)
            print(f"Response: {response[:200]}...")
        except Exception as e:
            print(f"Error: {e}")
    
    # Test Ollama connection
    print("\n🤖 Testing Ollama connection...")
    try:
        response = buddy.call_ollama("Hello, are you working?")
        if response:
            print("✅ Ollama is working!")
            print(f"Response: {response[:100]}...")
        else:
            print("❌ Ollama returned no response")
    except Exception as e:
        print(f"❌ Ollama error: {e}")
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    test_genz_buddy()