# BugBountyAI Framework - Integration Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│              Orchestrator (Brain)                           │
│  • Loads scope config                                       │
│  • Validates targets/vulns                                  │
│  • Uses Perplexity Pro LLM for planning                    │
│  • Logs all actions                                         │
└────────────┬──────────────────────┬─────────────────────────┘
             │                      │
        ┌────▼────┐           ┌─────▼──────┐
        │ Agent-S │           │   MAPTA    │
        │(GUI)    │           │ (Backend)  │
        └────┬────┘           └─────┬──────┘
             │                      │
        ┌────▼────────────────────────┴─────┐
        │  Integrated Bug Bounty Engine      │
        │  • Automate reconnaissance        │
        │  • Discover vulnerabilities       │
        │  • Generate PoC exploits          │
        │  • Stay within scope              │
        └──────────────────────────────────┘
```

## Agent-S Role (GUI Automation)

**What it does:**
- Automates browser interactions (Firefox, Burp Suite)
- Takes screenshots and analyzes visual elements
- Clicks buttons, fills forms, navigates pages
- Records user interactions for replay

**In BugBountyAI:**
- Launches Burp Suite Pro automatically
- Intercepts and modifies HTTP requests
- Performs authenticated testing
- Visual vulnerability detection

**Example Workflow:**
```python
# Use Agent-S to automate Burp scanning
agent_s_controller = AgentS()
agent_s_controller.open_burp_suite()
agent_s_controller.configure_scope(in_scope_domains)
agent_s_controller.start_active_scan()
agent_s_controller.capture_findings()  # Screenshots + data
```

## MAPTA Role (Multi-Agent Backend)

**What it does:**
- Runs CLI tools (nmap, subfinder, ffuf, sqlmap, etc.)
- Parses tool outputs
- Chains tools for complex attacks
- Generates proof-of-concept code

**In BugBountyAI:**
- Passive reconnaissance (no GUI needed)
- Subdomain enumeration
- Vulnerability-specific testing
- Log analysis and reporting

**Example Workflow:**
```python
# Use MAPTA for backend scanning
mapta_engine = MapataOrchestrator()
mapta_engine.run_recon_phase(target, scope)
mapta_engine.run_scanning_phase()
mapta_engine.generate_poc()
```

## Integration: Orchestrator Coordinates Both

**Workflow:**

```
1. Load Scope Config
   └─> Validate target domains, vulns, paths

2. LLM Planning (Perplexity Pro)
   └─> Generate intelligent reconnaissance plan
   └─> Recommend which tools/methods to use
   └─> Prioritize high-value targets

3. Agent-S Phase (GUI)
   └─> Launch Burp Suite
   └─> Configure scope
   └─> Start authenticated session testing
   └─> Capture findings

4. MAPTA Phase (Backend)
   └─> Run passive reconnaissance
   └─> Execute subdomain enumeration
   └─> Perform vulnerability scanning
   └─> Generate exploits

5. Orchestrator Synthesis
   └─> Combine Agent-S findings + MAPTA results
   └─> Validate all findings against scope
   └─> Generate compliance report

6. Reporting
   └─> Save session log with all actions
   └─> Export findings to file
   └─> Prepare for submission
```

## How to Use Both Together

### Setup (One-Time)

```python
from orchestrator import BugBountyOrchestrator
from agent_s_wrapper import AgentSController  # Custom wrapper
from mapta_wrapper import MapataController     # Custom wrapper

# Initialize
orchestrator = BugBountyOrchestrator()
agent_s = AgentSController()
mapta = MapataController()

# Load scope
orchestrator.load_scope_config('config/target_vdp.json')
```

### Execution (Per Target)

```python
# 1. Validate scope
orchestrator.check_api_connection()

# 2. Plan reconnaissance (LLM-powered)
plan = orchestrator.plan_reconnaissance()

# 3. Phase 1: Passive recon with MAPTA
mapta.run_passive_recon(
    target=orchestrator.target,
    scope=orchestrator.scope
)

# 4. Phase 2: GUI automation with Agent-S
agent_s.launch_burp()
agent_s.set_scope(orchestrator.scope['domain_scope']['in_scope_domains'])
agent_s.start_scan()
findings_gui = agent_s.extract_findings()

# 5. Combine findings
all_findings = {
    'mapta_results': mapta.results,
    'agent_s_results': findings_gui
}

# 6. Validate against scope
for finding in all_findings:
    is_valid, reason = orchestrator.validate_vulnerability_type(
        finding['type']
    )
    if not is_valid:
        print(f"Skipping out-of-scope finding: {reason}")
        continue
    
    # Process finding

# 7. Log & report
orchestrator.save_session_log()
```

## Communication Between Tools

**Agent-S → Orchestrator:**
- Sends discovered URLs for scope validation
- Reports vulnerability type (auto-checked against scope)
- Passes screenshots for LLM analysis

**MAPTA → Orchestrator:**
- Returns tool outputs (nmap, subfinder, etc.)
- Proposes next steps
- Sends findings for scope validation

**Orchestrator → Agent-S/MAPTA:**
- Validates targets before testing
- Blocks out-of-scope attempts
- Provides rate limiting instructions
- Enforces compliance rules

## Expected Output

```
[Orchestrator] Loading scope: config/target_vdp.json
[Orchestrator] Target: microsoft.com
[Orchestrator] LLM Planning...

[MAPTA] Phase 1: Passive Recon
  ├─ Subfinder: 50 subdomains
  ├─ Certificate Transparency: 15 subdomains
  └─ Total: 65 unique subdomains

[Agent-S] Phase 2: GUI Testing
  ├─ Burp Active Scan: 24 findings
  ├─ Screenshots: 50 captured
  └─ Authenticated tests: Complete

[Orchestrator] Combining results...
  ├─ Validating 89 findings against scope
  ├─ Filtering out 12 out-of-scope items
  └─ Final: 77 valid findings

[Orchestrator] Session Summary
  ├─ URLs tested: 65
  ├─ Vulns found: 77
  ├─ Scope violations: 0
  └─ Status: COMPLIANCE_PASS ✅

[Logging] Session saved: logs/session_20251103_170000.json
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent-S not finding Burp | Check Burp is installed, PATH set correctly |
| MAPTA tools not found | Install: `pip install -r mapta/requirements.txt` |
| Scope violations | Review config, ensure domain/path is in scope |
| Rate limiting issues | Reduce concurrent connections in orchestrator config |
| LLM plan too broad | Add more specific vulnerability types to out-of-scope list |

## Next Steps

1. Install Agent-S dependencies (see Agent-S README)
2. Install MAPTA dependencies (see MAPTA README)
3. Create wrapper classes for integration (see examples above)
4. Test with `test_scope_validation.py`
5. Run on real target with `orchestrator.py`
