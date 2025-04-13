# stock-exchange-quote


This project consists of two FastAPI-based microservices designed to work together via Docker Compose.

Rate Limiter Service: A gateway service that restricts access to upstream API calls using IP-based rate limiting.

Quote Data Service: A microservice that retrieves real-time stock quote data from a third-party provider (Alpha Vantage).

Redis is used as a shared store for rate limiting, quote stock data and tracking query costs.

## Features

### Rate Limiter Service

- IP-based rate limiting using Redis

- Tracks number of calls for rate limiting


### Quote Data Service

- Issues signed JWT bearer tokens

- Validates bearer token from requests

- Received requests from Rate Limiter Service

- Fetches stock quote data from Alpha Vantage

- Tracks cost of quote queries (with support to fetch/reset cost)


## Architecture Overview
```
+-------------------+        +--------------------+
|                   |        |                    |
| Rate Limiter API  +------->+  Quote Data API    |
| (port 8000)       |        |  (port 8001)       |
|                   |        |                    |
+-------------------+        +--------------------+
         ^                             ^
         |                             |
      [Redis] <------------------------+
         | (shared cache)

```

## Technologies Used

- FastAPI

- aiohttp

- Redis

- PyJWT

- Docker Compose

## Prerequisites

- Python 3.8+

- Docker & Docker Compose installed

- .env file in the root directory

Note: The .env file must be added manually. It contains API keys and secrets that will be sent via email.

## .env file 

REDIS_HOST=redis

REDIS_PORT=6379

ALPHAVANTAGE_URL=https://www.alphavantage.co

QUOTE_DATA_SERVICE_URL=http://quote-data-service:8001

API_KEY=your_alphavantage_api_key

SECRET_KEY=your_jwt_secret_key


## Build & Run the Services

#### Step 1: Clone the repository
```buildoutcfg
$ git clone https://github.com/matan2009/stock-exchange-quote.git
$ cd stock-exchange-quote
```
##### Step 2: Add your .env file to the root directory

#### Step 3: Build and start the services
```buildoutcfg
$ docker-compose up --build
```

## Your services will be available at:

#### Rate Limiter Service: 
http://localhost:8000 (Bearer Token required in headers!)

#### Quote Data Service: 
http://localhost:8001

To interact with the services, use Postman or curl.

##API Endpoints

###Rate Limiter Service
```buildoutcfg
GET /rate_limiter/{symbol} — Fetch quote data with rate limiting
```

### Quote Data Service
```buildoutcfg
GET /quote_data/{symbol} — Fetch stock quote data

GET /total_cost — View accumulated cost

POST /total_cost/reset — Reset cost counter
```

