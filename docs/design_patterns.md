
# 📐 Design Patterns for a URL Shortener System (FastAPI Edition)

Applying design patterns to your FastAPI-based URL shortener helps improve scalability, maintainability, and system design understanding.

---

## ✅ Essential Design Patterns

### 1. **Factory Pattern**
- **Use case**: Generate short keys using different strategies (e.g., random, hash-based, KGS-based).
- **Benefit**: Easily swap or add key-generation strategies.

```python
class KeyGeneratorFactory:
    def get_generator(self, method: str):
        if method == "random":
            return RandomKeyGenerator()
        elif method == "hash":
            return HashKeyGenerator()
```

---

### 2. **Singleton Pattern**
- **Use case**: Redis client, KGS client, DB connection manager.
- **Benefit**: Ensures one instance of shared resources.

```python
class RedisClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Redis(host="localhost")
        return cls._instance
```

---

### 3. **Repository Pattern**
- **Use case**: Abstract DB operations for URLs.
- **Benefit**: Clean separation of data and business logic.

```python
class URLRepository:
    def __init__(self, db):
        self.db = db

    def get_by_key(self, key: str):
        return self.db.query(URL).filter(URL.key == key).first()
```

---

### 4. **Strategy Pattern**
- **Use case**: Multiple key generation algorithms.
- **Benefit**: Plug-and-play key generation logic.

```python
class KeyGenerationStrategy:
    def generate(self, url: str) -> str:
        pass

class RandomKeyStrategy(KeyGenerationStrategy):
    def generate(self, url: str) -> str:
        return generate_random_key()

class HashKeyStrategy(KeyGenerationStrategy):
    def generate(self, url: str) -> str:
        return hash_url(url)
```

---

### 5. **Decorator Pattern**
- **Use case**: Add logging, caching, or metrics.
- **Benefit**: Adds functionality without altering logic.

```python
def cache_result(func):
    def wrapper(*args, **kwargs):
        cached = redis.get(args[0])
        if cached:
            return cached
        result = func(*args, **kwargs)
        redis.set(args[0], result)
        return result
    return wrapper
```

---

### 6. **Observer Pattern**
- **Use case**: Track analytics/events on URL accesses.
- **Benefit**: Decouples telemetry from core logic.

---

### 7. **Builder Pattern**
- **Use case**: Build complex response objects (e.g., analytics data).
- **Benefit**: Organizes construction of optional fields.

---

## 🛠 Optional Advanced Patterns

| Pattern           | Use Case                                      |
|------------------|-----------------------------------------------|
| Circuit Breaker   | Handle failing dependencies gracefully        |
| Rate Limiter      | Protect the service from abuse/spam           |
| Proxy             | Apply caching or transformation in middleware |

---

## ✅ TL;DR — Start With These

| Pattern        | Purpose                        |
|----------------|-------------------------------|
| Factory        | Switching key generation logic |
| Singleton      | Redis/DB connection sharing    |
| Repository     | Data access abstraction        |
| Strategy       | Pluggable key generation       |
| Decorator      | Caching, logging, auth         |
| Observer       | Event handling (logging/analytics) |
