FROM python:3.10-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends gcc

WORKDIR /build

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir pyarmor

COPY . .

# Obfuscate the entire diamond_scraper folder recursively
RUN mkdir -p dist_obf && pyarmor obfuscate diamond_scraper --recursive --output dist_obf --exact

# Debug: list obfuscated files
RUN echo "==== Debug listing dist_obf ====" && ls -R dist_obf

# Remove raw elements after obfuscation
RUN rm -rf diamond_scraper


# Runtime image
FROM python:3.10-slim AS runtime

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy obfuscated diamond_scraper folder
COPY --from=builder /build/dist_obf/diamond_scraper /app/diamond_scraper

# Copy remaining non-sensitive files
COPY --from=builder /build/runner.py /app/runner.py
COPY --from=builder /build/scrapy.cfg /app/scrapy.cfg

# Default entrypoint
CMD ["python", "runner.py", "base_spider"]
