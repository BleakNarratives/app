#!/usr/bin/env python3
"""
🎭 ADVANCED ATTACK SCENARIOS & DEFENSE
Multi-stage attacks, social engineering, supply chain compromises
"""

import random
import time
from datetime import datetime

# ============================================================================
# SCENARIO 1: MULTI-STAGE ATTACK (APT - Advanced Persistent Threat)
# ============================================================================

class MultiStageAttack:
    """Sophisticated multi-week attack campaign"""
    
    @staticmethod
    def simulate_apt():
        """
        Advanced Persistent Threat targeting recovery business
        """
        print("\n" + "="*70)
        print("🎭 SCENARIO 1: MULTI-STAGE APT ATTACK")
        print("="*70)
        
        stages = [
            {
                "week": 1,
                "stage": "Reconnaissance",
                "actions": [
                    "Attacker researches your business online",
                    "Finds employee LinkedIn profiles",
                    "Identifies your tech stack from job postings",
                    "Maps your network infrastructure",
                    "Discovers Calvin handles client communication"
                ],
                "detection": "❌ No alerts (passive reconnaissance)",
                "defense": "Monitor for unusual traffic patterns"
            },
            {
                "week": 2,
                "stage": "Initial Access",
                "actions": [
                    "Sends phishing email to Calvin",
                    "Subject: 'Urgent: Client complaint about recovery'",
                    "Contains malicious PDF attachment",
                    "Calvin opens it (social engineering works)",
                    "Keylogger installed on Calvin's machine"
                ],
                "detection": "⚠️  Antivirus might catch this (if updated)",
                "defense": "✅ Security awareness training, email filtering"
            },
            {
                "week": 3,
                "stage": "Persistence",
                "actions": [
                    "Keylogger captures Calvin's passwords",
                    "Attacker gains access to email account",
                    "Sets up email forwarding rule (hidden)",
                    "Now sees ALL client communication",
                    "Learns about upcoming high-value recovery"
                ],
                "detection": "⚠️  Could detect if monitoring email rules",
                "defense": "✅ 2FA on all accounts, regular security audits"
            },
            {
                "week": 4,
                "stage": "Privilege Escalation",
                "actions": [
                    "From Calvin's email, sends password reset to your account",
                    "Calvin's email shows 'trusted', so you might not suspect",
                    "Gains access to recovery systems",
                    "Can now see recovered private keys",
                    "Waits for high-value target"
                ],
                "detection": "🚨 SHOULD alert if monitoring unusual logins",
                "defense": "✅ Separate admin accounts, IP whitelisting"
            },
            {
                "week": 5,
                "stage": "Execution",
                "actions": [
                    "You recover $850K in Bitcoin for client 'Richard'",
                    "Attacker intercepts encrypted key AND password",
                    "Decrypts key immediately",
                    "Moves funds before client can act",
                    "Mixes through tumblers, cashes out via DEX"
                ],
                "detection": "🚨 Transaction monitoring SHOULD catch this",
                "defense": "✅ Multi-sig wallets, time-locked transactions"
            },
            {
                "week": 6,
                "stage": "Cover Tracks",
                "actions": [
                    "Removes keylogger",
                    "Deletes email forwarding rule",
                    "Clears logs",
                    "You don't realize breach until client complains",
                    "Forensic investigation finds nothing obvious"
                ],
                "detection": "❌ Too late - funds already gone",
                "defense": "✅ Continuous monitoring, incident response plan"
            }
        ]
        
        for stage in stages:
            print(f"\n📅 WEEK {stage['week']}: {stage['stage'].upper()}")
            print("-" * 70)
            
            for action in stage['actions']:
                print(f"  • {action}")
                time.sleep(0.3)
            
            print(f"\n  Detection: {stage['detection']}")
            print(f"  Defense: {stage['defense']}")
        
        print("\n" + "="*70)
        print("💡 APT DEFENSE STRATEGY:")
        print("="*70)
        print("""
1. PREVENTION (Week 1-2):
   ✅ Security awareness training for all staff
   ✅ Email filtering and anti-phishing tools
   ✅ Regular security audits
   
2. DETECTION (Week 3-4):
   ✅ Monitor for unusual email rules
   ✅ Alert on login from new locations
   ✅ Track all admin actions
   
3. CONTAINMENT (Week 5):
   ✅ Multi-signature wallets (requires 2+ keys)
   ✅ Time-locked transactions (24hr delay)
   ✅ Separate air-gapped recovery system
   
4. RESPONSE (Week 6):
   ✅ Incident response plan
   ✅ Forensic capabilities
   ✅ Cyber insurance
   ✅ Law enforcement contacts
        """)


# ============================================================================
# SCENARIO 2: SOCIAL ENGINEERING ATTACK
# ============================================================================

class SocialEngineeringAttack:
    """Human manipulation attacks"""
    
    @staticmethod
    def simulate_social_engineering():
        """
        Attacker impersonates client to steal recovery
        """
        print("\n" + "="*70)
        print("🗣️  SCENARIO 2: SOCIAL ENGINEERING ATTACK")
        print("="*70)
        
        print("\n📋 THE SETUP:")
        print("-" * 70)
        print("""
Real Client: "Michael Anderson"
- Contacted you 2 weeks ago
- High-value recovery: $320K Bitcoin
- Legitimate recovery in progress
- Uses email: manderson1975@gmail.com
        """)
        
        print("\n🎭 THE ATTACK:")
        print("-" * 70)
        
        attack_steps = [
            {
                "time": "Day 1, 9:00 AM",
                "actor": "Attacker",
                "action": "Researches Michael Anderson on social media",
                "details": "Finds birthday, hometown, job history, family names"
            },
            {
                "time": "Day 1, 2:00 PM",
                "actor": "Attacker",
                "action": "Registers lookalike email",
                "details": "manderson1975@gmai1.com (note the '1' vs 'l')"
            },
            {
                "time": "Day 2, 10:00 AM",
                "actor": "Attacker",
                "action": "Emails Calvin pretending to be Michael",
                "details": """
Subject: Update to my contact info

Hi Calvin,

I'm changing my email address. Please update your records:
OLD: manderson1975@gmail.com
NEW: manderson1975@gmai1.com

Also, I'll be traveling next week so I'll be calling from a 
different number. I'll verify with my security question when ready.

Thanks,
Michael
                """
            },
            {
                "time": "Day 2, 10:30 AM",
                "actor": "Calvin",
                "action": "Updates contact info (MISTAKE)",
                "details": "Didn't notice the email difference (gmai1 vs gmail)"
            },
            {
                "time": "Day 5, 2:00 PM",
                "actor": "You",
                "action": "Complete recovery",
                "details": "Recovered $320K. Ready for handoff."
            },
            {
                "time": "Day 5, 2:15 PM",
                "actor": "Attacker",
                "action": "Calls posing as Michael",
                "details": """
Attacker: "Hi, this is Michael Anderson. My recovery ready?"
Calvin: "Yes! Let me verify your identity. Mother's maiden name?"
Attacker: "Thompson" (found on social media)
Calvin: "Perfect! Here's your password..."
                """
            },
            {
                "time": "Day 5, 2:30 PM",
                "actor": "Attacker",
                "action": "Receives encrypted key + password",
                "details": "Decrypts and steals $320K"
            },
            {
                "time": "Day 5, 3:00 PM",
                "actor": "Real Michael",
                "action": "Calls you: 'Where's my Bitcoin?!'",
                "details": "Realizes the fraud. Too late - funds gone."
            }
        ]
        
        for step in attack_steps:
            print(f"\n⏰ {step['time']}")
            print(f"👤 {step['actor']}: {step['action']}")
            print(f"   {step['details']}")
            time.sleep(0.4)
        
        print("\n" + "="*70)
        print("🛡️  DEFENSE AGAINST SOCIAL ENGINEERING:")
        print("="*70)
        print("""
✅ NEVER update contact info via email
   → Require in-person or video call verification

✅ Use multiple verification factors
   → Not just mother's maiden name (easily researched)
   → Use info only client would know (from intake form)
   
✅ Verify email domains carefully
   → gmai1.com vs gmail.com type attacks are common
   → Highlight domain in CRM system
   
✅ Callback verification
   → Always call client at ORIGINAL number
   → Don't trust "I have a new number" claims
   
✅ Video verification for high-value
   → $100K+? Require video call to confirm identity
   → Hard to fake someone's face in real-time
   
✅ Time delays for contact changes
   → "Contact info change requests require 48hr hold"
   → Gives real client time to notice fraud
        """)


# ============================================================================
# SCENARIO 3: SUPPLY CHAIN ATTACK
# ============================================================================

class SupplyChainAttack:
    """Compromise through dependencies"""
    
    @staticmethod
    def simulate_supply_chain():
        """
        Attacker compromises a tool/library you depend on
        """
        print("\n" + "="*70)
        print("📦 SCENARIO 3: SUPPLY CHAIN ATTACK")
        print("="*70)
        
        print("\n🎯 THE SCENARIO:")
        print("-" * 70)
        print("""
Your recovery tools depend on Python packages:
- requests (for blockchain API calls)
- cryptography (for encryption)
- bitcoin-utils (for key derivation)

Attacker compromises 'bitcoin-utils' package...
        """)
        
        timeline = [
            {
                "stage": "Compromise",
                "events": [
                    "Attacker hacks bitcoin-utils PyPI account",
                    "Uploads malicious version 2.3.1",
                    "Malware hidden in key generation function",
                    "Sends all generated keys to attacker's server"
                ]
            },
            {
                "stage": "Distribution",
                "events": [
                    "You run 'pip install --upgrade bitcoin-utils'",
                    "Installs compromised version 2.3.1",
                    "No immediate signs of compromise",
                    "Your tools still work perfectly"
                ]
            },
            {
                "stage": "Data Exfiltration",
                "events": [
                    "Every recovered key is sent to attacker",
                    "Happens silently in background",
                    "You recover 10 clients over 2 weeks",
                    "Attacker has ALL their keys"
                ]
            },
            {
                "stage": "Exploitation",
                "events": [
                    "Attacker waits until you have $2M in recoveries",
                    "One day, moves ALL funds simultaneously",
                    "10 clients, all wallets drained",
                    "Your business destroyed in minutes"
                ]
            }
        ]
        
        for entry in timeline:
            print(f"\n📍 {entry['stage'].upper()}")
            print("-" * 70)
            for event in entry['events']:
                print(f"  • {event}")
                time.sleep(0.3)
        
        print("\n" + "="*70)
        print("🛡️  DEFENSE AGAINST SUPPLY CHAIN:")
        print("="*70)
        print("""
✅ PIN package versions
   requirements.txt:
   bitcoin-utils==2.3.0  # Tested, secure version
   (Don't auto-upgrade without testing)

✅ Verify package hashes
   pip install --require-hashes -r requirements.txt
   
✅ Use virtual environments
   Isolate each project's dependencies
   
✅ Code review dependencies
   Check source code of critical packages
   Especially crypto libraries
   
✅ Network isolation
   Recovery tools should NOT have internet access
   Air-gapped system for key generation
   
✅ Supply chain scanning
   Tools: Snyk, Dependabot, OWASP Dependency-Check
   Alert on vulnerable packages
   
✅ Build your own critical functions
   Don't depend on third-party for key generation
   Write and audit your own crypto functions
        """)


# ============================================================================
# SCENARIO 4: INSIDER THREAT
# ============================================================================

class InsiderThreat:
    """Attack from within the organization"""
    
    @staticmethod
    def simulate_insider():
        """
        What if Calvin goes rogue?
        """
        print("\n" + "="*70)
        print("👔 SCENARIO 4: INSIDER THREAT")
        print("="*70)
        
        print("\n⚠️  THE SCENARIO:")
        print("-" * 70)
        print("""
Calvin has been working with you for 6 months.
Business is doing well - recovering $200K+/month.
Calvin handles all client communication.
Calvin knows the process intimately.

Then... Calvin gets greedy.
        """)
        
        print("\n🎭 THE ATTACK:")
        print("-" * 70)
        
        stages = [
            "Week 1: Calvin identifies a high-value client ($1.2M recovery)",
            "Week 2: Calvin creates fake 'backup' of encrypted key",
            "Week 3: You complete recovery, Calvin handles handoff",
            "Week 4: Calvin calls password to client as normal",
            "Week 4: Calvin ALSO uses password himself to decrypt",
            "Week 4: 10 minutes before client can act, Calvin moves funds",
            "Week 4: Mixes through tumblers, converts to Monero",
            "Week 5: Calvin quits, disappears with $1.2M"
        ]
        
        for i, stage in enumerate(stages, 1):
            print(f"  {i}. {stage}")
            time.sleep(0.3)
        
        print("\n" + "="*70)
        print("🛡️  DEFENSE AGAINST INSIDER THREAT:")
        print("="*70)
        print("""
✅ SEPARATION OF DUTIES
   - Calvin handles client communication
   - You handle technical recovery
   - NEITHER has complete access alone
   
✅ TWO-PERSON RULE for high-value
   - Recoveries over $500K require both signatures
   - Neither can act alone
   - Multi-signature wallet custody
   
✅ AUDIT TRAILS
   - Log every action with timestamps
   - Who accessed what, when
   - Regular review of logs
   
✅ BACKGROUND CHECKS
   - Before hiring
   - Periodic re-checks
   - Financial stress monitoring
   
✅ INSURANCE
   - Employee dishonesty insurance
   - Fidelity bonds
   - Covers insider theft
   
✅ TECHNICAL CONTROLS
   - Keys encrypted with YOUR password only
   - Calvin can communicate but can't decrypt
   - Air-gapped key storage
   
✅ GRADUAL TRUST
   - Start with small recoveries
   - Increase responsibility over time
   - Observe behavior under pressure
        """)


# ============================================================================
# COMPLETE DEFENSE MATRIX
# ============================================================================

class DefenseMatrix:
    """Complete defense strategy against all threats"""
    
    @staticmethod
    def show_defense_matrix():
        print("\n" + "="*70)
        print("🛡️  COMPLETE DEFENSE MATRIX")
        print("="*70)
        
        matrix = {
            "Technical Defenses": [
                "✅ Encrypted key delivery (password via phone)",
                "✅ Multi-signature wallets (2-of-2 or 2-of-3)",
                "✅ Air-gapped recovery system (offline key generation)",
                "✅ Transaction monitoring (real-time alerts)",
                "✅ Network isolation (no internet on critical systems)",
                "✅ Package pinning (no auto-updates)",
                "✅ Code audits (review all dependencies)"
            ],
            "Process Defenses": [
                "✅ Two-person rule (high-value recoveries)",
                "✅ Separation of duties (client vs technical)",
                "✅ Verification protocols (multi-factor identity)",
                "✅ Time delays (48hr for contact changes)",
                "✅ Audit trails (log everything)",
                "✅ Incident response plan (documented procedures)",
                "✅ Regular security training (monthly updates)"
            ],
            "Human Defenses": [
                "✅ Security awareness training (anti-phishing)",
                "✅ Background checks (before hiring)",
                "✅ Video verification (high-value clients)",
                "✅ Callback protocols (original phone only)",
                "✅ Email verification (check domains carefully)",
                "✅ Social engineering tests (quarterly drills)",
                "✅ Stress monitoring (watch for financial pressure)"
            ],
            "Insurance & Legal": [
                "✅ Cyber insurance (covers breaches)",
                "✅ E&O insurance (errors and omissions)",
                "✅ Fidelity bonds (employee dishonesty)",
                "✅ Client agreements (limit liability)",
                "✅ Incident response retainer (legal team ready)",
                "✅ Law enforcement contacts (FBI cyber division)",
                "✅ Forensic capabilities (document everything)"
            ]
        }
        
        for category, defenses in matrix.items():
            print(f"\n📋 {category.upper()}")
            print("-" * 70)
            for defense in defenses:
                print(f"  {defense}")
        
        print("\n" + "="*70)
        print("💰 COST vs VALUE")
        print("="*70)
        print("""
Initial Setup Cost: ~$5,000-10,000
  - Security tools/software
  - Training
  - Insurance
  - Legal review

Monthly Ongoing: ~$1,000-2,000
  - Insurance premiums
  - Monitoring tools
  - Security updates

Protection Value: PRICELESS
  - One $500K theft destroys your business
  - Legal liability could be millions
  - Reputation damage = business death
  
ROI: Infinite
  - Prevents catastrophic loss
  - Enables high-value clients (they trust you)
  - Sleep well at night
        """)


# ============================================================================
# MAIN DEMO
# ============================================================================

def main():
    print("="*70)
    print("🎭 ADVANCED ATTACK SCENARIOS & DEFENSE")
    print("="*70)
    print()
    print("Available Scenarios:")
    print("  1. Multi-Stage APT Attack (6-week campaign)")
    print("  2. Social Engineering (impersonation)")
    print("  3. Supply Chain Attack (compromised packages)")
    print("  4. Insider Threat (rogue employee)")
    print("  5. Complete Defense Matrix")
    print("  6. Run All Scenarios")
    print()
    
    choice = input("Select scenario (1-6): ").strip()
    
    if choice == "1":
        MultiStageAttack.simulate_apt()
    elif choice == "2":
        SocialEngineeringAttack.simulate_social_engineering()
    elif choice == "3":
        SupplyChainAttack.simulate_supply_chain()
    elif choice == "4":
        InsiderThreat.simulate_insider()
    elif choice == "5":
        DefenseMatrix.show_defense_matrix()
    elif choice == "6":
        print("\n🎬 RUNNING ALL SCENARIOS...")
        MultiStageAttack.simulate_apt()
        SocialEngineeringAttack.simulate_social_engineering()
        SupplyChainAttack.simulate_supply_chain()
        InsiderThreat.simulate_insider()
        DefenseMatrix.show_defense_matrix()
        
        print("\n" + "="*70)
        print("🎓 FINAL LESSON")
        print("="*70)
        print("""
You've seen 4 major attack types:
1. APT - Patient, sophisticated, multi-week
2. Social Engineering - Exploits human trust
3. Supply Chain - Compromises your tools
4. Insider - Threat from within

KEY INSIGHT:
No single defense stops everything.
Defense in depth = Multiple layers.

EVERY layer adds cost to attacker:
- Technical controls (encryption, monitoring)
- Process controls (two-person rule, audits)
- Human controls (training, verification)
- Insurance (financial backup)

Make attacking you MORE EXPENSIVE than the potential gain.

That's how you win.
        """)

if __name__ == "__main__":
    main()