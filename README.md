# TripAdvisor Vacation Rental Data Scraping

## Overview

This project consists of two Scrapy spiders designed to scrape vacation rental data from TripAdvisor. The spiders utilize Selenium to handle dynamic content, enabling the extraction of detailed information about vacation rentals and related places. The data is then stored in a MongoDB database for further analysis or usage.

## Spiders

### Spider 1: `TripadvisorLvSpider`

This spider is responsible for scraping vacation rental information from TripAdvisor. It navigates through multiple pages of vacation rentals in Tokyo, extracts data like property name, type, bedrooms, bathrooms, guests allowed, reviews, URLs, and image URLs. The extracted data is stored in a MongoDB collection.

### Spider 2: `TripadvisorPvSpider`

The purpose of this spider is to gather additional information about vacation rental places. It takes the URLs stored in the previous MongoDB collection, navigates to each URL using Selenium, and extracts place overview, amenities, and things to know data. The collected data is stored in a separate MongoDB collection for comprehensive analysis.

## Prerequisites

- Python 3.x
- Scrapy
- Selenium
- MongoDB

## Setup

1. Install the required dependencies using the following command:
   ```
   pip install scrapy selenium pymongo
   ```

2. Download the appropriate version of the ChromeDriver executable and set its path in the `DRIVER_FILE_PATH` variable in both spider scripts.

3. Adjust the `USER_AGENT_LIST` in both spider scripts if desired.

4. Make sure your MongoDB server is running and accessible.

## Usage

1. **Running Spider 1:**
   - Navigate to the directory containing `tripadvisor_lv.py`.
   - Run the spider using the following command:
     ```
     scrapy crawl tripadvisor_lv
     ```
   - Spider 1 will scrape vacation rental data and store it in the specified MongoDB collection.

2. **Running Spider 2:**
   - After running Spider 1, navigate to the directory containing `tripadvisor_pv.py`.
   - Run the spider using the following command:
     ```
     scrapy crawl tripadvisor_pv
     ```
   - Spider 2 will extract additional information about vacation rental places and store it in a separate MongoDB collection.

## Notes

- These spiders are designed for educational and informational purposes. Always review and adhere to the website's terms of use and scraping guidelines.
- Be prepared to adapt the spiders if TripAdvisor's website structure changes.
