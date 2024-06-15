FROM python:3.12-slim-bullseye
LABEL authors="wm3ndez"


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

RUN pip install -U pip setuptools wheel

RUN apt update
RUN apt install -y \
    gcc \
    g++ \
    python3-dev \
    git \
    wget

RUN apt-get install -y \
	apt-transport-https \
	ca-certificates \
	curl \
	gnupg \
	fontconfig \
	fonts-ipafont-gothic \
	fonts-wqy-zenhei \
	fonts-thai-tlwg \
	fonts-kacst \
	fonts-symbola \
	fonts-noto \
	fonts-freefont-ttf \
	--no-install-recommends

RUN wget --no-verbose -O /tmp/chrome.deb \
    https://dl.google.com/linux/deb/pool/main/g/google-chrome-stable/google-chrome-stable_126.0.6478.61-1_amd64.deb \
    && apt install -y /tmp/chrome.deb \
    && rm /tmp/chrome.deb

RUN apt install unzip \
    && apt-get purge --auto-remove -y curl gnupg \
    && apt clean  \
    && rm -rf /var/lib/apt

RUN wget https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.61/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && rm chromedriver-linux64.zip \
    && mv chromedriver /usr/bin/chromedriver

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY app.py .
COPY html_to_pdf.py .

EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
