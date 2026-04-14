#!/usr/bin/env python3
"""
Validation Gateway: REQUIREMENTS State
Validates requirements.json structure and completeness
"""

import sys
import json
from pathlib import Path

def validate_file_exists():
    """Check if requirements.json exists"""
    print("Checking: requirements.json exists...")
    if Path("requirements.json").exists():
        print("✓ Check passed: File exists")
        return True
    else:
        print("✗ Check failed: requirements.json not found")
        return False

def validate_json_structure():
    """Check if requirements.json is valid JSON with required fields"""
    print("Checking: JSON structure and required fields...")

    required_fields = [
        "workflow_name",
        "purpose",
        "trigger",
        "deliverables",
        "constraints",
        "states",
        "validation_methods"
    ]

    try:
        with open("requirements.json") as f:
            data = json.load(f)

        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            print(f"✗ Check failed: Missing required fields: {missing_fields}")
            return False

        print("✓ Check passed: All required fields present")
        return True

    except json.JSONDecodeError as e:
        print(f"✗ Check failed: Invalid JSON - {e}")
        return False
    except Exception as e:
        print(f"✗ Check failed: {e}")
        return False

def validate_states_count():
    """Check if at least 3 states are defined"""
    print("Checking: Minimum state count...")

    try:
        with open("requirements.json") as f:
            data = json.load(f)

        states = data.get("states", [])
        if len(states) >= 3:
            print(f"✓ Check passed: {len(states)} states defined (minimum 3)")
            return True
        else:
            print(f"✗ Check failed: Only {len(states)} states defined (minimum 3 required)")
            return False

    except Exception as e:
        print(f"✗ Check failed: {e}")
        return False

def validate_validation_methods():
    """Check if validation methods are defined"""
    print("Checking: Validation methods...")

    try:
        with open("requirements.json") as f:
            data = json.load(f)

        methods = data.get("validation_methods", [])
        states = data.get("states", [])

        if len(methods) >= len(states):
            print(f"✓ Check passed: {len(methods)} validation methods for {len(states)} states")
            return True
        else:
            print(f"✗ Check failed: {len(methods)} validation methods for {len(states)} states (need at least 1 per state)")
            return False

    except Exception as e:
        print(f"✗ Check failed: {e}")
        return False

def main():
    print("=== Validation Gateway: REQUIREMENTS ===")
    print()

    checks = [
        validate_file_exists(),
        validate_json_structure(),
        validate_states_count(),
        validate_validation_methods(),
    ]

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
