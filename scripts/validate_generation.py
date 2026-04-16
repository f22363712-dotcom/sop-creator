#!/usr/bin/env python3
"""
Validation Gateway: GENERATION State
Validates that all SOP files are generated correctly
"""

import sys
import os
import re
from pathlib import Path

def validate_sop_markdown():
    """Check if SOP markdown file exists and has no placeholders"""
    print("Checking: SOP markdown file...")

    sop_files = list(Path(".").glob("*_sop.md"))

    if not sop_files:
        print("✗ Check failed: No *_sop.md file found")
        return False

    sop_file = sop_files[0]
    print(f"  Found: {sop_file}")

    with open(sop_file) as f:
        content = f.read()

    # Check for unreplaced placeholders
    placeholders = re.findall(r'\[PLACEHOLDER[^\]]*\]|\[STATE_NAME\]|\[Description\]', content)

    if placeholders:
        print(f"✗ Check failed: Found {len(placeholders)} unreplaced placeholders:")
        for ph in placeholders[:5]:  # Show first 5
            print(f"  - {ph}")
        return False

    print("✓ Check passed: SOP markdown complete")
    return True

def validate_gateway_scripts():
    """Check if all gateway scripts exist and are executable"""
    print("Checking: Gateway scripts...")

    scripts_dir = Path("scripts")
    if not scripts_dir.exists():
        print("✗ Check failed: scripts/ directory not found")
        return False

    # Look for validate_state*.sh or validate_state*.py files
    gateway_scripts = list(scripts_dir.glob("validate_state*.*"))

    if not gateway_scripts:
        print("✗ Check failed: No gateway scripts found")
        return False

    non_executable = []
    for script in gateway_scripts:
        if not os.access(script, os.X_OK) and script.suffix == ".sh":
            non_executable.append(script.name)

    if non_executable:
        print(f"✗ Check failed: Non-executable scripts: {non_executable}")
        return False

    print(f"✓ Check passed: {len(gateway_scripts)} gateway scripts found")
    return True

def validate_support_files():
    """Check if support files exist"""
    print("Checking: Support files...")

    required_files = ["progress.md"]
    missing = []

    for filename in required_files:
        if not Path(filename).exists():
            missing.append(filename)

    if missing:
        print(f"✗ Check failed: Missing files: {missing}")
        return False

    print("✓ Check passed: All support files present")
    return True

def validate_no_template_artifacts():
    """Check that no template artifacts remain"""
    print("Checking: No template artifacts...")

    sop_files = list(Path(".").glob("*_sop.md"))
    if not sop_files:
        return True  # Already caught by earlier check

    with open(sop_files[0]) as f:
        content = f.read()

    template_markers = [
        "Template Usage Notes",
        "[add workflow-specific",
        "Customize this for your",
    ]

    found_markers = [marker for marker in template_markers if marker in content]

    if found_markers:
        print(f"✗ Check failed: Template artifacts found: {found_markers}")
        return False

    print("✓ Check passed: No template artifacts")
    return True

def main():
    print("=== Validation Gateway: GENERATION ===")
    print()

    checks = [
        validate_sop_markdown(),
        validate_gateway_scripts(),
        validate_support_files(),
        validate_no_template_artifacts(),
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
