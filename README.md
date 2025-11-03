# 🦗 Locust Load Testing

Load testing suite with three test scenarios for different APIs and use cases.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Web UI
locust -f locustfile1.py

# Run headless
locust -f locustfile1.py --headless -u 10 -r 2 -t 60s
```

Open `http://localhost:8089` to configure and start tests.

## 📁 Test Files

### `locustfile1.py` - DummyJSON API

- Tests CRUD operations on `https://dummyjson.com`
- Weighted tasks: products (5x), posts (4x), create (3x), update (2x), users (1x), delete (1x)
- Use for: REST API performance testing

### `locustfile2.py` - Image Service

- Tests `https://dummyimage.com` with random image parameters
- Random sizes, colors, formats (JPG/PNG/WebP)
- Use for: CDN performance and cache testing

### `locustfile3.py` - Authentication Flow

- Simulates login attempts on `https://dummyjson.com`
- Fetches random user, attempts login (max 5 tries), stores token
- Use for: Authentication system load testing

## 🛠️ Common Commands

```bash
# Different test files
locust -f locustfile1.py
locust -f locustfile2.py
locust -f locustfile3.py

# Headless with 100 users, 10/sec spawn rate, 5 min duration
locust -f locustfile1.py --headless -u 100 -r 10 -t 5m

# Generate HTML report
locust -f locustfile1.py --headless -u 100 -r 10 -t 5m --html=report.html
```

## 📋 Key Dependencies

- **locust** 2.42.0 - Load testing framework
- **requests** 2.32.4 - HTTP library
- **gevent** 25.9.1 - Async networking

See `requirements.txt` for full list.

---

