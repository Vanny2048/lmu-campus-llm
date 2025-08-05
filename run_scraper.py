#!/usr/bin/env python3
"""
LMU Data Scraper Runner
This script runs the comprehensive LMU data scraper to generate the data files
needed for the Enhanced LMU Buddy.
"""

import os
import sys
from lmu_scraper import LMUDataScraper

def main():
    print("🦁 LMU Data Scraper - Bringing Back the Roar!")
    print("=" * 50)
    
    # Check if data file already exists
    if os.path.exists('lmu_data.json'):
        print("📁 Found existing lmu_data.json")
        response = input("Do you want to regenerate the data? (y/n): ").lower()
        if response != 'y':
            print("✅ Using existing data file")
            return
    
    print("🚀 Starting comprehensive LMU data scraping...")
    print("This will gather data from:")
    print("• Rate My Professor")
    print("• Official LMU websites")
    print("• Course catalogs")
    print("• Events and activities")
    print("• News and announcements")
    print()
    
    try:
        # Initialize scraper
        scraper = LMUDataScraper()
        
        # Run full scraping
        data = scraper.run_full_scrape()
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 Scraping Summary:")
        print(f"• Professors: {len(data['professors'])}")
        print(f"• Courses: {len(data['courses'])}")
        print(f"• Dining Options: {len(data['dining'])}")
        print(f"• Housing Options: {len(data['housing'])}")
        print(f"• Events: {len(data['events'])}")
        print(f"• Organizations: {len(data['organizations'])}")
        print(f"• Facilities: {len(data['facilities'])}")
        print(f"• News Articles: {len(data['news'])}")
        print(f"• Total Data Points: {sum(len(v) for v in data.values())}")
        
        print("\n✅ Data scraping completed successfully!")
        print("📁 Files created:")
        print("• lmu_data.json - Main data file")
        print("• lmu_embeddings.pkl - Semantic search embeddings (will be created on first run)")
        
        print("\n🦁 Your Enhanced LMU Buddy is ready to roar!")
        
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        print("Please check your internet connection and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()