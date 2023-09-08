# Price Tracker

This is a simple Python script for tracking product prices on Amazon and generating a report in JSON format. It uses Selenium for web scraping to retrieve product information.

## Features

- Searches for products on Amazon based on a search term and price range.
- Retrieves product details such as title, seller, and price.
- Generates a report containing the search results and saves it in a JSON file.

## Prerequisites

Before using this script, ensure you have the following:

- Python 3.x installed.
- Chrome web browser installed.
- Python packages listed in `requirements.txt` installed.

## Getting Started

1. Clone this repository to your local machine.
2. Install the required Python packages using pip:

   ```
   pip install -r requirements.txt
   ```

3. Open `price_tracker.py` and configure the following variables at the end of the script:

   - `name`: The name of your search.
   - `filters`: Minimum and maximum price range for filtering products.
   - `base_url`: The Amazon website URL you want to scrape (e.g., amazon.com).
   - `currency`: The currency in which prices should be displayed.

4. Run the script:

   ```
   python price_tracker.py
   ```

5. The script will scrape Amazon for products matching your search criteria and generate a JSON report with product details.

## Report Output

The generated JSON report will contain the following information:

- `title`: The name of the search.
- `date`: The date and time when the report was created.
- `best_item`: Information about the product with the lowest price.
- `products`: A list of products found during the search, including ASIN, URL, title, seller, and price.

## Notes

- This script is for educational purposes and should be used responsibly and in compliance with Amazon's terms of service.
- Web scraping may be subject to legal restrictions, so make sure to review and comply with the website's terms and conditions and robots.txt file.
- Be considerate of Amazon's server resources and avoid making too many requests in a short period of time.

Feel free to modify and customize this script to suit your specific needs!
