#!/usr/bin/env python3
"""
LMU Data Collection Script
Collects authentic LMU data from Reddit and RateMyProfessors
"""

import os
import sys
import logging
from datetime import datetime
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main data collection function"""
    logger.info("🚀 Starting LMU Data Collection...")
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Step 1: Collect Reddit data
    logger.info("📱 Collecting LMU Reddit data...")
    try:
        from lmu_reddit_scraper import LMURedditScraper
        reddit_scraper = LMURedditScraper()
        reddit_data = reddit_scraper.run_scrape()
        logger.info(f"✅ Collected {reddit_data['summary']['total_posts']} Reddit posts")
    except Exception as e:
        logger.error(f"❌ Error collecting Reddit data: {e}")
        reddit_data = {'campus_tea': [], 'slang': []}
    
    # Step 2: Collect RateMyProfessors data
    logger.info("👨‍🏫 Collecting LMU RateMyProfessors data...")
    try:
        from lmu_rmp_scraper import LMURateMyProfessorScraper
        rmp_scraper = LMURateMyProfessorScraper()
        rmp_data = rmp_scraper.run_scrape()
        logger.info(f"✅ Collected {len(rmp_data['professors'])} professor profiles")
    except Exception as e:
        logger.error(f"❌ Error collecting RMP data: {e}")
        rmp_data = {'professors': [], 'professor_tea': []}
    
    # Step 3: Combine and enhance data
    logger.info("🔗 Combining and enhancing data...")
    
    # Load existing LMU data
    try:
        with open('enhanced_lmu_data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        logger.warning("enhanced_lmu_data.json not found, creating new data structure")
        existing_data = {
            'professors': [],
            'courses': [],
            'dining': [],
            'housing': [],
            'events': [],
            'organizations': [],
            'facilities': [],
            'news': []
        }
    
    # Enhance existing data with scraped data
    enhanced_data = existing_data.copy()
    
    # Add RMP professor data
    if rmp_data.get('professors'):
        enhanced_data['professors'] = rmp_data['professors']
        logger.info(f"✅ Enhanced professor data with {len(rmp_data['professors'])} profiles")
    
    # Add Reddit campus tea
    if reddit_data.get('campus_tea'):
        enhanced_data['campus_tea'] = reddit_data['campus_tea']
        logger.info(f"✅ Added {len(reddit_data['campus_tea'])} campus tea entries")
    
    # Add campus slang
    if reddit_data.get('slang'):
        enhanced_data['campus_slang'] = reddit_data['slang']
        logger.info(f"✅ Added {len(reddit_data['slang'])} campus slang terms")
    
    # Add metadata
    enhanced_data['metadata'] = {
        'last_updated': datetime.now().isoformat(),
        'reddit_posts_collected': reddit_data.get('summary', {}).get('total_posts', 0),
        'professors_collected': len(rmp_data.get('professors', [])),
        'campus_tea_count': len(reddit_data.get('campus_tea', [])),
        'slang_count': len(reddit_data.get('slang', [])),
        'data_sources': ['reddit', 'ratemyprofessors', 'existing_lmu_data']
    }
    
    # Step 4: Save enhanced data
    logger.info("💾 Saving enhanced data...")
    
    # Save individual data files
    with open('lmu_reddit_data.json', 'w', encoding='utf-8') as f:
        json.dump(reddit_data, f, indent=2, ensure_ascii=False)
    
    with open('lmu_rmp_data.json', 'w', encoding='utf-8') as f:
        json.dump(rmp_data, f, indent=2, ensure_ascii=False)
    
    # Save enhanced combined data
    with open('enhanced_lmu_data_v2.json', 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
    
    # Step 5: Generate summary report
    logger.info("📊 Generating summary report...")
    
    summary = {
        'collection_date': datetime.now().isoformat(),
        'reddit_data': {
            'total_posts': reddit_data.get('summary', {}).get('total_posts', 0),
            'campus_tea': len(reddit_data.get('campus_tea', [])),
            'dorm_gossip': len(reddit_data.get('data', {}).get('dorm_gossip', [])),
            'professor_tea': len(reddit_data.get('data', {}).get('professor_tea', [])),
            'food_reviews': len(reddit_data.get('data', {}).get('food_reviews', [])),
            'event_opinions': len(reddit_data.get('data', {}).get('event_opinions', [])),
            'admin_complaints': len(reddit_data.get('data', {}).get('admin_complaints', [])),
            'campus_slang': len(reddit_data.get('slang', [])),
            'student_experiences': len(reddit_data.get('data', {}).get('student_experiences', []))
        },
        'rmp_data': {
            'total_professors': len(rmp_data.get('professors', [])),
            'professors_with_ratings': len([p for p in rmp_data.get('professors', []) if p.get('rating')]),
            'average_rating': sum(p.get('rating', 0) for p in rmp_data.get('professors', [])) / max(len([p for p in rmp_data.get('professors', []) if p.get('rating')]), 1),
            'total_reviews': sum(p.get('review_count', 0) for p in rmp_data.get('professors', [])),
            'professor_tea': len(rmp_data.get('professor_tea', []))
        },
        'enhanced_data': {
            'total_professors': len(enhanced_data.get('professors', [])),
            'total_courses': len(enhanced_data.get('courses', [])),
            'total_dining': len(enhanced_data.get('dining', [])),
            'total_housing': len(enhanced_data.get('housing', [])),
            'total_events': len(enhanced_data.get('events', [])),
            'total_organizations': len(enhanced_data.get('organizations', [])),
            'total_facilities': len(enhanced_data.get('facilities', [])),
            'total_news': len(enhanced_data.get('news', [])),
            'campus_tea': len(enhanced_data.get('campus_tea', [])),
            'campus_slang': len(enhanced_data.get('campus_slang', []))
        }
    }
    
    # Save summary report
    with open('data_collection_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "="*60)
    print("🎉 LMU DATA COLLECTION COMPLETE!")
    print("="*60)
    print(f"📱 Reddit Data:")
    print(f"   • Total Posts: {summary['reddit_data']['total_posts']}")
    print(f"   • Campus Tea: {summary['reddit_data']['campus_tea']}")
    print(f"   • Dorm Gossip: {summary['reddit_data']['dorm_gossip']}")
    print(f"   • Professor Tea: {summary['reddit_data']['professor_tea']}")
    print(f"   • Food Reviews: {summary['reddit_data']['food_reviews']}")
    print(f"   • Event Opinions: {summary['reddit_data']['event_opinions']}")
    print(f"   • Admin Complaints: {summary['reddit_data']['admin_complaints']}")
    print(f"   • Campus Slang: {summary['reddit_data']['campus_slang']}")
    print(f"   • Student Experiences: {summary['reddit_data']['student_experiences']}")
    
    print(f"\n👨‍🏫 RateMyProfessors Data:")
    print(f"   • Total Professors: {summary['rmp_data']['total_professors']}")
    print(f"   • Professors with Ratings: {summary['rmp_data']['professors_with_ratings']}")
    print(f"   • Average Rating: {summary['rmp_data']['average_rating']:.2f}/5.0")
    print(f"   • Total Reviews: {summary['rmp_data']['total_reviews']}")
    print(f"   • Professor Tea: {summary['rmp_data']['professor_tea']}")
    
    print(f"\n🔗 Enhanced Data:")
    print(f"   • Total Professors: {summary['enhanced_data']['total_professors']}")
    print(f"   • Total Courses: {summary['enhanced_data']['total_courses']}")
    print(f"   • Total Dining: {summary['enhanced_data']['total_dining']}")
    print(f"   • Total Housing: {summary['enhanced_data']['total_housing']}")
    print(f"   • Total Events: {summary['enhanced_data']['total_events']}")
    print(f"   • Total Organizations: {summary['enhanced_data']['total_organizations']}")
    print(f"   • Total Facilities: {summary['enhanced_data']['total_facilities']}")
    print(f"   • Total News: {summary['enhanced_data']['total_news']}")
    print(f"   • Campus Tea: {summary['enhanced_data']['campus_tea']}")
    print(f"   • Campus Slang: {summary['enhanced_data']['campus_slang']}")
    
    print(f"\n💾 Files Created:")
    print(f"   • lmu_reddit_data.json")
    print(f"   • lmu_rmp_data.json")
    print(f"   • enhanced_lmu_data_v2.json")
    print(f"   • data_collection_summary.json")
    
    print("\n🚀 Ready to use Enhanced LMU Buddy V2!")
    print("="*60)
    
    return summary

if __name__ == "__main__":
    try:
        summary = main()
        sys.exit(0)
    except KeyboardInterrupt:
        logger.info("Data collection interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)