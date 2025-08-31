FROM python:3.10-slim AS compiletime

WORKDIR /app
COPY requirements.txt ./
COPY ./data ./data
COPY ./modules ./modules
COPY ./routes ./routes
COPY .env main.py Makefile ./

RUN pip install torch torchvision --break-system-packages --index-url https://download.pytorch.org/whl/cpu

RUN pip install -r requirements.txt --break-system-packages


CMD ["python3", "main.py"]

# RUN pip install --break-system-packages pyinstaller

# RUN make build

# FROM debian:stable-slim AS runtime
# WORKDIR /app
# COPY --from=compiletime /app/dist /app/dist
# CMD ["./dist/main/main"]
