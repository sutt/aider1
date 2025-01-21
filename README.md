# FastAPI Factorial Service

A FastAPI service that calculates factorials and stores results in PostgreSQL.

## Testing

### Prerequisites
- PostgreSQL running on port 5433
- Python 3.11+
- Virtual environment with dependencies installed

### Running Tests

Basic test run:
```bash
pytest tests/test_api.py -v
```

Run tests with database cleanup (removes old test databases):
```bash
pytest --cleanup-test-dbs tests/test_api.py -v
```

### Test Database Management

- Failed tests preserve their database for debugging
- Database names follow pattern: `test_db_YYYYMMDD_HHMMSS_uuid`
- Connect to preserved test database:
```bash
psql -h localhost -p 5433 -U postgres -d test_db_YYYYMMDD_HHMMSS_uuid
```

Clean up all test databases without running tests:
```bash
pytest --cleanup-test-dbs
```
