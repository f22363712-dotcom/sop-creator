# Engineering Gateways: Physical Validation Mechanisms

## Core Concept

**Physical Gateway (物理门禁):** A programmatic checkpoint that AI cannot bypass through persuasion or rationalization. The gateway returns a binary signal (pass/fail) that determines whether workflow progression is allowed.

## Why Physical Gateways Matter

### The Problem with Human-Only Validation

Traditional SOPs rely on human verification:
```markdown
"After implementing the feature, wait for my approval before proceeding"
```

**Limitations:**
- Creates human bottleneck (developer must be present)
- Subjective evaluation (what does "looks good" mean?)
- Doesn't scale (can't validate 100 steps manually)
- Prone to fatigue (humans miss issues after reviewing many steps)

### The Power of Automated Validation

Physical gateways shift validation from human judgment to programmatic verification:
```markdown
"After implementing the feature, run `npm test`. 
Only if exit code = 0, update progress and proceed to next step."
```

**Benefits:**
- Objective criteria (exit code 0 = pass, non-zero = fail)
- Immediate feedback (no waiting for human review)
- Scales infinitely (can validate thousands of operations)
- Never fatigues (consistent validation quality)

## Gateway Types

### 1. Test-Driven Gateways (TDD)

**Principle:** Write tests before implementation. Tests define "done."

**Implementation Pattern:**
```markdown
## Step 1: Define Success Criteria
BEFORE writing any implementation code:
1. Create test file: `tests/test_feature.py`
2. Write test cases that define expected behavior
3. Run tests (they should fail initially)
4. Commit test file

## Step 2: Implement Feature
1. Write implementation code
2. Run `pytest tests/test_feature.py`
3. IF exit code ≠ 0:
   - Fix implementation
   - Retry (max 3 attempts)
   - If still failing, STOP and request help
4. IF exit code = 0:
   - Update progress.md
   - Proceed to next step

FORBIDDEN: Update progress.md if tests are not passing
```

**Example Gateway Script:**
```bash
#!/bin/bash
# gateway_test.sh

pytest tests/ --tb=short
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Gateway PASSED: All tests passing"
    exit 0
else
    echo "✗ Gateway FAILED: Tests failing"
    echo "Fix issues before proceeding"
    exit 1
fi
```

### 2. Linting & Type-Checking Gateways

**Principle:** Code must meet quality standards before progression.

**Implementation Pattern:**
```markdown
## Code Quality Gateway

After writing any code:
1. Run linter: `npm run lint`
2. Run type checker: `npm run type-check`
3. Both must return exit code 0

Gateway script: `scripts/quality_gate.sh`

FORBIDDEN: Commit code that fails quality checks
```

**Example Gateway Script:**
```bash
#!/bin/bash
# quality_gate.sh

echo "Running linter..."
npm run lint
LINT_EXIT=$?

echo "Running type checker..."
npm run type-check
TYPE_EXIT=$?

if [ $LINT_EXIT -eq 0 ] && [ $TYPE_EXIT -eq 0 ]; then
    echo "✓ Quality Gateway PASSED"
    exit 0
else
    echo "✗ Quality Gateway FAILED"
    [ $LINT_EXIT -ne 0 ] && echo "  - Linting errors detected"
    [ $TYPE_EXIT -ne 0 ] && echo "  - Type errors detected"
    exit 1
fi
```

### 3. Schema Validation Gateways

**Principle:** Structured data must conform to schema before use.

**Implementation Pattern:**
```markdown
## Configuration Validation Gateway

After generating any JSON/YAML configuration:
1. Run validator: `python scripts/validate_config.py <config_file>`
2. Must return exit code 0

FORBIDDEN: Use configuration files that fail schema validation
```

**Example Gateway Script:**
```python
#!/usr/bin/env python3
# validate_config.py

import sys
import json
from jsonschema import validate, ValidationError

SCHEMA = {
    "type": "object",
    "required": ["name", "version", "dependencies"],
    "properties": {
        "name": {"type": "string"},
        "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
        "dependencies": {"type": "array"}
    }
}

def validate_config(filepath):
    with open(filepath) as f:
        config = json.load(f)
    
    try:
        validate(instance=config, schema=SCHEMA)
        print(f"✓ Config validation PASSED: {filepath}")
        return 0
    except ValidationError as e:
        print(f"✗ Config validation FAILED: {e.message}")
        return 1

if __name__ == "__main__":
    sys.exit(validate_config(sys.argv[1]))
```

### 4. Diff-Based Gateways

**Principle:** Changes must meet specific criteria (size, scope, files affected).

**Implementation Pattern:**
```markdown
## Change Scope Gateway

Before committing:
1. Run: `python scripts/check_diff.py`
2. Validates:
   - No changes to files outside current feature scope
   - Total diff < 500 lines (prevents scope creep)
   - No sensitive files modified (.env, credentials)

FORBIDDEN: Commit if gateway fails
```

**Example Gateway Script:**
```python
#!/usr/bin/env python3
# check_diff.py

import subprocess
import sys

FORBIDDEN_FILES = ['.env', 'credentials.json', 'secrets.yaml']
MAX_LINES = 500

def check_diff():
    # Get changed files
    result = subprocess.run(['git', 'diff', '--name-only'], 
                          capture_output=True, text=True)
    changed_files = result.stdout.strip().split('\n')
    
    # Check forbidden files
    forbidden_changed = [f for f in changed_files if f in FORBIDDEN_FILES]
    if forbidden_changed:
        print(f"✗ Gateway FAILED: Forbidden files modified: {forbidden_changed}")
        return 1
    
    # Check diff size
    result = subprocess.run(['git', 'diff', '--stat'], 
                          capture_output=True, text=True)
    # Parse total lines changed
    # (simplified - real implementation would parse git output)
    
    print("✓ Diff Gateway PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(check_diff())
```

## Integration with State Machines

Physical gateways enforce state transitions:

```markdown
## State Transition: Implementation → Testing

### Exit Conditions from Implementation State
1. All implementation code written
2. **GATEWAY:** Run `scripts/test_gateway.sh`
   - IF exit code = 0: Transition to Testing state
   - IF exit code ≠ 0: Remain in Implementation state, fix issues

### Entry Conditions to Testing State
- Can only enter if test_gateway.sh passed
- progress.md must show "Implementation: COMPLETE"

This creates a physical barrier: AI cannot claim "implementation is done" 
without proving it via passing tests.
```

## Best Practices

### 1. Make Gateways Fast
- Gateways should complete in < 30 seconds
- For slow tests, create fast smoke tests as gateways
- Full test suite can run separately

### 2. Make Gateways Informative
```bash
# Bad: Silent failure
exit 1

# Good: Actionable feedback
echo "✗ Gateway FAILED: 3 tests failing in auth module"
echo "Run 'pytest tests/auth/ -v' for details"
exit 1
```

### 3. Make Gateways Composable
```bash
# master_gateway.sh - runs all sub-gateways
./scripts/test_gateway.sh && \
./scripts/quality_gateway.sh && \
./scripts/security_gateway.sh
```

### 4. Version Control Gateway Scripts
- Store all gateway scripts in `scripts/` directory
- Include them in git repository
- Document their purpose in SOP

## Anti-Patterns

### ❌ Soft Validation
```markdown
"Run tests and make sure they mostly pass"
(What is "mostly"? 90%? 95%?)
```

### ❌ Optional Gateways
```markdown
"If you have time, run the test suite"
(Gateways must be mandatory, not optional)
```

### ❌ Human-Interpretable-Only Output
```bash
# Bad: Requires human to interpret
echo "Tests completed. Please review results."

# Good: Machine-readable exit code
exit $TEST_EXIT_CODE
```

## The Gateway Mindset

When designing SOPs, ask:

1. **What does "done" mean for this step?**
   → Write a test that verifies it

2. **How do I know the output is correct?**
   → Write a validator script

3. **Can AI bypass this check through clever prompting?**
   → If yes, it's not a real gateway

4. **Does this scale to 100 iterations?**
   → If no, automate it

Physical gateways transform SOPs from "guidelines AI should follow" into "constraints AI cannot violate." This is the foundation of reliable AI automation.
