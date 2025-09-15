#!/usr/bin/env python3
"""
Test Runner for Philos AI Companion
Organizes and runs all tests with proper reporting
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔍 {description}")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print("✅ PASSED")
            if result.stdout:
                print(f"Output: {result.stdout[:200]}...")
            return True
        else:
            print("❌ FAILED")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️  TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 EXCEPTION: {e}")
        return False

def check_environment():
    """Check if the environment is set up correctly"""
    print("🔧 Checking Environment")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if virtual environment is active
    venv_active = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    print(f"Virtual Environment: {'✅ Active' if venv_active else '❌ Not Active'}")
    
    # Check for required environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"OpenAI API Key: {'✅ Set' if api_key else '❌ Missing'}")
    
    # Check if required directories exist
    required_dirs = ['src', 'tests/unit', 'tests/integration', 'examples', 'docs']
    for dir_name in required_dirs:
        exists = Path(dir_name).exists()
        print(f"Directory {dir_name}: {'✅ Exists' if exists else '❌ Missing'}")
    
    return venv_active and api_key

def run_unit_tests():
    """Run unit tests"""
    unit_test_dir = Path("tests/unit")
    if not unit_test_dir.exists():
        return 0, 0
        
    test_files = list(unit_test_dir.glob("test_*.py"))
    passed = 0
    total = len(test_files)
    
    print(f"\n🧪 Running Unit Tests ({total} tests)")
    print("=" * 50)
    
    for test_file in test_files:
        test_name = test_file.stem.replace("test_", "").replace("_", " ").title()
        if run_command(f"python {test_file}", f"Unit Test: {test_name}"):
            passed += 1
    
    return passed, total

def run_integration_tests():
    """Run integration tests"""
    integration_test_dir = Path("tests/integration")
    if not integration_test_dir.exists():
        return 0, 0
        
    test_files = list(integration_test_dir.glob("test_*.py"))
    passed = 0
    total = len(test_files)
    
    print(f"\n🔗 Running Integration Tests ({total} tests)")
    print("=" * 50)
    
    for test_file in test_files:
        test_name = test_file.stem.replace("test_", "").replace("_", " ").title()
        if run_command(f"python {test_file}", f"Integration Test: {test_name}"):
            passed += 1
    
    return passed, total

def main():
    """Main test runner"""
    start_time = time.time()
    
    print("🧠 Philos AI Companion - Test Suite")
    print("=" * 60)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment setup incomplete. Please check configuration.")
        return False
    
    total_passed = 0
    total_tests = 0
    
    # Run unit tests
    unit_passed, unit_total = run_unit_tests()
    total_passed += unit_passed
    total_tests += unit_total
    
    # Run integration tests
    integration_passed, integration_total = run_integration_tests()
    total_passed += integration_passed
    total_tests += integration_total
    
    # Summary
    elapsed_time = time.time() - start_time
    
    print(f"\n📊 Test Summary")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    print(f"Success Rate: {(total_passed/total_tests)*100:.1f}%" if total_tests > 0 else "No tests run")
    print(f"Time Elapsed: {elapsed_time:.1f}s")
    
    if total_passed == total_tests and total_tests > 0:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
