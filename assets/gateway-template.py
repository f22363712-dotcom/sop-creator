#!/usr/bin/env python3
"""
Example validation gateway script template (Python version)
Customize this for your specific validation needs
"""

import sys
import os
from pathlib import Path

def validate_check_1():
    """Validation Check 1: [Description]"""
    print("Checking: [What is being validated]...")

    if Path("expected_file.txt").exists():
        print("✓ Check 1 passed: File exists")
        return True
    else:
        print("✗ Check 1 failed: expected_file.txt not found")
        return False

def validate_check_2():
    """Validation Check 2: [Description]"""
    print("Checking: [What is being validated]...")

    # Example: Check if a module can be imported
    try:
        import json
        print("✓ Check 2 passed: Required module available")
        return True
    except ImportError:
        print("✗ Check 2 failed: Required module not available")
        return False

def validate_check_3():
    """Validation Check 3: [Description]"""
    print("Checking: [What is being validated]...")

    # Example: Validate JSON structure
    try:
        with open("config.json") as f:
            import json
            data = json.load(f)

            required_keys = ["name", "version"]
            if all(key in data for key in required_keys):
                print("✓ Check 3 passed: Config has required keys")
                return True
            else:
                print("✗ Check 3 failed: Config missing required keys")
                return False
    except FileNotFoundError:
        print("✗ Check 3 failed: config.json not found")
        return False
    except json.JSONDecodeError:
        print("✗ Check 3 failed: config.json is not valid JSON")
        return False

def main():
    print("=== Validation Gateway: [STATE_NAME] ===")
    print()

    # Run all validation checks
    checks = [
        validate_check_1(),
        validate_check_2(),
        validate_check_3(),
    ]

    # Determine overall result
    all_passed = all(checks)

    print()
    if all_passed:
        print("=" * 45)
        print("✓ GATEWAY PASSED: All validations successful")
        print("=" * 45)
        return 0
    else:
        print("=" * 45)
        print("✗ GATEWAY FAILED: Some validations failed")
        print("=" * 45)
        print()
        print("Fix the issues above and re-run this script.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
