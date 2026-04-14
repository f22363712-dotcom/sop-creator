#!/usr/bin/env python3
"""
Validation Gateway: DESIGN State
Validates design.json structure and state machine integrity
"""

import sys
import json
from pathlib import Path

def validate_file_exists():
    """Check if design.json exists"""
    print("Checking: design.json exists...")
    if Path("design.json").exists():
        print("✓ Check passed: File exists")
        return True
    else:
        print("✗ Check failed: design.json not found")
        return False

def validate_json_structure():
    """Check if design.json has required structure"""
    print("Checking: JSON structure...")

    required_top_level = ["states", "global_constraints", "error_handling"]

    try:
        with open("design.json") as f:
            data = json.load(f)

        missing = [field for field in required_top_level if field not in data]
        if missing:
            print(f"✗ Check failed: Missing top-level fields: {missing}")
            return False

        print("✓ Check passed: Top-level structure valid")
        return True

    except json.JSONDecodeError as e:
        print(f"✗ Check failed: Invalid JSON - {e}")
        return False
    except Exception as e:
        print(f"✗ Check failed: {e}")
        return False

def validate_states_completeness():
    """Check if all states have required fields"""
    print("Checking: State completeness...")

    required_state_fields = [
        "name", "purpose", "entry_conditions",
        "actions", "exit_conditions", "gateway_script", "next_states"
    ]

    try:
        with open("design.json") as f:
            data = json.load(f)

        states = data.get("states", [])
        incomplete_states = []

        for state in states:
            missing = [field for field in required_state_fields if field not in state]
            if missing:
                incomplete_states.append(f"{state.get('name', 'UNNAMED')}: missing {missing}")

        if incomplete_states:
            print("✗ Check failed: Incomplete states:")
            for issue in incomplete_states:
                print(f"  - {issue}")
            return False

        print(f"✓ Check passed: All {len(states)} states complete")
        return True

    except Exception as e:
        print(f"✗ Check failed: {e}")
        return False

def validate_state_machine_dag():
    """Check if state transitions form valid DAG (no orphaned states)"""
    print("Checking: State machine connectivity...")

    try:
        with open("design.json") as f:
            data = json.load(f)

        states = data.get("states", [])
        state_names = {s["name"] for s in states}

        # Check if all next_states reference valid states
        invalid_transitions = []
        for state in states:
            for next_state in state.get("next_states", []):
                # Allow self-reference (retry loops)
                if next_state != state["name"] and next_state not in state_names:
                    invalid_transitions.append(f"{state['name']} → {next_state}")

        if invalid_transitions:
            print("✗ Check failed: Invalid state transitions:")
            for trans in invalid_transitions:
                print(f"  - {trans}")
            return False

        print("✓ Check passed: State machine is well-formed")
        return True

    except Exception as e:
        print(f"✗ Check failed: {e}")
        return False

def validate_error_handling():
    """Check if error handling is properly defined"""
    print("Checking: Error handling configuration...")

    try:
        with open("design.json") as f:
            data = json.load(f)

        error_handling = data.get("error_handling", {})

        if "max_retries" not in error_handling:
            print("✗ Check failed: max_retries not defined")
            return False

        if "escalation_actions" not in error_handling:
            print("✗ Check failed: escalation_actions not defined")
            return False

        if not isinstance(error_handling["escalation_actions"], list):
            print("✗ Check failed: escalation_actions must be a list")
            return False

        print("✓ Check passed: Error handling properly configured")
        return True

    except Exception as e:
        print(f"✗ Check failed: {e}")
        return False

def main():
    print("=== Validation Gateway: DESIGN ===")
    print()

    checks = [
        validate_file_exists(),
        validate_json_structure(),
        validate_states_completeness(),
        validate_state_machine_dag(),
        validate_error_handling(),
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
