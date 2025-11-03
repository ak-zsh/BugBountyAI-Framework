# BugBountyAI Framework - Installation Guide

## Prerequisites

- **OS:** Windows 11, Kali Linux, or macOS
- **Python:** 3.11 or higher
- **RAM:** 6GB minimum (8GB+ recommended)
- **Storage:** 500MB free space
- **Internet:** Required for API calls
- **Account:** Perplexity Pro subscription

## Step-by-Step Installation

### Step 1: Install Python 3.11+

#### Windows
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click Install

Verify:
```powershell
python --version
# Output: Python 3.11.x or higher
```

#### Kali Linux
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3 --version
```

### Step 2: Clone Repository

```bash
# Navigate to your workspace
cd C:\Users\aksha\Documents\Docker\Tools

# Clone the repository
git clone https://github.com/ak-zsh/BugBountyAI-Framework.git

# Navigate into directory
cd BugBountyAI-Framework
```

### Step 3: Create Virtual Environment (Optional but Recommended)

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Kali/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Agent-S

```bash
# Navigate to Agent-S directory
cd Agent-S

# Install in development mode
pip install -e .

# Return to framework root
cd ..
```

**Expected Output:**
```
Successfully installed agent-s-X.X.X
```

### Step 5: Install MAPTA

```bash
# Navigate to MAPTA directory
cd mapta

# Install in development mode
pip install -e .

# Return to framework root
cd ..
```

**Expected Output:**
```
Successfully installed mapta-X.X.X
```

### Step 6: Install Framework Dependencies

```bash
pip install langchain langchain-openai openai python-dotenv requests
```

**Expected Output:**
```
Successfully installed langchain-1.0.3 langchain-core-1.0.2 ...
```

### Step 7: Verify Installation

```bash
python -c "from orchestrator import BugBountyOrchestrator; print('✅ Framework ready')"
```

**Expected Output:**
```
✅ Framework ready
```

### Step 8: Get Perplexity Pro API Key

1. Go to https://www.perplexity.ai
2. Log in to your account
3. Go to Settings → API
4. Generate API key
5. Copy the key (save it securely)

### Step 9: Configure API Key

```bash
# Copy template
cp .env.example Agent-S/.env

# Edit the .env file
notepad Agent-S/.env
```

Add your API key:
```
PERPLEXITY_API_KEY=your_actual_api_key_here
```

**⚠️ Security:** Never commit this file or share your API key!

### Step 10: Test Installation

```bash
# Run validation test
python test_scope_validation.py
```

**Expected Output:**
```
======================================================================
Scope Validation Test - Microsoft MSRC VDP
======================================================================

✅ Perplexity Pro API connected
[STEP 1] Loading scope configuration...
[STEP 2] Testing URL validation...
✅ ALLOWED: https://microsoft.com/login
...
✅ Scope validation complete - Framework is scope-aware!
```

## Troubleshooting Installation

### Error: `ModuleNotFoundError: openai`

**Solution:**
```bash
pip install openai
```

### Error: `Python not found`

**Solution:**
1. Reinstall Python
2. Check PATH environment variable
3. Use full path: `C:\Python311\python.exe --version`

### Error: `Permission denied` (Kali)

**Solution:**
```bash
sudo pip install -e Agent-S/
sudo pip install -e mapta/
sudo pip install langchain langchain-openai openai python-dotenv requests
```

### Error: `API Connection Error`

**Solution:**
1. Check internet connection
2. Verify API key in `Agent-S/.env`
3. Ensure Perplexity Pro is active
4. Test with: `python -c "from dotenv import load_dotenv; import os; load_dotenv('Agent-S/.env'); print(os.getenv('PERPLEXITY_API_KEY'))"`

### Error: Agent-S installation fails

**Solution:**
```bash
# Try manual installation
cd Agent-S
pip install --upgrade pip setuptools wheel
pip install -e .
cd ..
```

### Error: MAPTA tools not found

**Solution:**
```bash
# Ensure Kali VM has tools installed
sudo apt update
sudo apt install -y nmap subfinder ffuf sqlmap

# Or install individual tools
pip install subfinder nmap ffuf
```

## Post-Installation Setup

### 1. Create Your First Scope Config

```bash
# Copy template
cp config/microsoft_vdp_scope.json config/my_target.json

# Edit with your target
notepad config/my_target.json
```

### 2. Test with Your Config

```bash
python -c "
from orchestrator import BugBountyOrchestrator
o = BugBountyOrchestrator()
o.check_api_connection()
o.load_scope_config('config/my_target.json')
"
```

### 3. Run Full Integration Test

```bash
python test_scope_validation.py
```

### 4. Create Initial Scope Config

```bash
# Create config directory structure
mkdir -p config logs reports

# Create sample config
echo '{
  \"program\": {\"name\": \"Test Program\"},
  \"target\": \"example.com\",
  \"domain_scope\": {
    \"in_scope_domains\": [\"example.com\"],
    \"out_of_scope_domains\": []
  },
  \"vulnerability_scope\": {
    \"in_scope_vulns\": [\"XSS\"],
    \"out_of_scope_vulns\": []
  },
  \"testing_restrictions\": {
    \"blocked_paths\": [],
    \"blocked_methods\": [\"DoS\"]
  },
  \"rate_limits\": {
    \"requests_per_second\": 5
  }
}' > config/test.json
```

## Verification Checklist

Run through this to verify complete installation:

```bash
# Check Python version
python --version
# ✅ Should be 3.11+

# Check orchestrator import
python -c "from orchestrator import BugBountyOrchestrator; print('OK')"
# ✅ Should print OK

# Check Agent-S import
python -c "import agent_s; print('OK')" 2>/dev/null || echo "Agent-S optional"
# ✅ OK or optional message

# Check MAPTA import
python -c "import mapta; print('OK')" 2>/dev/null || echo "MAPTA optional"
# ✅ OK or optional message

# Check dependencies
python -c "import openai, langchain, dotenv; print('OK')"
# ✅ Should print OK

# Check API connection
python -c "
from orchestrator import BugBountyOrchestrator
o = BugBountyOrchestrator()
result = o.check_api_connection()
print('✅ API Ready' if result else '❌ API Failed')
"
# ✅ Should show API Ready

# Check config loading
python -c "
from orchestrator import BugBountyOrchestrator
from pathlib import Path
o = BugBountyOrchestrator()
if Path('config/microsoft_vdp_scope.json').exists():
    o.load_scope_config('config/microsoft_vdp_scope.json')
    print('✅ Config Loaded')
"
# ✅ Should show Config Loaded
```

## Environment Variables

### Required

```bash
# In Agent-S/.env
PERPLEXITY_API_KEY=your_key_here
```

### Optional

```bash
# For Gemini Pro 2.5 (future)
GOOGLE_API_KEY=your_key_here

# For local Ollama
OLLAMA_BASE_URL=http://localhost:11434
```

## File Structure After Installation

```
BugBountyAI-Framework/
├── Agent-S/                 ✅ Installed
├── mapta/                   ✅ Installed
├── config/
│   └── microsoft_vdp_scope.json  ✅ Ready
├── payloads/
│   └── oda-xss.csv         ✅ Ready
├── orchestrator.py         ✅ Ready
├── test_scope_validation.py ✅ Ready
├── Agent-S/.env            ⚠️ Configured (keep secret)
└── .gitignore              ✅ Configured
```

## Next Steps

1. ✅ Installation complete
2. 📋 Create your first scope config (see [Quick Reference](QUICK-Reference.md))
3. 🧪 Run `python test_scope_validation.py`
4. 🎯 Test on authorized target
5. 🐙 Push to GitHub (see [GitHub Setup](GITHUB-Setup.md))

## Getting Help

### Common Issues

| Issue | Link |
|-------|------|
| API errors | Check `.env` configuration |
| Import errors | Reinstall with `pip install -e .` |
| Scope issues | Review `config/` templates |
| Performance | Check logs in `logs/` directory |

### Support

- 📧 GitHub Issues: [Create issue](https://github.com/ak-zsh/BugBountyAI-Framework/issues)
- 🐦 Twitter: [@ak_zsh](https://twitter.com/ak_zsh)
- 🌐 Website: [aksh.qzz.io](https://aksh.qzz.io)

---

**Installation Complete! 🎉**

Ready to start bug bounty testing. See [Quick Reference](QUICK-Reference.md) for next steps.

**Created:** November 3, 2025  
**Author:** AK_ZSH (Aksh)
