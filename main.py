import os
import time
import requests
import textwrap
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import markdown2
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pdfkit
import google.generativeai as genai

# .env dosyasını yükle
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
WKHTMLTOPDF_PATH = os.getenv("PDFKIT_PATH")
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
genai.configure(api_key=GENAI_API_KEY)

BLOCKED_DOMAINS = ["zhihu.com", "quora.com", "pinterest.com", "facebook.com", "instagram.com"]

def bing_search(query, max_results=5):
    print("🔍 Searching Bing...")
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"q": query}
    html = requests.get("https://www.bing.com/search", params=params, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for a in soup.select("li.b_algo h2 a"):
        href = a.get("href")
        if href and href.startswith("http") and not any(block in href for block in BLOCKED_DOMAINS):
            results.append(href)
        if len(results) >= max_results:
            break
    return results

def fetch_page_content(url):
    try:
        print(f"- Fetching: {url}")
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        return response.text if response.status_code == 200 else None
    except:
        return None

def extract_main_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in ['script', 'style', 'header', 'footer', 'nav', 'aside', 'form']:
        for element in soup.find_all(tag):
            element.decompose()
    main = soup.find(['main', 'article', 'section', 'div']) or soup.body
    return ' '.join(main.stripped_strings)[:10000] if main else None

def summarize_text(text):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        response = model.generate_content(f"Summarize this in 3 paragraphs:\n\n{text}")
        return response.text.strip()
    except Exception as e:
        return f"❌ Error summarizing content: {e}"

def take_screenshot(url, filename):
    driver = None
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(60)

        print(f"🚀 Opening URL: {url}")
        driver.get(url)
        print(f"Page title: {driver.title}")

        try:
            
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.TAG_NAME, 'main'))
            )
        except:
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.TAG_NAME, 'body'))
            )
        
        time.sleep(5)  

        driver.save_screenshot(filename)
        print(f"📸 Screenshot saved: {filename}")
        return True
    except Exception as e:
        print(f"❌ Screenshot error for {url}: {e}")
        return False
    finally:
        if driver:
            driver.quit()

def generate_markdown_report(keyword, summaries):
    lines = [
        f"# Research Report for: {keyword}",
        f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}",
        f"**Sources Found:** {len(summaries)}",
        "## Summaries\n"
    ]
    for i, (url, summary) in enumerate(summaries, 1):
        lines.extend([
            f"### Source {i}",
            f"- **URL:** {url}",
            f"- **Summary:**\n{textwrap.fill(summary, width=100)}\n"
        ])
    return "\n".join(lines)

def save_pdf(markdown_text, filename):
    html = markdown2.markdown(markdown_text)
    pdfkit.from_string(html, filename, configuration=PDFKIT_CONFIG)
    print(f"✅ PDF saved as {filename}")

def main():
    keyword = input("🔑 Enter your search keyword: ")
    urls = bing_search(keyword)
    if not urls:
        print("❌ No valid search results.")
        return

    os.makedirs("screenshots", exist_ok=True)
    summaries = []

    print("🌐 Fetching and processing websites...")
    for i, url in enumerate(urls, 0):
        html = fetch_page_content(url)
        if not html:
            summaries.append((url, "❌ Could not fetch content."))
            continue

        text = extract_main_text(html)
        if not text or len(text) < 10:
            summaries.append((url, "⚠️ Not enough readable content."))
            continue

        screenshot_path = f"screenshots/site_{i}.png"
        take_screenshot(url, screenshot_path)
        summary = summarize_text(text)
        summaries.append((url, summary))

    if not summaries:
        print("❌ No summaries could be generated.")
        return

    print("📝 Generating final report...")
    markdown_report = generate_markdown_report(keyword, summaries)
    pdf_filename = f"{keyword.replace(' ', '_')}_report.pdf"
    save_pdf(markdown_report, pdf_filename)

if __name__ == "__main__":
    main()
