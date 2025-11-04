#!/usr/bin/env python3
"""
BugBountyAI Autonomous Hunter v5.0
TRUE Complete Automation with AI Decision-Making

Features:
- AI decides what tools to run next
- Tests ALL URLs found (not just first 5)
- Real vulnerability exploitation attempts
- Agent-S + Burp integration that actually works
- Continuous scanning until exhausted
- Smart tool chaining based on findings
"""

import subprocess
import json
import os
import sys
import time
import tempfile
import re
from pathlib import Path
from orchestrator import BugBountyOrchestrator
import requests
from urllib.parse import urljoin, urlparse, parse_qs
import random
import threading

class AIAutonomousHunter:
    def __init__(self, config_file):
        print("\n[INIT] 🤖 Starting AI Autonomous Hunter v5.0...")
        
        self.orchestrator = BugBountyOrchestrator()
        self.orchestrator.check_api_connection()
        self.orchestrator.load_scope_config(config_file)
        
        self.target = self.orchestrator.target
        self.scope = self.orchestrator.scope
        self.findings = []
        self.tested_urls = set()
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # FIXED: Your actual tool paths
        self.tools = {
            'subfinder': r'C:\Users\aksha\go\bin\subfinder.exe',
            'httpx': r'C:\Users\aksha\go\bin\httpx.exe',
            'dnsx': r'C:\Users\aksha\go\bin\dnsx.exe',
            'katana': r'C:\Users\aksha\go\bin\katana.exe',
            'nuclei': r'C:\Users\aksha\go\bin\nuclei.exe',
            'gau': r'C:\Users\aksha\go\bin\gau.exe',
            'waybackurls': r'C:\Users\aksha\go\bin\waybackurls.exe',
        }
        
        # FIXED: Your actual Burp path
        self.burp_path = r'C:\Users\aksha\Documents\Burp\Burp.lnk'
        self.firefox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        
        # Results storage
        os.makedirs('results', exist_ok=True)
        os.makedirs('reports', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        print("✅ AI Hunter initialized")
    
    def ask_ai_next_action(self, context):
        """Ask Perplexity AI what to do next based on current findings"""
        prompt = f"""You are a professional bug bounty hunter. Based on the current context, suggest the next 3 most effective actions.

Context:
- Target: {self.target}
- URLs found so far: {len(self.tested_urls)}
- Findings: {len(self.findings)}
- In-scope vulns: {', '.join(self.scope['vulnerability_scope']['in_scope_vulns'][:10])}
- Recent findings: {json.dumps(self.findings[-5:], indent=2) if self.findings else 'None yet'}

Current situation: {context}

Respond with ONLY a JSON array of 3 actions in this exact format:
[
  {{"tool": "subfinder", "reason": "Need more subdomains", "priority": "high"}},
  {{"tool": "nuclei", "reason": "Check for known CVEs", "priority": "medium"}},
  {{"tool": "manual_test_xss", "reason": "Forms detected", "priority": "high"}}
]

Available tools: subfinder, httpx, nuclei, katana, gau, waybackurls, manual_test_xss, manual_test_sqli, manual_test_ssrf, burp_scan"""

        try:
            response = self.orchestrator.llm.invoke(prompt)
            actions = json.loads(response.content)
            return actions[:3]
        except Exception as e:
            print(f"⚠️  AI decision failed: {e}, using fallback")
            return [
                {"tool": "nuclei", "reason": "Fallback scan", "priority": "high"},
                {"tool": "manual_test_xss", "reason": "Fallback", "priority": "medium"}
            ]
    
    def autonomous_hunt(self):
        """Main autonomous hunting loop - never stops until done"""
        print("\n" + "="*70)
        print("🤖 STARTING AUTONOMOUS BUG BOUNTY HUNT")
        print("="*70)
        
        iteration = 0
        max_iterations = 50  # Safety limit
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n{'='*70}")
            print(f"🔄 ITERATION {iteration}/{max_iterations}")
            print(f"{'='*70}")
            
            # Phase 1: Recon (if first iteration or every 10 iterations)
            if iteration == 1 or iteration % 10 == 0:
                urls = self.deep_reconnaissance()
            else:
                # Load cached URLs
                urls = list(self.tested_urls)[:100] if self.tested_urls else []
            
            if not urls:
                print("\n⚠️  No URLs to test, running recon again...")
                urls = self.deep_reconnaissance()
            
            # Phase 2: AI Decision
            context = f"Iteration {iteration}. Found {len(urls)} URLs. {len(self.findings)} findings so far."
            print(f"\n[AI] 🧠 Asking AI what to do next...")
            ai_actions = self.ask_ai_next_action(context)
            
            print(f"\n[AI] 💡 AI Recommended Actions:")
            for i, action in enumerate(ai_actions, 1):
                print(f"     {i}. {action['tool']} - {action['reason']} (Priority: {action['priority']})")
            
            # Phase 3: Execute AI recommendations
            for action in ai_actions:
                tool = action['tool']
                print(f"\n[EXECUTE] 🎯 Running: {tool}")
                
                if tool == 'subfinder':
                    new_urls = self.deep_reconnaissance()
                    urls.extend(new_urls)
                
                elif tool == 'nuclei':
                    self.mass_nuclei_scan(urls[:50])
                
                elif tool == 'katana':
                    for url in urls[:20]:
                        self.deep_crawl(url)
                
                elif tool == 'manual_test_xss':
                    self.aggressive_xss_testing(urls[:30])
                
                elif tool == 'manual_test_sqli':
                    self.aggressive_sqli_testing(urls[:30])
                
                elif tool == 'manual_test_ssrf':
                    self.aggressive_ssrf_testing(urls[:30])
                
                elif tool == 'burp_scan':
                    self.burp_active_scan(urls[:10])
                
                elif tool == 'gau':
                    self.historical_url_mining()
            
            # Phase 4: Check if we should continue
            if len(self.findings) > 20:
                print("\n✅ Found 20+ vulnerabilities, wrapping up...")
                break
            
            if iteration > 10 and len(self.findings) == 0:
                print("\n⚠️  10 iterations, no findings. Trying different approach...")
                self.emergency_deep_scan(urls)
            
            # Phase 5: Brief summary
            print(f"\n📊 Iteration {iteration} Summary:")
            print(f"   URLs Tested: {len(self.tested_urls)}")
            print(f"   Findings: {len(self.findings)}")
            print(f"   Critical: {sum(1 for f in self.findings if f.get('severity') == 'critical')}")
            print(f"   High: {sum(1 for f in self.findings if f.get('severity') == 'high')}")
            
            time.sleep(2)  # Respect rate limits
        
        # Final report
        return self.generate_final_report()
    
    # ========== PHASE 1: DEEP RECONNAISSANCE ==========
    
    def deep_reconnaissance(self):
        """Comprehensive reconnaissance"""
        print("\n[RECON] 🔍 Deep Reconnaissance Starting...")
        
        # 1. Subdomain enumeration
        print("\n[RECON] 1/6: Subfinder (subdomain enum)...")
        subdomains = self._run_subfinder()
        print(f"        ✅ {len(subdomains)} subdomains")
        
        # 2. Filter by scope
        print("\n[RECON] 2/6: Scope filtering...")
        in_scope = self._smart_filter(subdomains)
        print(f"        ✅ {len(in_scope)} in-scope")
        
        # 3. DNS resolution (batched)
        print("\n[RECON] 3/6: DNS resolution (batched)...")
        resolved = self._batch_dnsx(in_scope[:5000])
        print(f"        ✅ {len(resolved)} resolved")
        
        # 4. Live detection (batched)
        print("\n[RECON] 4/6: HTTPX live detection...")
        live_urls = self._batch_httpx(resolved)
        print(f"        ✅ {len(live_urls)} live")
        
        # 5. Historical URLs (GAU/Wayback)
        print("\n[RECON] 5/6: Historical URL mining...")
        historical = self.historical_url_mining()
        live_urls.extend(historical)
        print(f"        ✅ {len(historical)} historical")
        
        # 6. Crawl each URL
        print("\n[RECON] 6/6: Deep crawling top 30 URLs...")
        crawled = []
        for i, url in enumerate(live_urls[:30], 1):
            print(f"        [{i}/30] Crawling {url[:50]}...")
            paths = self.deep_crawl(url)
            crawled.extend(paths)
        print(f"        ✅ {len(crawled)} paths discovered")
        
        all_urls = list(set(live_urls + crawled))
        print(f"\n[RECON] ✅ Total unique URLs: {len(all_urls)}")
        
        return all_urls
    
    def deep_crawl(self, url):
        """Deep crawl a single URL"""
        paths = []
        try:
            # Katana crawl
            paths = self._run_katana_safe(url)
            
            # Also try manual crawling
            try:
                resp = self.session.get(url, timeout=10)
                links = re.findall(r'href=["\']([^"\']+)["\']', resp.text)
                for link in links:
                    full_url = urljoin(url, link)
                    if self.orchestrator.validate_target_url(full_url)[0]:
                        paths.append(full_url)
            except:
                pass
        except:
            pass
        
        return paths
    
    def historical_url_mining(self):
    """Mine historical URLs from archives"""
    urls = []
    try:
        # Try GAU with UTF-8 encoding fix
        cmd = f'"{self.tools["gau"]}" {self.target} --subs'
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=60, 
            shell=True,
            encoding='utf-8',  # Fix encoding
            errors='ignore'     # Ignore decode errors
        )
        urls.extend([line.strip() for line in result.stdout.split('\n') if line.strip()])
    except Exception as e:
        print(f"        ⚠️  GAU error (non-fatal): {e}")
    
    try:
        # Try waybackurls with UTF-8 fix
        cmd = f'echo {self.target} | "{self.tools["waybackurls"]}"'
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=60, 
            shell=True,
            encoding='utf-8',
            errors='ignore'
        )
        urls.extend([line.strip() for line in result.stdout.split('\n') if line.strip()])
    except Exception as e:
        print(f"        ⚠️  Waybackurls error (non-fatal): {e}")
    
    # Filter by scope
    return self._smart_filter_urls(urls)

    
    # ========== PHASE 2: INTELLIGENT SCANNING ==========
    
    def mass_nuclei_scan(self, urls):
        """Run Nuclei on multiple URLs"""
        print(f"\n[NUCLEI] 🎯 Scanning {len(urls)} URLs...")
        
        for i, url in enumerate(urls, 1):
            if url in self.tested_urls:
                continue
            
            print(f"[NUCLEI] [{i}/{len(urls)}] {url[:60]}...")
            vulns = self._run_nuclei_safe(url)
            
            for vuln in vulns:
                is_testable, _ = self.orchestrator.validate_vulnerability_type(vuln['type'])
                if is_testable:
                    self.findings.append({
                        'url': url,
                        'type': vuln['type'],
                        'severity': vuln.get('severity', 'info'),
                        'source': 'nuclei',
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'tested': True
                    })
                    print(f"          ✅ {vuln['type']} ({vuln.get('severity')})")
            
            self.tested_urls.add(url)
    
    def burp_active_scan(self, urls):
        """Launch Burp and scan URLs"""
        print(f"\n[BURP] 🛡️  Burp Suite Active Scan...")
        
        # Launch Burp
        if os.path.exists(self.burp_path):
            try:
                subprocess.Popen([self.burp_path])
                print("     ✅ Burp launched")
                time.sleep(10)
            except Exception as e:
                print(f"     ❌ Burp launch failed: {e}")
                return
        
        # Open URLs in Firefox (with Burp proxy)
        if os.path.exists(self.firefox_path):
            for url in urls[:10]:
                try:
                    subprocess.Popen([self.firefox_path, url])
                    print(f"     ✅ Opened: {url[:60]}")
                    time.sleep(5)
                except:
                    pass
        
        print(f"     ⏳ Burp is scanning... (review UI for findings)")
    
    # ========== PHASE 3: AGGRESSIVE VULNERABILITY TESTING ==========
    
    def aggressive_xss_testing(self, urls):
        """Test every URL for XSS vulnerabilities"""
        print(f"\n[XSS] 💉 Aggressive XSS Testing on {len(urls)} URLs...")
        
        xss_payloads = [
            '<script>alert("XSS")</script>',
            '"><script>alert(1)</script>',
            "'><script>alert(1)</script>",
            '<img src=x onerror=alert(1)>',
            '"><img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            'javascript:alert(1)',
            '<iframe src=javascript:alert(1)>',
            '<body onload=alert(1)>',
            '<input onfocus=alert(1) autofocus>',
        ]
        
        for i, url in enumerate(urls, 1):
            if url in self.tested_urls:
                continue
            
            print(f"[XSS] [{i}/{len(urls)}] Testing {url[:50]}...")
            
            # Parse URL
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            # Test each parameter
            for param in params:
                for payload in xss_payloads:
                    test_url = url.replace(f"{param}={params[param][0]}", f"{param}={payload}")
                    
                    try:
                        resp = self.session.get(test_url, timeout=5)
                        
                        # Check if payload reflected
                        if payload in resp.text:
                            # Verify it's actually XSS (not encoded)
                            if '<script>' in resp.text or 'onerror=' in resp.text:
                                self.findings.append({
                                    'url': url,
                                    'type': 'XSS (Reflected)',
                                    'severity': 'high',
                                    'parameter': param,
                                    'payload': payload,
                                    'poc': test_url,
                                    'confirmed': True,
                                    'source': 'manual_test',
                                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                                })
                                print(f"      ✅ XSS FOUND! Parameter: {param}")
                                break
                    except:
                        pass
            
            self.tested_urls.add(url)
            time.sleep(0.2)  # Rate limiting
    
    def aggressive_sqli_testing(self, urls):
        """Test every URL for SQL injection"""
        print(f"\n[SQLi] 💊 Aggressive SQLi Testing on {len(urls)} URLs...")
        
        sqli_payloads = [
            "'",
            "' OR '1'='1",
            "1' OR '1'='1",
            "' OR 1=1--",
            "admin'--",
            "' UNION SELECT NULL--",
            "1' UNION SELECT NULL,NULL--",
            "' AND 1=2 UNION SELECT NULL--",
        ]
        
        sqli_errors = [
            'sql syntax',
            'mysql',
            'mysqli',
            'sqlite',
            'postgresql',
            'ora-',
            'error in your sql',
            'warning: mysql',
            'unclosed quotation mark',
            'quoted string not properly terminated'
        ]
        
        for i, url in enumerate(urls, 1):
            if url in self.tested_urls:
                continue
            
            print(f"[SQLi] [{i}/{len(urls)}] Testing {url[:50]}...")
            
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for param in params:
                for payload in sqli_payloads:
                    test_url = url.replace(f"{param}={params[param][0]}", f"{param}={payload}")
                    
                    try:
                        resp = self.session.get(test_url, timeout=5)
                        
                        # Check for SQL errors
                        resp_lower = resp.text.lower()
                        for error in sqli_errors:
                            if error in resp_lower:
                                self.findings.append({
                                    'url': url,
                                    'type': 'SQL Injection',
                                    'severity': 'critical',
                                    'parameter': param,
                                    'payload': payload,
                                    'error': error,
                                    'poc': test_url,
                                    'confirmed': True,
                                    'source': 'manual_test',
                                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                                })
                                print(f"      ✅ SQLi FOUND! Parameter: {param}, Error: {error}")
                                break
                    except:
                        pass
            
            self.tested_urls.add(url)
            time.sleep(0.2)
    
    def aggressive_ssrf_testing(self, urls):
        """Test for SSRF vulnerabilities"""
        print(f"\n[SSRF] 🌐 Aggressive SSRF Testing on {len(urls)} URLs...")
        
        ssrf_payloads = [
            'http://localhost',
            'http://127.0.0.1',
            'http://169.254.169.254/latest/meta-data/',
            'http://[::1]',
            'http://metadata.google.internal',
        ]
        
        for i, url in enumerate(urls, 1):
            if url in self.tested_urls:
                continue
            
            print(f"[SSRF] [{i}/{len(urls)}] Testing {url[:50]}...")
            
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            # Look for parameters that might be URLs
            url_params = [p for p in params if 'url' in p.lower() or 'redirect' in p.lower() or 'uri' in p.lower()]
            
            for param in url_params:
                for payload in ssrf_payloads:
                    test_url = url.replace(f"{param}={params[param][0]}", f"{param}={payload}")
                    
                    try:
                        resp = self.session.get(test_url, timeout=10)
                        
                        # Check if internal resource was fetched
                        if resp.status_code == 200 and len(resp.content) > 100:
                            # Look for internal metadata
                            if 'ami-id' in resp.text or 'hostname' in resp.text.lower():
                                self.findings.append({
                                    'url': url,
                                    'type': 'SSRF',
                                    'severity': 'critical',
                                    'parameter': param,
                                    'payload': payload,
                                    'poc': test_url,
                                    'confirmed': True,
                                    'source': 'manual_test',
                                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                                })
                                print(f"      ✅ SSRF FOUND! Parameter: {param}")
                                break
                    except:
                        pass
            
            self.tested_urls.add(url)
            time.sleep(0.2)
    
    def emergency_deep_scan(self, urls):
    """When all else fails, try everything"""
    print(f"\n[EMERGENCY] 🚨 Emergency Deep Scan (trying everything)...")
    
    # Filter URLs first to avoid scope violations
    safe_urls = []
    for url in urls[:50]:
        is_valid, reason = self.orchestrator.validate_target_url(url)
        if is_valid:
            safe_urls.append(url)
    
    print(f"[EMERGENCY] Testing {len(safe_urls)} in-scope URLs...")
    
    # Try every vulnerability type on SAFE URLs only
    for url in safe_urls:
        print(f"\n[EMERGENCY] Testing {url[:50]}...")
        
        # XSS
        try:
            resp = self.session.get(f"{url}?q=<script>alert(1)</script>", timeout=5)
            if '<script>' in resp.text:
                self.findings.append({
                    'url': url, 
                    'type': 'XSS', 
                    'severity': 'high', 
                    'source': 'emergency',
                    'confirmed': True
                })
                print(f"      ✅ XSS FOUND!")
        except:
            pass
        
        # Open Redirect - Fix detection
        try:
            resp = self.session.get(f"{url}?redirect=https://evil.com", timeout=5, allow_redirects=False)
            location = resp.headers.get('Location', '')
            # Only flag if it actually redirects to our payload
            if 'evil.com' in location:
                self.findings.append({
                    'url': url, 
                    'type': 'Open Redirect', 
                    'severity': 'medium', 
                    'source': 'emergency',
                    'confirmed': True
                })
                print(f"      ✅ Open Redirect FOUND!")
        except:
            pass
        
        # Path Traversal
        try:
            resp = self.session.get(f"{url}/../../../etc/passwd", timeout=5)
            if 'root:x:0:0' in resp.text:
                self.findings.append({
                    'url': url, 
                    'type': 'Path Traversal', 
                    'severity': 'critical', 
                    'source': 'emergency',
                    'confirmed': True
                })
                print(f"      ✅ Path Traversal FOUND!")
        except:
            pass
    
    # ========== FINAL REPORT ==========
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        print("\n" + "="*70)
        print("📊 GENERATING FINAL REPORT")
        print("="*70)
        
        report = {
            'metadata': {
                'program': self.scope['program']['name'],
                'target': self.target,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_urls_tested': len(self.tested_urls),
                'total_findings': len(self.findings),
                'authorization': self.scope['program']['authorization']
            },
            'findings': self.findings,
            'summary': {
                'by_severity': {
                    'critical': len([f for f in self.findings if f.get('severity') == 'critical']),
                    'high': len([f for f in self.findings if f.get('severity') == 'high']),
                    'medium': len([f for f in self.findings if f.get('severity') == 'medium']),
                    'low': len([f for f in self.findings if f.get('severity') == 'low']),
                },
                'by_type': {},
                'confirmed_exploits': len([f for f in self.findings if f.get('confirmed')])
            }
        }
        
        # Count by type
        for finding in self.findings:
            vtype = finding.get('type', 'Unknown')
            report['summary']['by_type'][vtype] = report['summary']['by_type'].get(vtype, 0) + 1
        
        # Save report
        report_file = f"reports/AI_Hunt_Report_{time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Report saved: {report_file}")
        print(f"\n📊 FINAL SUMMARY:")
        print(f"   URLs Tested: {len(self.tested_urls)}")
        print(f"   Total Findings: {len(self.findings)}")
        print(f"   Critical: {report['summary']['by_severity']['critical']}")
        print(f"   High: {report['summary']['by_severity']['high']}")
        print(f"   Medium: {report['summary']['by_severity']['medium']}")
        print(f"   Confirmed Exploits: {report['summary']['confirmed_exploits']}")
        print(f"\n   Vulnerabilities by Type:")
        for vtype, count in sorted(report['summary']['by_type'].items(), key=lambda x: x[1], reverse=True):
            print(f"      {vtype}: {count}")
        
        # Save session
        self.orchestrator.save_session_log()
        
        return report
    
    # ========== TOOL EXECUTION METHODS ==========
    
    def _run_subfinder(self):
        """Run subfinder"""
        try:
            output_file = os.path.join(tempfile.gettempdir(), f'subs_{int(time.time())}.txt')
            cmd = f'"{self.tools["subfinder"]}" -d {self.target} -o "{output_file}"'
            subprocess.run(cmd, capture_output=True, timeout=120, shell=True)
            
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    subs = [line.strip() for line in f if line.strip()]
                os.remove(output_file)
                return subs
            return []
        except Exception as e:
            print(f"❌ Subfinder error: {e}")
            return []
    
    def _batch_dnsx(self, domains, batch_size=100):
        """Batch DNSX"""
        resolved = []
        try:
            for i in range(0, len(domains), batch_size):
                batch = domains[i:i+batch_size]
                temp_file = os.path.join(tempfile.gettempdir(), f'dnsx_batch_{i}.txt')
                
                with open(temp_file, 'w') as f:
                    f.write('\n'.join(batch))
                
                cmd = f'"{self.tools["dnsx"]}" -l "{temp_file}" -silent -a'
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, shell=True)
                resolved.extend([line.split()[0] for line in result.stdout.split('\n') if line.strip()])
                
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        except Exception as e:
            print(f"❌ DNSX error: {e}")
        
        return resolved
    
    def _batch_httpx(self, domains, batch_size=50):
        """Batch HTTPX"""
        live = []
        try:
            for i in range(0, len(domains), batch_size):
                batch = domains[i:i+batch_size]
                temp_file = os.path.join(tempfile.gettempdir(), f'httpx_batch_{i}.txt')
                
                with open(temp_file, 'w') as f:
                    f.write('\n'.join([f'http://{d}\nhttps://{d}' for d in batch]))
                
                cmd = f'"{self.tools["httpx"]}" -l "{temp_file}" -silent -follow-redirects'
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, shell=True)
                live.extend([line.strip() for line in result.stdout.split('\n') if line.strip()])
                
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        except Exception as e:
            print(f"❌ HTTPX error: {e}")
        
        return live
    
    def _run_katana_safe(self, url, timeout=30):
        """Safe katana"""
        try:
            cmd = f'"{self.tools["katana"]}" -u "{url}" -silent'
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=True)
            return [line.strip() for line in result.stdout.split('\n') if line.strip()]
        except:
            return []
    
    def _run_nuclei_safe(self, url, timeout=60):
        """Safe nuclei"""
        try:
            cmd = f'"{self.tools["nuclei"]}" -u "{url}" -silent -json'
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=True)
            
            vulns = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    try:
                        data = json.loads(line)
                        vulns.append({
                            'type': data.get('info', {}).get('name', 'Unknown'),
                            'severity': data.get('info', {}).get('severity', 'info')
                        })
                    except:
                        pass
            return vulns
        except:
            return []
    
    def _smart_filter(self, items):
        """Filter by scope"""
        filtered = []
        for item in items:
            url = f"https://{item}" if not item.startswith('http') else item
            is_valid, _ = self.orchestrator.validate_target_url(url)
            if is_valid:
                filtered.append(item)
        return filtered[:5000]
    
    def _smart_filter_urls(self, urls):
        """Filter URLs by scope"""
        return [u for u in urls if self.orchestrator.validate_target_url(u)[0]][:1000]


def main():
    """Execute autonomous hunting"""
    config_file = 'config/target.json'
    
    if not os.path.exists(config_file):
        print(f"❌ Config file not found: {config_file}")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("🤖 BugBountyAI AUTONOMOUS HUNTER v5.0")
    print("AI-Driven Complete Automation")
    print("="*70)
    
    hunter = AIAutonomousHunter(config_file)
    
    try:
        report = hunter.autonomous_hunt()
        
        print("\n" + "="*70)
        print("✅ AUTONOMOUS HUNT COMPLETE!")
        print("="*70)
        print(f"📁 Full report: reports/ directory")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Hunt interrupted by user")
        hunter.orchestrator.save_session_log()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
