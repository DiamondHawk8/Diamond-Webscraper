FROM python:3.10-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends gcc

WORKDIR /build

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir pyarmor

COPY . .

# Obfuscate selected modules
RUN pyarmor obfuscate \
    diamond_scraper/utils/stealth_utils.py \
    diamond_scraper/proxy_rotation_middleware.py \
    diamond_scraper/settings.py \
    diamond_scraper/spiders/base_spider.py \
    diamond_scraper/spiders/intoli_spider.py \
    --output dist_obf/
# Remove raw elements after obfuscation
RUN rm -f \
    diamond_scraper/utils/stealth_utils.py \
    diamond_scraper/proxy_rotation_middleware.py \
    diamond_scraper/settings.py \
    diamond_scraper/spiders/base_spider.py \
    diamond_scraper/spiders/intoli_spider.py



# Runtime image
FROM python:3.10-slim as runtime

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy obfuscated files
COPY --from=builder /build/dist_obf/settings.py /app/diamond_scraper/settings.py
COPY --from=builder /build/dist_obf/base_spider.py /app/diamond_scraper/spiders/base_spider.py
COPY --from=builder /build/dist_obf/intoli_spider.py /app/diamond_scraper/spiders/intoli_spider.py
COPY --from=builder /build/dist_obf/stealth_utils /app/diamond_scraper/utils/stealth_utils
COPY --from=builder /build/dist_obf/proxy_rotation_middleware.py /app/diamond_scraper/proxy_rotation_middleware.py

# Copy remaining non-sensitive files
COPY --from=builder /build/runner.py /app/runner.py
COPY --from=builder /build/scrapy.cfg /app/scrapy.cfg
COPY --from=builder /build/diamond_scraper/items.py /app/diamond_scraper/items.py
COPY --from=builder /build/diamond_scraper/db_pipeline.py /app/diamond_scraper/db_pipeline.py
COPY --from=builder /build/diamond_scraper/core_pipelines.py /app/diamond_scraper/core_pipelines.py
COPY --from=builder /build/diamond_scraper/core_middlewares.py /app/diamond_scraper/core_middlewares.py
COPY --from=builder /build/diamond_scraper/utils/db_utils.py /app/diamond_scraper/utils/db_utils.py
COPY --from=builder /build/diamond_scraper/utils/stats_util.py /app/diamond_scraper/utils/stats_util.py
COPY --from=builder /build/diamond_scraper/utils/validation_logger.py /app/diamond_scraper/utils/validation_logger.py


# Default entrypoint
CMD ["python", "runner.py", "base_spider"]