# Backend Testing Guide

## Setup

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Configure Test Database
- Ensure PostgreSQL is installed
- Create a test database user:
```sql
CREATE USER testuser WITH PASSWORD 'testpassword';
CREATE DATABASE test_swahili_learn;
GRANT ALL PRIVILEGES ON DATABASE test_swahili_learn TO testuser;
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=app
```

### Run Specific Test Files
```bash
pytest tests/test_users.py
pytest tests/test_courses.py
```

## Test Categories
- `test_users.py`: User authentication and profile management
- `test_courses.py`: Course CRUD operations
- `test_enrollments.py`: Enrollment and progress tracking tests

## Best Practices
- Each test should be independent
- Use fixtures for setup and teardown
- Mock external services when necessary
- Aim for high test coverage
