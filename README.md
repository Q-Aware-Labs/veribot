# VeriBot: Intelligent AI Response Testing Automation

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

VeriBot is a lightweight, configurable framework for automated testing of AI language models. It allows testers to validate AI responses against expected keywords and criteria, providing a structured approach to quality assurance for conversational AI systems.

## Features

- **Test Case Management**: Parse and execute test cases from structured text files
- **Keyword Validation**: Verify AI responses contain expected keywords and phrases
- **Multi-turn Conversation Testing**: Support for contextual tests that span multiple exchanges
- **Detailed Reporting**: Generate CSV reports with test results and failure details
- **Progress Tracking**: Real-time visibility into test execution status
- **Configurable API Integration**: Currently supports DeepSeek API with extensible design

## Installation

```bash
# Clone the repository
git clone https://github.com/antonyga/VeriBot.git
cd VeriBot

# Install dependencies
pip install requests
```

## Configuration

1. Create a `config.py` file in the project root with your API credentials:

```python
# DeepSeek API configuration
DEEPSEEK_API_KEY = 'your-api-key-here'
```

2. Customize test cases in `testCases.txt` following the format:

```
**1. Test Name**  
Prompt: "Your test prompt here"  
Expected Keywords: ["keyword1", "keyword2"]  
Pass criteria: Response contains "keyword1", "keyword2"
```

## Usage

Run the test suite:

```bash
python test_runner.py
```

The script will:
1. Parse all test cases from your test file
2. Send each prompt to the AI service
3. Validate responses against expected keywords
4. Generate a detailed report of results

## Test Case Format

VeriBot supports various test case types:

### Standard Test Case
```
**1. Factual Q&A**  
Prompt: "What year did humans first land on the moon?"  
Expected Keywords: ["1969"]  
Pass criteria: Response contains "1969"
```

### Multi-turn Conversation Test
```
**5. Multi-Turn Context**  
Prompt 1: "Who wrote Romeo and Juliet?"  
Expected Keywords: ["Shakespeare"]  
Pass criteria: Response contains "Shakespeare"  
Prompt 2 (follow-up): "What other tragedies did they write?"  
Expected Keywords: ["Hamlet", "Macbeth"]  
Pass criteria: Response contains "Hamlet", "Macbeth"
```

## Test Categories

The included test cases cover a wide range of AI capabilities:
- Factual knowledge retrieval
- Creative content generation
- Instructional responses
- Role-playing scenarios
- Contextual understanding
- Ambiguity handling
- Mathematical computations
- Linguistic capabilities
- Cultural knowledge

## Output

Results are saved to `test_results.csv` with the following information:
- Test number and name
- Prompt used
- Expected keywords
- Pass/fail status
- Missing keywords (if any)
- Response snippet

## Customization

### Adding New Test Cases
Add new test cases to `testCases.txt` following the established format.

### Supporting Different AI Providers
To use a different AI provider:
1. Update the API endpoint in `test_runner.py`
2. Modify the request structure in `call_deepseek_api()`
3. Adjust the response parsing logic if needed

## Project Structure

```
VeriBot/
├── test_runner.py     # Main execution script
├── config.py          # API credentials
├── testCases.txt      # Test case definitions
└── test_results.csv   # Generated test results
```

## Use Cases

- **QA Testing**: Verify AI responses meet quality standards
- **Regression Testing**: Ensure new model versions maintain expected behavior
- **Response Validation**: Check factual accuracy and keyword presence
- **Multi-turn Validation**: Test conversational memory and context handling

## Future Enhancements

- Support for more complex validation beyond keyword matching
- Response time measurement and performance benchmarking
- HTML report generation with interactive visualizations
- Integration with CI/CD pipelines

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## About

Created by @antonyga for Q-Aware Labs - ISTQB Certified AI Software Tester, specializing in AI system validation and prompt engineering.