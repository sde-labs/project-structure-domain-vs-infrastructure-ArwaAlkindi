# Week 3: Environment Variables & Secrets

## Learning Objectives
By the end of this lesson, you will:
- Understand why secrets should never be hardcoded
- Learn how environment variables separate code from configuration
- Validate configuration early to fail fast (just like week2 input validation)
- Recognize the boundary between config validation and business logic (config is niether infra nor domain)

---

## The Problem with Week 2 Code

We validated data, but configuration is still implicit. That leads to brittle deployments and leaked secrets.

```python
# Hardcoded values or hidden assumptions
db_path = "oil_well_monitoring.db"  # ❌
api_token = "super-secret-token"    # ❌
```

**What happens?**
1. ✅ Code runs locally
2. ❌ Secrets end up in source control
3. ❌ Prod needs different config than dev/test
4. ❌ Failures show up late instead of at startup

---

## The Solution: Environment Variables

Environment variables keep configuration out of code. Combine them with validation so your app fails fast and loudly.

### Enter python-dotenv
`python-dotenv` loads a local `.env` file during development so your shell stays clean, while production still uses real environment variables.

---

## Your Assignment

You’ll add a configuration layer that loads and validates environment variables.

### What You Need to Do

**In `src/config/settings.py`**: Implement a Settings model with validation and env loading.

1. **from_env()**
   - Load variables using `python-dotenv`
   - Required variables: `APP_ENV`, `DATABASE_URL`, `API_TOKEN`
   - Raise a clear error for missing values

2. **Environment Validator**
   - `env` must be one of: `dev`, `test`, `prod`

3. **Database URL Validator**
   - Must be non-empty
   - Must end with `.db`

4. **API Token Validator**
   - Must be non-empty

**In `src/main.py`**: Implement `load_settings()`
   - Should return `Settings.from_env()`

---

## Example Pattern

```python
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator

class Settings(BaseModel):
    env: str
    database_url: str
    api_token: str

    @classmethod
    def from_env(cls):
        load_dotenv()
        return cls(
            env=os.getenv("APP_ENV"),
            database_url=os.getenv("DATABASE_URL"),
            api_token=os.getenv("API_TOKEN"),
        )

    @field_validator("env")
    def validate_env(cls, v):
        if v not in {"dev", "test", "prod"}:
            raise ValueError("env must be one of: dev, test, prod")
        return v
```

---

## Understanding the Architecture

### Where Does Configuration Belong?

Configuration is not business logic. It sits at the boundary and should be validated before your domain logic runs.

- **Config validation**: Infrastructure concern - Domain does not know this exists, but reaps the benefit when it accesses process.env 
- **Business validation**: Domain concern

---

## Testing Your Solution

### Run Tests Locally
```bash
pytest tests/test_week3.py -v  # Should pass after implementing config, and prior weeks should still pass
```

### Expected Behavior

**Valid config (should work):**
```bash
export APP_ENV=dev
export DATABASE_URL=alerts.db
export API_TOKEN=secret-token
```

**Missing config (should fail fast):**
```bash
unset DATABASE_URL
```

---

## Real-World Connection

### Where You’ll Use This
- Data pipelines reading secrets from a vault
- Container deployments with environment-based config
- CI systems injecting credentials at runtime

### Industry Standard
- 12-factor apps
- Kubernetes secrets
- Vault/SSM/Secrets Manager

---

## Discussion Questions

**Production Scenario:** A developer accidentally checks in a `.env` file with real API keys. What could go wrong? How do you prevent it? How do you remediate it?

---

## Next Week Preview

Week 4 will introduce **error handling and logging**, so failures become visible and debuggable in production.

---

## Success Criteria

- ✅ All tests from this week and prior weeks pass
- ✅ Missing env vars fail fast
- ✅ Invalid config is rejected
- ✅ Valid config loads cleanly
