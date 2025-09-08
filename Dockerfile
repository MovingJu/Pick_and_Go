FROM python:3.10-slim AS compiletime

RUN apt update && apt install -y --no-install-recommends make binutils

WORKDIR /app
COPY requirements.txt ./

RUN pip install torch torchvision --break-system-packages --index-url https://download.pytorch.org/whl/cpu

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
