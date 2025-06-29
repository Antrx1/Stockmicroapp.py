# Stockmicroapp.py

A secure, Dockerized Python microservice for stock and crypto analytics. This app offers real-time prices, social trending tickers, and financial analysis using modern tools like Streamlit, Finnhub, and Polygon.

---

## 🚀 Features

- 📊 Live stock/crypto cards (SPY, QQQ, BTC, etc)
- 📈 Chart view with market caps and financials
- 🔍 Trending tickers via social scraping (ApeWisdom)
- 🐳 Docker containerized for scalability
- 🔐 Non-root + SELinux-compatible

---

## 🛠 Requirements

- Docker (any Linux host)
- API keys:
  - `api.txt` for [Finnhub.io](https://finnhub.io)
  - `apip.txt` for [Polygon.io](https://polygon.io)

---

## ⚙️ Setup

### 1. Clone

```bash
git clone https://github.com/Antrx1/stocks.py-microservice-docker.git
cd stocks.py-microservice-docker
