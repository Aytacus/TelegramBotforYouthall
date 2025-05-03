# Youthall Job Scraper & Telegram Bot

## 📌 Purpose
This project is designed to filter **job listings** related to **Computer Engineering** and **Software Development** positions on **Youthall** and send them via a **Telegram bot**. The bot allows users to directly access the job listings and application links, simplifying the process of finding and applying for jobs.

## 🚀 Features
- Automatically scrapes job listings from **Youthall**.
- Filters job listings based on specific keywords.
- Sends job details (title, company, and application link) to a **Telegram bot**.
- Sends job notifications in batches to avoid spamming users.

## 🔧 Technologies
- **Python** – The main programming language for the project
- **BeautifulSoup** – For scraping job listings from HTML pages
- **Requests** – For making HTTP requests
- **Telegram Bot API** – To send messages via Telegram
- **Regex (Regular Expressions)** – To filter job titles based on keywords

## 📝 Usage

### 1. Prerequisites
- Python 3.x
- Install the necessary Python packages by running:

```bash
pip install requests beautifulsoup4 python-telegram-bot
```
### 2. Create a Telegram Bot
- Create a new bot via BotFather.
- Obtain the token for your bot.
- Get the chat ID for the Telegram group or individual chat.
### 3. Configuration
- Edit the bot.py file and configure the Telegram token and chat ID values as follows:

``` python
TELEGRAM_TOKEN = 'Your_Telegram_Token'  # Replace with your bot's token
CHAT_ID = 'Your_Chat_ID'  # Replace with your chat ID
```
### 4. Running the Bot
- Run the bot using the following command:

```bash
python bot.py
```
## 🔍 Keywords (KEYWORDS)
The bot filters job listings based on the following keywords:
- **Computer Engineering**
- **Software Developer**
- **Developer**
- **Software Engineer**
- **Programmer**
- **IT**

These keywords are defined in the KEYWORDS list, and only job listings containing these keywords in the title will be sent to Telegram.
``` python
KEYWORDS = ['computer engineering', 'bilgisayar mühendisliği', 'developer', 'software', 'software developer', 'yazılım', 'bilgisayar', 'computer', 'it', 'information technology', 'bilgi teknolojileri', 'programlama', 'coder', 'kod', 'code', 'program']
```
## ⚙️ How It Works
- **Job Scraping:** The bot scrapes job listings from the Youthall website using BeautifulSoup to parse the page content.

- **Job Filtering:** Listings are filtered based on the defined keywords. Only job titles that match the keywords are sent to the Telegram bot.

- **Telegram Notification:** Filtered job listings are sent to the Telegram bot, including the job title, company name, and application link.

- **Duplicate Removal:** The bot removes duplicate job listings by checking for previously sent links.

## 🛠️ Future Plans

- **Add More Filtering Options**:  
  Enhance the filtering system to allow for more specific job searches. For example, add options to filter by **experience level** (e.g., entry-level, mid-level, senior), **job type** (e.g., part-time, full-time, freelance), **location**, and **industry**. This will allow users to find the most relevant job opportunities based on their individual preferences.

- **Make the Bot More Personalized**:  
  Allow the bot to send personalized job recommendations to users. This could be based on their previously expressed preferences (e.g., preferred job titles, skills, and experience levels). Each user could receive tailored job suggestions that match their profile, enhancing their experience and making the bot more useful.

- **Improve Adaptability to Website Changes**:  
  Build a more flexible scraping system that can adapt to potential changes in the website's structure. This includes implementing more robust checks for finding job listings, error handling, and automatic updates to the scraping logic when necessary. This will ensure that the bot remains functional even if the Youthall website updates its layout or structure.

- **Enhance Job Filtering**:  
  Improve the current filtering system by implementing more sophisticated algorithms. This could involve:
  - Advanced **regular expressions** to better match job titles, descriptions, and categories.
  - Multiple **keyword categories** such as job type, experience level, and location for more granular filtering.
  - Exclusion of less relevant roles (e.g., internships, junior positions) based on user preferences.
  - Implementing a **ranking system** to prioritize job listings based on relevance or user preferences.

By implementing these features, the bot will become more adaptable, personalized, and efficient in filtering job listings, improving user satisfaction and engagement.
***This code was written by Yücel Aytaç Akgün.***
