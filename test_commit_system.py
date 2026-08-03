#!/usr/bin/env python3
"""
Test suite for Daily Notes Intelligent Commit System
Windows-compatible version
"""

import os
import sys
import subprocess
import time
from datetime import datetime

# Force UTF-8 for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Simple colors (avoid emojis for Windows compatibility)
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test_header(test_name):
    """Print test header"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}[TEST] {test_name}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def print_success(msg):
    print(f"{GREEN}[PASS] {msg}{RESET}")

def print_error(msg):
    print(f"{RED}[FAIL] {msg}{RESET}")

def print_info(msg):
    print(f"{YELLOW}[INFO] {msg}{RESET}")

def print_result(passed, total):
    print(f"\n{GREEN}Results: {passed}/{total} tests passed{RESET}")

def test_environment():
    """Test 1: Verify environment setup"""
    print_test_header("Environment Setup")
    passed = 0
    total = 5
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print_success(f"Python {python_version.major}.{python_version.minor}")
        passed += 1
    else:
        print_error(f"Python {python_version.major}.{python_version.minor} (need 3.8+)")
    
    # Check git
    result = subprocess.run(["git", "--version"], capture_output=True, text=True)
    if result.returncode == 0:
        print_success("Git installed")
        passed += 1
    else:
        print_error("Git not found")
    
    # Check required files
    required_files = ["update_number.py", "number.txt", ".git"]
    for file in required_files:
        if os.path.exists(file) or (file == ".git" and os.path.exists(".git")):
            print_success(f"{file} exists")
            passed += 1
        else:
            if file == ".git":
                print_error(".git directory not found (run 'git init')")
            else:
                print_error(f"{file} not found")
    
    # Check git remote
    result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
    if "origin" in result.stdout:
        print_success("Git remote configured")
        passed += 1
    else:
        print_error("No git remote configured")
    
    print_result(passed, total)
    return passed == total

def test_llm_installation():
    """Test 2: Verify LLM dependencies"""
    print_test_header("LLM Dependencies")
    passed = 0
    total = 3
    
    try:
        import transformers
        print_success("Transformers installed")
        passed += 1
    except ImportError:
        print_error("Transformers not installed")
    
    try:
        import torch
        print_success(f"PyTorch {torch.__version__} installed")
        passed += 1
    except ImportError:
        print_error("PyTorch not installed")
    
    # Check if model can be loaded
    try:
        from transformers import pipeline
        print_info("Loading GPT-2 model (this may take a moment)...")
        generator = pipeline('text-generation', model='openai-community/gpt2')
        result = generator("test", max_new_tokens=5)
        print_success("GPT-2 model loaded successfully")
        passed += 1
    except Exception as e:
        print_error(f"Failed to load GPT-2: {str(e)[:100]}")
    
    print_result(passed, total)
    return passed == total

def test_basic_commit():
    """Test 3: Test basic commit without LLM"""
    print_test_header("Basic Commit (No LLM)")
    
    try:
        with open("number.txt", "r") as f:
            old_number = int(f.read().strip())
    except:
        old_number = 0
    
    os.environ.pop("FANCY_JOB_USE_LLM", None)
    result = subprocess.run(
        ["python", "update_number.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success("Script ran successfully")
        
        with open("number.txt", "r") as f:
            new_number = int(f.read().strip())
        
        if new_number == old_number + 1:
            print_success(f"Number incremented: {old_number} -> {new_number}")
        else:
            print_error(f"Number not incremented correctly")
            return False
        
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print_success(f"Commit created: {result.stdout.strip()}")
            return True
        else:
            print_error("No commit created")
            return False
    else:
        print_error(f"Script failed: {result.stderr[:200]}")
        return False

def test_llm_commit():
    """Test 4: Test commit with LLM"""
    print_test_header("LLM Commit Generation")
    
    try:
        with open("number.txt", "r") as f:
            old_number = int(f.read().strip())
    except:
        old_number = 0
    
    result = subprocess.run(
        ["python", "update_number.py"],
        capture_output=True,
        text=True,
        env={**os.environ, "FANCY_JOB_USE_LLM": "true"}
    )
    
    if result.returncode == 0:
        print_success("Script ran with LLM")
        
        with open("number.txt", "r") as f:
            new_number = int(f.read().strip())
        
        if new_number == old_number + 1:
            print_success(f"Number incremented: {old_number} -> {new_number}")
        else:
            print_error("Number not incremented correctly")
            return False
        
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print_success(f"Commit created: {result.stdout.strip()}")
            return True
        else:
            print_error("No commit created")
            return False
    else:
        print_error(f"Script failed with LLM: {result.stderr[:200]}")
        return False

def test_content_creation():
    """Test 5: Verify daily content creation"""
    print_test_header("Daily Content Creation")
    passed = 0
    total = 3
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    year = datetime.now().year
    month = datetime.now().month
    journal_path = f"journal/{year}/{month:02d}/{date_str}.md"
    
    if os.path.exists(journal_path):
        print_success(f"Journal created: {journal_path}")
        passed += 1
    else:
        print_error(f"Journal not found: {journal_path}")
    
    practice_path = f"practice/{year}-{month:02d}-{date_str}.py"
    if os.path.exists(practice_path):
        print_success(f"Practice file created: {practice_path}")
        passed += 1
    else:
        print_error(f"Practice file not found: {practice_path}")
    
    if os.path.exists(journal_path):
        with open(journal_path, "r", encoding='utf-8') as f:
            content = f.read()
            if len(content) > 50:
                print_success("Journal content is substantial")
                passed += 1
            else:
                print_error("Journal content is too short")
    
    print_result(passed, total)
    return passed == total

def test_push():
    """Test 6: Test GitHub push"""
    print_test_header("GitHub Push")
    
    result = subprocess.run(["git", "push", "--dry-run"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print_success("Git push ready")
        print_info("Run 'git push' to push to GitHub")
        return True
    else:
        print_error(f"Push failed: {result.stderr[:200]}")
        return False

def main():
    """Run all tests"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}DAILY NOTES COMMIT SYSTEM TEST SUITE{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directory: {os.getcwd()}")
    
    tests = [
        ("Environment Setup", test_environment),
        ("LLM Dependencies", test_llm_installation),
        ("Basic Commit", test_basic_commit),
        ("LLM Commit", test_llm_commit),
        ("Content Creation", test_content_creation),
        ("GitHub Push", test_push)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {str(e)[:100]}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}FINAL RESULTS{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    for i, (test_name, result) in enumerate(zip([t[0] for t in tests], results), 1):
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{i:2}. {test_name:<30} {status}")
    
    print(f"\n{BLUE}Total: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}ALL TESTS PASSED! Your system is ready!{RESET}")
        print(f"\n{GREEN}Next steps:{RESET}")
        print("  1. Run 'python update_number.py' for a manual commit")
        print("  2. Set up Task Scheduler for automatic daily commits")
        print("  3. Check your GitHub profile for the green streak!")
    else:
        print(f"\n{YELLOW}Some tests failed. Please fix the issues above.{RESET}")
    
    return passed == total

if __name__ == "__main__":
    main()