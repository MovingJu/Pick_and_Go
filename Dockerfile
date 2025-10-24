FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        binutils \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.13 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install torch torchvision --break-system-packages --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt ./
RUN pip install -r requirements.txt --break-system-packages

COPY ./modules ./modules
COPY ./routes ./routes
COPY ./data ./data
COPY main.py Makefile .env ./

CMD ["python3", "-O", "-X", "perf", "-X", "no_debug_ranges", "-X", "noadaptive", "-m", "uvicorn", "main:app", \
     "--host", "0.0.0.0", "--port", "8080", \
     "--workers", "4", "--loop", "uvloop", "--http", "httptools", \
     "--interface", "asgi3", "--backlog", "2048", "--timeout-keep-alive", "15", "--no-access-log"]