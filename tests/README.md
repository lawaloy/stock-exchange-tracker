# Stock Exchange Tracker - Tests

## Overview

This directory contains unit tests for the Stock Exchange Tracker project, organized to mirror the source code structure.

## Test Structure

```txt
tests/
├── __init__.py
├── test_core_config.py         # Tests for core/config.py
├── test_core_logger.py          # Tests for core/logger.py
├── test_services_api_client.py  # Tests for services/api_client.py
├── test_analysis_analyzer.py    # Tests for analysis/analyzer.py
└── test_storage.py              # Tests for storage/data_storage.py
```

## Running Tests

### Run All Tests

```bash
# From project root
python -m pytest tests/

# Or using unittest
python -m unittest discover tests/
```

### Run Specific Test File

```bash
python -m pytest tests/test_core_config.py

# Or
python -m unittest tests.test_core_config
```

### Run Specific Test Class

```bash
python -m pytest tests/test_core_config.py::TestCoreConfig

# Or
python -m unittest tests.test_core_config.TestCoreConfig
```

### Run Specific Test Method

```bash
python -m pytest tests/test_core_config.py::TestCoreConfig::test_default_indices

# Or
python -m unittest tests.test_core_config.TestCoreConfig.test_default_indices
```

### Run with Coverage

```bash
# Install coverage first
pip install pytest-cov

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Test Coverage

Current test coverage by module:

- **core/config.py**: Configuration loading and defaults
- **core/logger.py**: Logging setup and handlers
- **services/api_client.py**: Rate limiting and API calls
- **analysis/analyzer.py**: Stock data analysis
- **storage/data_storage.py**: Data persistence

## Writing New Tests

When adding new functionality, follow these guidelines:

1. **Mirror the source structure**: Test file names should match source files
   - `src/core/config.py` → `tests/test_core_config.py`

2. **Use descriptive test names**: Start with `test_` and describe what's being tested
   ```python
   def test_load_from_config_file(self):
       """Test loading indices from config file."""
   ```

3. **Follow AAA pattern**: Arrange, Act, Assert
   ```python
   def test_example(self):
       # Arrange: Set up test data
       data = create_test_data()
       
       # Act: Execute the function
       result = function_under_test(data)
       
       # Assert: Verify the result
       self.assertEqual(result, expected)
   ```

4. **Use mocks for external dependencies**:
   ```python
   @patch('requests.Session')
   def test_api_call(self, mock_session):
       # Mock external API calls
   ```

5. **Clean up resources**: Use `setUp()` and `tearDown()` for test fixtures
   ```python
   def setUp(self):
       self.temp_dir = tempfile.mkdtemp()
   
   def tearDown(self):
       shutil.rmtree(self.temp_dir)
   ```

## Dependencies

Tests require these additional packages:

```bash
pip install pytest pytest-cov
```

Or for unittest (built-in, no install needed):
```bash
python -m unittest discover tests/
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines. Example GitHub Actions:

```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    python -m pytest tests/ --cov=src --cov-report=xml
```

## TODO

**Priority - New Feature Tests:**
- [ ] Tests for new screening filters (when added)
- [ ] Tests for additional exchanges (when added)
- [ ] Tests for visualization module (when added)
- [ ] Tests for alert system (when added)

**Current - Missing Tests:**
- [ ] Integration tests for full workflow
- [ ] Tests for services/data_fetcher.py
- [ ] Tests for services/stock_screener.py
- [ ] Tests for services/index_fetcher.py
- [ ] Tests for analysis/ai_summarizer.py
- [ ] Performance tests for API rate limiting

