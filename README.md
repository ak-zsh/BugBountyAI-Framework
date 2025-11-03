# 🎯 BugBountyAI Framework

> **AI-Powered, Scope-Aware Bug Bounty Automation**
> 
> Unify **Agent-S** (GUI automation) + **MAPTA** (multi-agent pentesting) + **Perplexity Pro** (LLM reasoning) into one intelligent bug bounty engine.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![VDP/BBP](https://img.shields.io/badge/VDP%2FBBP-Ready-orange)

---

## 📖 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Configuration](#configuration)
  - [Basic Testing](#basic-testing)
  - [Advanced Integration](#advanced-integration)
- [Architecture](#architecture)
- [Scope Enforcement](#scope-enforcement)
- [Compliance & Logging](#compliance--logging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

---

## ✨ Features

### 🔐 **Scope-Aware Testing**
- Automatic domain/path validation
- Vulnerability type filtering
- HTTP method restriction
- Rate limiting enforcement
- Real-time scope violation detection

### 🧠 **LLM-Powered Intelligence**
- **Perplexity Pro** generates intelligent reconnaissance plans
- Context-aware vulnerability analysis
- Smart tool recommendations
- Finding prioritization

### 🤖 **GUI & CLI Automation**
- **Agent-S**: Browser automation (Burp Suite, Firefox)
- **MAPTA**: Multi-agent tool orchestration
- Automatic tool chaining
- Screenshot capture & analysis

### 📋 **Compliance First**
- Timestamped action logging
- Audit trails for authorization proof
- Scope violation reports
- Session summaries

### 🛡️ **Enterprise-Grade**
- Windows primary + Kali VM support
- Docker integration ready
- Multi-LLM support (Perplexity Pro, Gemini Pro 2.5)
- Extensible architecture

---

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Windows 11 / Kali Linux (6.9GB+ RAM recommended)
# Python 3.11+
# Docker Desktop (optional)
# Perplexity Pro subscription (API key required)
```

### 2. Clone & Setup

```bash
git clone https://github.com/ak-zsh/BugBountyAI-Framework.git
cd BugBountyAI-Framework

# Install dependencies
pip install -e Agent-S/
pip install langchain langchain-openai openai python-dotenv requests
```

### 3. Configure API

```bash
# Create .env from template
cp .env.example Agent-S/.env

# Edit with your Perplexity Pro API key
notepad Agent-S/.env
# Add: PERPLEXITY_API_KEY=your_key_here
```

### 4. Test Installation

```bash
python test_scope_validation.py
```

Expected: ✅ All tests pass, scope validation working

### 5. Run on Your Target

```bash
# Create scope config for your target
cp config/microsoft_vdp_scope.json config/your_target.json

# Edit config with your target details
notepad config/your_target.json

# Run orchestrator
python orchestrator.py --config config/your_target.json
```

---

## 📦 Installation

### Full Setup Guide

#### Step 1: Clone Repository

```bash
git clone https://github.com/ak-zsh/BugBountyAI-Framework.git
cd BugBountyAI-Framework
```

#### Step 2: Install Agent-S (GUI Automation)

```bash
cd Agent-S
pip install -e .
cd ..
```

#### Step 3: Install MAPTA (Backend Tools)

```bash
cd mapta
pip install -e .
cd ..
```

#### Step 4: Install Framework Dependencies

```bash
pip install langchain langchain-openai openai python-dotenv requests
```

#### Step 5: Configure API Keys

```bash
# Copy template
cp .env.example Agent-S/.env

# Add your Perplexity Pro API key
# https://www.perplexity.ai/settings/api
```

#### Step 6: Verify Installation

```bash
python -c "from orchestrator import BugBountyOrchestrator; print('✅ Framework ready')"
```

---

## 🎮 Usage

### Configuration

#### Create VDP/BBP Scope Config

```bash
notepad config/my_target.json
```

**Example Config (Microsoft MSRC VDP):**

```json
{
  "program": {
    "name": "Microsoft MSRC VDP",
    "platform": "Microsoft Security Response Center",
    "type": "VDP",
    "authorization": "Public Disclosure Program",
    "link": "https://msrc.microsoft.com/vulnerability-disclosure"
  },
  "target": "microsoft.com",
  "domain_scope": {
    "in_scope_domains": [
      "microsoft.com",
      "*.microsoft.com",
      "*.office.com",
      "*.azure.com"
    ],
    "out_of_scope_domains": [
      "*.test.microsoft.com",
      "internal.microsoft.com"
    ]
  },
  "vulnerability_scope": {
    "in_scope_vulns": [
      "XSS", "CSRF", "SQLi", "RCE", "Authentication Bypass",
      "Authorization Bypass", "Information Disclosure", "SSRF"
    ],
    "out_of_scope_vulns": [
      "Social Engineering", "Phishing", "Brute Force", "Clickjacking"
    ]
  },
  "testing_restrictions": {
    "blocked_paths": ["/admin", "/internal", "/api/internal", "/debug"],
    "blocked_methods": [
      "DoS", "DDoS", "Data Exfiltration", "Account Takeover"
    ]
  },
  "rate_limits": {
    "requests_per_second": 5,
    "requests_per_minute": 300,
    "concurrent_connections": 2
  }
}
```

### Basic Testing

#### 1. Validate Scope Configuration

```bash
python test_scope_validation.py
```

**Output:**
- ✅ All domains loaded
- ✅ Vulnerabilities filtered
- ✅ Scope violations detected
- ✅ Session logged

#### 2. Test URL Against Scope

```python
from orchestrator import BugBountyOrchestrator

orchestrator = BugBountyOrchestrator()
orchestrator.load_scope_config('config/microsoft_vdp_scope.json')

# Test URLs
is_valid, reason = orchestrator.validate_target_url('https://microsoft.com/login')
print(f"Valid: {is_valid}, Reason: {reason}")
# Output: Valid: True, Reason: Domain microsoft.com is in scope and allowed

# Test blocked URL
is_valid, reason = orchestrator.validate_target_url('https://internal.microsoft.com/admin')
print(f"Valid: {is_valid}, Reason: {reason}")
# Output: Valid: False, Reason: Domain internal.microsoft.com is explicitly blocked
```

#### 3. Generate LLM-Powered Reconnaissance Plan

```python
orchestrator.plan_reconnaissance()
```

**Output:**
- Step-by-step recon plan
- Tools recommended
- Rate limits applied
- Scope constraints enforced

#### 4. Save Session & Generate Compliance Report

```python
log_file = orchestrator.save_session_log()
orchestrator.print_violation_report()
```

**Output:**
- `logs/session_20251103_170000.json` (audit trail)
- Summary: 65 URLs tested, 77 findings, 0 scope violations ✅

### Advanced Integration

#### Using Agent-S for Authenticated Testing

```python
from orchestrator import BugBountyOrchestrator
# Note: Agent-S integration requires additional setup
# See docs/INTEGRATION_GUIDE.md for details

orchestrator = BugBountyOrchestrator()
orchestrator.load_scope_config('config/target.json')

# Launch Burp Suite (Agent-S handles automation)
# Configuration happens automatically based on scope

# Findings are validated against scope before reporting
```

#### Using MAPTA for Backend Scanning

```python
# Note: MAPTA integration requires tool installation
# See docs/INTEGRATION_GUIDE.md for details

orchestrator = BugBountyOrchestrator()
orchestrator.load_scope_config('config/target.json')

# MAPTA runs CLI tools respecting orchestrator scope
# All findings validated before reporting
```

#### Custom Vulnerability Analysis

```python
# Analyze a finding within program scope context
analysis = orchestrator.analyze_findings(
    finding_description="XSS in search parameter with CSP bypass"
)
print(analysis)
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              BugBountyAI Framework                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐    ┌──────────────┐              │
│  │ Orchestrator │    │ Perplexity   │              │
│  │ (Validator & │◄──►│ Pro LLM      │              │
│  │  Planner)    │    │ (sonar-pro)  │              │
│  └──┬───┬───┬──┘     └──────────────┘              │
│     │   │   │                                      │
│  ┌──▼─┐│   │ ┌──────────────────────┐              │
│  │    ││   └─►│ Scope Validator      │              │
│  │    │└─────►│ • URLs               │              │
│  │    │       │ • Vulns              │              │
│  │    │       │ • Methods            │              │
│  │    │       │ • Rate Limits        │              │
│  │    │       └──────────────────────┘              │
│  │    │                                            │
│  │    ├─────────────────┬──────────────┐           │
│  │    │                 │              │           │
│  └────┴─┐          ┌────▼────┐   ┌────▼────┐      │
│         │          │ Agent-S  │   │  MAPTA  │      │
│         │          │ (GUI)    │   │(Backend)│      │
│         │          └──────────┘   └─────────┘      │
│         │                                          │
│    ┌────▼────────────────────────────────────┐    │
│    │ Session Logging & Compliance Tracking  │    │
│    │ • Timestamped actions                  │    │
│    │ • Scope violations detected            │    │
│    │ • Audit trail for proof                │    │
│    └───────────────────────────────────────┘    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔐 Scope Enforcement

### How It Works

```python
# 1. Load scope
orchestrator.load_scope_config('config/target.json')

# 2. Validate before testing
is_valid, reason = orchestrator.validate_target_url(url)
if not is_valid:
    print(f"Blocked: {reason}")
    return

# 3. Check vulnerability type
is_testable, reason = orchestrator.validate_vulnerability_type(vuln)
if not is_testable:
    print(f"Out of scope: {reason}")
    return

# 4. Verify testing method
is_allowed, reason = orchestrator.validate_method(method)
if not is_allowed:
    print(f"Method forbidden: {reason}")
    return

# 5. Test safely within bounds
perform_test()

# 6. Log for compliance
orchestrator.save_session_log()
```

### Violation Examples

```
❌ BLOCKED: https://internal.microsoft.com/admin
   Reason: Domain internal.microsoft.com is explicitly blocked

❌ NOT ALLOWED: Social Engineering
   Reason: Vulnerability Social Engineering is OUT OF SCOPE

❌ BLOCKED: DoS Attack
   Reason: Method DoS is not allowed

❌ RATE LIMIT: 10 requests/sec
   Reason: Exceeds configured limit of 5 requests/sec
```

---

## 📊 Compliance & Logging

### Session Log Structure

```json
{
  "timestamp": "2025-11-03T17:00:00.000000",
  "framework_version": "2.0",
  "program": "Microsoft MSRC VDP",
  "target": "microsoft.com",
  "summary": {
    "total_actions": 150,
    "urls_validated": 65,
    "vulns_tested": 77,
    "scope_violations": 0,
    "compliance_status": "PASSED"
  },
  "actions": [
    {
      "timestamp": "2025-11-03T17:00:05.123456",
      "action": "scope_config_loaded",
      "program": "Microsoft MSRC VDP",
      "status": "success"
    },
    {
      "timestamp": "2025-11-03T17:00:10.234567",
      "action": "url_validated",
      "url": "https://microsoft.com/login",
      "status": "allowed"
    }
  ],
  "validated_urls": [...],
  "scope_violations": [],
  "tested_vulnerabilities": [...]
}
```

### Generating Compliance Reports

```bash
# View violation report
python -c "from orchestrator import BugBountyOrchestrator; \
o = BugBountyOrchestrator(); \
o.load_scope_config('config/target.json'); \
o.print_violation_report()"

# Export session log (automatic)
# Saved to: logs/session_YYYYMMDD_HHMMSS.json
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: openai` | `pip install openai python-dotenv` |
| API connection failed | Check `PERPLEXITY_API_KEY` in `Agent-S/.env` |
| Config file not found | Create config: `cp config/microsoft_vdp_scope.json config/your_target.json` |
| Scope violations detected | Review config, ensure domain/path is in `in_scope_*` list |
| Rate limiting errors | Reduce `requests_per_second` in config |
| Agent-S not launching Burp | Ensure Burp Suite is installed and in PATH |

### Debug Mode

```python
from orchestrator import BugBountyOrchestrator
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

orchestrator = BugBountyOrchestrator()
orchestrator.load_scope_config('config/target.json')
# Detailed logs now printed
```

---

## 🤝 Contributing

Found a bug? Have an improvement? We welcome contributions!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m "Add your feature"`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

**Note:** Never commit API keys or sensitive credentials.

---

## 📄 License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.

**Includes:**
- **Agent-S**: [simular-ai/Agent-S](https://github.com/simular-ai/Agent-S) - MIT License
- **MAPTA**: [arthurgervais/mapta](https://github.com/arthurgervais/mapta) - MIT License

---

## 🙏 Credits & Attribution

**BugBountyAI-Framework** by **AK_ZSH** (Aksh)

- 🌐 Website: [aksh.qzz.io](https://aksh.qzz.io)
- 🐦 Twitter/X: [@ak_zsh](https://twitter.com/ak_zsh)
- 💼 LinkedIn: [Aksh](https://linkedin.com/in/aksh-security)

**Based on:**
- **Agent-S**: Open-source GUI automation framework
- **MAPTA**: Multi-agent pentesting framework
- **Perplexity Pro API**: Advanced LLM reasoning

**Special Thanks:**
- Simular AI (Agent-S development)
- Arthur Gervais et al. (MAPTA)
- Perplexity AI (API access)

---

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Integration Guide](docs/INTEGRATION_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Configuration Template](config/microsoft_vdp_scope.json)

---

## 🎯 Roadmap

- [ ] Native Burp Suite Pro integration
- [ ] Advanced MAPTA agent customization
- [ ] Google Gemini Pro 2.5 multi-modal support
- [ ] Web dashboard for real-time monitoring
- [ ] Automated report generation
- [ ] Slack/Discord integration for notifications
- [ ] Cloud deployment templates

---

## ⚠️ Legal & Ethical Notice

**This framework is designed for authorized security testing only.**

- ✅ Only test targets where you have **explicit written authorization**
- ✅ Comply with all bug bounty program rules and scope definitions
- ✅ Keep API keys secure and never commit `.env` files
- ✅ Respect all rate limits and testing restrictions
- ✅ Review all findings before submission

**Unauthorized access to computer systems is illegal.**

---

## 📞 Support

- 📧 Report issues: [GitHub Issues](https://github.com/ak-zsh/BugBountyAI-Framework/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ak-zsh/BugBountyAI-Framework/discussions)
- 🐦 Twitter: [@ak_zsh](https://twitter.com/ak_zsh)

---

## 🌟 Show Your Support

If this framework helps your bug bounty journey, please:
- ⭐ Star the repository
- 🔗 Share with your security community
- 📰 Write about your experience
- 🤝 Contribute improvements

**Happy hunting! 🎯🚀**

---

**Last Updated:** November 3, 2025  
**Status:** ✅ Production Ready  
**License:** MIT  
**Author:** AK_ZSH (Aksh)