# Diamond Scraper

Diamond Scraper is a modular and scalable Scrapy-based web scraping framework designed for structured data extraction and robust validation.

## Project Overview

Diamond Scraper provides a configurable framework for scraping financial and structured web data. It supports validation, transformation, and error tracking through a pipeline-oriented architecture.

## Features

- Modular spider design with extendable base classes
- Field-level validation and suspicious value flagging
- Custom logging and statistics middleware
- Cleaned data exported to JSON Lines
- Logging output to `scraper.log`

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/diamond_scraper.git
cd diamond_scraper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run a Spider

```bash
scrapy crawl base
```

## Validation & Logging

Validation is handled through a `ValidationLogger` utility, which supports:

- Rule-based field validation and transformations
- Suspicious value flagging (not dropped)
- Logging of invalid, flagged, and dropped items
- Threshold-based item dropping logic

For details, see `validation_logger.md`.

## Settings Overview

Key configurable settings can be found in `settings.py`, including:

- Retry and backoff settings
- AutoThrottle behavior
- Caching and concurrency
- Logging level and destination

## Pipelines

Several pipelines are defined in `pipelines.py`, including:

- `DiamondScraperPipeline`: Basic field normalization
- `InvalidDataPipeline`: Field-level validation with drop logic
- `DuplicatesPipeline`: Deduplication by timestamp
- `TestPipeline`: Demonstration pipeline using artificial item validation

## Middleware

