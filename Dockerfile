FROM ubuntu:24.04 AS compiletime

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
COPY certifications ./certifications
COPY main.py Makefile .env ./

CMD ["python3", "main.py"]

# RUN pyinstaller --log-level=ERROR main.py

# FROM python:3.10-slim AS runtime

# WORKDIR /app

# COPY --from=compiletime /app/dist/main /app/main
# COPY ./.env /app/main
# COPY ./data /app/main/data

# CMD ["./main/main"]
