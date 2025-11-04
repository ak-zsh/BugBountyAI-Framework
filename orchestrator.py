#!/usr/bin/env python3
"""
BugBountyAI Orchestrator v2.0
Unified control for Agent-S (GUI) + MAPTA (Backend) + Perplexity Pro (LLM)
With comprehensive scope validation & compliance enforcement
For authorized bug bounty/VDP testing only.
"""

import openai
import os
import json
import sys
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path

# Load environment variables
load_dotenv('Agent-S/.env')

class BugBountyOrchestrator:
    def __init__(self):
        """Initialize orchestrator with Perplexity Pro API"""
        self.perplexity_key = os.getenv('PERPLEXITY_API_KEY')
        self.llm_model = 'sonar-pro'
        self.base_url = 'https://api.perplexity.ai'
        self.client = openai.OpenAI(base_url=self.base_url, api_key=self.perplexity_key)
                # Expose LLM for AI Hunter
        from langchain_openai import ChatOpenAI
        self.llm = ChatOpenAI(
            model="sonar-pro",
            openai_api_key=self.api_key,
            openai_api_base="https://api.perplexity.ai",
            temperature=0.2
        )

        # Scope management
        self.target = None
        self.program = {}
        self.scope = {}
        self.config_file = None
        
        # Session tracking for compliance
        self.session_log = {
            'timestamp': datetime.now().isoformat(),
            'framework_version': '2.0',
            'actions': [],
            'scope_violations': [],
            'validated_urls': [],
            'tested_vulnerabilities': []
        }
    
    # ============================================================================
    # API & CONNECTION MANAGEMENT
    # ============================================================================
    
    def check_api_connection(self):
        """Verify Perplexity Pro API is accessible"""
        try:
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=[{'role': 'user', 'content': 'Say OK'}]
            )
            print("✅ Perplexity Pro API connected")
            self.session_log['actions'].append({
                'timestamp': datetime.now().isoformat(),
                'action': 'api_connection_verified',
                'model': self.llm_model,
                'status': 'success'
            })
            return True
        except Exception as e:
            print(f"❌ API Connection Error: {e}")
            self.session_log['actions'].append({
                'timestamp': datetime.now().isoformat(),
                'action': 'api_connection_failed',
                'error': str(e)
            })
            return False
    
    # ============================================================================
    # SCOPE CONFIGURATION MANAGEMENT
    # ============================================================================
    
    def load_scope_config(self, config_file):
        """Load comprehensive scope configuration from JSON file"""
        try:
            config_path = Path(config_file)
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found: {config_file}")
            
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Validate config structure
            required_keys = ['target', 'program', 'domain_scope', 'vulnerability_scope', 
                           'testing_restrictions', 'rate_limits']
            missing_keys = [k for k in required_keys if k not in config]
            if missing_keys:
                raise ValueError(f"Config missing required keys: {missing_keys}")
            
            self.target = config.get('target')
            self.program = config.get('program', {})
            self.scope = config
            self.config_file = config_file
            
            # Display scope summary
            self._display_scope_summary()
            
            self.session_log['actions'].append({
                'timestamp': datetime.now().isoformat(),
                'action': 'scope_config_loaded',
                'program': self.program.get('name'),
                'target': self.target,
                'config_file': config_file,
                'in_scope_domains': len(config['domain_scope']['in_scope_domains']),
                'in_scope_vulns': len(config['vulnerability_scope']['in_scope_vulns']),
                'status': 'success'
            })
            
            print("\n✅ Scope configuration loaded successfully!")
            print("⚠️  COMPLIANCE: All testing will be restricted to in-scope items only.")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load scope: {e}")
            self.session_log['actions'].append({
                'timestamp': datetime.now().isoformat(),
                'action': 'scope_config_load_failed',
                'error': str(e)
            })
            return False
    
    def _display_scope_summary(self):
        """Display comprehensive scope summary"""
        if not self.scope:
            return
        
        print("\n" + "="*70)
        print(f"📋 Program: {self.program.get('name', 'N/A')}")
        print(f"🎯 Target: {self.target}")
        print(f"📌 Platform: {self.program.get('platform', 'N/A')}")
        print(f"✅ Authorization: {self.program.get('authorization', 'Manual Review Required')}")
        print("="*70)
        
        # Domains
        print("\n✅ IN-SCOPE DOMAINS:")
        for domain in self.scope.get('domain_scope', {}).get('in_scope_domains', []):
            print(f"   ✓ {domain}")
        
        print("\n❌ OUT-OF-SCOPE DOMAINS:")
        for domain in self.scope.get('domain_scope', {}).get('out_of_scope_domains', []):
            print(f"   ✗ {domain}")
        
        # Vulnerabilities
        print("\n✅ IN-SCOPE VULNERABILITIES:")
        vulns = self.scope.get('vulnerability_scope', {}).get('in_scope_vulns', [])
        for vuln in vulns[:10]:  # Show first 10
            print(f"   ✓ {vuln}")
        if len(vulns) > 10:
            print(f"   ... and {len(vulns) - 10} more")
        
        print("\n❌ OUT-OF-SCOPE VULNERABILITIES:")
        blocked = self.scope.get('vulnerability_scope', {}).get('out_of_scope_vulns', [])
        for vuln in blocked[:5]:
            print(f"   ✗ {vuln}")
        if len(blocked) > 5:
            print(f"   ... and {len(blocked) - 5} more")
        
        # Restrictions
        print("\n⛔ BLOCKED PATHS (Auto-Excluded from Testing):")
        for path in self.scope.get('testing_restrictions', {}).get('blocked_paths', [])[:5]:
            print(f"   ✗ {path}")
        blocked_paths = self.scope.get('testing_restrictions', {}).get('blocked_paths', [])
        if len(blocked_paths) > 5:
            print(f"   ... and {len(blocked_paths) - 5} more")
        
        print("\n⛔ BLOCKED METHODS (Forbidden):")
        for method in self.scope.get('testing_restrictions', {}).get('blocked_methods', []):
            print(f"   ✗ {method}")
        
        # Rate limits
        limits = self.scope.get('rate_limits', {})
        print(f"\n🔄 Rate Limits:")
        print(f"   • {limits.get('requests_per_second', 'N/A')} req/sec")
        print(f"   • {limits.get('requests_per_minute', 'N/A')} req/min")
        print(f"   • {limits.get('concurrent_connections', 'N/A')} concurrent connections")
    
    def set_target_and_scope(self, target_url, scope_rules):
        """Legacy method: Set target domain and scope manually"""
        self.target = target_url
        self.scope = scope_rules
        print(f"✅ Target Set: {target_url}")
        print(f"✅ Scope: {json.dumps(scope_rules, indent=2)}")
        self.session_log['actions'].append({
            'timestamp': datetime.now().isoformat(),
            'action': 'set_target_scope_manual',
            'target': target_url,
            'scope': scope_rules
        })
        return True
    
    # ============================================================================
    # SCOPE VALIDATION & ENFORCEMENT
    # ============================================================================
    
    def validate_target_url(self, url):
        """Validate URL is in scope before testing"""
        if not self.scope or 'domain_scope' not in self.scope:
            return False, "Scope not configured"
        
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        
        in_scope = self.scope['domain_scope']['in_scope_domains']
        out_scope = self.scope['domain_scope']['out_of_scope_domains']
        blocked_paths = self.scope.get('testing_restrictions', {}).get('blocked_paths', [])
        
        # Check if domain is in scope
        domain_allowed = False
        for allowed in in_scope:
            if allowed.startswith('*.'):
                base = allowed[2:]
                if domain.endswith(base) or domain == base:
                    domain_allowed = True
                    break
            elif domain == allowed:
                domain_allowed = True
                break
        
        if not domain_allowed:
            msg = f"Domain {url} is not in scope"
            self.session_log['scope_violations'].append({
                'timestamp': datetime.now().isoformat(),
                'type': 'domain_not_in_scope',
                'url': url,
                'reason': msg
            })
            return False, msg
        
        # Check against out-of-scope domains
        for blocked in out_scope:
            if blocked.startswith('*.'):
                blocked_base = blocked[2:]
                if domain.endswith(blocked_base):
                    msg = f"Domain {url} is explicitly blocked"
                    self.session_log['scope_violations'].append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'domain_explicitly_blocked',
                        'url': url,
                        'reason': msg
                    })
                    return False, msg
            elif domain == blocked:
                msg = f"Domain {url} is explicitly blocked"
                self.session_log['scope_violations'].append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'domain_explicitly_blocked',
                    'url': url,
                    'reason': msg
                })
                return False, msg
        
        # Check blocked paths
        for blocked_path in blocked_paths:
            if path.startswith(blocked_path):
                msg = f"Path {path} in {url} is blocked"
                self.session_log['scope_violations'].append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'path_blocked',
                    'url': url,
                    'reason': msg
                })
                return False, msg
        
        self.session_log['validated_urls'].append({
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'status': 'allowed'
        })
        return True, f"Domain {url} is in scope and allowed"
    
    def validate_vulnerability_type(self, vuln_type):
        """Check if vulnerability type is testable"""
        if not self.scope or 'vulnerability_scope' not in self.scope:
            return False, "Scope not configured"
        
        in_scope = [v.lower() for v in self.scope['vulnerability_scope'].get('in_scope_vulns', [])]
        
        if vuln_type.lower() in in_scope:
            self.session_log['tested_vulnerabilities'].append({
                'timestamp': datetime.now().isoformat(),
                'vuln_type': vuln_type,
                'status': 'in_scope'
            })
            return True, f"Vulnerability {vuln_type} is in scope"
        else:
            self.session_log['scope_violations'].append({
                'timestamp': datetime.now().isoformat(),
                'type': 'vuln_out_of_scope',
                'vuln_type': vuln_type,
                'reason': f"Vulnerability {vuln_type} is OUT OF SCOPE"
            })
            return False, f"Vulnerability {vuln_type} is OUT OF SCOPE"
    
    def validate_method(self, method):
        """Check if testing method is allowed"""
        if not self.scope or 'testing_restrictions' not in self.scope:
            return False, "Scope not configured"
        
        blocked = [m.lower() for m in self.scope['testing_restrictions'].get('blocked_methods', [])]
        
        if method.lower() in blocked:
            msg = f"Method {method} is not allowed"
            self.session_log['scope_violations'].append({
                'timestamp': datetime.now().isoformat(),
                'type': 'method_blocked',
                'method': method,
                'reason': msg
            })
            return False, msg
        else:
            return True, f"Method {method} is allowed"
    
    # ============================================================================
    # LLM-POWERED REASONING & PLANNING
    # ============================================================================
    
    def plan_reconnaissance(self, custom_instruction=None):
        """Use Perplexity Pro to intelligently plan reconnaissance"""
        if not self.scope:
            print("❌ Scope not configured. Load scope first with load_scope_config()")
            return None
        
        instruction = custom_instruction or f"""
        Plan a bug bounty reconnaissance workflow for {self.target} with these constraints:
        
        IN-SCOPE DOMAINS: {', '.join(self.scope.get('domain_scope', {}).get('in_scope_domains', []))}
        OUT-OF-SCOPE DOMAINS: {', '.join(self.scope.get('domain_scope', {}).get('out_of_scope_domains', []))}
        
        IN-SCOPE VULNS: {', '.join(self.scope.get('vulnerability_scope', {}).get('in_scope_vulns', [])[:10])}
        OUT-OF-SCOPE VULNS: {', '.join(self.scope.get('vulnerability_scope', {}).get('out_of_scope_vulns', []))}
        
        RATE LIMIT: {self.scope.get('rate_limits', {}).get('requests_per_second', 'N/A')} req/sec
        BLOCKED PATHS: {', '.join(self.scope.get('testing_restrictions', {}).get('blocked_paths', []))}
        
        Requirements:
        - ONLY test in-scope domains
        - NEVER attempt blocked paths or methods
        - NEVER perform DoS, DDoS, or data exfiltration
        - RESPECT all rate limits
        - Return step-by-step reconnaissance plan
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=[{'role': 'user', 'content': instruction}]
            )
            plan = response.choices[0].message.content
            self.session_log['actions'].append({
                'timestamp': datetime.now().isoformat(),
                'action': 'reconnaissance_plan_generated',
                'status': 'success',
                'plan_length': len(plan)
            })
            print("\n📋 Reconnaissance Plan (Scope-Aware):\n", plan)
            return plan
        except Exception as e:
            print(f"❌ Planning Error: {e}")
            self.session_log['actions'].append({
                'timestamp': datetime.now().isoformat(),
                'action': 'reconnaissance_plan_failed',
                'error': str(e)
            })
            return None
    
    def analyze_findings(self, finding_description):
        """Use LLM to analyze findings within scope context"""
        if not self.scope:
            print("❌ Scope not configured")
            return None
        
        instruction = f"""
        Analyze this security finding within the context of this bug bounty program:
        
        FINDING: {finding_description}
        
        PROGRAM: {self.program.get('name', 'N/A')}
        IN-SCOPE VULNS: {', '.join(self.scope.get('vulnerability_scope', {}).get('in_scope_vulns', []))}
        
        Questions to answer:
        1. Is this vulnerability type in scope for this program?
        2. What's the potential impact?
        3. How should it be reported?
        4. Is it a duplicate risk?
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=[{'role': 'user', 'content': instruction}]
            )
            analysis = response.choices[0].message.content
            return analysis
        except Exception as e:
            print(f"❌ Analysis Error: {e}")
            return None
    
    # ============================================================================
    # SESSION LOGGING & COMPLIANCE
    # ============================================================================
    
    def save_session_log(self):
        """Save comprehensive session activity log for compliance"""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Add summary
        self.session_log['summary'] = {
            'total_actions': len(self.session_log['actions']),
            'scope_violations': len(self.session_log['scope_violations']),
            'urls_validated': len(self.session_log['validated_urls']),
            'vulns_tested': len(self.session_log['tested_vulnerabilities']),
            'compliance_status': 'PASSED' if len(self.session_log['scope_violations']) == 0 else 'VIOLATIONS_DETECTED'
        }
        
        with open(log_file, 'w') as f:
            json.dump(self.session_log, f, indent=2)
        
        print(f"✅ Session logged: {log_file}")
        print(f"\n📊 Session Summary:")
        print(f"   • Total Actions: {self.session_log['summary']['total_actions']}")
        print(f"   • URLs Validated: {self.session_log['summary']['urls_validated']}")
        print(f"   • Vulns Tested: {self.session_log['summary']['vulns_tested']}")
        print(f"   • Scope Violations: {self.session_log['summary']['scope_violations']}")
        print(f"   • Compliance: {self.session_log['summary']['compliance_status']}")
        
        return str(log_file)
    
    def print_violation_report(self):
        """Print any scope violations encountered"""
        if not self.session_log['scope_violations']:
            print("✅ No scope violations detected")
            return
        
        print("\n⚠️  SCOPE VIOLATIONS DETECTED:")
        print("="*70)
        for violation in self.session_log['scope_violations']:
            print(f"Type: {violation.get('type', 'N/A')}")
            print(f"Reason: {violation.get('reason', 'N/A')}")
            print(f"Time: {violation.get('timestamp', 'N/A')}")
            print("-"*70)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("BugBountyAI Orchestrator v2.0")
    print("Scope-Aware, Compliance-Enforced Bug Bounty Automation")
    print("=" * 70)
    
    orchestrator = BugBountyOrchestrator()
    
    # Check API
    if not orchestrator.check_api_connection():
        print("⚠️  Cannot connect to Perplexity Pro. Check API key in Agent-S/.env")
        sys.exit(1)
    
    # Try to load config if available
    config_file = 'config/microsoft_vdp_scope.json'
    if Path(config_file).exists():
        print(f"\n[LOADING] Configuration: {config_file}")
        if orchestrator.load_scope_config(config_file):
            # Test URL validation
            print("\n[TESTING] URL Validation Examples:")
            test_urls = [
                "https://microsoft.com/security",
                "https://internal.microsoft.com/admin",
                "https://example.com/test"
            ]
            for url in test_urls:
                is_valid, reason = orchestrator.validate_target_url(url)
                status = "✅ ALLOWED" if is_valid else "❌ BLOCKED"
                print(f"{status}: {url} - {reason}")
            
            # Test vulnerability validation
            print("\n[TESTING] Vulnerability Scope Validation:")
            test_vulns = ["XSS", "Social Engineering", "SQLi"]
            for vuln in test_vulns:
                is_valid, reason = orchestrator.validate_vulnerability_type(vuln)
                status = "✅ IN-SCOPE" if is_valid else "❌ OUT-OF-SCOPE"
                print(f"{status}: {vuln} - {reason}")
            
            # Generate plan
            print("\n[PLANNING] Generating reconnaissance plan...")
            orchestrator.plan_reconnaissance()
            
            # Save log
            orchestrator.save_session_log()
            print("\n✅ Orchestrator test complete. Ready for scoped testing!")
    else:
        print(f"\n⚠️  Config file not found: {config_file}")
        print("   Create your VDP scope config in config/ directory first")
        print("   Example: config/your_program_scope.json")
