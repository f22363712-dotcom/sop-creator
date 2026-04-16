---
name: sop-creator
description: Generate deterministic state-machine SOPs that transform probabilistic AI into reliable automation pipelines
version: 1.0.0
---

# SOP Creator: VibeCoding Meta-Skill

Transform natural language requirements into high-certainty state machine workflows.

## Purpose

This skill generates Standard Operating Procedures (SOPs) that constrain AI behavior through:
- Physical validation gateways (exit code enforcement)
- Explicit state machines (finite, auditable transitions)
- Built-in error handling (degradation ladders)
- Structured I/O (typed inputs/outputs)

## When to Use

Invoke `/sop-creator` when you need to:
- Automate multi-step workflows with AI
- Ensure consistent execution across iterations
- Prevent context drift and premature actions
- Create auditable, verifiable processes

## State Machine

```
INIT → REQUIREMENTS → DESIGN → GENERATION → VALIDATION → COMPLETE
  ↓        ↓            ↓          ↓            ↓
[Gate]   [Gate]      [Gate]    [Gate]       [Gate]
```

---

## State 1: REQUIREMENTS

### Entry Conditions
- User has provided workflow description
- Working directory is writable

### Actions
1. **Extract Core Requirements**
   - Identify workflow trigger condition
   - Define expected deliverables
   - List critical constraints
   - Determine validation criteria

2. **Generate requirements.json**
   ```json
   {
     "workflow_name": "string",
     "purpose": "string",
     "trigger": "string",
     "deliverables": ["string"],
     "constraints": ["string"],
     "states": ["string"],
     "validation_methods": ["string"]
   }
   ```

### Validation Gateway
**Script:** `scripts/validate_requirements.py`

Checks:
- [ ] requirements.json exists and is valid JSON
- [ ] All required fields present
- [ ] At least 3 states defined
- [ ] At least 1 validation method per state

### Exit Conditions
- [ ] requirements.json created
- [ ] Gateway returns exit code 0
- [ ] User approves requirements

### Next State
→ DESIGN (if approved)
→ REQUIREMENTS (if rejected - revise)

---

## State 2: DESIGN

### Entry Conditions
- requirements.json exists and validated
- User approval received

### Actions
1. **Design State Transitions**
   - Map state flow diagram
   - Define entry/exit conditions per state
   - Specify allowed actions per state
   - Design validation gateways

2. **Generate design.json**
   ```json
   {
     "states": [
       {
         "name": "string",
         "purpose": "string",
         "entry_conditions": ["string"],
         "actions": ["string"],
         "exit_conditions": ["string"],
         "gateway_script": "string",
         "next_states": ["string"]
       }
     ],
     "global_constraints": ["string"],
     "error_handling": {
       "max_retries": 3,
       "escalation_actions": ["string"]
     }
   }
   ```

### Validation Gateway
**Script:** `scripts/validate_design.py`

Checks:
- [ ] design.json exists and is valid JSON
- [ ] All states have entry/exit conditions
- [ ] All states have gateway scripts defined
- [ ] State transitions form valid DAG (no orphans)
- [ ] Error handling defined

### Exit Conditions
- [ ] design.json created
- [ ] Gateway returns exit code 0
- [ ] State machine is acyclic (except retry loops)

### Next State
→ GENERATION

---

## State 3: GENERATION

### Entry Conditions
- design.json exists and validated
- Output directory specified

### Actions
1. **Generate SOP Markdown**
   - Use `assets/state-machine-sop.md` as template
   - Populate with design.json data
   - Ensure < 200 lines per section
   - Add workflow-specific constraints

2. **Generate Gateway Scripts**
   - Create `scripts/validate_state{N}.sh` for each state
   - Use `assets/gateway-template.sh` as base
   - Implement validation logic from design.json
   - Ensure scripts return proper exit codes

3. **Generate Support Files**
   - Create `progress.md` template
   - Create `errors.log` template
   - Create `BLOCKED.md` template

### Validation Gateway
**Script:** `scripts/validate_generation.py`

Checks:
- [ ] SOP markdown file exists
- [ ] All gateway scripts exist and are executable
- [ ] progress.md template exists
- [ ] All placeholders replaced

### Exit Conditions
- [ ] All files generated
- [ ] Gateway returns exit code 0
- [ ] No [PLACEHOLDER] text remains

### Next State
→ VALIDATION

---

## State 4: VALIDATION

### Entry Conditions
- All SOP files generated
- Gateway scripts executable

### Actions
1. **Dry-Run Test**
   - Execute each gateway script with test data
   - Verify exit codes (0 for pass, non-zero for fail)
   - Check error messages are actionable

2. **Structure Validation**
   - Verify state machine completeness
   - Check all states have gateways
   - Ensure error handling present
   - Validate constraint clarity

3. **Generate Validation Report**
   ```markdown
   # SOP Validation Report
   
   ## Gateway Tests
   - [x] validate_state1.sh: PASS
   - [x] validate_state2.sh: PASS
   
   ## Structure Checks
   - [x] All states have entry/exit conditions
   - [x] All gateways return proper exit codes
   - [x] Error handling defined
   
   ## Issues Found
   [List any issues]
   
   ## Status: READY / NEEDS_REVISION
   ```

### Validation Gateway
**Script:** `scripts/final_validation.sh`

Checks:
- [ ] All state gateways executable
- [ ] Test execution successful
- [ ] No structural issues found
- [ ] Validation report shows READY

### Exit Conditions
- [ ] Validation report generated
- [ ] Gateway returns exit code 0
- [ ] Status = READY

### Next State
→ COMPLETE

---

## Global Constraints

### FORBIDDEN Actions
- MUST NOT generate SOPs without validation gateways
- MUST NOT create states without exit conditions
- MUST NOT skip gateway script generation
- MUST NOT exceed 200 lines per SOP section
- MUST NOT use vague language ("should", "might", "consider")

### REQUIRED Behaviors
- MUST use imperative language ("MUST", "FORBIDDEN")
- MUST include error handling for each state
- MUST generate executable gateway scripts
- MUST validate all outputs before proceeding
- MUST update progress after each state

---

## Error Handling

### Degradation Ladder

**Level 1: First Failure**
- Log error to errors.log
- Analyze validation output
- Retry with corrections

**Level 2: Second Failure**
- Log error to errors.log
- Review reference documentation
- Check constraint violations
- Retry with revised approach

**Level 3: Third Failure (ESCALATION)**
- Log error to errors.log
- STOP all generation
- Create BLOCKED.md:
  ```markdown
  # SOP Generation Blocked
  
  ## State: [STATE_NAME]
  ## Attempts: 3
  
  ## Problem
  [Description]
  
  ## Gateway Output
  [Full output]
  
  ## Tried Approaches
  1. [Approach 1 - why failed]
  2. [Approach 2 - why failed]
  3. [Approach 3 - why failed]
  
  ## Questions
  1. [Specific question]
  2. [Clarification needed]
  ```
- Request user intervention
- DO NOT proceed until user responds

---

## Output Structure

```
{output_directory}/
├── {workflow_name}_sop.md    # Main SOP document
├── progress.md               # Progress tracking template
├── errors.log                # Error log template
├── BLOCKED.md                # Escalation template (if needed)
├── scripts/
│   ├── validate_state1.sh    # Gateway for state 1
│   ├── validate_state2.sh    # Gateway for state 2
│   ├── validate_state3.sh    # Gateway for state 3
│   └── final_validation.sh   # Final validation
└── .sop-metadata.json        # Generation metadata
```

---

## Usage Example

```bash
# Invoke the skill
/sop-creator

# Provide requirements when prompted
"Create an SOP for deploying a Docker container to production"

# Review generated requirements.json
# Approve or request revisions

# Skill generates complete SOP package
# All files created in specified output directory

# Test the generated SOP
cd output_directory
bash scripts/validate_state1.sh
```

---

## References

- **VibeCoding Principles:** `references/vibecoding-principles.md`
- **Gateway Design:** `references/engineering-gateways.md`
- **SOP Template:** `assets/state-machine-sop.md`
- **Gateway Templates:** `assets/gateway-template.{sh,py}`

---

## Version History

- **1.0.0** - Initial release with 4-state generation pipeline
