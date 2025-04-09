
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

## Example Use Cases

- Monitoring product data across multiple retailers.
- Fingerprinting detection and anti-bot analysis.
- Financial or market data extraction with validation pipelines.
- Academic research involving structured web data collection.

---

## Getting Started

1. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

2. **Run a Spider**  
   ```bash
   python runner.py your_spider_name
   ```

3. **Configure Output & Logging**  
   - Set output format with `-o`, `-f`.  
   - Enable debugging or override settings with `-s`.

4. **Select Database Backend**  
   - Default is SQLite.  
   - For PostgreSQL, use environment variables to supply credentials.

---

## Project Structure (Simplified)

```
diamond_scraper/
├── items.py
├── middlewares/
│   ├── core_middlewares.py
│   └── proxy_rotation_middleware.py
├── pipelines/
│   ├── core_pipelines.py
│   └──  db_pipeline.py
├── spiders/
│   ├── base_spider.py
│   ├── intoli_spider.py
│   └── ...
├── utils/
│   ├── db_utils.py
│   ├── stats_util.py
│   ├── stealth_utils.py
│   └── validation_logger.py
├── settings.py
└── runner.py
```