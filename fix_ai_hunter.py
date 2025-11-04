#!/usr/bin/env python3
"""
Quick fix for AI Hunter issues - UTF-8 compatible
"""

import json

# Fix orchestrator.py with UTF-8 encoding
print("[1/3] Fixing orchestrator.py...")

try:
    with open('orchestrator.py', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Add LLM exposure
    if 'self.llm = ChatOpenAI' not in content:
        # Find the line with self.client = OpenAI
        if 'self.client = OpenAI(' in content:
            llm_code = '''
        
        # Expose LLM for AI Hunter
        from langchain_openai import ChatOpenAI
        self.llm = ChatOpenAI(
            model="sonar-pro",
            openai_api_key=self.api_key,
            openai_api_base="https://api.perplexity.ai",
            temperature=0.2
        )
'''
            # Insert after the OpenAI client initialization
            content = content.replace(
                'base_url="https://api.perplexity.ai"\n        )',
                f'base_url="https://api.perplexity.ai"\n        ){llm_code}'
            )
            
            with open('orchestrator.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✅ Added LLM exposure to orchestrator")
        else:
            print("   ⚠️  Could not find OpenAI client initialization")
    else:
        print("   ℹ️  LLM already exposed")

except Exception as e:
    print(f"   ❌ Error: {e}")
    print("   ℹ️  Will use manual fix instead")

# Check findings validity
print("\n[2/3] Validating findings...")

try:
    with open('reports/AI_Hunt_Report_20251104_011529.json', 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    print(f"   Total: {len(report['findings'])} findings")
    confirmed = sum(1 for f in report['findings'] if f.get('confirmed'))
    print(f"   Confirmed: {confirmed}")
    print(f"   Needs verification: {len(report['findings']) - confirmed}")
    
    # Show breakdown
    types = {}
    severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    
    for f in report['findings']:
        t = f['type']
        types[t] = types.get(t, 0) + 1
        sev = f.get('severity', 'low')
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
    
    print("\n   By Type:")
    for vtype, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print(f"      {vtype}: {count}")
    
    print("\n   By Severity:")
    for sev, count in severity_counts.items():
        if count > 0:
            print(f"      {sev.capitalize()}: {count}")

except Exception as e:
    print(f"   ⚠️  Could not read report: {e}")

# Generate verification script
print("\n[3/3] Generating verification script...")

try:
    verification_script = """#!/usr/bin/env python3
'''
Manual Verification Script
Test each finding to confirm it's real before submission
'''

import requests
import json

# Load findings
with open('reports/AI_Hunt_Report_20251104_011529.json', 'r') as f:
    report = json.load(f)

print("="*70)
print("MANUAL VERIFICATION CHECKLIST")
print("="*70)

for i, finding in enumerate(report['findings'], 1):
    print(f"\\n[{i}/{len(report['findings'])}] {finding['type']} - {finding['severity']}")
    print(f"    URL: {finding['url']}")
    
    if finding['type'] == 'XSS':
        print(f"    Test: Visit URL and inject: <script>alert('XSS')</script>")
        print(f"    Expected: Alert box appears (or check source for unescaped script)")
    
    elif finding['type'] == 'Open Redirect':
        print(f"    Test: Add ?redirect=https://evil.com to URL")
        print(f"    Expected: Browser redirects to evil.com")
    
    print(f"    Verified: [ ] Yes  [ ] No  [ ] False Positive")
    print(f"    Notes: ___________________________________________")

print("\\n" + "="*70)
print("After verification, submit only CONFIRMED findings to Microsoft MSRC")
print("="*70)
"""
    
    with open('verify_findings.py', 'w', encoding='utf-8') as f:
        f.write(verification_script)
    
    print("   ✅ Created verify_findings.py")

except Exception as e:
    print(f"   ❌ Error creating verification script: {e}")

print("\n" + "="*70)
print("✅ FIXES COMPLETE!")
print("="*70)
print("\nNext steps:")
print("1. Run: python verify_findings.py")
print("2. Manually verify each finding")
print("3. Submit confirmed findings to Microsoft MSRC")
print("4. Run: python ai_autonomous_hunter.py (with AI fixes)")
