#!/bin/bash
# Example validation gateway script template
# Customize this for your specific validation needs

set -e  # Exit on any error

echo "=== Validation Gateway: [STATE_NAME] ==="
echo ""

# Initialize validation status
VALIDATION_PASSED=true

# ============================================
# Validation Check 1: [Description]
# ============================================
echo "Checking: [What is being validated]..."

if [ -f "expected_file.txt" ]; then
    echo "✓ Check 1 passed: File exists"
else
    echo "✗ Check 1 failed: expected_file.txt not found"
    VALIDATION_PASSED=false
fi

# ============================================
# Validation Check 2: [Description]
# ============================================
echo "Checking: [What is being validated]..."

# Example: Run a command and check exit code
if command -v python3 &> /dev/null; then
    echo "✓ Check 2 passed: Python3 available"
else
    echo "✗ Check 2 failed: Python3 not found"
    VALIDATION_PASSED=false
fi

# ============================================
# Validation Check 3: [Description]
# ============================================
echo "Checking: [What is being validated]..."

# Example: Validate file content
if grep -q "expected_pattern" some_file.txt 2>/dev/null; then
    echo "✓ Check 3 passed: Pattern found"
else
    echo "✗ Check 3 failed: Expected pattern not found in some_file.txt"
    VALIDATION_PASSED=false
fi

# ============================================
# Final Result
# ============================================
echo ""
if [ "$VALIDATION_PASSED" = true ]; then
    echo "========================================="
    echo "✓ GATEWAY PASSED: All validations successful"
    echo "========================================="
    exit 0
else
    echo "========================================="
    echo "✗ GATEWAY FAILED: Some validations failed"
    echo "========================================="
    echo ""
    echo "Fix the issues above and re-run this script."
    exit 1
fi
