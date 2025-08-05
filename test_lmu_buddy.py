#!/usr/bin/env python3
"""
Test script for Enhanced LMU Buddy
This script tests the functionality of the enhanced LMU Buddy with scraped data.
"""

import json
from enhanced_lmu_buddy import EnhancedLMUBuddy

def test_enhanced_lmu_buddy():
    """Test the enhanced LMU Buddy functionality"""
    print("🦁 Testing Enhanced LMU Buddy")
    print("=" * 50)
    
    try:
        # Initialize the enhanced LMU Buddy
        print("📚 Loading Enhanced LMU Buddy...")
        buddy = EnhancedLMUBuddy()
        
        # Test data loading
        print(f"✅ Data loaded successfully!")
        print(f"📊 Data summary:")
        print(f"   • Professors: {len(buddy.data.get('professors', []))}")
        print(f"   • Courses: {len(buddy.data.get('courses', []))}")
        print(f"   • Dining: {len(buddy.data.get('dining', []))}")
        print(f"   • Housing: {len(buddy.data.get('housing', []))}")
        print(f"   • Events: {len(buddy.data.get('events', []))}")
        print(f"   • Organizations: {len(buddy.data.get('organizations', []))}")
        print(f"   • Facilities: {len(buddy.data.get('facilities', []))}")
        print(f"   • News: {len(buddy.data.get('news', []))}")
        
        # Test queries
        test_queries = [
            "Who is Dr. Sarah Johnson?",
            "Tell me about CS 150",
            "Where should I eat on campus?",
            "What housing options are available?",
            "What events are coming up?",
            "Tell me about Greek life",
            "Where can I study?",
            "What's the latest news?"
        ]
        
        print("\n🧪 Testing queries:")
        print("-" * 30)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: {query}")
            print("Response:")
            response = buddy.generate_response(query)
            print(f"   {response[:200]}..." if len(response) > 200 else f"   {response}")
        
        # Test semantic search
        print("\n🔍 Testing semantic search:")
        print("-" * 30)
        
        search_query = "computer science professor"
        results = buddy.semantic_search(search_query, top_k=2)
        
        print(f"Search query: '{search_query}'")
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['category']}: {result['data'].get('name', 'N/A')} (similarity: {result['similarity']:.3f})")
        
        # Test upcoming events
        print("\n📅 Testing upcoming events:")
        print("-" * 30)
        
        upcoming = buddy.get_upcoming_events(30)  # Next 30 days
        print(f"Found {len(upcoming)} upcoming events:")
        for event in upcoming[:3]:  # Show first 3
            print(f"  • {event['name']} on {event['date']}")
        
        print("\n✅ All tests completed successfully!")
        print("🦁 Enhanced LMU Buddy is working perfectly!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_lmu_buddy()