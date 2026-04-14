# [SOP_NAME] - State Machine Workflow

> **Purpose:** [One-sentence description of what this SOP automates]
> 
> **Trigger Condition:** [When should this SOP be activated?]
> 
> **Expected Outcome:** [What deliverables/artifacts will be produced?]

---

## 🔒 Global Constraints (MUST READ FIRST)

These constraints apply to ALL states and ALL actions in this workflow:

### Forbidden Actions
- [ ] MUST NOT proceed to next state without passing exit gateway
- [ ] MUST NOT modify files without reading them first
- [ ] MUST NOT skip validation steps
- [ ] MUST NOT [add workflow-specific constraint]
- [ ] MUST NOT [add workflow-specific constraint]

### Required Behaviors
- [ ] MUST update `progress.md` after each state transition
- [ ] MUST log all errors to `errors.log` before requesting help
- [ ] MUST run validation gateway before claiming step completion
- [ ] MUST [add workflow-specific requirement]

### Error Handling Protocol
```
IF any step fails:
1. Log error with full context to errors.log
2. Increment failure counter for current state
3. Apply degradation ladder:
   - 1st failure: Retry with modified approach
   - 2nd failure: Read relevant documentation, then retry
   - 3rd failure: STOP all modifications
     → Write failure report to BLOCKED.md
     → Request user intervention with specific questions
     → DO NOT proceed until user responds
```

---

## 📋 Workflow States

```
[State_1] → [State_2] → [State_3] → [State_4] → [Complete]
    ↓           ↓           ↓           ↓
  [Gateway]   [Gateway]   [Gateway]   [Gateway]
```

---

## State 1: [STATE_NAME]

### Purpose
[What is accomplished in this state?]

### Entry Conditions (准入条件)
Before entering this state, verify:
- [ ] [Prerequisite 1 - must be verifiable]
- [ ] [Prerequisite 2 - must be verifiable]
- [ ] [File/artifact X exists and is valid]

### Allowed Actions
1. **[Action A]**
   - Description: [What this action does]
   - Constraints: [What must NOT be done]
   - Output: [What artifact is produced]

2. **[Action B]**
   - Description: [What this action does]
   - Constraints: [What must NOT be done]
   - Output: [What artifact is produced]

### Validation Gateway
**Script:** `scripts/validate_state1.sh` (or `.py`)

**What it checks:**
- [ ] [Validation criterion 1]
- [ ] [Validation criterion 2]
- [ ] [Validation criterion 3]

**How to run:**
```bash
bash scripts/validate_state1.sh
# Must return exit code 0 to proceed
```

**If gateway fails:**
- Review errors.log for details
- Fix issues identified by gateway
- Re-run gateway
- DO NOT proceed until exit code = 0

### Exit Conditions (准出条件)
To leave this state, ALL must be true:
- [ ] [Deliverable D1 produced and validated]
- [ ] [Deliverable D2 produced and validated]
- [ ] Validation gateway returns exit code 0
- [ ] progress.md updated with completion status

### Output Artifacts
```
Required files/updates:
- [artifact1.ext] - [description]
- [artifact2.ext] - [description]
- progress.md - [state completion logged]
```

### Next Valid States
- **[State_2]** - If all exit conditions met
- **[State_1]** (retry) - If gateway fails

---

## State 2: [STATE_NAME]

### Purpose
[What is accomplished in this state?]

### Entry Conditions (准入条件)
Before entering this state, verify:
- [ ] State 1 completed (check progress.md)
- [ ] [Prerequisite specific to this state]
- [ ] [Required artifact from State 1 exists]

### Allowed Actions
1. **[Action A]**
   - Description: [What this action does]
   - Constraints: [What must NOT be done]
   - Output: [What artifact is produced]

2. **[Action B]**
   - Description: [What this action does]
   - Constraints: [What must NOT be done]
   - Output: [What artifact is produced]

### Validation Gateway
**Script:** `scripts/validate_state2.sh` (or `.py`)

**What it checks:**
- [ ] [Validation criterion 1]
- [ ] [Validation criterion 2]

**How to run:**
```bash
bash scripts/validate_state2.sh
# Must return exit code 0 to proceed
```

### Exit Conditions (准出条件)
To leave this state, ALL must be true:
- [ ] [Deliverable produced]
- [ ] Validation gateway returns exit code 0
- [ ] progress.md updated

### Output Artifacts
```
Required files/updates:
- [artifact.ext] - [description]
- progress.md - [state completion logged]
```

### Next Valid States
- **[State_3]** - If all exit conditions met
- **[State_2]** (retry) - If gateway fails

---

## State 3: [STATE_NAME]

[Repeat structure from State 1/2]

---

## State 4: [STATE_NAME]

[Repeat structure from State 1/2]

---

## 📊 Progress Tracking

### progress.md Format
```markdown
# [SOP_NAME] Progress

## Current State
[STATE_NAME]

## Completed States
- [x] State 1: [STATE_NAME] - [timestamp]
- [x] State 2: [STATE_NAME] - [timestamp]
- [ ] State 3: [STATE_NAME]
- [ ] State 4: [STATE_NAME]

## Current Step Details
- Started: [timestamp]
- Attempts: [number]
- Last gateway result: [PASS/FAIL]

## Artifacts Produced
- [artifact1.ext] - [State 1]
- [artifact2.ext] - [State 2]
```

**Update Rule:** MUST update progress.md immediately after:
- Entering a new state
- Completing a state (gateway passes)
- Gateway failure (increment attempt counter)

---

## 🚨 Error Handling & Degradation

### Error Log Format (errors.log)
```
[TIMESTAMP] [STATE_NAME] [ATTEMPT_N]
Error: [error message]
Context: [what was being attempted]
Gateway output: [full gateway output]
---
```

### Degradation Ladder

#### Level 1: First Failure
- Log error to errors.log
- Analyze gateway output
- Modify approach based on error message
- Retry same state

#### Level 2: Second Failure
- Log error to errors.log
- Read relevant reference documentation
- Check if constraints were violated
- Retry with corrected approach

#### Level 3: Third Failure (ESCALATION)
- Log error to errors.log
- STOP all modifications immediately
- Create BLOCKED.md with:
  ```markdown
  # Workflow Blocked
  
  ## State: [STATE_NAME]
  ## Attempts: 3
  
  ## Problem Description
  [Detailed description of what's failing]
  
  ## Gateway Output
  [Full output from validation gateway]
  
  ## What I've Tried
  1. [Approach 1 - why it failed]
  2. [Approach 2 - why it failed]
  3. [Approach 3 - why it failed]
  
  ## Questions for User
  1. [Specific question about requirement]
  2. [Specific question about constraint]
  3. [Request for clarification on X]
  ```
- Request user intervention
- DO NOT proceed until user responds

---

## 🔍 Reflection Checkpoints

After every [N] completed states:
1. Review all artifacts produced
2. Verify alignment with original purpose
3. Check for scope creep:
   - Are we solving the original problem?
   - Have we added unnecessary features?
   - Are we still following the constraints?

**Reflection Output:** Add to progress.md
```markdown
## Reflection Checkpoint [N]
- States completed: [list]
- Alignment check: [PASS/DRIFT]
- Scope check: [ON_TRACK/CREEP_DETECTED]
- Notes: [observations]
```

---

## 📦 Final Deliverables

Upon completing all states, the following must exist:

### Required Artifacts
- [ ] [artifact1.ext] - [description]
- [ ] [artifact2.ext] - [description]
- [ ] progress.md - All states marked complete
- [ ] [workflow-specific deliverable]

### Validation
Run final validation:
```bash
bash scripts/final_validation.sh
# Must return exit code 0
```

### Completion Criteria
- [ ] All states completed
- [ ] All validation gateways passed
- [ ] All required artifacts produced
- [ ] Final validation returns exit code 0
- [ ] No BLOCKED.md exists (or has been resolved)

---

## 🛠️ Gateway Scripts Reference

All validation scripts are located in `scripts/` directory:

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `validate_state1.sh` | [description] | After State 1 actions |
| `validate_state2.sh` | [description] | After State 2 actions |
| `validate_state3.sh` | [description] | After State 3 actions |
| `final_validation.sh` | [description] | After all states complete |

**Script Requirements:**
- Must return exit code 0 on success
- Must return non-zero exit code on failure
- Must output actionable error messages
- Must complete in < 30 seconds

---

## 📚 Reference Documentation

For detailed information on principles behind this SOP:
- **VibeCoding Principles:** See `references/vibecoding-principles.md`
- **Gateway Design:** See `references/engineering-gateways.md`

---

## Template Usage Notes

**When creating a new SOP from this template:**

1. Replace all `[PLACEHOLDER]` text with actual content
2. Define 3-7 states (not too few, not too many)
3. Create validation gateway scripts for each state
4. Test the workflow end-to-end before deployment
5. Remove this "Template Usage Notes" section

**Key Customization Points:**
- Global Constraints section: Add workflow-specific forbidden actions
- Number of states: Adjust based on workflow complexity
- Gateway scripts: Implement actual validation logic
- Reflection frequency: Set checkpoint interval (every 2-3 states)
- Error handling: Customize degradation ladder if needed
