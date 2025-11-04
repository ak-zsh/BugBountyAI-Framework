# 🤖 BugBountyAI Framework v5.0

> **Production-Ready Autonomous Bug Bounty Hunter with AI Decision-Making**
> 
> Complete end-to-end automation combining **Subfinder**, **HTTPX**, **Katana**, **Nuclei**, **Burp Suite Pro**, **Agent-S**, and **Perplexity Pro** into one intelligent autonomous security testing engine.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Production%20Ready%20v5.0-brightgreen)
![VDP/BBP](https://img.shields.io/badge/Verified%20On-Microsoft%20MSRC%20VDP-orange)
![License](https://img.shields.io/badge/License-Proprietary-red)

---

## 📖 Table of Contents

- [What's New](#whats-new-in-v50)
- [Real-World Proof](#real-world-proof)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [How It Works](#how-it-works)
- [Features](#features)
- [Usage Examples](#usage-examples)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Legal & Ethical](#legal--ethical)

---

## 🆕 What's New in v5.0

### **AI-Powered Autonomous Hunting**
✅ **Perplexity Pro LLM Integration** — AI decides what tools to run next  
✅ **5-Phase Complete Pipeline** — Recon → Agent-S → MAPTA → Testing → Report  
✅ **Smart False Positive Filtering** — Automatically removes WAF-blocked findings  
✅ **Real Vulnerability Exploitation** — Generates working Proof-of-Concepts  
✅ **71.4% Accuracy Verified** — Tested on Microsoft MSRC VDP (5 real vulns found)  
✅ **7,000+ Subdomain Handling** — Batch processing without command-line limits  

---

## 🚀 Quick Start

### Prerequisites

```bash
# Minimum Requirements
- Python 3.11+
- Go 1.21+ (for Go tools)
- Windows 11 / Kali Linux / macOS
- Perplexity Pro subscription (free tier or paid)
- Burp Suite Pro (optional but recommended)
- Firefox browser
```

### 60-Second Setup

```bash
# 1. Clone repository
git clone https://github.com/ak-zsh/BugBountyAI-Framework.git
cd BugBountyAI-Framework

# 2. Install dependencies
pip install langchain langchain-openai openai python-dotenv requests

# 3. Install Go tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# 4. Configure API key
cp Agent-S/.env.example Agent-S/.env
# Edit Agent-S/.env with your Perplexity Pro API key

# 5. Configure target
cp config/microsoft_vdp_scope.json config/my_target.json
# Edit config/my_target.json with your authorized target

# 6. Run
python ai_autonomous_hunter.py
```

---

## 📦 Installation

### Step 1: System Requirements

| Component | Requirement | Check |
|-----------|-------------|-------|
| **Python** | 3.11 or higher | `python --version` |
| **Go** | 1.21 or higher | `go version` |
| **Git** | Any recent version | `git --version` |
| **RAM** | 8GB minimum | `wmic OS get totalVisibleMemorySize` |
| **Storage** | 2GB free | Verify partition size |

### Step 2: Clone Repository

```bash
git clone https://github.com/ak-zsh/BugBountyAI-Framework.git
cd BugBountyAI-Framework
```

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install langchain langchain-openai openai python-dotenv requests beautifulsoup4
```

**Verify:**
```bash
python -c "import langchain, openai; print('✅ Python dependencies OK')"
```

### Step 4: Install Go-Based Tools

**macOS/Linux:**
```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

**Windows (PowerShell):**
```powershell
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

**Verify:**
```bash
subfinder -version
httpx -version
katana -version
nuclei -version
```

### Step 5: Configure Perplexity Pro API

```bash
# Copy template
cp Agent-S/.env.example Agent-S/.env

# Edit with your API key
# Windows: notepad Agent-S/.env
# macOS/Linux: nano Agent-S/.env
```

**Add:**
```
PERPLEXITY_API_KEY=your_actual_api_key_here
```

Get your API key at: https://www.perplexity.ai/account/api

### Step 6: Configure Burp Suite (Optional)

**Install:**
- Download from: https://portswigger.net/burp/pro

**Windows Path:**
```
C:\Program Files\BurpSuitePro\burpsuite.exe
```

**macOS Path:**
```
/Applications/Burp Suite Professional.app/Contents/MacOS/burpsuite
```

**Configure Firefox Proxy:**
1. Open Firefox
2. Settings → Network Settings
3. Manual Proxy Configuration
4. HTTP Proxy: `127.0.0.1`, Port: `8080`
5. ✅ "Use this proxy for HTTPS"

### Step 7: Test Installation

```bash
python test_scope_validation.py
```

Expected output:
```
✅ Perplexity Pro API connected
✅ Scope configuration loaded
✅ All dependencies verified
```

---

## 🤖 How It Works

### The 5-Phase Autonomous Pipeline

#### **Phase 1: Reconnaissance** 🔍 (5-10 min)

Discovers all attack surface:
- **Subfinder**: Finds 7,000+ subdomains
- **DNSX**: Batch resolves to IPs
- **HTTPX**: Identifies 600+ live websites
- **Katana**: Deep crawls each site

Output: `results/all_urls.txt` (1,000+ unique endpoints)

#### **Phase 2: Agent-S + Burp Integration** 🛡️ (2-5 min)

Combines browser automation with proxy capture:
- Launches **Burp Suite Pro** (if available)
- Opens **Firefox** with Burp proxy configured
- Automatically navigates to discovered URLs
- Captures HTTP traffic for analysis

Output: Burp project file with intercepted traffic

#### **Phase 3: MAPTA Active Scanning** 🎯 (10-30 min)

Intelligent vulnerability detection:
- **Katana**: Crawls each URL for hidden paths
- **Nuclei**: Tests against 5,000+ vulnerability templates
- Smart scope validation: Only reports in-scope vulns
- Filters duplicates and false positives

Output: `reports/nuclei_findings.json`

#### **Phase 4: AI-Powered Exploitation** 💥 (10-20 min)

**Perplexity Pro LLM decides**:
- Which tools to run next
- What payloads to test
- When to escalate findings
- How to chain vulnerabilities

Tests automatically:
- **XSS**: 10 different payloads per endpoint
- **SQLi**: Error-based, union-based, time-based
- **SSRF**: Internal metadata, file:// URIs
- **Open Redirect**: Whitelist bypass attempts
- **Auth Bypass**: Default credentials, logic flaws

Output: `reports/ai_exploits.json` with PoCs

#### **Phase 5: Reporting & Filtering** 📊 (2 min)

**Smart false positive removal**:
- Detects WAF blocking patterns
- Removes duplicate findings
- Verifies exploitability
- Generates MSRC-ready reports

Output: `reports/FILTERED_Verified_Findings.json`

---

## ✨ Features

### 🔐 Scope-Aware Testing

```json
{
  "domain_scope": {
    "in_scope_domains": ["example.com", "*.example.com"],
    "out_of_scope_domains": ["*.internal.example.com"]
  },
  "vulnerability_scope": {
    "in_scope_vulns": ["XSS", "SQLi", "SSRF"],
    "out_of_scope_vulns": ["DoS", "Social Engineering"]
  },
  "blocked_paths": ["/admin", "/internal"],
  "rate_limits": {
    "requests_per_second": 5,
    "requests_per_minute": 300
  }
}
```

### 🧠 AI Decision Making

**Perplexity Pro analyzes**:
- Found vulnerabilities
- Attack surface patterns
- Tool effectiveness
- Next best actions

**Automatically decides**:
- Run Nuclei or move to exploitation?
- Escalate finding or continue scanning?
- Chain vulnerabilities?
- When to stop and report

### 📊 Real-Time Reporting

```bash
# View findings as they're discovered
cat reports/findings_live.json | python -m json.tool | grep "severity"

# Monitor automation progress
tail -f logs/session_*.json
```

### ✅ Verified Vulnerability Types

- ✅ Reflected XSS (CWE-79)
- ✅ Stored XSS (CWE-79)
- ✅ SQL Injection (CWE-89)
- ✅ Server-Side Request Forgery (CWE-918)
- ✅ Open Redirect (CWE-601)
- ✅ Path Traversal (CWE-22)
- ✅ Authentication Bypass (CWE-287)
- ✅ Information Disclosure (CWE-200)

---

## 🎯 Usage Examples

### Example 1: Run on Default Config (Microsoft VDP)

```bash
python ai_autonomous_hunter.py
```

Uses `config/microsoft_vdp_scope.json` by default.

Expected runtime: **30-60 minutes**

### Example 2: Custom Target

```bash
# Create config
cat > config/my_vdp.json << 'EOF'
{
  "program": {
    "name": "My Custom VDP",
    "platform": "HackerOne",
    "type": "VDP",
    "authorization": "Public Program"
  },
  "target": "mycompany.com",
  "domain_scope": {
    "in_scope_domains": ["mycompany.com", "*.mycompany.com"],
    "out_of_scope_domains": []
  },
  "vulnerability_scope": {
    "in_scope_vulns": ["XSS", "SQLi", "SSRF", "Open Redirect"],
    "out_of_scope_vulns": ["DoS", "DDoS"]
  },
  "testing_restrictions": {
    "blocked_paths": ["/admin", "/internal", "/api/internal"],
    "blocked_methods": []
  },
  "rate_limits": {
    "requests_per_second": 10,
    "requests_per_minute": 600
  }
}
EOF

# Run
python ai_autonomous_hunter.py --config config/my_vdp.json
```

### Example 3: Verify Findings Manually

```bash
python verify_real_vulns.py
```

This will:
- Test each discovered finding
- Verify it's not a false positive
- Generate proof-of-concept
- Create verification report

### Example 4: Filter False Positives

```bash
python filter_false_positives.py
```

Automatically removes:
- WAF-blocked attempts
- Rate-limited responses
- Redirects to error pages

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│   BugBountyAI Framework v5.0 - Architecture        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐         ┌──────────────┐        │
│  │ Orchestrator │◄───────►│ Perplexity   │        │
│  │              │         │ Pro LLM      │        │
│  └──────┬───────┘         └──────────────┘        │
│         │                                          │
│    ┌────▼──────────┬──────────┬────────────┐      │
│    │               │          │            │      │
│  ┌─▼──┐      ┌────▼───┐  ┌──▼───┐   ┌────▼──┐   │
│  │    │      │ MAPTA  │  │Agent-│   │ Burp  │   │
│  │    │      │ Tools  │  │ S    │   │ Suite │   │
│  │    │      └────────┘  └──────┘   └───────┘   │
│  │    │                                           │
│  │    ├─ Subfinder (subdomains)                   │
│  │    ├─ HTTPX (live detection)                   │
│  │    ├─ Katana (path crawling)                   │
│  │    ├─ Nuclei (vuln scanning)                   │
│  │    │                                           │
│  └────┴─────────────────────────────────┬────────┘
│                                          │
│   ┌────────────────────────────────────▼─┐       │
│   │ Vulnerability Testing Engine          │       │
│   │ • XSS (10+ payloads)                 │       │
│   │ • SQLi (3 techniques)                │       │
│   │ • SSRF (metadata extraction)         │       │
│   │ • Open Redirect (bypass attempts)    │       │
│   │ • Auth Bypass (default creds)        │       │
│   └────────────────────────────────────┬─┘       │
│                                        │         │
│   ┌────────────────────────────────────▼─┐       │
│   │ Report Generation & Filtering         │       │
│   │ • Severity grouping                  │       │
│   │ • WAF detection                      │       │
│   │ • False positive removal             │       │
│   │ • MSRC-ready export                  │       │
│   └──────────────────────────────────────┘       │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Subfinder not found"** | Run: `go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest` |
| **"API key invalid"** | Check `PERPLEXITY_API_KEY` in `Agent-S/.env`, ensure no extra spaces |
| **"Too many subdomains"** | Framework handles 7,000+ automatically with batching |
| **"Burp doesn't launch"** | Update `burp_path` in `ai_autonomous_hunter.py` to your installation |
| **"Firefox not opening"** | Update `firefox_path` or ensure Firefox is in PATH |
| **"Rate limit exceeded"** | Wait 60 seconds, framework respects rate limits automatically |
| **"Timeout errors"** | Normal for large targets (1,000+ endpoints). Framework continues. |

### Debug Mode

```bash
# Enable verbose logging
python -u ai_autonomous_hunter.py 2>&1 | tee debug.log
```

---

## 📋 Files Overview

| File | Purpose |
|------|---------|
| `ai_autonomous_hunter.py` | **Main automation engine** (5-phase pipeline) |
| `orchestrator.py` | Scope validation & LLM planning |
| `verify_real_vulns.py` | Manual verification of findings |
| `filter_false_positives.py` | WAF detection & false positive removal |
| `config/` | Target scope configurations (JSON) |
| `reports/` | Generated findings (JSON format) |
| `logs/` | Session logs & compliance records |

---

## ⚠️ Legal & Ethical

**This framework is for authorized security testing only.**

### ✅ Do:
- ✅ Only test targets you own or have **explicit written authorization**
- ✅ Comply with all bug bounty program rules and scope definitions
- ✅ Verify scope carefully before running
- ✅ Keep API keys secure (never commit `.env`)
- ✅ Respect all rate limits and testing restrictions
- ✅ Review findings before submission

### ❌ Don't:
- ❌ Test production systems without permission
- ❌ Perform DoS/DDoS attacks
- ❌ Exfiltrate sensitive data
- ❌ Modify application data
- ❌ Assume VDP targets are always in scope
- ❌ Publish zero-days before disclosure period

**Unauthorized access to computer systems is illegal.**

---

## 📊 Sample Output

### Filtered Report Example

```json
{
  "metadata": {
    "program": "Microsoft MSRC VDP",
    "target": "microsoft.com",
    "total_urls_tested": 8608,
    "total_findings": 5,
    "verified_rate": 71.4
  },
  "findings": [
    {
      "url": "https://chinaevent.microsoft.com/register",
      "type": "XSS",
      "severity": "high",
      "parameter": "q",
      "payload": "<img src=x onerror=alert(1)>",
      "verified": true,
      "poc_url": "https://chinaevent.microsoft.com/register?q=<img src=x onerror=alert(1)>"
    },
    {
      "url": "https://careers.microsoft.com/",
      "type": "Open Redirect",
      "severity": "medium",
      "parameter": "redirect",
      "target_url": "https://attacker.com",
      "verified": true,
      "http_status": 302
    }
  ]
}
```

---

## 🚀 Next Steps

1. **Install & Test** → Follow installation guide
2. **Configure Target** → Create scope config
3. **Run Automation** → `python ai_autonomous_hunter.py`
4. **Verify Findings** → Run `verify_real_vulns.py`
5. **Submit to VDP** → Go to https://msrc.microsoft.com/create-report

---

## 🤝 Support & Community

- **GitHub Issues**: https://github.com/ak-zsh/BugBountyAI-Framework/issues
- **GitHub Discussions**: https://github.com/ak-zsh/BugBountyAI-Framework/discussions
- **Twitter**: [@ak_zsh](https://twitter.com/ak_zsh)
- **Website**: https://aksh.qzz.io

---

## 📄 License

**Proprietary Software**

This software is proprietary and confidential. Unauthorized copying, distribution, or modification is strictly prohibited.

Full license: See `LICENSE` file

---

## 🙏 Credits

**BugBountyAI Framework v5.0** by **AK_ZSH** (Aksh)

**Based on:**
- [Subfinder](https://github.com/projectdiscovery/subfinder) - ProjectDiscovery
- [HTTPX](https://github.com/projectdiscovery/httpx) - ProjectDiscovery
- [Katana](https://github.com/projectdiscovery/katana) - ProjectDiscovery
- [Nuclei](https://github.com/projectdiscovery/nuclei) - ProjectDiscovery
- [Agent-S](https://github.com/simular-ai/Agent-S) - Simular AI
- [Perplexity Pro API](https://www.perplexity.ai) - Perplexity AI

---

**Status**: ✅ Production Ready  
**Last Updated**: November 4, 2025  
**Version**: 5.0.0  
**Verified On**: Microsoft MSRC VDP (5 real vulns found, 71.4% accuracy)
