# Y Combinator Directory Scraper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A Python scraper for extracting company data from the [Y Combinator directory](https://www.ycombinator.com/companies/), featuring an interactive web-based explorer.

## Features

- 🚀 **User-Friendly Selenium Scraping**: No API keys required - just Firefox and geckodriver
- 💾 **30-Day URL Caching**: Avoid unnecessary re-scraping
- 🔄 **Checkpoint/Resume**: Recover from interrupted scrapes
- 🎯 **Flexible Batch Filtering**: Select specific batches or recent N batches
- 🌐 **Interactive Web Explorer**: Browse and filter companies with a sleek UI
- 📊 **Rich Dataset**: Includes founder profiles with bios and social links

## About Y Combinator

Y Combinator is a startup accelerator that has invested in over 4,000 companies with a combined valuation exceeding $600B. Notable alumni include Airbnb, Stripe, DoorDash, Coinbase, and Reddit.

## Requirements

- **Python**: 3.10 or higher
- **Browser**: [Firefox](https://www.mozilla.org/en-US/firefox/new/)
- **WebDriver**: [geckodriver](https://github.com/mozilla/geckodriver/releases)

### Installing geckodriver

**macOS**:
```bash
brew install geckodriver
```

**Linux**:
```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz
tar -xvzf geckodriver-v0.35.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
```

**Windows**:
Download from [GitHub releases](https://github.com/mozilla/geckodriver/releases) and add to PATH.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/corralm/yc-scraper.git
   cd yc-scraper
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   python -m pip install -r requirements.txt
   ```

## Usage

### Quick Start

```bash
# Step 1: Extract company URLs (takes 10-15 minutes)
python yc_links_extractor.py

# Step 2: Scrape company data
cd scrapy-project
python -m scrapy runspider ycombinator/spiders/yscraper.py -o output.jl

# Step 3: Analyze data with Pandas
python -c "import pandas as pd; df = pd.read_json('output.jl', lines=True); print(df.head())"
```

### Step 1: Extract Company URLs

```bash
python yc_links_extractor.py
```

This script:
- Opens the YC directory in headless Firefox
- Iterates through all batch filters (Summer 2007 - present)
- Collects unique company URLs
- Saves to `scrapy-project/ycombinator/start_urls.txt`

### Step 2: Scrape Company Data

```bash
cd scrapy-project
python -m scrapy runspider ycombinator/spiders/yscraper.py -o output.jl
```

**Supported output formats**:
- JSON Lines (`.jl`) - Recommended for large datasets
- JSON (`.json`) - Standard JSON array
- CSV (`.csv`) - Spreadsheet format

### Step 3: Analyze Data

```python
import pandas as pd

# Load data
df = pd.read_json('output.jl', lines=True)

# Basic statistics
print(f"Total companies: {len(df)}")
print(f"Active companies: {len(df[df['status'] == 'Active'])}")

# Top industries
print("\nTop 10 Industries:")
print(df['tags'].explode().value_counts().head(10))

# Geographic distribution
print("\nTop 10 Locations:")
print(df['location'].value_counts().head(10))
```

### Optional: Launch Web Explorer

After scraping, you can launch an interactive web-based explorer:

```bash
# Convert scraped data to JSON format for the web UI
python scripts/convert_output_to_json.py

# Launch local web server
python -m http.server 3000
```

Then open [http://localhost:3000](http://localhost:3000) in your browser.

**Web Explorer Features:**
- 🔍 Real-time search and filtering by batch, tags, and keywords
- 📊 Sortable directory with ascending/descending options
- 👥 Full founder profiles with bios and social links
- 📥 Export filtered results as JSON
- ⚡ Lazy loading for smooth performance with thousands of companies

## Data Schema

| Attribute         | Description                       | Type   |
|-------------------|-----------------------------------|--------|
| company_id        | Company ID provided by YC         | int    |
| company_name      | Company name                      | string |
| short_description | One-line description              | string |
| long_description  | Full company description          | string |
| batch             | YC batch (e.g., "W23", "S24")     | string |
| status            | Active, Inactive, Public, etc.    | string |
| tags              | Industry tags                     | list   |
| location          | City                              | string |
| country           | Country code                      | string |
| year_founded      | Year founded                      | int    |
| num_founders      | Number of founders                | int    |
| founders_names    | List of founder names             | list   |
| founder_details   | Extended bios and social links    | list   |
| team_size         | Number of employees               | int    |
| website           | Company website                   | string |
| cb_url            | Crunchbase URL                    | string |
| linkedin_url      | LinkedIn URL                      | string |

## Example Output

| company_id | company_name | batch | status | location      | year_founded | team_size |
|------------|--------------|-------|--------|---------------|--------------|-----------|
| 240        | Stripe       | S09   | Active | San Francisco | 2010         | 7000      |
| 271        | Airbnb       | W09   | Public | San Francisco | 2008         | 6132      |
| 325        | Dropbox      | S07   | Public | San Francisco | 2008         | 4000      |
| 439        | Coinbase     | S12   | Public | San Francisco | 2012         | 6112      |
| 531        | DoorDash     | S13   | Public | San Francisco | 2013         | 8600      |

## Troubleshooting

**Issue**: `WebDriverException: 'geckodriver' executable needs to be in PATH`

**Solution**: 
```bash
brew install geckodriver  # macOS
geckodriver --version     # Verify installation
```

---

**Issue**: `FileNotFoundError: Start URLs file not found`

**Solution**: Run `python yc_links_extractor.py` first to generate the URLs file.

---

**Issue**: `ModuleNotFoundError: No module named 'pkg_resources'` when running `scrapy`

**Solution**: Run Scrapy through the active Python environment instead of a shell-resolved executable:

```bash
cd scrapy-project
python -m scrapy runspider ycombinator/spiders/yscraper.py -o output.jl
```

If you use Conda and `which scrapy` points to an Anaconda path while your virtualenv is active, reinstall with `python -m pip install -r requirements.txt` and keep using `python -m scrapy`.

---

**Issue**: Scraper gets stuck or times out

**Solution**:
- Check your internet connection
- Verify Firefox isn't already running
- Ensure YC website is accessible: `curl https://www.ycombinator.com/companies`

### Debug Mode

Enable verbose logging:

```bash
LOGLEVEL=DEBUG python yc_links_extractor.py
```

## Data Analysis Examples

### Companies by Batch

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json('output.jl', lines=True)
active = df[df['status'] == 'Active']

batch_counts = active['batch'].value_counts().sort_index()
batch_counts.plot(kind='bar', figsize=(15, 5))
plt.title('Active YC Companies by Batch')
plt.show()
```

### Industry Trends

```python
# Most common industries
tags = df['tags'].explode()
top_15 = tags.value_counts().head(15)
print(top_15)
```

### Geographic Analysis

```python
# Companies by country
countries = df['country'].value_counts()
print(countries.head(10))
```

## Dataset

For a pre-scraped dataset, check out [Y Combinator Directory on Kaggle](https://www.kaggle.com/datasets/miguelcorraljr/y-combinator-directory).

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributors

**Original Author**: Miguel Corral Jr.
- Email: corraljrmiguel@gmail.com
- LinkedIn: [linkedin.com/in/imiguel](https://www.linkedin.com/in/imiguel)
- GitHub: [github.com/corralm](https://github.com/corralm)

**Web Explorer Contributor**: Tario You
- LinkedIn: [linkedin.com/in/tario-you](https://linkedin.com/in/tario-you)
- Contributions: Interactive web UI, enhanced founder profiles

---

**Last Updated**: October 2025
