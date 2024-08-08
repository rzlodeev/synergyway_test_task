FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install required packages for Selenium and Firefox
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz \
    && tar -xzf geckodriver-v0.35.0-linux64.tar.gz -C /usr/local/bin \
    && rm geckodriver-v0.35.0-linux64.tar.gz

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
