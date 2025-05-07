import requests
import json
import csv
import re
from datetime import datetime

# Import API key from config file
from config import DEEPSEEK_API_KEY

# Constants
API_URL = "https://api.deepseek.com/v1/chat/completions"
TEST_CASES_FILE = "testCases.txt"
RESULTS_FILE = "test_results.csv"

def parse_test_cases(file_path):
    """
    Parse the test cases file and extract prompts and expected keywords
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expression pattern to extract test cases
    pattern = r'\*\*(\d+)\. ([^*]+)\*\*\s+Prompt: "([^"]+)"\s+Expected Keywords: \[(.*?)\]\s+Pass criteria: Response contains (.*?)(?:\n\n|\Z)'
    test_cases = []
    
    for match in re.finditer(pattern, content):
        test_num = match.group(1)
        test_name = match.group(2).strip()
        prompt = match.group(3).strip()
        keywords_str = match.group(4).strip()
        
        # Parse keywords from the string
        keywords = []
        for keyword in re.finditer(r'"([^"]+)"', keywords_str):
            keywords.append(keyword.group(1))
        
        # If no keywords were found with quotes, try splitting by comma
        if not keywords:
            keywords = [k.strip() for k in keywords_str.split(',')]
        
        test_cases.append({
            'test_num': test_num,
            'test_name': test_name,
            'prompt': prompt,
            'expected_keywords': keywords
        })
    
    
    return test_cases

def call_deepseek_api(prompt, conversation_history=None):
    """
    Send a prompt to the DeepSeek API and get the response
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    messages = []
    if conversation_history:
        messages.extend(conversation_history)
    
    messages.append({"role": "user", "content": prompt})
    
    data = {
        "model": "deepseek-chat",  # Update with the correct model name
        "messages": messages,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        result = response.json()
        return result['choices'][0]['message']['content'], messages + [{"role": "assistant", "content": result['choices'][0]['message']['content']}]
    
    except Exception as e:
        print(f"API call failed: {e}")
        return f"Error: {e}", conversation_history

def check_keywords(response, keywords):
    """
    Check if the response contains the expected keywords
    """
    missing_keywords = []
    for keyword in keywords:
        if keyword.lower() not in response.lower():
            missing_keywords.append(keyword)
    
    return len(missing_keywords) == 0, missing_keywords

def save_results(results):
    """
    Save test results to a CSV file
    """
    with open(RESULTS_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Test #', 'Test Name', 'Prompt', 'Expected Keywords', 'Passed', 'Missing Keywords', 'Response'])
        
        for result in results:
            writer.writerow([
                result['test_num'],
                result['test_name'],
                result['prompt'],
                ', '.join(result['expected_keywords']),
                result['passed'],
                ', '.join(result['missing_keywords']),
                result['response'][:100] + '...' if len(result['response']) > 100 else result['response']
            ])
            
            # Write follow-up result if available
            if 'follow_up_result' in result:
                follow_up = result['follow_up_result']
                writer.writerow([
                    result['test_num'] + ' (follow-up)',
                    result['test_name'] + ' (follow-up)',
                    result['follow_up_prompt'],
                    ', '.join(result['follow_up_keywords']),
                    follow_up['passed'],
                    ', '.join(follow_up['missing_keywords']),
                    follow_up['response'][:100] + '...' if len(follow_up['response']) > 100 else follow_up['response']
                ])

def run_tests():
    """
    Run all tests and collect results
    """
    print(f"Starting test run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Parsing test cases...")
    test_cases = parse_test_cases(TEST_CASES_FILE)
    print(f"Found {len(test_cases)} test cases")
    
    results = []
    passed_count = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases):
        print(f"\nRunning test {test_case['test_num']}: {test_case['test_name']}")
        print(f"Prompt: {test_case['prompt']}")
        
        # Call the API
        response, conversation_history = call_deepseek_api(test_case['prompt'])
        
        # Check if response contains expected keywords
        passed, missing_keywords = check_keywords(response, test_case['expected_keywords'])
        
        if passed:
            passed_count += 1
            print("✅ Test passed!")
        else:
            print(f"❌ Test failed. Missing keywords: {', '.join(missing_keywords)}")
        
        result = {
            'test_num': test_case['test_num'],
            'test_name': test_case['test_name'],
            'prompt': test_case['prompt'],
            'expected_keywords': test_case['expected_keywords'],
            'passed': passed,
            'missing_keywords': missing_keywords,
            'response': response
        }
        
      
        results.append(result)
        
        # Print progress
        print(f"Progress: {i+1}/{len(test_cases)} test cases completed")
    
    # Save results
    save_results(results)
    
    # Print summary
    print("\n" + "="*50)
    print(f"Test run completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Results: {passed_count}/{total_tests} tests passed ({passed_count/total_tests*100:.1f}%)")
    print(f"Detailed results saved to {RESULTS_FILE}")
    print("="*50)

if __name__ == "__main__":
    run_tests()