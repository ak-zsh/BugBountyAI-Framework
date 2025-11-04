#!/usr/bin/env python3
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
    print(f"\n[{i}/{len(report['findings'])}] {finding['type']} - {finding['severity']}")
    print(f"    URL: {finding['url']}")
    
    if finding['type'] == 'XSS':
        print(f"    Test: Visit URL and inject: <script>alert('XSS')</script>")
        print(f"    Expected: Alert box appears (or check source for unescaped script)")
    
    elif finding['type'] == 'Open Redirect':
        print(f"    Test: Add ?redirect=https://evil.com to URL")
        print(f"    Expected: Browser redirects to evil.com")
    
    print(f"    Verified: [ ] Yes  [ ] No  [ ] False Positive")
    print(f"    Notes: ___________________________________________")

print("\n" + "="*70)
print("After verification, submit only CONFIRMED findings to Microsoft MSRC")
print("="*70)
