# Canvas Web Scraper

  A Python web scraper using Selenium that automates the downloading of videos and PDFs from your class Canvas pages. It organizes the files into separate folders based on modules, allowing you to continue studying even after the semester ends. The scraper supports multi-threading, enabling users to scrape multiple classes simultaneously, given that all classes follow the same HTML structure.

# Features

  Automated Scraping: Fetches videos and PDFs from your Canvas courses.
  
  Module-Based Organization: Saves files into structured folders based on modules.
  
  Multi-Threading Support: Scrape multiple classes concurrently.
  
  Persistence: Ensures access to class materials even after the semester concludes.

# Requirements

  Python 3.7 >
  
  Selenium-Wire
  
  `pip install selenium-wire`
  
  WebDriver for your browser (e.g., ChromeDriver for Google Chrome)

# Installation

  Clone the repository:

  `git clone https://github.com/your-username/canvas-web-scraper.git`

# Install dependencies:

`pip install -r requirements.txt`
  
Download the appropriate WebDriver for your browser and place it in your system's PATH or the project folder.

# Usage

  Configure your login details with a .env file
  
  Run the scraper:
  
  `python scraper.py`
  
  The downloaded files will be stored in organized module-based folders.
