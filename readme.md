
# Diamond Webscraper

A web scraping project built on **Scrapy**, designed for scalability, modularity, and secure data handling. Current capabilities include:
- Intermediate Stealth with **Playwright** (rotating proxies, user-agent spoofing, JavaScript rendering).
- Data validation, logging, and stats tracking via custom pipelines.
- Flexible database output (SQLite or PostgreSQL).
- Containerized deployment on OKD or similar platforms, with environment-based configurations.

---

## Key Features

1. **Multiple Pipelines**  
   - `InvalidDataPipeline`, `ValidationLogger`, `DuplicatesPipeline`, etc.  
   - Ensures robust data validation, deduplication, and structured logging.

2. **Stealth Spiders (Playwright)**  
   - `intoli_spider.py` showcases scraping a JS-heavy site.  
   - Random user-agent rotation, IP proxy usage, basic Captcha detection (if configured).

3. **Flexible Database**  
   - Default: local SQLite (`DWS_scraper.db` in the container).  
   - Optional PostgreSQL integration via environment variables (`DB_BACKEND=postgres`).

4. **Runner Script (`runner.py`)**  
   - Simplifies spider execution with CLI arguments for logs, multiple spiders, custom settings, etc.

5. **Deployment on OKD**  
   - Docker-compatible image automatically built from commits.  
   - Secrets and credentials injected at runtime via environment variables or K8s secrets.

---