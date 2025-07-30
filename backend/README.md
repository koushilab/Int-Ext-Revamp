# Houzz Professionals Extractor

A comprehensive Python script to extract professional contact information from Houzz.in across multiple categories including interior designers, civil engineers, contractors, and more.

## Features

- ✅ **8 Professional Categories**: Interior designers, civil engineers, design-build firms, kitchen & bath designers, landscape contractors, tile & stone professionals, furniture dealers, and flooring specialists
- ✅ **Complete Contact Data**: Name, phone, address, coordinates, social media links, websites
- ✅ **Smart Pagination**: Uses Houzz's `fi` parameter to extract all available professionals
- ✅ **Dual Output**: Saves data in both CSV and JSON formats
- ✅ **Anti-Bottleneck**: No cookie storage and proper rate limiting
- ✅ **Error Handling**: Continues extraction even if individual pages fail

## Quick Start

### 1. Create Virtual Environment

#### Windows:
```bash
# Create virtual environment
python -m venv houzz_env

# Activate virtual environment
houzz_env\Scripts\activate
```

#### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv houzz_env

# Activate virtual environment
source houzz_env/bin/activate
```

### 2. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 3. Run the Extractor

```bash
# Extract all professional categories
python extract_all_houzz_professionals.py
```

## Dependencies

The script requires the following Python packages:

- **aiohttp** (3.9.1+) - Async HTTP client for web scraping
- **beautifulsoup4** (4.12.2+) - HTML parsing and data extraction
- **lxml** (4.9.3+) - Fast XML/HTML parser for BeautifulSoup

All dependencies are automatically installed with:
```bash
pip install -r requirements.txt
```

## Output

The script creates the following directory structure:

```
houzz_data/
└── professionals/
    ├── interior-designers-and-decorators.csv
    ├── interior-designers-and-decorators.json
    ├── civil-engineers-and-contractors.csv
    ├── civil-engineers-and-contractors.json
    ├── design-build-firms.csv
    ├── design-build-firms.json
    ├── kitchen-and-bath-designers.csv
    ├── kitchen-and-bath-designers.json
    ├── landscape-architects-and-contractors.csv
    ├── landscape-architects-and-contractors.json
    ├── tile-stone-and-countertops.csv
    ├── tile-stone-and-countertops.json
    ├── furniture-and-accessories.csv
    ├── furniture-and-accessories.json
    ├── flooring-and-carpet.csv
    └── flooring-and-carpet.json
```

## CSV Data Structure

Each CSV file contains the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `name` | Professional/Company name | "ABC Interior Designs" |
| `telephone` | Contact phone number | "+91 98765 43210" |
| `image` | Profile image URL | "https://st.hzcdn.com/..." |
| `street_address` | Street address | "123 Design Street, Sector 5" |
| `city` | City name | "Mumbai" |
| `state` | State/Region | "Maharashtra" |
| `postal_code` | ZIP/Postal code | "400001" |
| `country` | Country code | "IN" |
| `full_address` | Complete formatted address | "123 Design Street, Mumbai, Maharashtra, 400001" |
| `latitude` | Geographic latitude | "19.0760" |
| `longitude` | Geographic longitude | "72.8777" |
| `area_served` | Service area | "Mumbai Metropolitan Area" |
| `facebook` | Facebook profile URL | "https://facebook.com/abc-designs" |
| `twitter` | Twitter profile URL | "https://twitter.com/abc_designs" |
| `linkedin` | LinkedIn profile URL | "https://linkedin.com/company/abc" |
| `website` | Company website | "https://abcdesigns.com" |
| `houzz_profile` | Houzz profile URL | "https://houzz.in/pro/abc-designs" |
| `category` | Professional category | "interior-designers" |

## Extracted Categories

The script extracts professionals from these 8 categories:

1. **Interior Designers & Decorators** (`probr0-bo~t_26677`)
2. **Civil Engineers & Contractors** (`probr0-bo~t_26731`)
3. **Design-Build Firms** (`probr0-bo~t_26721`)
4. **Kitchen & Bath Designers** (`probr0-bo~t_26687`)
5. **Landscape Architects & Contractors** (`probr0-bo~t_26678`)
6. **Tile, Stone & Countertops** (`probr0-bo~t_26701`)
7. **Furniture & Accessories** (`probr0-bo~t_26728`)
8. **Flooring & Carpet** (`probr0-bo~t_26718`)

## Usage Examples

### Extract All Categories (Default)
```bash
python extract_all_houzz_professionals.py
```

### Extract Specific Categories
To modify the script to extract only specific categories, edit the `main()` function:

```python
# Extract only interior designers and civil engineers
categories_to_extract = ["interior-designers", "civil-engineers"]
```

## Performance & Scalability

- **Rate Limiting**: 2-second delay between requests to avoid server overload
- **No Cookie Storage**: Uses `DummyCookieJar()` to prevent bottlenecks
- **Connection Limits**: 30 total connections, 10 per host
- **Pagination**: Up to 200 pages per category (3,000+ professionals each)
- **Memory Efficient**: Processes one category at a time

## Expected Results

Typical extraction yields:

- **Interior Designers**: 1,000-3,000 professionals
- **Civil Engineers**: 800-2,500 professionals
- **Design-Build Firms**: 500-1,500 professionals
- **Kitchen & Bath**: 600-2,000 professionals
- **Landscape**: 700-2,200 professionals
- **Tile & Stone**: 400-1,200 professionals
- **Furniture**: 500-1,500 professionals
- **Flooring**: 300-1,000 professionals

**Total Expected**: 4,800-15,900 professionals across all categories

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure virtual environment is activated and dependencies installed
   ```bash
   # Activate environment first
   houzz_env\Scripts\activate  # Windows
   source houzz_env/bin/activate  # macOS/Linux
   
   # Then install dependencies
   pip install -r requirements.txt
   ```

2. **Network Timeout**: Increase timeout in the script if you have a slow connection
3. **Too Few Results**: The script has built-in retry logic and will stop when no more data is available
4. **Permission Errors**: Run terminal as administrator (Windows) or use `sudo` (macOS/Linux) if needed

### Debug Mode

To see detailed logging, the script automatically provides INFO level logs. For more verbose output, modify the logging level:

```python
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
```

## System Requirements

- **Python**: 3.7 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 100MB for output files
- **Internet**: Stable broadband connection
- **OS**: Windows 10+, macOS 10.14+, or Linux

## Legal & Ethical Use

This tool is designed for legitimate business research and lead generation. Please ensure you:

- ✅ Respect Houzz's terms of service
- ✅ Use extracted data responsibly
- ✅ Don't overwhelm their servers (built-in rate limiting helps)
- ✅ Comply with local data protection laws (GDPR, CCPA, etc.)

## License

This project is for educational and business research purposes. Please use responsibly and in accordance with applicable laws and website terms of service.

---

**Happy Extracting!** 🏗️📊

For issues or questions, check the console output for detailed error messages and extraction progress.