import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import re

# Telegram bot token and chat ID
TELEGRAM_TOKEN = 'Your_Telegram_Token'
CHAT_ID = 'Your_Chat_ID'

BASE_URL = 'https://www.youthall.com'
JOBS_URL = 'https://www.youthall.com/tr/jobs/'

# Keywords to filter jobs (including internships)
KEYWORDS = ['computer engineering', 'bilgisayar mühendisliği', 
            'developer', 'software','software developer', 'yazılım', 'bilgisayar', 'computer',
            'it', 'information technology', 'bilgi teknolojileri', 'programlama',
            'coder', 'kod', 'code','program']

# Headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Referer": "https://www.youthall.com/",
    "Connection": "keep-alive"
}

# Function to scrape job listings from Youthall with pagination
async def get_youthall_jobs():
    page_num = 1
    all_jobs = []
    max_pages = 5  # Limit to 5 pages to avoid too many requests
    
    while page_num <= max_pages:
        try:
            # Construct URL with page number
            current_url = f"{JOBS_URL}?page={page_num}" if page_num > 1 else JOBS_URL
            
            response = requests.get(current_url, headers=HEADERS, timeout=30)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs_on_page = []
            
            
            job_cards = soup.select('div.job-list-item, div.job-card, article.job-listing, div.p-listItem')
            
            
            if not job_cards:
                job_cards = soup.select('.jobs-list > div, ul.jobs-list > li, .job-container, .job, .listing-item')
            
            
            if not job_cards:
                job_cards = soup.select('[class*="job-"], [class*="posting"], [class*="vacancy"], [class*="listing"]')
            
            if not job_cards:
                all_links = soup.find_all('a', href=True)
                job_links = [link for link in all_links if '/job/' in link['href'] or '/position/' in link['href'] or '/ilan/' in link['href']]
                
                for link in job_links:
                    title = link.get_text().strip()
                    if not title:
                        nearby_heading = link.find_next(['h1', 'h2', 'h3', 'h4', 'h5'])
                        if nearby_heading:
                            title = nearby_heading.get_text().strip()
                    
                    if not title:
                        parent = link.parent
                        for i in range(3):  
                            if parent:
                                text = parent.get_text().strip()
                                if text and len(text) < 100:  
                                    title = text
                                    break
                                parent = parent.parent
                    
                    href = link['href']
                    if not href.startswith('http'):
                        href = BASE_URL + href
                    
                    
                    if title and any(re.search(r'\b' + re.escape(keyword.lower()) + r'\b', title.lower()) for keyword in KEYWORDS):
                        jobs_on_page.append({
                            'title': title,
                            'link': link,
                            'company': company
                        })
            
            
            for card in job_cards:
                title_elem = card.select_one('h2, h3, h4, .title, .job-title, [class*="title"]')
                company_elem = card.select_one('.company, .company-name, .employer, [class*="company"]')
                link_elem = card.select_one('a[href]')
                
                title = None
                if title_elem:
                    title = title_elem.get_text().strip()
                elif link_elem:
                    title = link_elem.get_text().strip()
                
                company = 'Not specified'
                if company_elem:
                    company = company_elem.get_text().strip()
                
                link = None
                if link_elem:
                    link = link_elem['href']
                    if not link.startswith('http'):
                        link = BASE_URL + link
                
                if title and link and any(keyword.lower() in title.lower() for keyword in KEYWORDS):
                    jobs_on_page.append({
                        'title': title,
                        'link': link,
                        'company': company
                    })
            
            all_jobs.extend(jobs_on_page)
            
            next_page = False
            
            pagination = soup.select_one('.pagination, .pager, [class*="pagination"]')
            if pagination:
                next_link = pagination.select_one(f'a[href*="page={page_num+1}"], a.next, a[rel="next"]')
                if next_link:
                    next_page = True
            
            if not next_page:
                page_regex = re.compile(r'Page\s+\d+\s+of\s+(\d+)|Sayfa\s+\d+\s+\/\s+(\d+)')
                page_match = page_regex.search(soup.get_text())
                if page_match:
                    total_pages = int(page_match.group(1) or page_match.group(2))
                    next_page = page_num < total_pages
            
            if not next_page and jobs_on_page:
                if page_num < max_pages:
                    next_page = True
            
            if not next_page or not jobs_on_page:
                break
            
            page_num += 1
            await asyncio.sleep(2)
            
        except Exception as e:
            break
    
    formatted_jobs = []
    for job in all_jobs:
        formatted_job = f"{job['title']}\nŞirket: {job['company']}\n{job['link']}"
        formatted_jobs.append(formatted_job)
    
    return formatted_jobs

def remove_duplicates(jobs):
    unique_jobs = []
    seen_links = set()
    
    for job in jobs:
        link = job.splitlines()[-1]
        
        if link not in seen_links:
            seen_links.add(link)
            unique_jobs.append(job)
    
    return unique_jobs

async def send_jobs():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        jobs = await get_youthall_jobs()
        
        unique_jobs = remove_duplicates(jobs)
        
        if not unique_jobs:
            await bot.send_message(chat_id=CHAT_ID, text="Şu anda uygun ilan bulunamadı. Website yapısı değişmiş olabilir.")
        else:
            await bot.send_message(
                chat_id=CHAT_ID, 
                text=f"Youthall'da {len(unique_jobs)} adet uygun ilan bulundu:"
            )
            
            batch_size = 5
            for i in range(0, len(unique_jobs), batch_size):
                batch = unique_jobs[i:i+batch_size]
                
                batch_message = "\n\n---\n\n".join(batch)
                await bot.send_message(chat_id=CHAT_ID, text=batch_message)
                await asyncio.sleep(2)
    
    except Exception as e:
        pass

async def main():
    await send_jobs()

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
