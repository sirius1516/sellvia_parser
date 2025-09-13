# Web Scraping Pipeline for Product Data Extraction

A modular system for collecting product data from SellViaCatalog website with local HTML caching.

## ⚠️ Trial Version Notice

**This is a trial version of the parser** designed for testing and development purposes. The current implementation is limited to:

- **Only 2 product catalog pages** are being processed
- The website contains **over 2000 pages** of products
- This limited scope allows for:
  - Testing the scraping logic
  - Verifying data extraction accuracy
  - Adjusting delays and error handling
  - Ensuring compliance with website policies

## 🚀 Features

- **Two-phase process**: Link collection followed by data parsing
- **Local caching**: HTML pages saved to avoid repeated requests
- **Error handling**: Comprehensive exception handling system
- **Random delays**: To avoid blocking and respect server limits
- **Excel export**: Structured data saving with formatted columns
- **Modular architecture**: Each phase can be executed independently

## 📁 Project Structure

web_scraping/
├── main.py # Main script
├── item_links.xlsx # Generated file with product links
├── items.xlsx # Final file with product data
├── page_1.html # Locally saved HTML pages
├── page_2.html
└── ...

## ⚙️ Installation

```bash
pip install requests beautifulsoup4 pandas xlsxwriter
```

## 🎯 Usage

1. Collect Product Links
get_item_links()  # Creates item_links.xlsx
2. Download HTML Pages
download_pages()  # Saves page_*.html files
3. Parse Data from Local Files
get_item_info()   # Creates items.xlsx with product data

📊 Extracted Data
Product Title

* Sale Price

* Retail Price

* Save Amount

* Product Description

* Image URL

⚡ Functions
get_item_links()
 
  * Crawls catalog pages (default: 2 pages)

  * Extracts individual product links

  * Saves to item_links.xlsx

  * Includes 8-second delays between page requests
____________________________________________________________

download_pages()

  * Downloads HTML of each product page

  * Saves to local page_*.html files

  * Includes 7-second delays between requests

  * Uses proper User-Agent headers
____________________________________________________________

get_item_info()

  * Parses data from local HTML files

  * Extracts comprehensive product information

  * Saves to structured items.xlsx with formatted columns

  * Includes random delays (1-4 seconds) between parsing

🛡️ Protective Mechanisms
User-Agent headers: Browser simulation

Random delays: 1-4 seconds between parsing operations

Request timeouts: 5-second connection timeout

Exception handling: Graceful error recovery

Element validation: Fallback values ("Not found") for missing elements

## 📈 Configuration

# Number of Pages to Scan
max_page = 2  # In get_item_links() function

# Request Delays
time.sleep(7)                   # Fixed delay between downloads
time.sleep(random.uniform(1, 4))  # Random delay between parsing

# File Paths
- In get_item_links()
df.to_excel('item_links.xlsx', index=False)

- In get_item_info() 
book = xlsxwriter.Workbook(r'D:\web_scraping\projects\sellviacatalog\items.xlsx')

## 🐛 Debugging
For debugging, you can uncomment function calls individually:
# get_item_links()     # Link collection only
# download_pages()     # Page downloading only  
get_item_info()       # Parsing from local files only

## 📝 Logging
- The program provides detailed logging:

- Progress of each phase

- Number of processed pages

- Encountered errors

- Execution progress

## ⚠️ Important Notes
- Ensure the website allows scraping before running

- Adjust delays according to website's terms of service

- Regularly check CSS selector validity

- Keep local copies for debugging purposes

- Respect server resources and bandwidth

## 🔄 Modularity
- Each function operates independently:

- Run only link collection

- Run only page downloading

- Run only parsing of existing files

## 📊 Output Files
- item_links.xlsx - List of product URLs

- page_*.html - Local page copies for offline parsing

- items.xlsx - Final structured product data with formatting

## 🎨 Excel Formatting
- The output Excel file includes:

- Column width optimization

- Proper headers formatting

- Structured data organization

- Error value handling

## 🔧 Technical Details
- Python Version: 3.10+

- Dependencies: requests, BeautifulSoup4, pandas, xlsxwriter

- Encoding: UTF-8 support for international content

- Error Recovery: Continues processing after errors

## 📄 License
This project is for educational purposes. Always ensure compliance with website terms of service and legal regulations when web scraping.




