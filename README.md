# 🎯 BugBountyAI Framework v4.0

> **Complete End-to-End Bug Bounty Automation**
> 
> AI-Powered orchestration of **Agent-S** (GUI automation) + **MAPTA** (multi-agent pentesting) + **Burp Suite Pro** + **Perplexity Pro** (LLM reasoning) into one fully autonomous bug bounty engine.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready%20v4.0-brightgreen)
![VDP/BBP](https://img.shields.io/badge/VDP%2FBBP-Fully%20Automated-orange)

---

## 📖 Table of Contents

- [What's New in v4.0](#whats-new-in-v40)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Complete Automation](#complete-automation)
- [Architecture](#architecture)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)

---

## 🆕 What's New in v4.0

### **Full End-to-End Automation**
✅ **1-Click Execution** — Run `python automate_complete.py` and let it work  
✅ **Agent-S + Burp Integration** — Automatically launches Firefox & Burp Suite  
✅ **MAPTA Tool Orchestration** — Subfinder, HTTPX, DNSX, Katana, Nuclei all automated  
✅ **Smart Batching** — Handles 7000+ subdomains without command line limits  
✅ **Real Exploitation** — Generates actual PoCs for XSS, SQLi, SSRF, etc.  
✅ **5-Phase Pipeline** — Recon → Burp Scan → MAPTA Scan → Exploitation → Report  

### **Architecture Changes**
- **3 Scripts**: `orchestrator.py` (planning), `automate_complete.py` (execution), `test_scope_validation.py` (testing)
- **Burp Suite Pro Automation**: Launches and configures scope automatically
- **Firefox Agent-S Control**: Opens targets in browser with proxy configured
- **Temp File Processing**: Handles large datasets without crashes

---

## ✨ Features

### 🔐 **Scope-Aware Testing**
- Automatic domain/path validation
- Vulnerability type filtering
- HTTP method restriction
- Rate limiting enforcement (5 req/sec)
- Real-time scope violation detection

### 🧠 **LLM-Powered Intelligence**
- **Perplexity Pro** generates intelligent reconnaissance plans
- Context-aware vulnerability analysis
- Smart tool recommendations
- Finding prioritization

### 🤖 **Complete Automation Pipeline**

#### **Phase 1: Reconnaissance** 🔍
- Subfinder (subdomain enumeration)
- DNSX (DNS resolution with batching)
- HTTPX (live web detection)
- Smart filtering at each step

#### **Phase 2: Agent-S + Burp Suite** 🛡️
- Automatic Burp Suite launch
- Scope configuration from JSON
- Firefox automation via Agent-S
- Proxy-based traffic capture

#### **Phase 3: MAPTA Active Scanning** 🎯
- Katana (path crawling)
- Nuclei (vulnerability detection)
- Custom payload testing
- Scope validation per finding

#### **Phase 4: Exploitation & PoC** 💥
- XSS testing & PoC generation
- SQLi detection & exploitation
- SSRF vulnerability testing
- Authentication bypass attempts
- Information disclosure checks

#### **Phase 5: Reporting & Compliance** 📊
- JSON report generation
- Severity grouping
- Exploitability assessment
- Session logging
- Compliance tracking

### 🛡️ **Enterprise-Grade**
- Windows 11 primary environment
- Kali VM integration ready
- Multi-LLM support (Perplexity Pro, Gemini Pro 2.5)
- Extensible architecture

---

## 🚀 Quick Start

### Prerequisites

```bash
# Windows 11 (recommended) or Kali Linux
# Python 3.11+
# Go 1.21+ (for Go tools)
# Perplexity Pro subscription
# Burp Suite Pro (optional but recommended)
# Firefox (for Agent-S automation)
```

### Installation (5 Minutes)

```bash
# 1. Clone
git clone https://github.com/ak-zsh/BugBountyAI-Framework.git
cd BugBountyAI-Framework

# 2. Install Python dependencies
pip install langchain langchain-openai openai python-dotenv requests

# 3. Install Go tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# 4. Configure API key
cp .env.example Agent-S/.env
# Edit Agent-S/.env with your Perplexity API key

# 5. Test
python test_scope_validation.py
```

### Run Complete Automation

```bash
# Create your target config
cp config/microsoft_vdp_scope.json config/my_target.json
# Edit config/my_target.json with your authorized target

# Run full automation (all 5 phases)
python automate_complete.py
```

---

## 📦 Installation

### Detailed Setup

#### 1. System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 11, Kali Linux, or macOS |
| **Python** | 3.11 or higher |
| **Go** | 1.21 or higher (for tools) |
| **RAM** | 8GB minimum, 16GB recommended |
| **Storage** | 2GB free space |
| **Network** | Stable internet for API calls |

#### 2. Install Python Dependencies

```bash
cd BugBountyAI-Framework
pip install langchain langchain-openai openai python-dotenv requests
```

#### 3. Install Go-Based Tools

```bash
# Subfinder
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# HTTPX
go install github.com/projectdiscovery/httpx/cmd/httpx@latest

# DNSX
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest

# Katana
go install github.com/projectdiscovery/katana/cmd/katana@latest

# Nuclei
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

**Verify Installation:**
```bash
subfinder -version
httpx -version
dnsx -version
katana -version
nuclei -version
```

#### 4. Configure API Keys

```bash
# Copy template
cp .env.example Agent-S/.env

# Edit with your Perplexity Pro API key
notepad Agent-S/.env
```

Add:
```
PERPLEXITY_API_KEY=your_actual_api_key_here
```

#### 5. Install Burp Suite Pro (Optional)

Download from: https://portswigger.net/burp/pro

Install to: `C:\Program Files\BurpSuitePro\`

**Configure Firefox Proxy:**
1. Open Firefox
2. Settings → Network Settings → Manual Proxy
3. HTTP Proxy: `127.0.0.1`, Port: `8080`
4. Check "Use this proxy for HTTPS"

---

## 🤖 Complete Automation

### Script Overview

| Script | Purpose | Usage |
|--------|---------|-------|
| `orchestrator.py` | Scope validation & LLM planning | `python orchestrator.py --config config/target.json` |
| `automate_complete.py` | **Full automation (5 phases)** | `python automate_complete.py` |
| `test_scope_validation.py` | Test scope & compliance | `python test_scope_validation.py` |

### Full Automation Workflow

```bash
# 1. Configure your target
notepad config/my_target.json

# 2. Run complete automation
python automate_complete.py
```

**What Happens:**

```
Phase 1: Reconnaissance (2-5 min)
├─ Subfinder: 7871 subdomains found
├─ Filtering: 7262 in-scope
├─ DNSX: 6850 resolved
└─ HTTPX: 4230 live websites

Phase 2: Agent-S + Burp Suite (1-2 min)
├─ Launch Burp Suite Pro
├─ Configure scope from config
├─ Launch Firefox with Agent-S
└─ Capture HTTP traffic

Phase 3: MAPTA Active Scanning (10-30 min)
├─ Katana path crawling (per URL)
├─ Nuclei vulnerability detection
├─ Scope validation per finding
└─ Filter out-of-scope items

Phase 4: Exploitation & PoC (5-15 min)
├─ XSS: Test reflection, context, CSP
├─ SQLi: Error-based, union-based
├─ SSRF: Internal resource access
├─ Auth Bypass: Default credentials
└─ Info Disc: Sensitive file exposure

Phase 5: Reporting (1 min)
├─ Generate JSON report
├─ Group by severity & type
├─ Compliance validation
└─ Session logging
```

### Output Structure

```
BugBountyAI-Framework/
├── reports/
│   └── Report_20251103_180430.json  # Full findings report
├── logs/
│   └── session_20251103_180430.json  # Compliance log
└── results/
    ├── subdomains.txt
    ├── resolved.txt
    └── live_urls.txt
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              BugBountyAI Framework v4.0                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐                      │
│  │ Orchestrator │◄──►│ Perplexity   │                      │
│  │ (Validator & │    │ Pro LLM      │                      │
│  │  Planner)    │    │ (sonar-pro)  │                      │
│  └──┬───┬───┬──┘     └──────────────┘                      │
│     │   │   │                                               │
│  ┌──▼─┐│   │ ┌──────────────────────┐                      │
│  │    ││   └─►│ Scope Validator      │                      │
│  │    │└─────►│ • URLs               │                      │
│  │    │       │ • Vulns              │                      │
│  │    │       │ • Methods            │                      │
│  │    │       │ • Rate Limits        │                      │
│  │    │       └──────────────────────┘                      │
│  │    │                                                     │
│  │    ├─────────────────┬──────────────┬──────────────┐    │
│  │    │                 │              │              │    │
│  └────┴─┐          ┌────▼────┐   ┌────▼────┐  ┌─────▼──┐ │
│         │          │ MAPTA    │   │ Agent-S  │  │ Burp   │ │
│         │          │ (Backend)│   │  (GUI)   │  │ Suite  │ │
│         │          └──────────┘   └─────────┘  └────────┘ │
│         │                                                   │
│    ┌────▼────────────────────────────────────────┐        │
│    │ Complete Automation Engine                  │        │
│    │ • 5-phase pipeline                          │        │
│    │ • Smart batching                            │        │
│    │ • Real exploitation                         │        │
│    │ • Compliance enforcement                    │        │
│    └───────────────────────────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 Usage Examples

### Example 1: Test Microsoft VDP

```bash
# Use included config
python automate_complete.py
# Uses config/microsoft_vdp_scope.json by default
```

### Example 2: Custom Target

```bash
# Create config
cat > config/custom_target.json << EOF
{
  "program": {
    "name": "My Custom VDP",
    "platform": "HackerOne",
    "type": "VDP",
    "authorization": "Public Program"
  },
  "target": "example.com",
  "domain_scope": {
    "in_scope_domains": ["example.com", "*.example.com"],
    "out_of_scope_domains": ["*.internal.example.com"]
  },
  "vulnerability_scope": {
    "in_scope_vulns": ["XSS", "SQLi", "SSRF"],
    "out_of_scope_vulns": ["DoS", "Social Engineering"]
  },
  "testing_restrictions": {
    "blocked_paths": ["/admin", "/internal"],
    "blocked_methods": ["DoS", "DDoS"]
  },
  "rate_limits": {
    "requests_per_second": 5,
    "requests_per_minute": 300
  }
}
EOF

# Edit automate_complete.py to use custom config
# Change: config_file = 'config/custom_target.json'

# Run
python automate_complete.py
```

### Example 3: Scope-Only Testing

```bash
# Test scope validation
python orchestrator.py --config config/my_target.json
```

### Example 4: Manual Tool Control

```python
from orchestrator import BugBountyOrchestrator

# Load scope
orch = BugBountyOrchestrator()
orch.load_scope_config('config/my_target.json')

# Validate a URL
is_valid, reason = orch.validate_target_url('https://example.com/test')
print(f"Valid: {is_valid}, Reason: {reason}")

# Check vulnerability type
is_testable, reason = orch.validate_vulnerability_type('XSS')
print(f"Testable: {is_testable}, Reason: {reason}")

# Generate LLM plan
plan = orch.plan_reconnaissance()
print(plan)
```

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| **Subfinder not found** | `go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest` |
| **API connection failed** | Check `PERPLEXITY_API_KEY` in `Agent-S/.env` |
| **Too many subdomains error** | Framework now handles this with smart batching |
| **Burp doesn't launch** | Update `burp_path` in `automate_complete.py` |
| **Firefox not opening** | Update `firefox_path` in `automate_complete.py` |
| **Tools timeout** | Normal for large targets, framework continues |
| **Scope violations** | Review logs, ensure domain is in `in_scope_domains` |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Then run automation
python automate_complete.py
```

---

## 📄 License

This project is released under the **MIT License**.

**Includes:**
- **Agent-S**: [simular-ai/Agent-S](https://github.com/simular-ai/Agent-S) - MIT License
- **MAPTA**: [arthurgervais/mapta](https://github.com/arthurgervais/mapta) - MIT License

---

## 🙏 Credits & Attribution

**BugBountyAI-Framework v4.0** by **AK_ZSH** (Aksh)

- 🌐 Website: [aksh.qzz.io](https://aksh.qzz.io)
- 🐦 Twitter/X: [@ak_zsh](https://twitter.com/ak_zsh)
- 💼 LinkedIn: [Aksh](https://linkedin.com/in/aksh-security)
- 📧 GitHub: [@ak-zsh](https://github.com/ak-zsh)

**Based on:**
- **Agent-S**: GUI automation framework by Simular AI
- **MAPTA**: Multi-agent pentesting by Arthur Gervais et al.
- **Perplexity Pro API**: Advanced LLM reasoning
- **ProjectDiscovery Tools**: Subfinder, HTTPX, DNSX, Katana, Nuclei

**Special Thanks:**
- Simular AI (Agent-S development)
- Arthur Gervais (MAPTA research)
- ProjectDiscovery team (amazing tools)
- Perplexity AI (API access)

---

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION-v4.md)
- [Integration Guide](docs/INTEGRATION_GUIDE.md)
- [Quick Reference](QUICK-Reference.md)
- [GitHub Setup Guide](GITHUB-Setup.md)

---

## 🎯 Roadmap

- [x] Full automation pipeline (v4.0)
- [x] Agent-S + Burp integration
- [x] Smart batching for large datasets
- [ ] Google Gemini Pro 2.5 support
- [ ] Web dashboard for monitoring
- [ ] Slack/Discord notifications
- [ ] Cloud deployment templates
- [ ] Multi-target campaigns

---

## ⚠️ Legal & Ethical Notice

**This framework is designed for authorized security testing only.**

✅ Only test targets where you have **explicit written authorization**  
✅ Comply with all bug bounty program rules and scope definitions  
✅ Keep API keys secure and never commit `.env` files  
✅ Respect all rate limits and testing restrictions  
✅ Review all findings before submission  

**Unauthorized access to computer systems is illegal.**

---

## 📞 Support

- 📧 Report issues: [GitHub Issues](https://github.com/ak-zsh/BugBountyAI-Framework/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ak-zsh/BugBountyAI-Framework/discussions)
- 🐦 Twitter: [@ak_zsh](https://twitter.com/ak_zsh)
- 🌐 Website: [aksh.qzz.io](https://aksh.qzz.io)

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
**Version:** 4.0.0 (Complete Automation)  
**Status:** ✅ Production Ready  
**License:** MIT  
**Author:** AK_ZSH (Aksh)