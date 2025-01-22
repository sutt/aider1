# FastAPI Factorial Service

A FastAPI service that calculates factorials and stores results in PostgreSQL.

## API Endpoints

### Calculate Factorial
- `GET /factorial/{input_num}`: Calculate factorial for a non-negative integer
- Returns: `{"result": calculated_factorial}`

### History
- `GET /history`: Retrieve calculation history with optional filters
- Filters:
  - `input_number`: Exact match for a specific input number
  - `min_input`: Show results with input number greater than or equal to this value
  - `max_input`: Show results with input number less than or equal to this value
- Examples:
  - `/history` - Get all results
  - `/history?input_number=5` - Get results for input 5
  - `/history?min_input=3` - Get results for inputs ≥ 3
  - `/history?max_input=5` - Get results for inputs ≤ 5
  - `/history?min_input=3&max_input=5` - Get results for inputs between 3 and 5 inclusive

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
