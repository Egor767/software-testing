# server

```bash
uv run app/main.py
```

# locust

with interface
```bash
uv run locust -f tests/locust/locustfile.py --config tests/locust/locust.conf
```

without interface
```bash
uv run locust -f tests/locust/locustfile.py --config tests/locust/locust.conf --headless
```

# k6

```bash
k6 run tests/k6/test.js
```
