FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl unzip gnupg wget fonts-liberation \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 \
    libxss1 libasound2 libxtst6 libx11-xcb1 libxrandr2 libgtk-3-0 \
    libxdamage1 libxcomposite1 libxext6 libxi6 libatk1.0-0 libxinerama1 \
    libdbus-glib-1-2 libxshmfence1 --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -fy && \
    rm google-chrome-stable_current_amd64.deb

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy main script
COPY main.py .

CMD ["python", "main.py"]