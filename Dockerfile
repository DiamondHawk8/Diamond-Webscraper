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
  --output dist_obf/stealth_utils

# Remove raw elements after obfuscation
RUN rm -f diamond_scraper/utils/stealth_utils.py

