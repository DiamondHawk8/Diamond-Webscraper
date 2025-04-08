# ----------------------------------------
# Stage 1: Builder
# ----------------------------------------
FROM python:3.10-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Working dir
WORKDIR /build

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# TODO figure out how to fix pyarmor


# ----------------------------------------
# Stage 2: Runtime
# ----------------------------------------
FROM python:3.10-slim as runtime

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /build /app

# Default command
CMD ["python", "runner.py", "base"]