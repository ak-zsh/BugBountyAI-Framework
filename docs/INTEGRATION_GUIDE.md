\# BugBountyAI Framework - Agent-S + MAPTA Integration Guide



\## Architecture Overview



┌─────────────────────────────────────────────────────────────┐

│ Orchestrator (Brain) │

│ - Loads scope config │

│ - Validates targets/vulns │

│ - Uses Perplexity Pro LLM for planning │

│ - Logs all actions │

└────────────┬──────────────────────┬─────────────────────────┘

│ │

┌────▼────┐ ┌─────▼──────┐

│ Agent-S │ │ MAPTA │

│(GUI) │ │ (Backend) │

└────┬────┘ └─────┬──────┘

│ │

┌────▼────────────────────────┴─────┐

│ Integrated Bug Bounty Engine │

│ - Automate reconnaissance │

│ - Discover vulnerabilities │

│ - Generate PoC exploits │

│ - Stay within scope │

└──────────────────────────────────┘



text



\## Agent-S Role (GUI Automation)



\*\*What it does:\*\*

\- Automates browser interactions (Firefox, Burp Suite)

\- Takes screenshots and analyzes visual elements

\- Clicks buttons, fills forms, navigates pages

\- Records user interactions for replay



\*\*In BugBountyAI:\*\*

\- Launches Burp Suite Pro automatically

\- Intercepts and modifies HTTP requests

\- Performs authenticated testing

\- Visual vulnerability detection



\*\*Example Workflow:\*\*

Use Agent-S to automate Burp scanning

agent\_s\_controller = AgentS()

agent\_s\_controller.open\_burp\_suite()

agent\_s\_controller.configure\_scope(in\_scope\_domains)

agent\_s\_controller.start\_active\_scan()

agent\_s\_controller.capture\_findings() # Screenshots + data



text



\## MAPTA Role (Multi-Agent Backend)



\*\*What it does:\*\*

\- Runs CLI tools (nmap, subfinder, ffuf, sqlmap, etc.)

\- Parses tool outputs

\- Chains tools for complex attacks

\- Generates proof-of-concept code



\*\*In BugBountyAI:\*\*

\- Passive reconnaissance (no GUI needed)

\- Subdomain enumeration

\- Vulnerability-specific testing

\- Log analysis and reporting



\*\*Example Workflow:\*\*

Use MAPTA for backend scanning

mapta\_engine = MapataOrchestrator()

mapta\_engine.run\_recon\_phase(target, scope)

mapta\_engine.run\_scanning\_phase()

mapta\_engine.generate\_poc()



text



\## Integration: Orchestrator Coordinates Both



\*\*Workflow:\*\*



Load Scope Config

└─> Validate target domains, vulns, paths



LLM Planning (Perplexity Pro)

└─> Generate intelligent reconnaissance plan

└─> Recommend which tools/methods to use

└─> Prioritize high-value targets



Agent-S Phase (GUI)

└─> Launch Burp Suite

└─> Configure scope

└─> Start authenticated session testing

└─> Capture findings



MAPTA Phase (Backend)

└─> Run passive reconnaissance

└─> Execute subdomain enumeration

└─> Perform vulnerability scanning

└─> Generate exploits



Orchestrator Synthesis

└─> Combine Agent-S findings + MAPTA results

└─> Validate all findings against scope

└─> Generate compliance report



Reporting

└─> Save session log with all actions

└─> Export findings to file

└─> Prepare for submission



text



\## How to Use Both Together



\### Setup (One-Time)



from orchestrator import BugBountyOrchestrator

from agent\_s\_wrapper import AgentSController # Custom wrapper

from mapta\_wrapper import MapataController # Custom wrapper



Initialize

orchestrator = BugBountyOrchestrator()

agent\_s = AgentSController()

mapta = MapataController()



Load scope

orchestrator.load\_scope\_config('config/target\_vdp.json')



text



\### Execution (Per Target)



1\. Validate scope

orchestrator.check\_api\_connection()



2\. Plan reconnaissance (LLM-powered)

plan = orchestrator.plan\_reconnaissance()



3\. Phase 1: Passive recon with MAPTA

mapta.run\_passive\_recon(

target=orchestrator.target,

scope=orchestrator.scope

)



4\. Phase 2: GUI automation with Agent-S

agent\_s.launch\_burp()

agent\_s.set\_scope(orchestrator.scope\['domain\_scope']\['in\_scope\_domains'])

agent\_s.start\_scan()

findings\_gui = agent\_s.extract\_findings()



5\. Combine findings

all\_findings = {

'mapta\_results': mapta.results,

'agent\_s\_results': findings\_gui

}



6\. Validate against scope

for finding in all\_findings:

is\_valid, reason = orchestrator.validate\_vulnerability\_type(

finding\['type']

)

if not is\_valid:

print(f"Skipping out-of-scope finding: {reason}")

continue



text

\# Process finding

7\. Log \& report

orchestrator.save\_session\_log()



text



\## Communication Between Tools



\*\*Agent-S → Orchestrator:\*\*

\- Sends discovered URLs for scope validation

\- Reports vulnerability type (auto-checked against scope)

\- Passes screenshots for LLM analysis



\*\*MAPTA → Orchestrator:\*\*

\- Returns tool outputs (nmap, subfinder, etc.)

\- Proposes next steps

\- Sends findings for scope validation



\*\*Orchestrator → Agent-S/MAPTA:\*\*

\- Validates targets before testing

\- Blocks out-of-scope attempts

\- Provides rate limiting instructions

\- Enforces compliance rules



\## Expected Output



\[Orchestrator] Loading scope: config/target\_vdp.json

\[Orchestrator] Target: microsoft.com

\[Orchestrator] LLM Planning...



\[MAPTA] Phase 1: Passive Recon

├─ Subfinder: 50 subdomains

├─ Certificate Transparency: 15 subdomains

└─ Total: 65 unique subdomains



\[Agent-S] Phase 2: GUI Testing

├─ Burp Active Scan: 24 findings

├─ Screenshots: 50 captured

└─ Authenticated tests: Complete



\[Orchestrator] Combining results...

├─ Validating 89 findings against scope

├─ Filtering out 12 out-of-scope items

└─ Final: 77 valid findings



\[Orchestrator] Session Summary

├─ URLs tested: 65

├─ Vulns found: 77

├─ Scope violations: 0

└─ Status: COMPLIANCE\_PASS ✅



\[Logging] Session saved: logs/session\_20251103\_170000.json



text



\## Troubleshooting



| Issue | Solution |

|-------|----------|

| Agent-S not finding Burp | Check Burp is installed, PATH set correctly |

| MAPTA tools not found | Install: `pip install -r mapta/requirements.txt` |

| Scope violations | Review config, ensure domain/path is in scope |

| Rate limiting issues | Reduce concurrent connections in orchestrator config |

| LLM plan too broad | Add more specific vulnerability types to out-of-scope list |



\## Next Steps



1\. Install Agent-S dependencies (see Agent-S README)

2\. Install MAPTA dependencies (see MAPTA README)

3\. Create wrapper classes for integration (see examples above)

4\. Test with `test\_scope\_validation.py`

5\. Run on real target with `orchestrator.py`

