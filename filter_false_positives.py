#!/usr/bin/env python3
"""
Filter out WAF-blocked findings (false positives)
"""

import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(429, 500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Load findings
with open('reports/AI_Hunt_Report_20251104_011529.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

print("="*70)
print("🔍 FILTERING FALSE POSITIVES (WAF-BLOCKED)")
print("="*70)

confirmed = []
false_positives = []
unknown = []

for i, finding in enumerate(report['findings'], 1):
    url = finding['url']
    ftype = finding['type']
    
    print(f"\n[{i}/{len(report['findings'])}] Testing {ftype}...")
    print(f"    URL: {url[:60]}...")
    
    try:
        # Quick test - just check if basic page loads
        resp = requests_retry_session().get(
            url, 
            timeout=5,
            allow_redirects=True,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        # Check for WAF signatures
        waf_indicators = [
            'you have been blocked',
            'security service',
            'access denied',
            'firewall',
            'rate limit',
            'challenge',
            'cloudflare',
            'akamai',
            'incapsula',
            '403 forbidden',
        ]
        
        response_text = resp.text.lower()
        
        if any(indicator in response_text for indicator in waf_indicators):
            print(f"    ⚠️  WAF BLOCKED - False positive")
            false_positives.append(finding)
        
        elif resp.status_code == 200:
            print(f"    ✅ REAL - Page loads normally (needs manual verification)")
            confirmed.append(finding)
        
        else:
            print(f"    ❓ UNKNOWN - Status: {resp.status_code}")
            unknown.append(finding)
    
    except requests.RequestException as e:
        print(f"    ❌ ERROR: {str(e)[:40]}")
        unknown.append(finding)

# Save filtered results
print("\n" + "="*70)
print("📊 RESULTS")
print("="*70)

print(f"\n✅ REAL (needs manual verification): {len(confirmed)}")
for f in confirmed[:5]:
    print(f"   - {f['type']} on {f['url'][:50]}")

print(f"\n⚠️  FALSE POSITIVES (WAF-blocked): {len(false_positives)}")
for f in false_positives[:5]:
    print(f"   - {f['type']} on {f['url'][:50]}")

print(f"\n❓ UNKNOWN: {len(unknown)}")

# Save filtered report
filtered_report = report.copy()
filtered_report['findings'] = confirmed
filtered_report['filtered_out'] = {
    'waf_blocked': len(false_positives),
    'unknown': len(unknown)
}

with open('reports/AI_Hunt_Report_FILTERED.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_report, f, indent=2)

print(f"\n✅ Filtered report saved: reports/AI_Hunt_Report_FILTERED.json")
print(f"   Ready to submit: {len(confirmed)} findings")
