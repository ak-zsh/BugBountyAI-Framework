# BugBountyAI Framework v4.0 - Complete Installation Guide

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Step-by-Step Installation](#step-by-step-installation)
3. [Tool Installation](#tool-installation)
4. [API Configuration](#api-configuration)
5. [Burp Suite Setup](#burp-suite-setup)
6. [Firefox Configuration](#firefox-configuration)
7. [Verification](#verification)
8. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Windows 11, Kali Linux, or macOS 12+ |
| **Python** | 3.11 or higher |
| **Go** | 1.21 or higher |
| **RAM** | 8GB minimum |
| **Storage** | 2GB free space |
| **Internet** | Stable connection for API calls |
| **Account** | Perplexity Pro subscription |

### Recommended Setup

- **OS**: Windows 11 Pro
- **CPU**: Intel Core i5 (12th Gen) or equivalent
- **RAM**: 16GB DDR4
- **Storage**: 512GB SSD
- **Display**: 1920x1080 or higher

---

## 🚀 Step-by-Step Installation

### Step 1: Install Python 3.11+

#### Windows:
```powershell
# Download from https://www.python.org/downloads/
# Run installer
# ✅ Check "Add Python to PATH"
# Click Install

# Verify installation
python --version
# Expected: Python 3.11.x or higher
```

#### Kali Linux:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3 --version
```

### Step 2: Install Go 1.21+

#### Windows:
```powershell
# Download from https://go.dev/dl/
# Run installer (default location: C:\Go)
# Verify installation
go version
# Expected: go version go1.21.x or higher
```

#### Kali Linux:
```bash
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version
```

### Step 3: Clone Repository

```bash
# Navigate to your workspace
cd C:\Users\aksha\Documents\Docker\Tools  # Windows
# or
cd ~/tools  # Linux

# Clone repository
git clone https://github.com/ak-zsh/BugBountyAI-Framework.git
cd BugBountyAI-Framework
```

### Step 4: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Python Dependencies

```bash
# Install core dependencies
pip install langchain langchain-openai openai python-dotenv requests

# Verify installations
pip list | grep -E "langchain|openai|dotenv|requests"
```

**Expected Output:**
```
langchain           1.0.3
langchain-core      1.0.2
langchain-openai    1.0.1
openai              1.40.0
python-dotenv       1.0.0
requests            2.31.0
```

---

## 🛠️ Tool Installation

### Install ProjectDiscovery Tools

These are the core scanning tools used by MAPTA:

```bash
# 1. Subfinder (Subdomain enumeration)
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# 2. HTTPX (HTTP toolkit)
go install github.com/projectdiscovery/httpx/cmd/httpx@latest

# 3. DNSX (DNS toolkit)
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest

# 4. Katana (Web crawling)
go install github.com/projectdiscovery/katana/cmd/katana@latest

# 5. Nuclei (Vulnerability scanner)
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

**Windows Note:** Tools will be installed to `C:\Users\<YourUsername>\go\bin`

**Linux Note:** Tools will be installed to `~/go/bin`

### Verify Tool Installation

```bash
# Windows
cd C:\Users\aksha\go\bin
dir

# Linux
ls -la ~/go/bin

# Test each tool
subfinder -version
httpx -version
dnsx -version
katana -version
nuclei -version
```

**Expected Output:**
```
subfinder v2.6.3
httpx v1.6.3
dnsx v1.2.1
katana v1.1.0
nuclei v3.2.9
```

### Update PATH (if tools not found)

#### Windows:
```powershell
# Add Go bin to PATH permanently
$goPath = "$env:USERPROFILE\go\bin"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$goPath", "User")

# Reload environment
refreshenv
# or restart PowerShell
```

#### Linux:
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export PATH=$PATH:~/go/bin' >> ~/.bashrc
source ~/.bashrc
```

---

## 🔑 API Configuration

### Step 1: Get Perplexity Pro API Key

1. Go to https://www.perplexity.ai
2. Log in to your Perplexity Pro account
3. Navigate to Settings → API
4. Click "Generate API Key"
5. **Copy the key** (save it securely)

### Step 2: Configure Environment File

```bash
# Navigate to framework
cd BugBountyAI-Framework

# Copy template
cp .env.example Agent-S/.env

# Edit the file
notepad Agent-S/.env  # Windows
nano Agent-S/.env     # Linux
```

**Add your API key:**
```
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ Security Warning:** Never commit `.env` files to Git!

### Step 3: Verify API Connection

```bash
python -c "
from orchestrator import BugBountyOrchestrator
o = BugBountyOrchestrator()
result = o.check_api_connection()
print('✅ API Connected' if result else '❌ API Failed')
"
```

**Expected Output:**
```
✅ Perplexity Pro API connected
✅ API Connected
```

---

## 🛡️ Burp Suite Setup

### Install Burp Suite Pro

1. **Download**: https://portswigger.net/burp/pro
2. **Install to**: `C:\Program Files\BurpSuitePro\` (Windows)
3. **Linux**: Install to `/opt/BurpSuitePro/`

### Verify Installation

```bash
# Windows
"C:\Program Files\BurpSuitePro\burpsuite_pro.exe" --version

# Linux
/opt/BurpSuitePro/burpsuite_pro --version
```

### Configure Framework Paths

Edit `automate_complete.py`:

```python
# Update these paths to match your installation
self.burp_path = r'C:\Program Files\BurpSuitePro\burpsuite_pro.exe'  # Windows
# or
self.burp_path = '/opt/BurpSuitePro/burpsuite_pro'  # Linux
```

---

## 🦊 Firefox Configuration

### Install Firefox

**Windows:**
```powershell
# Download from https://www.mozilla.org/firefox/
# Install to default location: C:\Program Files\Mozilla Firefox\
```

**Linux:**
```bash
sudo apt update
sudo apt install firefox
```

### Configure Proxy for Burp

1. Open Firefox
2. Go to Settings → Network Settings
3. Select "Manual proxy configuration"
4. **HTTP Proxy**: `127.0.0.1`
5. **Port**: `8080`
6. ✅ Check "Also use this proxy for HTTPS"
7. Click OK

### Update Framework Paths

Edit `automate_complete.py`:

```python
# Update Firefox path
self.firefox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # Windows
# or
self.firefox_path = '/usr/bin/firefox'  # Linux
```

### Install Burp Certificate in Firefox

1. Start Burp Suite
2. In Firefox, visit: `http://burp`
3. Click "CA Certificate" (top right)
4. Save `cacert.der`
5. Firefox → Settings → Privacy & Security → Certificates → View Certificates
6. Import → Select `cacert.der` → Trust for websites

---

## ✅ Verification

### Complete Installation Check

Run this verification script:

```bash
cd BugBountyAI-Framework
python -c "
import sys
print('Python:', sys.version)

try:
    from orchestrator import BugBountyOrchestrator
    print('✅ Orchestrator imported')
except Exception as e:
    print('❌ Orchestrator failed:', e)

try:
    import openai, langchain, dotenv
    print('✅ Dependencies OK')
except Exception as e:
    print('❌ Dependencies failed:', e)

try:
    o = BugBountyOrchestrator()
    result = o.check_api_connection()
    print('✅ API Connected' if result else '❌ API Failed')
except Exception as e:
    print('❌ API error:', e)
"
```

**Expected Output:**
```
Python: 3.11.x
✅ Orchestrator imported
✅ Dependencies OK
✅ Perplexity Pro API connected
✅ API Connected
```

### Test Tool Execution

```bash
# Test subfinder
subfinder -d example.com -silent | head -5

# Test httpx
echo "https://example.com" | httpx -silent

# Test nuclei
nuclei -u https://example.com -silent
```

### Run Validation Test

```bash
python test_scope_validation.py
```

**Expected Output:**
```
======================================================================
Scope Validation Test - Microsoft MSRC VDP
======================================================================
✅ Perplexity Pro API connected
✅ Scope configuration loaded successfully!
✅ URL validation working
✅ Vulnerability filtering working
✅ Session logged
✅ Scope validation complete - Framework is scope-aware!
======================================================================
```

---

## 🛠️ Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Python not found** | Reinstall Python, check "Add to PATH" |
| **Go tools not found** | Add `~/go/bin` to PATH |
| **API connection failed** | Verify `PERPLEXITY_API_KEY` in `Agent-S/.env` |
| **Subfinder timeout** | Normal for large domains, increase timeout |
| **Burp won't launch** | Verify path in `automate_complete.py` |
| **Firefox proxy error** | Check Burp is running on `127.0.0.1:8080` |
| **Import errors** | `pip install --upgrade langchain openai` |

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Then run your script
from orchestrator import BugBountyOrchestrator
o = BugBountyOrchestrator()
o.load_scope_config('config/microsoft_vdp_scope.json')
```

### Reset Installation

If something goes wrong, reset:

```bash
# Remove virtual environment
rm -rf venv

# Reinstall tools
go clean -modcache
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
# ... (repeat for all tools)

# Reinstall Python dependencies
pip uninstall -y langchain openai
pip install langchain langchain-openai openai python-dotenv requests
```

---

## 📦 Post-Installation

### Create Your First Config

```bash
# Copy template
cp config/microsoft_vdp_scope.json config/my_target.json

# Edit with your authorized target
notepad config/my_target.json
```

### Run Your First Automation

```bash
# Test with validation only
python orchestrator.py --config config/my_target.json

# Run complete automation (all 5 phases)
python automate_complete.py
```

---

## 🎯 Next Steps

1. ✅ **Installation complete!**
2. 📋 Create your target config (see [Usage Examples](README-v4-UPDATED.md#usage-examples))
3. 🧪 Run `python test_scope_validation.py`
4. 🚀 Run `python automate_complete.py`
5. 📊 Review findings in `reports/` directory

---

## 📞 Support

- 📧 Report issues: [GitHub Issues](https://github.com/ak-zsh/BugBountyAI-Framework/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ak-zsh/BugBountyAI-Framework/discussions)
- 🐦 Twitter: [@ak_zsh](https://twitter.com/ak_zsh)

---

**Installation Guide Last Updated:** November 3, 2025  
**Framework Version:** 4.0.0  
**Author:** AK_ZSH (Aksh)