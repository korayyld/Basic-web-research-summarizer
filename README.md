🧠 Web Research Summarizer
This Python project automates web research by:

Performing a Bing search on a user-defined keyword

Extracting and cleaning meaningful content from the top search results

Generating summaries using Google's Gemini LLM API

Taking screenshots of each site visited using Selenium

Creating a structured, printable PDF report from Markdown

📌 Features
🌐 Bing-based web search

🧹 Intelligent content extraction and cleaning

🤖 Summarization with Gemini LLM (Google Generative AI API)

📸 Automated webpage screenshots with Selenium

📝 PDF report generation from Markdown using pdfkit

🗂 Screenshot storage for auditing and visual inspection

🚀 Getting Started
1. Clone the Repository
bash
Kopyala
Düzenle
git clone https://github.com/yourusername/web-research-summarizer.git
cd web-research-summarizer
2. Install Dependencies
bash
Kopyala
Düzenle
pip install -r requirements.txt
3. Set Up Environment Variables
Create a .env file in the project root:

ini
Kopyala
Düzenle
GENAI_API_KEY=your_actual_genai_api_key
PDFKIT_PATH=/usr/local/bin/wkhtmltopdf  # Update based on your OS
You can refer to .env.example for the required variables.

🗂 Project Structure
bash
Kopyala
Düzenle
web-research-summarizer/
│
├── main.py               # Main script for automation
├── .env.example          # Environment variable template
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
└── screenshots/          # Stores screenshots of visited pages
🖼️ Screenshots Folder
During execution, the screenshots/ folder is automatically populated:

Kopyala
Düzenle
screenshots/
├── site_0.png
├── site_1.png
├── site_2.png
These are used for:

Verifying content sources

Manual inspection

Optional future enhancements to PDF reports

🛠 Dependencies
Make sure you have:

Python 3.8+

wkhtmltopdf installed and accessible (used by pdfkit)

Google GenAI API access (for summarization)

📌 Notes
Ensure your Google Gemini API key has sufficient quota.

Screenshots work best in headless mode with the Chrome WebDriver.

The tool uses Selenium, BeautifulSoup, and Markdown for flexible, structured scraping and reporting.

📬 Contributing
Feel free to fork the repo and submit pull requests. Issues and suggestions are welcome!

📄 License
This project is licensed under the MIT License.
