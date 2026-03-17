# Shadow News AI: Intelligent News Aggregator

Shadow News AI is a specialized full-stack web application designed to scrape, analyze, and categorize global news in real-time. Built with Django and powered by Groq Cloud (Llama 3), the system performs sentiment analysis and generates concise summaries of complex news topics, providing a clean and intelligent dashboard for decision-making.

## 🚀 Features
 * Multi-Source Scraper: Automated data extraction from elite sources like MIT Technology Review, BBC, Reuters, and specialized cybersecurity sites.
 * AI-Powered Analysis: Integration with Groq's Llama-3 models to generate professional summaries and sentiment labeling (Positive, Negative, Neutral).
 * Cybersecurity Focus: Dedicated module for tracking cybercrime and digital security trends.
 * Mobile-First Development: Entirely developed within a mobile environment using Termux and NeoVim.
 * Automated Workflow: Uses GitHub Actions as a CRON service to update news daily at midnight (UTC).
 * Continuous Integration: Automated testing suite that runs on every push to ensure code stability.
## 🛠️ Tech Stack
 * Backend: Python 3.12, Django 5.x
 * Database: PostgreSQL (Hosted on Neon.tech)
 * AI Engine: Groq SDK (Llama 3.3 / 3.1)
 * Frontend: Tailwind CSS (Modern Glassmorphism UI)
 * Deployment: Vercel (Frontend/API) & GitHub Actions (Automation)
 * Environment: Termux, NeoVim, Git
## 📂 Project Structure

```txt
news_intelligence/
├── news_aggregator/
│   ├── management/commands/  # Custom Django commands (fetch_news, clean_db)
│   ├── tests/                # Unit tests (Models, Views, Utils/Mocks)
│   ├── utils.py              # Scraper logic and IA integration
│   └── models.py             # Database schema with auto-ordering
├── templates/                # Responsive Glassmorphism UI
├── .github/workflows/        # CI/CD and Daily Scraper Automation
└── pytest.ini                # Test runner configuration
```

## ⚙️ Installation & Setup
 * Clone the repository:

```bash
   git clone https://github.com/ShadowRoot07/news_intelligence.git
cd news_intelligence
```

 * Set up the environment:

```bash
   python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

 * Configure Environment Variables:
   Create a .env file or export the variables:
   * DATABASE_URL: Your Neon.tech connection string.
   * GROQ_API_KEY: Your Groq Cloud API key.
   * SECRET_KEY: Django secret key.
 * Database Migration:
 ```bash
   python manage.py migrate
```

 * Run Tests:
   python manage.py test news_aggregator

## 🤖 Automated Tasks
The project includes custom management commands to interact with the system:
 * python manage.py fetch_news: Triggers the scraping and AI analysis process.
 * python manage.py clean_db: Wipes the database for fresh data ingestion.
## 🛡️ Testing Strategy
The application includes a robust testing suite located in news_aggregator/tests/:
 * Models: Ensures data integrity and category assignment.
 * Views: Validates HTTP responses and template rendering.
 * Utils (Mocks): Tests the scraper and AI logic using unittest.mock to avoid external API costs and network dependency during CI.
### Developed by ShadowRoot07 🌿🚀🧪
