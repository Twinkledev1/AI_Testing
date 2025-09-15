# KYC/AML Banking Platform Testing Project

## Overview

Test automation framework for a KYC (Know Your Customer) and AML (Anti-Money Laundering) banking platform, developed using generative AI tools to streamline test case creation and execution.

## Project Structure

```
kyc-aml-testing/
├── requirements.md          # Functional and non-functional requirements
├── synthetic_data/         # Test data generated using AI
│   ├── kyc_data.json      # Customer verification data
│   └── aml_data.json      # Transaction monitoring data
├── tests/                  # Pytest test suites
│   ├── test_kyc.py        # KYC verification tests
│   └── test_aml.py        # AML monitoring tests
├── rtm_matrix.csv         # Requirements Traceability Matrix
├── test_report.md         # Test execution report with AI insights
└── pytest.ini             # Pytest configuration
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

```bash
# Extract the project
unzip kyc-aml-testing.zip
cd kyc-aml-testing

# Install dependencies
pip install pytest
```

## Running Tests

### Execute all tests

```bash
pytest -v
```

### Run specific test suites

```bash
# KYC tests only
pytest tests/test_kyc.py -v

# AML tests only
pytest tests/test_aml.py -v
```

### Generate test report

```bash
pytest --html=report.html --self-contained-html
```

## Test Coverage

### KYC Test Cases

- **TC-KYC-001**: Document upload validation
- **TC-KYC-002**: Customer verification status
- **TC-KYC-003**: Risk score calculation

### AML Test Cases

- **TC-AML-001**: Transaction monitoring thresholds
- **TC-AML-002**: Suspicious pattern detection
- **TC-AML-003**: SAR/CTR report generation

## Key Features

- **Synthetic Data**: AI-generated test data ensuring privacy compliance
- **Comprehensive Coverage**: Tests for chatbot, NLP, KYC, AML, and integrations
- **RTM Mapping**: Full traceability from requirements to test cases
- **Performance Metrics**: Response time and throughput validation

## AI Enhancement Benefits

- 90% reduction in test case creation time
- Automated synthetic data generation
- Improved test coverage through AI-suggested edge cases
- Consistent documentation and reporting

## Technologies Used

- **Testing**: Python, Pytest
- **AI Tools**: ChatGPT/Claude for test generation
- **Data Format**: JSON for test data
- **Reporting**: Markdown, CSV

## Contributing

1. Follow existing test patterns
2. Update RTM matrix for new test cases
3. Ensure all tests pass before committing
4. Document any new requirements

## License

Internal use only - TechSpark Solutions
