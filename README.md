# Stockmicroapp

**A secure, Dockerized Python microservice for stock and crypto analytics.**  
This app offers real-time prices, social trending tickers, and financial analysis using modern tools like **Streamlit**, **Finnhub**, and **Polygon**.

## Features

- Live stock/crypto quote cards for price monitor (API: [FinnHub.io](https://finnhub.io/))
- Trending social tickers (API: [ApeWisdom.com](https://apewisdom.com/))
- Financial analysis (API: [Polygon.io](https://polygon.io/))
- Containerized via Docker for easy deployment in Linux OS.

## Tech Stack
- Linux OS RHEL/CentOS/Ubuntu 
- Python 3.11
- Streamlit
- Docker
- Finnhub API
- Polygon.io API

## Requirements

- API keys:
  - `api.txt` for Finnhub.io
  - `apip.txt` for Polygon.io
  - Once you have your API keys, you need to create text files to store the keys:

echo "your_finnhub_api_key" > api.txt

echo "your_polygon_api_key" > apip.txt

- Docker (any Linux host)
- docker build -t stockapp .
- docker run -d -p 8501:8501 --name stockmicroapp stockapp
- docker ps -a 

- http://localhost:8501

## Running the Application with Docker

Follow the steps below to manually **build** and **run** the Docker container.

### **1. Clone the Repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/stockmicroapp.git
cd stockmicroapp

