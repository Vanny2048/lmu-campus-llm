import requests
import json
import time
import re
from datetime import datetime
import logging
from typing import List, Dict, Any
import random
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LMURateMyProfessorScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://www.ratemyprofessors.com"
        self.school_id = "538"  # LMU's RMP school ID
        self.data = {
            'professors': [],
            'departments': {},
            'reviews': [],
            'ratings_summary': {}
        }
        
    def scrape_professor_list(self, page=1, max_pages=10):
        """Scrape list of professors from LMU's RMP page"""
        logger.info(f"Scraping professor list page {page}...")
        
        try:
            url = f"{self.base_url}/school/{self.school_id}?page={page}"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find professor cards
            professor_cards = soup.find_all('div', class_='TeacherCard')
            
            if not professor_cards:
                logger.info(f"No more professors found on page {page}")
                return False
            
            for card in professor_cards:
                try:
                    professor_data = self.extract_professor_data(card)
                    if professor_data:
                        self.data['professors'].append(professor_data)
                except Exception as e:
                    logger.error(f"Error extracting professor data: {e}")
                    continue
            
            # Add delay to be respectful
            time.sleep(random.uniform(2, 4))
            
            return True
            
        except Exception as e:
            logger.error(f"Error scraping professor list page {page}: {e}")
            return False
    
    def extract_professor_data(self, card):
        """Extract professor information from a card"""
        try:
            # Extract basic info
            name_elem = card.find('div', class_='TeacherName')
            if not name_elem:
                return None
            
            name = name_elem.get_text(strip=True)
            
            # Extract department
            dept_elem = card.find('div', class_='TeacherDepartment')
            department = dept_elem.get_text(strip=True) if dept_elem else "Unknown"
            
            # Extract rating
            rating_elem = card.find('div', class_='TeacherRating')
            rating = None
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    rating = float(rating_match.group(1))
            
            # Extract difficulty
            difficulty_elem = card.find('div', class_='TeacherDifficulty')
            difficulty = None
            if difficulty_elem:
                difficulty_text = difficulty_elem.get_text(strip=True)
                difficulty_match = re.search(r'(\d+\.?\d*)', difficulty_text)
                if difficulty_match:
                    difficulty = float(difficulty_match.group(1))
            
            # Extract review count
            reviews_elem = card.find('div', class_='TeacherReviewCount')
            review_count = 0
            if reviews_elem:
                reviews_text = reviews_elem.get_text(strip=True)
                reviews_match = re.search(r'(\d+)', reviews_text)
                if reviews_match:
                    review_count = int(reviews_match.group(1))
            
            # Extract professor ID for detailed scraping
            link_elem = card.find('a', href=True)
            professor_id = None
            if link_elem:
                href = link_elem['href']
                id_match = re.search(r'/professor/(\d+)', href)
                if id_match:
                    professor_id = id_match.group(1)
            
            return {
                'name': name,
                'department': department,
                'rating': rating,
                'difficulty': difficulty,
                'review_count': review_count,
                'professor_id': professor_id,
                'school': 'Loyola Marymount University'
            }
            
        except Exception as e:
            logger.error(f"Error extracting professor data: {e}")
            return None
    
    def scrape_professor_details(self, professor_id, name):
        """Scrape detailed information for a specific professor"""
        logger.info(f"Scraping details for {name} (ID: {professor_id})...")
        
        try:
            url = f"{self.base_url}/professor/{professor_id}"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract detailed information
            details = {
                'professor_id': professor_id,
                'name': name,
                'reviews': [],
                'courses': [],
                'tags': [],
                'would_take_again': None,
                'grade_distribution': {}
            }
            
            # Extract reviews
            review_elements = soup.find_all('div', class_='Review')
            for review_elem in review_elements[:10]:  # Limit to 10 reviews
                review_data = self.extract_review_data(review_elem)
                if review_data:
                    details['reviews'].append(review_data)
            
            # Extract courses
            course_elements = soup.find_all('div', class_='Course')
            for course_elem in course_elements:
                course_text = course_elem.get_text(strip=True)
                if course_text:
                    details['courses'].append(course_text)
            
            # Extract tags
            tag_elements = soup.find_all('span', class_='Tag')
            for tag_elem in tag_elements:
                tag_text = tag_elem.get_text(strip=True)
                if tag_text:
                    details['tags'].append(tag_text)
            
            # Extract "Would Take Again" percentage
            would_take_elem = soup.find('div', class_='WouldTakeAgain')
            if would_take_elem:
                would_take_text = would_take_elem.get_text(strip=True)
                percentage_match = re.search(r'(\d+)%', would_take_text)
                if percentage_match:
                    details['would_take_again'] = int(percentage_match.group(1))
            
            return details
            
        except Exception as e:
            logger.error(f"Error scraping professor details for {name}: {e}")
            return None
    
    def extract_review_data(self, review_elem):
        """Extract review information from a review element"""
        try:
            # Extract review text
            text_elem = review_elem.find('div', class_='ReviewText')
            text = text_elem.get_text(strip=True) if text_elem else ""
            
            # Extract rating
            rating_elem = review_elem.find('div', class_='Rating')
            rating = None
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    rating = float(rating_match.group(1))
            
            # Extract difficulty
            difficulty_elem = review_elem.find('div', class_='Difficulty')
            difficulty = None
            if difficulty_elem:
                difficulty_text = difficulty_elem.get_text(strip=True)
                difficulty_match = re.search(r'(\d+\.?\d*)', difficulty_text)
                if difficulty_match:
                    difficulty = float(difficulty_match.group(1))
            
            # Extract course
            course_elem = review_elem.find('div', class_='Course')
            course = course_elem.get_text(strip=True) if course_elem else ""
            
            # Extract date
            date_elem = review_elem.find('div', class_='Date')
            date = date_elem.get_text(strip=True) if date_elem else ""
            
            return {
                'text': text,
                'rating': rating,
                'difficulty': difficulty,
                'course': course,
                'date': date
            }
            
        except Exception as e:
            logger.error(f"Error extracting review data: {e}")
            return None
    
    def generate_professor_tea(self):
        """Generate authentic professor tea from scraped reviews"""
        tea_entries = []
        
        for professor in self.data['professors']:
            if professor.get('rating') and professor.get('review_count', 0) > 5:
                # Generate tea based on rating
                if professor['rating'] >= 4.5:
                    tea_type = "amazing_professor"
                    tea_content = f"{professor['name']} is literally the GOAT"
                elif professor['rating'] >= 4.0:
                    tea_type = "good_professor"
                    tea_content = f"{professor['name']} is pretty solid"
                elif professor['rating'] >= 3.0:
                    tea_type = "okay_professor"
                    tea_content = f"{professor['name']} is mid but manageable"
                else:
                    tea_type = "avoid_professor"
                    tea_content = f"avoid {professor['name']} at all costs"
                
                tea_entries.append({
                    'type': tea_type,
                    'professor': professor['name'],
                    'department': professor['department'],
                    'rating': professor['rating'],
                    'difficulty': professor['difficulty'],
                    'review_count': professor['review_count'],
                    'tea_content': tea_content,
                    'details': f"Rated {professor['rating']}/5 with {professor['review_count']} reviews"
                })
        
        return tea_entries
    
    def save_data(self, filename='lmu_rmp_data.json'):
        """Save scraped data to JSON file"""
        output_data = {
            'scraped_at': datetime.now().isoformat(),
            'school': 'Loyola Marymount University',
            'school_id': self.school_id,
            'professors': self.data['professors'],
            'professor_tea': self.generate_professor_tea(),
            'summary': {
                'total_professors': len(self.data['professors']),
                'professors_with_ratings': len([p for p in self.data['professors'] if p.get('rating')]),
                'average_rating': sum(p.get('rating', 0) for p in self.data['professors']) / max(len([p for p in self.data['professors'] if p.get('rating')]), 1),
                'total_reviews': sum(p.get('review_count', 0) for p in self.data['professors'])
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {filename} with {len(self.data['professors'])} professors")
        return output_data
    
    def run_scrape(self, max_pages=5):
        """Run the complete scraping process"""
        logger.info("Starting LMU RateMyProfessors scraping...")
        
        # Scrape professor list
        for page in range(1, max_pages + 1):
            success = self.scrape_professor_list(page)
            if not success:
                break
        
        # Scrape detailed information for top professors
        top_professors = sorted(
            [p for p in self.data['professors'] if p.get('rating') and p.get('review_count', 0) > 10],
            key=lambda x: (x.get('rating', 0), x.get('review_count', 0)),
            reverse=True
        )[:20]  # Top 20 professors
        
        for professor in top_professors:
            if professor.get('professor_id'):
                details = self.scrape_professor_details(professor['professor_id'], professor['name'])
                if details:
                    professor.update(details)
                time.sleep(random.uniform(1, 3))  # Be respectful
        
        return self.save_data()

if __name__ == "__main__":
    scraper = LMURateMyProfessorScraper()
    data = scraper.run_scrape()
    print(f"Scraped {len(data['professors'])} professors from LMU RateMyProfessors!")