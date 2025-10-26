"""
Description:
-------------
This project scrapes car data (brand, model, price, year, condition, etc.)
from two different websites and stores the information in a JSON file.

Chosen Websites:
----------------
1. Dubizzle Oman (https://www.dubizzle.com.om/en/vehicles/cars/)
   → Multi-brand car marketplace (used and new cars)
2. Toyota Oman (https://www.toyotaoman.com/)
   → Official Toyota website showing new models

Reason for choosing:
--------------------
- Both are **dynamic websites** that require JavaScript to load data.
- They represent **two different structures**:
    - Dubizzle → large car marketplace (multiple brands and sellers)
    - Toyota Oman → structured official brand site
- Demonstrates Selenium’s ability to handle both types efficiently.

Dependencies:
-------------
- Selenium → to automate the browser and extract rendered data
- JSON → to store data in a structured format
- re, datetime → for text parsing and timestamping
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time
from datetime import datetime
import re


class CarScraper:
    """Handles scraping operations for multiple car websites."""

    def __init__(self):
        """Initialize the Selenium Chrome WebDriver in headless mode."""
        print("🔧 Initializing Chrome WebDriver...")

        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run without opening Chrome window
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        # Initialize Chrome driver
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ WebDriver initialized successfully\n")
        except Exception as e:
            print(f"❌ Error initializing WebDriver: {e}")
            raise

        # List to store all scraped car dictionaries
        self.results = []

    # -----------------------------------------------------------------------

    def scrape_dubizzle_oman(self):
        """Scrape car listings from Dubizzle Oman (used and new cars)."""
        print("🚗 Scraping Dubizzle Oman...")
        url = "https://www.dubizzle.com.om/en/vehicles/cars/"

        try:
            # Open website and wait for JavaScript content to load
            self.driver.get(url)
            print(f"   Loaded: {url}")
            time.sleep(5)

            # Try several possible HTML selectors (depends on website version)
            selectors = [
                "//div[contains(@class, 'listing')]",
                "//article",
                "//div[contains(@class, 'card')]",
                "//li[contains(@class, 'item')]"
            ]

            listings = []
            for selector in selectors:
                try:
                    listings = self.driver.find_elements(By.XPATH, selector)
                    if len(listings) > 0:
                        print(f"   Found {len(listings)} listings with selector")
                        break
                except:
                    continue

            count = 0  # Number of successfully scraped cars

            for listing in listings[:20]:  # Limit to first 20 cars for efficiency
                try:
                    text = listing.text

                    # Filter out irrelevant blocks
                    if len(text) > 10 and any(brand.lower() in text.lower() for brand in
                                              ['toyota', 'nissan', 'honda', 'mazda', 'kia', 'hyundai']):

                        # Extract lines
                        lines = text.split('\n')
                        model = lines[0] if lines else 'Unknown'

                        # Extract price using regex (e.g., "OMR 5,000")
                        price_match = re.search(r'OMR\s*[\d,]+|[\d,]+\s*OMR', text, re.IGNORECASE)
                        price = price_match.group() if price_match else 'Contact for Price'

                        # Extract year (any 20xx format)
                        year_match = re.search(r'20\d{2}', text)
                        year = year_match.group() if year_match else 'N/A'

                        # Detect brand name from text
                        brand = 'Unknown'
                        for b in ['Toyota', 'Nissan', 'Honda', 'Mazda', 'Hyundai', 'Kia']:
                            if b.lower() in text.lower():
                                brand = b
                                break

                        # Create structured dictionary
                        car_data = {
                            'source': 'Dubizzle Oman',
                            'website': url,
                            'brand': brand,
                            'model': model[:50],
                            'price': price,
                            'year': year,
                            'condition': 'Used' if 'used' in text.lower() else 'New',
                            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }

                        self.results.append(car_data)
                        count += 1
                        print(f"   ✓ {brand} - {model[:30]}")

                        if count >= 10:  # Stop after 10 cars
                            break

                except Exception as e:
                    continue

            print(f"   ✅ Scraped {count} cars from Dubizzle Oman\n")

        except Exception as e:
            print(f"   ✗ Error: {e}")

    # -----------------------------------------------------------------------

    def scrape_toyota_oman(self):
        """Scrape car models from Toyota Oman official website."""
        print("🚗 Scraping Toyota Oman...")
        url = "https://www.toyotaoman.com/"

        try:
            self.driver.get(url)
            print(f"   Loaded: {url}")
            time.sleep(3)

            # Find links related to vehicle models
            vehicle_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/vehicles/') or contains(@href, '/models/')]")

            if not vehicle_links:
                # Fallback: search model names directly in page text
                page_text = self.driver.find_element(By.TAG_NAME, "body").text
                models = ['Camry', 'Land Cruiser', 'Hilux', 'RAV4', 'Corolla', 'Fortuner', 'Prado', 'Yaris']

                for model in models:
                    if model.lower() in page_text.lower():
                        self.results.append({
                            'source': 'Toyota Oman',
                            'website': url,
                            'brand': 'Toyota',
                            'model': f'Toyota {model} 2024',
                            'price': 'Contact Dealer',
                            'year': '2024',
                            'condition': 'New',
                            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        print(f"   ✓ Toyota {model}")
            else:
                # Extract models from found links
                for link in vehicle_links[:10]:
                    model_name = link.text.strip()
                    if len(model_name) > 2:
                        self.results.append({
                            'source': 'Toyota Oman',
                            'website': url,
                            'brand': 'Toyota',
                            'model': f'Toyota {model_name}',
                            'price': 'Contact Dealer',
                            'year': '2024',
                            'condition': 'New',
                            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        print(f"   ✓ Toyota {model_name}")

            print("   ✅ Toyota models scraped successfully\n")

        except Exception as e:
            print(f"   ✗ Error: {e}")

    # -----------------------------------------------------------------------

    def scrape_all(self):
        """Execute all scraping functions sequentially."""
        print("\n================ SCRAPING STARTED ================\n")
        self.scrape_dubizzle_oman()
        time.sleep(2)  # short pause to avoid overload
        self.scrape_toyota_oman()
        print("\n================ SCRAPING FINISHED ================\n")

    # -----------------------------------------------------------------------

    def save_to_json(self, filename='cars_data.json'):
        """Save scraped results to a JSON file with metadata."""
        data = {
            'metadata': {
                'total_cars': len(self.results),
                'scrape_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'sources': list(set([car['source'] for car in self.results]))
            },
            'cars': self.results
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Data saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")

    # -----------------------------------------------------------------------

    def display_results(self):
        """Print all scraped cars in a formatted table."""
        if not self.results:
            print("⚠️  No data scraped!")
            return

        print("\n📋 SCRAPED CAR DATA\n")
        print(f"{'No.':<5} {'Brand':<12} {'Model':<30} {'Price':<20} {'Year':<8}")
        print("-" * 90)

        for i, car in enumerate(self.results, 1):
            print(f"{i:<5} {car['brand']:<12} {car['model'][:28]:<30} {car['price'][:18]:<20} {car['year']:<8}")

        print("-" * 90)
        print(f"Total Cars: {len(self.results)}")

    # -----------------------------------------------------------------------

    def close(self):
        """Close the Selenium WebDriver."""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")


# ---------------------------------------------------------------------------

def main():
    """Main function that executes the entire scraping workflow."""
    print("""
╔══════════════════════════════════════════════════════╗
║        🚗 CAR SCRAPER - TP5 PROJECT 🚗              ║
╚══════════════════════════════════════════════════════╝
    """)

    try:
        scraper = CarScraper()
        scraper.scrape_all()       # Run both websites
        scraper.display_results()  # Show data in console
        scraper.save_to_json()     # Save to JSON file
        scraper.close()            # Close browser
        print("\n✅ SCRAPING COMPLETED SUCCESSFULLY!\n")

    except Exception as e:
        print(f"❌ Fatal error: {e}")


if __name__ == "__main__":
    main()
