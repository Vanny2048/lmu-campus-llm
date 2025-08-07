import requests
import json
import time
import re
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LMURedditScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://www.reddit.com/r/LMU"
        self.data = {
            'campus_tea': [],
            'dorm_gossip': [],
            'professor_tea': [],
            'food_reviews': [],
            'event_opinions': [],
            'admin_complaints': [],
            'campus_slang': [],
            'student_experiences': []
        }
        
    def scrape_reddit_posts(self, limit=100):
        """Scrape LMU subreddit posts for authentic student content"""
        logger.info("Scraping LMU Reddit for authentic student content...")
        
        try:
            # Use Reddit's JSON API
            url = f"{self.base_url}/.json?limit={limit}"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            for post in data['data']['children']:
                post_data = post['data']
                
                # Extract post content
                title = post_data.get('title', '')
                content = post_data.get('selftext', '')
                score = post_data.get('score', 0)
                comments_count = post_data.get('num_comments', 0)
                created_utc = post_data.get('created_utc', 0)
                
                # Skip low-quality posts
                if score < 5 or len(title) < 10:
                    continue
                
                # Categorize content
                self.categorize_content(title, content, score, comments_count)
                
                # Add delay to be respectful
                time.sleep(random.uniform(1, 3))
                
        except Exception as e:
            logger.error(f"Error scraping Reddit: {e}")
    
    def categorize_content(self, title: str, content: str, score: int, comments: int):
        """Categorize Reddit content into different types of campus tea"""
        
        text = f"{title} {content}".lower()
        
        # Campus tea and gossip
        if any(word in text for word in ['tea', 'gossip', 'drama', 'beef', 'rumor', 'scandal']):
            self.data['campus_tea'].append({
                'title': title,
                'content': content,
                'score': score,
                'comments': comments,
                'type': 'campus_tea'
            })
        
        # Dorm-related content
        if any(word in text for word in ['dorm', 'roommate', 'hannon', 'mccarthy', 'del rey', 'doheny', 'palm', 'rosecrans']):
            self.data['dorm_gossip'].append({
                'title': title,
                'content': content,
                'score': score,
                'comments': comments,
                'type': 'dorm_gossip'
            })
        
        # Professor-related content
        if any(word in text for word in ['professor', 'prof', 'teacher', 'class', 'course', 'exam', 'grade']):
            self.data['professor_tea'].append({
                'title': title,
                'content': content,
                'score': score,
                'comments': comments,
                'type': 'professor_tea'
            })
        
        # Food-related content
        if any(word in text for word in ['food', 'caf', 'lair', 'dining', 'meal', 'pizza', 'coffee', 'breakfast', 'lunch']):
            self.data['food_reviews'].append({
                'title': title,
                'content': content,
                'score': score,
                'comments': comments,
                'type': 'food_review'
            })
        
        # Event-related content
        if any(word in text for word in ['tnl', 'event', 'party', 'concert', 'game', 'basketball', 'football', 'weekend']):
            self.data['event_opinions'].append({
                'title': title,
                'content': content,
                'score': score,
                'comments': comments,
                'type': 'event_opinion'
            })
        
        # Admin/complaint content
        if any(word in text for word in ['admin', 'administration', 'complaint', 'problem', 'issue', 'advising', 'registration']):
            self.data['admin_complaints'].append({
                'title': title,
                'content': content,
                'score': score,
                'comments': comments,
                'type': 'admin_complaint'
            })
        
        # Campus slang and culture
        if any(word in text for word in ['bluff', 'lmu', 'campus', 'vibe', 'culture', 'slang', 'student life']):
            self.data['campus_slang'].append({
                'title': title,
                'content': content,
                'score': score,
                'comments': comments,
                'type': 'campus_slang'
            })
        
        # General student experiences
        self.data['student_experiences'].append({
            'title': title,
            'content': content,
            'score': score,
            'comments': comments,
            'type': 'student_experience'
        })
    
    def extract_lmu_slang(self):
        """Extract common LMU slang and phrases from scraped content"""
        slang_patterns = [
            r'\bthe bluff\b',
            r'\bbluff life\b',
            r'\bbluff vibes\b',
            r'\bbluff culture\b',
            r'\bhann\b',
            r'\bmccarthy\b',
            r'\bdel rey\b',
            r'\bdoheny\b',
            r'\bmalone\b',
            r'\bthe lair\b',
            r'\bthe caf\b',
            r'\btnl\b',
            r'\bcura personalis\b',
            r'\blmu\b',
            r'\bloyola\b',
            r'\bmarymount\b'
        ]
        
        extracted_slang = []
        
        for category, items in self.data.items():
            for item in items:
                text = f"{item['title']} {item['content']}"
                for pattern in slang_patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    extracted_slang.extend(matches)
        
        return list(set(extracted_slang))
    
    def generate_campus_tea(self):
        """Generate authentic campus tea from scraped content"""
        tea_entries = []
        
        # Campus tea
        for item in self.data['campus_tea'][:10]:  # Top 10
            tea_entries.append({
                'type': 'campus_tea',
                'content': item['title'],
                'details': item['content'][:200] + "..." if len(item['content']) > 200 else item['content'],
                'popularity': item['score']
            })
        
        # Dorm gossip
        for item in self.data['dorm_gossip'][:10]:
            tea_entries.append({
                'type': 'dorm_gossip',
                'content': item['title'],
                'details': item['content'][:200] + "..." if len(item['content']) > 200 else item['content'],
                'popularity': item['score']
            })
        
        # Professor tea
        for item in self.data['professor_tea'][:10]:
            tea_entries.append({
                'type': 'professor_tea',
                'content': item['title'],
                'details': item['content'][:200] + "..." if len(item['content']) > 200 else item['content'],
                'popularity': item['score']
            })
        
        return tea_entries
    
    def save_data(self, filename='lmu_reddit_data.json'):
        """Save scraped data to JSON file"""
        output_data = {
            'scraped_at': datetime.now().isoformat(),
            'data': self.data,
            'campus_tea': self.generate_campus_tea(),
            'slang': self.extract_lmu_slang(),
            'summary': {
                'total_posts': sum(len(items) for items in self.data.values()),
                'campus_tea_count': len(self.data['campus_tea']),
                'dorm_gossip_count': len(self.data['dorm_gossip']),
                'professor_tea_count': len(self.data['professor_tea']),
                'food_reviews_count': len(self.data['food_reviews']),
                'event_opinions_count': len(self.data['event_opinions']),
                'admin_complaints_count': len(self.data['admin_complaints']),
                'campus_slang_count': len(self.data['campus_slang']),
                'student_experiences_count': len(self.data['student_experiences'])
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {filename} with {output_data['summary']['total_posts']} total posts")
        return output_data
    
    def run_scrape(self):
        """Run the complete scraping process"""
        logger.info("Starting LMU Reddit scraping...")
        self.scrape_reddit_posts(limit=200)  # Scrape 200 posts
        return self.save_data()

if __name__ == "__main__":
    scraper = LMURedditScraper()
    data = scraper.run_scrape()
    print(f"Scraped {data['summary']['total_posts']} posts from LMU Reddit!")