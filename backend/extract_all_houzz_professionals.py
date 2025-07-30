#!/usr/bin/env python3
"""
Multi-Category Houzz Professionals Extractor
Extracts data from all professional categories using fi pagination
"""

import asyncio
import aiohttp
import json
import csv
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ProfessionalData:
    """Data class for professional information"""
    name: str = ""
    telephone: str = ""
    image: str = ""
    street_address: str = ""
    city: str = ""
    state: str = ""
    postal_code: str = ""
    country: str = ""
    latitude: str = ""
    longitude: str = ""
    area_served: str = ""
    facebook: str = ""
    twitter: str = ""
    linkedin: str = ""
    website: str = ""
    houzz_profile: str = ""
    full_address: str = ""
    category: str = ""

class HouzzMultiCategoryExtractor:
    def __init__(self):
        self.base_url = "https://www.houzz.in"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Category mappings - All Professional Categories
        self.categories = {
            "interior-designers": {
                "url_path": "/professionals/interior-designers-and-decorators/probr0-bo~t_26677",
                "filename": "interior-designers-and-decorators.csv"
            },
            "civil-engineers": {
                "url_path": "/professionals/civil-engineers-and-contractors/probr0-bo~t_26731",
                "filename": "civil-engineers-and-contractors.csv"
            },
            "design-build": {
                "url_path": "/professionals/design-build-firms/probr0-bo~t_26721",
                "filename": "design-build-firms.csv"
            },
            "kitchen-bath": {
                "url_path": "/professionals/kitchen-and-bath-designers/probr0-bo~t_26687",
                "filename": "kitchen-and-bath-designers.csv"
            },
            "landscape": {
                "url_path": "/professionals/landscape-architects-and-contractors/probr0-bo~t_26678",
                "filename": "landscape-architects-and-contractors.csv"
            },
            "tile-stone": {
                "url_path": "/professionals/tile-stone-and-countertops/probr0-bo~t_26701",
                "filename": "tile-stone-and-countertops.csv"
            },
            "furniture": {
                "url_path": "/professionals/furniture-and-accessories/probr0-bo~t_26728",
                "filename": "furniture-and-accessories.csv"
            },
            "flooring": {
                "url_path": "/professionals/flooring-and-carpet/probr0-bo~t_26718",
                "filename": "flooring-and-carpet.csv"
            }
        }
    
    async def extract_json_ld_from_page(self, url: str) -> List[Dict]:
        """Extract all JSON-LD LocalBusiness data from a page"""
        try:
            # Create session with no cookies and additional headers to avoid bottlenecks
            connector = aiohttp.TCPConnector(limit=30, limit_per_host=10)
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=45),
                headers=self.headers,
                connector=connector,
                cookie_jar=aiohttp.DummyCookieJar()  # Prevent cookie storage
            ) as session:
                
                async with session.get(url) as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch {url}: HTTP {response.status}")
                        return []
                    
                    html = await response.text()
                    logger.info(f"Fetched page: {url} ({len(html):,} chars)")
                    
                    # Parse HTML
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Find all JSON-LD scripts
                    json_scripts = soup.find_all('script', type='application/ld+json')
                    logger.info(f"Found {len(json_scripts)} JSON-LD scripts")
                    
                    businesses = []
                    for script in json_scripts:
                        try:
                            if script.string:
                                data = json.loads(script.string.strip())
                                if isinstance(data, dict) and data.get('@type') == 'LocalBusiness':
                                    businesses.append(data)
                                    logger.debug(f"Found LocalBusiness: {data.get('name', 'Unknown')}")
                        except json.JSONDecodeError as e:
                            logger.error(f"JSON decode error: {e}")
                            continue
                    
                    return businesses
                    
        except Exception as e:
            logger.error(f"Error extracting from {url}: {e}")
            return []
    
    def parse_business_data(self, business: Dict, category: str) -> ProfessionalData:
        """Parse JSON-LD LocalBusiness data into ProfessionalData"""
        professional = ProfessionalData()
        
        # Basic info
        professional.name = business.get('name', '')
        professional.telephone = business.get('telephone', '')
        professional.image = business.get('image', '')
        professional.category = category
        
        # Address
        address = business.get('address', {})
        if isinstance(address, dict):
            professional.street_address = address.get('streetAddress', '')
            professional.city = address.get('addressLocality', '')
            professional.state = address.get('addressRegion', '')
            professional.postal_code = address.get('postalCode', '')
            professional.country = address.get('addressCountry', '')
            
            # Build full address
            address_parts = []
            for part in [professional.street_address, professional.city, professional.state, professional.postal_code]:
                if part:
                    address_parts.append(part)
            professional.full_address = ', '.join(address_parts)
        
        # Geo coordinates
        geo = business.get('geo', {})
        if isinstance(geo, dict):
            professional.latitude = str(geo.get('latitude', ''))
            professional.longitude = str(geo.get('longitude', ''))
        
        # Area served
        area_served = business.get('areaServed', {})
        if isinstance(area_served, dict):
            professional.area_served = area_served.get('name', '')
        
        # Social media and links
        same_as = business.get('sameAs', [])
        if isinstance(same_as, list):
            for link in same_as:
                if 'facebook.com' in link:
                    professional.facebook = link
                elif 'twitter.com' in link:
                    professional.twitter = link
                elif 'linkedin.com' in link:
                    professional.linkedin = link
                elif 'houzz.in' in link:
                    professional.houzz_profile = link
                elif any(domain in link for domain in ['.com', '.in', '.org', '.net']):
                    if not professional.website:  # Take first non-social website
                        professional.website = link
        
        return professional
    
    async def extract_category_professionals(self, category_key: str, category_info: Dict) -> List[ProfessionalData]:
        """Extract all professionals from a specific category"""
        category_url = f"{self.base_url}{category_info['url_path']}"
        all_professionals = []
        
        logger.info(f"🔍 Starting extraction for {category_key}")
        logger.info(f"📍 URL: {category_url}")
        
        # Extract from first page
        businesses = await self.extract_json_ld_from_page(category_url)
        
        for business in businesses:
            professional = self.parse_business_data(business, category_key)
            if professional.name:  # Only add if we have a name
                all_professionals.append(professional)
        
        logger.info(f"✅ Found {len(all_professionals)} professionals on first page of {category_key}")
        
        # Try additional pages using fi parameter
        professionals_per_page = 15
        max_pages = 200  # Increased limit to get more professionals
        
        for page_num in range(1, max_pages):
            fi_value = page_num * professionals_per_page
            page_url = f"{category_url}?fi={fi_value}"
            
            logger.info(f"🔍 {category_key} - Page {page_num + 1} (fi={fi_value})")
            
            businesses = await self.extract_json_ld_from_page(page_url)
            
            if not businesses:
                logger.info(f"No more data for {category_key} on page {page_num + 1}")
                break
            
            page_professionals = []
            for business in businesses:
                professional = self.parse_business_data(business, category_key)
                if professional.name:
                    page_professionals.append(professional)
            
            all_professionals.extend(page_professionals)
            logger.info(f"✅ {category_key} - Found {len(page_professionals)} professionals on page {page_num + 1}")
            
            # If fewer results than expected, we might be near the end
            if len(page_professionals) < professionals_per_page:
                logger.info(f"{category_key} - Fewer results on page {page_num + 1}, likely reached end")
                break
            
            # Rate limiting - increased delay to avoid bottlenecks
            await asyncio.sleep(2)
        
        # Remove duplicates
        unique_professionals = []
        seen = set()
        
        for prof in all_professionals:
            # Use phone as primary key, fallback to name
            key = prof.telephone if prof.telephone else prof.name.lower()
            if key and key not in seen:
                unique_professionals.append(prof)
                seen.add(key)
        
        logger.info(f"🎯 {category_key} - Total unique professionals: {len(unique_professionals)}")
        return unique_professionals
    
    def save_to_csv(self, professionals: List[ProfessionalData], filename: str):
        """Save professionals data to CSV"""
        output_dir = Path("houzz_data/professionals")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        csv_path = output_dir / filename
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'name', 'telephone', 'image', 'street_address', 'city', 'state', 
                'postal_code', 'country', 'full_address', 'latitude', 'longitude', 
                'area_served', 'facebook', 'twitter', 'linkedin', 'website', 
                'houzz_profile', 'category'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for professional in professionals:
                writer.writerow(asdict(professional))
        
        logger.info(f"💾 Saved {len(professionals)} professionals to {csv_path}")
        return csv_path
    
    def save_to_json(self, professionals: List[ProfessionalData], filename: str):
        """Save professionals data to JSON"""
        output_dir = Path("houzz_data/professionals")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        json_filename = filename.replace('.csv', '.json')
        json_path = output_dir / json_filename
        
        data = [asdict(professional) for professional in professionals]
        
        with open(json_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Saved {len(professionals)} professionals to {json_path}")
        return json_path
    
    async def extract_all_categories(self, selected_categories: List[str] = None):
        """Extract professionals from all or selected categories"""
        if selected_categories is None:
            selected_categories = list(self.categories.keys())
        
        print("� HOUZZ INTERIOR DESIGNERS & DECORATORS EXTRACTOR")
        print("=" * 60)
        print(f"Extracting data from interior designers category:")
        for cat in selected_categories:
            print(f"  • {cat}")
        print("=" * 60)
        
        all_results = {}
        
        for category_key in selected_categories:
            if category_key not in self.categories:
                logger.warning(f"Unknown category: {category_key}")
                continue
            
            category_info = self.categories[category_key]
            
            try:
                # Extract professionals for this category
                professionals = await self.extract_category_professionals(category_key, category_info)
                
                if professionals:
                    # Save to both CSV and JSON
                    csv_path = self.save_to_csv(professionals, category_info['filename'])
                    json_path = self.save_to_json(professionals, category_info['filename'])
                    all_results[category_key] = {
                        'count': len(professionals),
                        'csv_file': csv_path,
                        'json_file': json_path,
                        'professionals': professionals
                    }
                    
                    print(f"\n✅ {category_key.upper()}: {len(professionals)} professionals")
                    print(f"   📁 CSV: {category_info['filename']}")
                    print(f"   📁 JSON: {category_info['filename'].replace('.csv', '.json')}")
                    
                    # Show sample data
                    for i, prof in enumerate(professionals[:2], 1):
                        print(f"   {i}. {prof.name}")
                        if prof.telephone:
                            print(f"      📞 {prof.telephone}")
                        if prof.full_address:
                            print(f"      📍 {prof.full_address}")
                
                else:
                    print(f"\n❌ {category_key.upper()}: No professionals found")
                
            except Exception as e:
                logger.error(f"Error extracting {category_key}: {e}")
                print(f"\n❌ {category_key.upper()}: Error during extraction")
            
            # Delay between categories
            await asyncio.sleep(2)
        
        # Summary
        print(f"\n🎉 EXTRACTION COMPLETED!")
        print(f"📊 SUMMARY:")
        total_professionals = sum(result['count'] for result in all_results.values())
        print(f"   Total professionals extracted: {total_professionals}")
        print(f"   Categories processed: {len(all_results)}")
        print(f"\n📁 FILES CREATED:")
        for category, result in all_results.items():
            print(f"   • {result['csv_file'].name}: {result['count']} professionals (CSV)")
            print(f"   • {result['json_file'].name}: {result['count']} professionals (JSON)")
        
        return all_results

async def main():
    """Main extraction function"""
    extractor = HouzzMultiCategoryExtractor()
    
    # Extract ALL categories
    categories_to_extract = None  # This will extract all categories
    
    try:
        results = await extractor.extract_all_categories(categories_to_extract)
        
        if results:
            print(f"\n🎯 Extraction successful! Check the houzz_data/professionals/ directory for CSV files.")
        else:
            print(f"\n❌ No data extracted. Check your internet connection and try again.")
            
    except KeyboardInterrupt:
        print(f"\n❌ Extraction interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        logger.error(f"Main extraction failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())