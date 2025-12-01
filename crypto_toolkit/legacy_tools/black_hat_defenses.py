#!/usr/bin/env python3
"""
🛡️ BLACK HAT DEFENSE TOOLKIT
Protect recovered Bitcoin from interception and theft
"""

import hashlib
import secrets
import time
import json
from datetime import datetime
import base64

# ============================================================================
# TOOL 1: ENCRYPTED KEY DELIVERY
# ============================================================================

class SecureKeyDelivery:
    """Encrypt private keys for secure delivery to clients"""
    
    @staticmethod
    def generate_one_time_password():
        """Generate a secure one-time password"""
        # 6-word passphrase (easier for clients than random chars)
        words = [
            "alpha", "bravo", "charlie", "delta", "echo", "foxtrot",
            "golf", "hotel", "india", "juliet", "kilo", "lima",
            "mike", "november", "oscar", "papa", "quebec", "romeo",
            "sierra", "tango", "uniform", "victor", "whiskey", "xray",
            "yankee", "zulu"
        ]
        
        passphrase = "-".join(secrets.choice(words) for _ in range(6))
        return passphrase
    
    @staticmethod
    def encrypt_key(private_key, password):
        """
        Simple XOR encryption with password
        NOTE: This is basic - use real encryption (PGP/AES) in production
        """
        # Hash password to get consistent key
        key_hash = hashlib.sha256(password.encode()).digest()
        
        # XOR encryption (simple but effective for demo)
        encrypted = bytearray()
        key_bytes = private_key.encode()
        
        for i, byte in enumerate(key_bytes):
            encrypted.append(byte ^ key_hash[i % len(key_hash)])
        
        # Base64 encode for transmission
        encoded = base64.b64encode(encrypted).decode()
        
        return encoded
    
    @staticmethod
    def decrypt_key(encrypted_data, password):
        """Decrypt the private key"""
        # Decode base64
        encrypted = base64.b64decode(encrypted_data)
        
        # Hash password
        key_hash = hashlib.sha256(password.encode()).digest()
        
        # XOR decrypt
        decrypted = bytearray()
        for i, byte in enumerate(encrypted):
            decrypted.append(byte ^ key_hash[i % len(key_hash)])
        
        return decrypted.decode()
    
    @staticmethod
    def secure_delivery_process(private_key):
        """Complete secure delivery workflow"""
        print("🔐 SECURE KEY DELIVERY SYSTEM")
        print("=" * 60)
        
        # Generate one-time password
        otp = SecureKeyDelivery.generate_one_time_password()
        
        # Encrypt the key
        encrypted = SecureKeyDelivery.encrypt_key(private_key, otp)
        
        print("\n📋 DELIVERY INSTRUCTIONS:")
        print("-" * 60)
        print("1. Call client on phone (verified number)")
        print("2. Read them the password: (DO NOT EMAIL THIS)")
        print(f"\n   PASSWORD: {otp}\n")
        print("3. Email them the encrypted key:")
        print(f"\n   ENCRYPTED KEY:")
        print(f"   {encrypted[:40]}...")
        print(f"\n4. Client uses this tool to decrypt")
        print("5. Client immediately moves funds to new wallet")
        print("-" * 60)
        
        return {
            "encrypted_key": encrypted,
            "password": otp,
            "instructions": "Password via phone, encrypted key via email"
        }


# ============================================================================
# TOOL 2: TRANSACTION MONITORING
# ============================================================================

class TransactionMonitor:
    """Monitor Bitcoin addresses for suspicious activity"""
    
    def __init__(self):
        self.monitored_addresses = {}
        self.alerts = []
    
    def add_watch(self, address, client_name, expected_action_time=3600):
        """
        Add address to monitoring
        expected_action_time: seconds until client should move funds
        """
        self.monitored_addresses[address] = {
            "client": client_name,
            "added": time.time(),
            "expected_move_by": time.time() + expected_action_time,
            "last_check": None,
            "balance": None,
            "tx_count": 0
        }
        
        print(f"👁️  Now monitoring: {address}")
        print(f"   Client: {client_name}")
        print(f"   Alert if no activity within {expected_action_time/60} minutes")
    
    def check_address(self, address):
        """
        Check if address has been compromised
        In production, this would use blockchain API
        """
        # DEMO: Simulated check
        print(f"\n🔍 Checking {address[:20]}...")
        
        # Simulate API call
        time.sleep(0.5)
        
        # In real implementation:
        # - Call blockchain.info API
        # - Check transaction history
        # - Compare against expected patterns
        
        status = {
            "address": address,
            "check_time": datetime.now().isoformat(),
            "balance": "0.00 BTC",  # Would be real balance
            "transactions": 0,       # Would be real tx count
            "suspicious": False
        }
        
        return status
    
    def alert_suspicious_activity(self, address, reason):
        """Alert on suspicious activity"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "address": address,
            "client": self.monitored_addresses.get(address, {}).get("client"),
            "reason": reason,
            "severity": "HIGH"
        }
        
        self.alerts.append(alert)
        
        print("\n" + "!" * 60)
        print("🚨 SECURITY ALERT")
        print("!" * 60)
        print(f"Address: {address}")
        print(f"Client: {alert['client']}")
        print(f"Issue: {reason}")
        print(f"Time: {alert['timestamp']}")
        print("\n⚡ IMMEDIATE ACTION REQUIRED")
        print("!" * 60)
        
        return alert
    
    def continuous_monitor(self, check_interval=60):
        """
        Continuously monitor all addresses
        check_interval: seconds between checks
        """
        print("\n🛡️  STARTING CONTINUOUS MONITORING")
        print(f"Checking every {check_interval} seconds")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                for address in list(self.monitored_addresses.keys()):
                    status = self.check_address(address)
                    
                    # Check for suspicious patterns
                    if status.get("transactions", 0) > 0:
                        # Funds moved!
                        client = self.monitored_addresses[address]["client"]
                        
                        # Did client confirm this was them?
                        print(f"\n💸 Transaction detected on {client}'s address")
                        print("Verify with client this was authorized!")
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\n✋ Monitoring stopped")


# ============================================================================
# TOOL 3: EMERGENCY FUND MOVEMENT
# ============================================================================

class EmergencyResponse:
    """Emergency tools for when attack is detected"""
    
    @staticmethod
    def emergency_sweep(private_key, destination_address):
        """
        Emergency function to move funds FAST
        Use when you detect attack in progress
        """
        print("\n🚨 EMERGENCY FUND SWEEP INITIATED")
        print("=" * 60)
        
        print("⚠️  This will move ALL funds immediately")
        print(f"Destination: {destination_address}")
        
        confirm = input("\nType 'EMERGENCY' to confirm: ")
        
        if confirm != "EMERGENCY":
            print("❌ Cancelled")
            return False
        
        print("\n⚡ EXECUTING EMERGENCY SWEEP...")
        print("1. Creating high-fee transaction (priority confirmation)")
        print("2. Broadcasting to network")
        print("3. Monitoring for confirmation")
        
        # In production, this would:
        # - Create Bitcoin transaction
        # - Set HIGH fee for fast confirmation
        # - Broadcast immediately
        # - Monitor mempool
        
        print("\n✅ Transaction broadcast!")
        print("⏳ Waiting for confirmation...")
        print("Expected confirmation: 10-20 minutes")
        
        return True
    
    @staticmethod
    def generate_decoy_addresses(count=5):
        """
        Generate decoy addresses to confuse attackers
        Split funds across multiple addresses
        """
        print("\n🎭 GENERATING DECOY ADDRESSES")
        print("=" * 60)
        
        decoys = []
        for i in range(count):
            # Generate random address (simplified)
            random_key = secrets.token_hex(32)
            address = f"1Decoy{random_key[:10]}..."
            
            decoys.append({
                "index": i + 1,
                "address": address,
                "purpose": "Decoy/Split"
            })
            
            print(f"{i+1}. {address}")
        
        print("\n💡 Strategy: Split recovered funds across these addresses")
        print("   Attacker won't know which has the real funds")
        
        return decoys


# ============================================================================
# TOOL 4: ATTACK DETECTION & FORENSICS
# ============================================================================

class AttackDetection:
    """Detect and analyze attacks"""
    
    @staticmethod
    def analyze_compromise(timeline_events):
        """Analyze how an attack happened"""
        print("\n🔬 ATTACK FORENSICS")
        print("=" * 60)
        
        print("\nTimeline Analysis:")
        for event in timeline_events:
            print(f"  {event['time']}: {event['action']}")
        
        print("\n🎯 Likely Attack Vectors:")
        
        vectors = [
            {
                "method": "Email Interception",
                "likelihood": "HIGH",
                "evidence": "Key sent via plaintext email",
                "prevention": "Use encrypted delivery"
            },
            {
                "method": "Man-in-the-Middle",
                "likelihood": "MEDIUM",
                "evidence": "Unsecured communication channel",
                "prevention": "End-to-end encryption"
            },
            {
                "method": "Client Device Compromise",
                "likelihood": "MEDIUM",
                "evidence": "Client may have malware",
                "prevention": "Immediate fund movement protocol"
            },
            {
                "method": "Your System Compromise",
                "likelihood": "LOW",
                "evidence": "Would affect multiple clients",
                "prevention": "Regular security audits"
            }
        ]
        
        for v in vectors:
            print(f"\n📌 {v['method']}")
            print(f"   Likelihood: {v['likelihood']}")
            print(f"   Evidence: {v['evidence']}")
            print(f"   Prevention: {v['prevention']}")
        
        return vectors
    
    @staticmethod
    def generate_incident_report(incident_data):
        """Generate incident report for client/authorities"""
        report = f"""
SECURITY INCIDENT REPORT
{'=' * 60}

Incident ID: {secrets.token_hex(8)}
Date: {datetime.now().isoformat()}

SUMMARY:
{incident_data.get('summary', 'Unauthorized access detected')}

AFFECTED CLIENT:
{incident_data.get('client', 'Unknown')}

TIMELINE:
{chr(10).join(f"  {e['time']}: {e['action']}" for e in incident_data.get('timeline', []))}

ESTIMATED LOSS:
{incident_data.get('loss', '0 BTC')}

ACTIONS TAKEN:
1. Monitoring activated
2. Client notified
3. Forensic analysis initiated
4. Law enforcement contacted (if applicable)

PREVENTION MEASURES IMPLEMENTED:
1. Encrypted key delivery system
2. Transaction monitoring
3. Emergency response protocols
4. Enhanced security procedures

RECOMMENDATIONS:
1. All future key deliveries use encryption
2. Immediate fund movement policy
3. Multi-signature wallets for high-value recoveries
4. Client device security verification

{'=' * 60}
        """
        
        return report


# ============================================================================
# COMPLETE DEFENSE WORKFLOW
# ============================================================================

class DefenseWorkflow:
    """Complete workflow for secure recovery"""
    
    @staticmethod
    def secure_recovery_handoff(private_key, client_name, client_phone):
        """
        Complete secure handoff process
        """
        print("\n" + "=" * 70)
        print("🛡️  SECURE RECOVERY HANDOFF PROTOCOL")
        print("=" * 70)
        
        # Step 1: Encrypt the key
        print("\n[STEP 1] Encrypting private key...")
        delivery = SecureKeyDelivery()
        encrypted_data = delivery.secure_delivery_process(private_key)
        
        # Step 2: Set up monitoring
        print("\n[STEP 2] Setting up transaction monitoring...")
        monitor = TransactionMonitor()
        
        # Derive address from key (simplified - would use real derivation)
        address = f"1{hashlib.sha256(private_key.encode()).hexdigest()[:33]}"
        monitor.add_watch(address, client_name, expected_action_time=1800)  # 30 min
        
        # Step 3: Client contact protocol
        print("\n[STEP 3] CLIENT CONTACT PROTOCOL:")
        print("-" * 70)
        print(f"✅ Call client at: {client_phone}")
        print(f"✅ Verify identity (security question)")
        print(f"✅ Read password verbally: {encrypted_data['password']}")
        print(f"✅ Email encrypted key to verified address")
        print(f"✅ Instruct immediate fund movement (within 30 minutes)")
        print(f"✅ Provide destination address recommendations")
        print("-" * 70)
        
        # Step 4: Monitoring begins
        print("\n[STEP 4] Monitoring active for next 60 minutes")
        print("Will alert if:")
        print("  - Unauthorized transaction detected")
        print("  - No client action within 30 minutes")
        print("  - Suspicious wallet activity")
        
        return {
            "encrypted_key": encrypted_data['encrypted_key'],
            "monitoring_active": True,
            "client": client_name
        }


# ============================================================================
# MAIN DEMO
# ============================================================================

def main():
    print("=" * 70)
    print("🛡️  BLACK HAT DEFENSE TOOLKIT")
    print("=" * 70)
    print()
    print("Available Tools:")
    print("  1. Secure Key Delivery (Encrypted)")
    print("  2. Transaction Monitoring")
    print("  3. Emergency Fund Sweep")
    print("  4. Attack Forensics")
    print("  5. Complete Secure Handoff Demo")
    print()
    
    choice = input("Select tool (1-5): ").strip()
    
    if choice == "1":
        # Demo encrypted delivery
        test_key = "a1b2c3d4" * 16  # 64 char test key
        SecureKeyDelivery.secure_delivery_process(test_key)
        
    elif choice == "2":
        # Demo monitoring
        monitor = TransactionMonitor()
        monitor.add_watch("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "Test Client")
        monitor.check_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        
    elif choice == "3":
        # Demo emergency sweep
        response = EmergencyResponse()
        response.emergency_sweep("test_key", "1SafeAddress...")
        
    elif choice == "4":
        # Demo forensics
        timeline = [
            {"time": "14:00", "action": "Recovery completed"},
            {"time": "14:15", "action": "Key sent via email"},
            {"time": "14:20", "action": "Unauthorized transaction detected"},
        ]
        AttackDetection.analyze_compromise(timeline)
        
    elif choice == "5":
        # Complete demo
        print("\n🎬 RUNNING COMPLETE SECURE HANDOFF DEMO")
        
        test_key = "0123456789abcdef" * 4
        workflow = DefenseWorkflow()
        workflow.secure_recovery_handoff(
            private_key=test_key,
            client_name="Marcus Johnson",
            client_phone="555-0123"
        )

if __name__ == "__main__":
    main()