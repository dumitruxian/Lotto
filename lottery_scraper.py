"""
Lottery Historical Data Scraper
Downloads historical draw data for Romania 6/49 and Canada Ontario 6/49

Installation:
pip install requests beautifulsoup4 lxml

Usage:
python lottery_scraper.py
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime

class LotteryScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_romania_649(self):
        """
        Scrape Romania Loto 6/49 historical data
        """
        print("Scraping Romania Loto 6/49 data...")
        draws = []
        
        # Using lottery extreme which has historical data
        base_url = "https://www.lotteryextreme.com/romania/lotto-6-49/results"
        
        try:
            # Try to get data from multiple pages
            for page in range(1, 50):  # Adjust range as needed
                print(f"Fetching page {page}...")
                url = f"{base_url}?page={page}" if page > 1 else base_url
                
                response = self.session.get(url, timeout=10)
                if response.status_code != 200:
                    print(f"Failed to fetch page {page}")
                    break
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find draw results - adjust selectors based on actual HTML
                # This is a generic approach that will need fine-tuning
                result_rows = soup.find_all(['tr', 'div'], class_=re.compile('result|draw', re.I))
                
                if not result_rows:
                    print(f"No more results found at page {page}")
                    break
                
                for row in result_rows:
                    try:
                        # Extract date and numbers
                        text = row.get_text()
                        
                        # Look for date pattern
                        date_match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', text)
                        if not date_match:
                            continue
                        
                        date_str = date_match.group(1)
                        
                        # Look for numbers (6 main + 1 bonus)
                        numbers = re.findall(r'\b([1-9]|[1-4][0-9])\b', text)
                        
                        if len(numbers) >= 7:
                            draws.append({
                                'date': self.normalize_date(date_str),
                                'numbers': [int(n) for n in numbers[:6]],
                                'bonus': int(numbers[6])
                            })
                    except Exception as e:
                        continue
                
                time.sleep(1)  # Be polite to the server
                
        except Exception as e:
            print(f"Error scraping Romania data: {e}")
        
        print(f"Collected {len(draws)} Romania draws")
        return draws
    
    def scrape_ontario_649(self):
        """
        Scrape Canada Ontario Lotto 6/49 historical data
        """
        print("Scraping Canada Ontario Lotto 6/49 data...")
        draws = []
        
        # Try multiple sources
        urls_to_try = [
            "https://lottery.olg.ca/en-ca/winning-numbers/lotto-649/winning-numbers",
            "https://www.national-lottery.com/canada-lotto-649/results"
        ]
        
        for base_url in urls_to_try:
            try:
                print(f"Trying source: {base_url}")
                
                # Attempt to scrape
                for attempt in range(1, 20):
                    print(f"Fetching data set {attempt}...")
                    
                    response = self.session.get(base_url, timeout=10)
                    if response.status_code != 200:
                        break
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find results - generic approach
                    result_elements = soup.find_all(['tr', 'div', 'article'], 
                                                    class_=re.compile('result|draw|winning', re.I))
                    
                    if not result_elements:
                        break
                    
                    for element in result_elements:
                        try:
                            text = element.get_text()
                            
                            # Extract date
                            date_match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', text)
                            if not date_match:
                                continue
                            
                            date_str = date_match.group(1)
                            
                            # Extract numbers
                            numbers = re.findall(r'\b([1-9]|[1-4][0-9])\b', text)
                            
                            if len(numbers) >= 7:
                                draw = {
                                    'date': self.normalize_date(date_str),
                                    'numbers': [int(n) for n in numbers[:6]],
                                    'bonus': int(numbers[6])
                                }
                                
                                # Avoid duplicates
                                if not any(d['date'] == draw['date'] for d in draws):
                                    draws.append(draw)
                        except Exception as e:
                            continue
                    
                    time.sleep(1)
                    
                if draws:
                    break  # If we got data, don't try other sources
                    
            except Exception as e:
                print(f"Error with source {base_url}: {e}")
                continue
        
        print(f"Collected {len(draws)} Ontario draws")
        return draws
    
    def normalize_date(self, date_str):
        """Convert various date formats to YYYY-MM-DD"""
        formats = ['%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y', 
                   '%d/%m/%y', '%m/%d/%y', '%Y-%m-%d']
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        return date_str
    
    def save_to_txt(self, draws, filename):
        """Save draws to text file"""
        draws_sorted = sorted(draws, key=lambda x: x['date'])
        
        with open(filename, 'w') as f:
            f.write("# Lottery Draw History\n")
            f.write("# Format: Date: , N1, N2, N3, N4, N5, N6,  Bonus\n\n")
            
            for draw in draws_sorted:
                nums_str = ', '.join(f"{n:2d}" for n in draw['numbers'])
                f.write(f"{draw['date']}: , {nums_str},  {draw['bonus']:2d}\n")
        
        print(f"Saved {len(draws_sorted)} draws to {filename}")
    
    def save_to_json(self, draws, filename):
        """Save draws to JSON file"""
        draws_sorted = sorted(draws, key=lambda x: x['date'])
        
        with open(filename, 'w') as f:
            json.dump({'draws': draws_sorted}, f, indent=2)
        
        print(f"Saved {len(draws_sorted)} draws to {filename}")

def manual_data_template():
    """
    Create template files if scraping doesn't work
    """
    print("\n" + "="*60)
    print("ALTERNATIVE: Manual Data Collection")
    print("="*60)
    print("\nIf the scraper doesn't work well, you can manually collect data from:")
    print("\nRomania Loto 6/49:")
    print("  - Official: https://www.loto.ro/")
    print("  - Archive: https://www.lotteryextreme.com/romania/lotto-6-49/results")
    print("\nCanada Ontario 6/49:")
    print("  - Official: https://lottery.olg.ca/en-ca/winning-numbers/lotto-649")
    print("  - Archive: https://www.national-lottery.com/canada-lotto-649/results")
    print("\nFormat for manual entry (one draw per line):")
    print("YYYY-MM-DD: , N1, N2, N3, N4, N5, N6,  BONUS")
    print("Example: 2024-01-15: ,  3, 12, 23, 31, 42, 45,  18")
    print("\nSave as .txt and import into the analyzer app.")
    print("="*60)

def main():
    scraper = LotteryScraper()
    
    print("="*60)
    print("Lottery Historical Data Scraper")
    print("="*60)
    print("\nThis will attempt to scrape historical lottery data.")
    print("Note: Websites may change, requiring scraper updates.\n")
    
    # Scrape Romania
    print("\n[1/2] Romania Loto 6/49")
    print("-" * 40)
    romania_draws = scraper.scrape_romania_649()
    
    if romania_draws:
        scraper.save_to_txt(romania_draws, 'romania_649_history.txt')
        scraper.save_to_json(romania_draws, 'romania_649_history.json')
    else:
        print("⚠️  No Romania data collected. Website structure may have changed.")
    
    # Scrape Ontario
    print("\n[2/2] Canada Ontario Lotto 6/49")
    print("-" * 40)
    ontario_draws = scraper.scrape_ontario_649()
    
    if ontario_draws:
        scraper.save_to_txt(ontario_draws, 'ontario_649_history.txt')
        scraper.save_to_json(ontario_draws, 'ontario_649_history.json')
    else:
        print("⚠️  No Ontario data collected. Website structure may have changed.")
    
    # Summary
    print("\n" + "="*60)
    print("SCRAPING COMPLETE")
    print("="*60)
    print(f"\nRomania draws collected: {len(romania_draws)}")
    print(f"Ontario draws collected: {len(ontario_draws)}")
    
    if romania_draws or ontario_draws:
        print("\n✅ Files created:")
        if romania_draws:
            print("   - romania_649_history.txt")
            print("   - romania_649_history.json")
        if ontario_draws:
            print("   - ontario_649_history.txt")
            print("   - ontario_649_history.json")
        print("\nYou can import these files into your lottery analyzer!")
    else:
        print("\n⚠️  No data was collected.")
        manual_data_template()

if __name__ == "__main__":
    main()