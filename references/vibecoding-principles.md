# VibeCoding Core Principles

## Overview

VibeCoding transforms probabilistic AI behavior into deterministic engineering workflows by applying four fundamental laws. These principles guide the creation of SOPs that constrain AI's natural tendency toward context drift and premature action.

## The Four Laws

### 1. Constraint-First Law (约束至上法则)

**Core Principle:** Good SOPs define what AI MUST NOT do, not what it can do.

**Why:** Large language models are probability generators that naturally drift toward "smooth continuation" rather than "planned execution." Without explicit constraints, AI will optimize for fluency over correctness.

**Implementation:**
- Use "MUST NOT" and "FORBIDDEN" instead of "should avoid"
- Define hard boundaries before describing workflows
- Specify exact conditions that trigger workflow termination

**Examples:**
```markdown
✗ BAD: "Try to avoid modifying files without reading them first"
✓ GOOD: "FORBIDDEN: Modify any file before running Read tool on it"

✗ BAD: "It's better to test before deploying"
✓ GOOD: "MUST NOT: Deploy to production without exit code 0 from test suite"

✗ BAD: "Consider checking environment variables"
✓ GOOD: "FORBIDDEN: Modify port mappings without verifying .env configuration exists"
```

### 2. Input-Output Standardization (输入输出标准化)

**Core Principle:** Treat AI as a typed function. SOPs are type declarations that enforce structure.

**Why:** Unstructured natural language output leads to inconsistent results and makes validation impossible. Structured output enables programmatic verification.

**Implementation:**
- Provide exact JSON schemas or Markdown templates
- Specify required fields and their formats
- Define validation criteria for each output type

**Examples:**
```markdown
## Required Output Format

ALWAYS output in this exact structure:

{
  "status": "pending" | "in_progress" | "completed" | "blocked",
  "artifacts": ["file1.py", "file2.md"],
  "next_step": "string describing next action",
  "validation_passed": boolean
}

Any deviation from this schema will be rejected.
```

### 3. State Machine Mechanism (状态流转机制)

**Core Principle:** SOPs must define clear states and legal transitions between them.

**Why:** Without explicit state tracking, AI loses context about project phase and may skip critical steps or repeat completed work.

**Implementation:**
- Define all valid states (e.g., "requirements", "design", "implementation", "testing")
- Specify entry conditions (prerequisites to enter a state)
- Specify exit conditions (requirements to leave a state)
- Make state transitions explicit and verifiable

**State Transition Template:**
```markdown
## State: [STATE_NAME]

### Entry Conditions (准入条件)
- [ ] Condition 1 must be satisfied
- [ ] Condition 2 must be verified
- [ ] File X must exist and pass validation

### Allowed Actions
- Action A (with constraints)
- Action B (with constraints)

### Exit Conditions (准出条件)
- [ ] Deliverable D produced
- [ ] Validation script returns exit code 0
- [ ] User approval received

### Next Valid States
- State X (if condition A)
- State Y (if condition B)
```

### 4. Built-in Degradation & Reflection (内置降级与反思)

**Core Principle:** Excellent SOPs assume failure and define recovery procedures.

**Why:** The worst SOPs assume AI will succeed on the first attempt. Real workflows require error handling and escalation paths.

**Implementation:**
- Define error thresholds (e.g., "3 consecutive failures")
- Specify degradation actions (rollback, request help, switch approach)
- Require error logging before escalation
- Build in reflection checkpoints

**Error Handling Template:**
```markdown
## Error Handling Protocol

### Failure Detection
IF any step fails:
1. Log the error with full context to `errors.log`
2. Increment failure counter for this step
3. Check failure counter threshold

### Degradation Ladder
- **1st failure:** Retry with modified approach
- **2nd failure:** Read related documentation, then retry
- **3rd failure:** STOP all modifications
  - Write failure report to `BLOCKED.md`
  - Request user intervention with specific questions
  - DO NOT proceed until user responds

### Reflection Checkpoints
After every 3 completed steps:
1. Review artifacts produced
2. Verify alignment with original requirements
3. Check for scope creep or architectural drift
```

## Anti-Patterns to Avoid

### ❌ Vague Suggestions
```markdown
"You might want to consider testing your changes"
"It would be good to check the documentation"
```

### ❌ Assuming Success
```markdown
"After implementing the feature, move to the next step"
(What if implementation fails?)
```

### ❌ Unbounded Freedom
```markdown
"Implement the authentication system however you think is best"
(No constraints = unpredictable results)
```

## The Dimensionality Reduction Metaphor

VibeCoding is fundamentally about **降维打击** (dimensionality reduction attack):

- **High-dimensional space:** Natural language programming with infinite possible interpretations
- **Low-dimensional space:** Constrained state machine with finite, verifiable transitions

Good SOPs compress the infinite possibility space of "what AI might do" into a finite, auditable workflow that humans can reason about and machines can verify.

## Practical Application

When creating a new SOP:

1. **Start with constraints:** What must NEVER happen?
2. **Define states:** What are the discrete phases of this workflow?
3. **Specify transitions:** What must be true to move between states?
4. **Add validation:** How do we verify each transition is legal?
5. **Build error handling:** What happens when validation fails?

The goal is not to write more documentation—it's to write **executable specifications** that transform probabilistic AI into deterministic automation.
