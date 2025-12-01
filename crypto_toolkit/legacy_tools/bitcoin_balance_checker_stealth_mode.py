#!/usr/bin/env python3
"""
💰 BITCOIN BALANCE CHECKER - Stealth Mode
Check addresses for balances without rate limits
"""

import hashlib
import requests
import time

class BitcoinBalanceChecker:
    """Check Bitcoin addresses for balances"""
    
    def __init__(self):
        # Multiple free endpoints (rotate if one fails)
        self.endpoints = [
            "https://blockchain.info/q/addressbalance/",
            "https://blockstream.info/api/address/",
        ]
    
    def private_key_to_address(self, private_key_hex):
        """Convert private key to Bitcoin address (simplified)"""
        # This is a SIMPLIFIED version - real implementation needs:
        # - ECDSA secp256k1 for pubkey generation
        # - Base58Check encoding
        # - Proper Bitcoin address derivation
        
        # For now, just hash it (NOT A REAL ADDRESS - placeholder)
        fake_addr = "1" + hashlib.sha256(private_key_hex.encode()).hexdigest()[:33]
        return fake_addr
    
    def check_balance(self, address):
        """Check balance of Bitcoin address"""
        try:
            # Try blockchain.info
            url = f"https://blockchain.info/q/addressbalance/{address}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                satoshis = int(response.text)
                btc = satoshis / 100000000
                return {
                    "address": address,
                    "balance_btc": btc,
                    "balance_satoshis": satoshis,
                    "has_funds": btc > 0
                }
        except:
            pass
        
        return {
            "address": address,
            "error": "Could not fetch balance",
            "has_funds": None
        }
    
    def batch_check(self, addresses, delay=0.5):
        """Check multiple addresses (with politeness delay)"""
        results = []
        
        for i, addr in enumerate(addresses, 1):
            print(f"Checking {i}/{len(addresses)}: {addr[:10]}...")
            result = self.check_balance(addr)
            results.append(result)
            
            if result.get("has_funds"):
                print(f"  💰 FOUND: {result['balance_btc']} BTC")
            
            time.sleep(delay)  # Be nice to free APIs
        
        return results
    
    def check_recovered_keys(self, key_candidates):
        """Check if recovered keys have any funds"""
        print("🔍 Checking recovered keys for balances...")
        print("⚠️  Note: Need proper key→address conversion for real use")
        
        hits = []
        
        for key in key_candidates[:10]:  # Limit for demo
            # In real use, convert key to address properly
            addr = self.private_key_to_address(key)
            result = self.check_balance(addr)
            
            if result.get("has_funds"):
                hits.append(result)
        
        return hits


# ============================================================================
# BONUS: Pattern-based key generator
# ============================================================================

class PatternKeyGenerator:
    """Generate keys based on patterns people commonly use"""
    
    @staticmethod
    def generate_weak_keys():
        """Generate commonly used weak patterns"""
        patterns = []
        
        # Repeating patterns
        for char in "0123456789abcdef":
            patterns.append(char * 64)
        
        # Sequential
        patterns.append("0123456789abcdef" * 4)
        
        # Common hex strings
        patterns.append("deadbeef" * 8)
        patterns.append("cafebabe" * 8)
        patterns.append("00000000" * 8)
        patterns.append("ffffffff" * 8)
        
        # Birthday-based (people use birthdays as entropy)
        for year in range(1970, 2000):
            for month in range(1, 13):
                base = f"{year}{month:02d}"
                # Pad to 64 chars
                key = (base * 10)[:64]
                patterns.append(key)
        
        return patterns


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("💰 BITCOIN BALANCE CHECKER - Stealth Mode")
    print("=" * 70)
    print()
    
    checker = BitcoinBalanceChecker()
    
    print("What do you want to do?")
    print("  1. Check a specific address")
    print("  2. Check multiple addresses from file")
    print("  3. Generate weak pattern keys (research)")
    print()
    
    choice = input("Select (1-3): ").strip()
    
    if choice == "1":
        addr = input("\nEnter Bitcoin address: ").strip()
        result = checker.check_balance(addr)
        
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"\n{'💰' if result['has_funds'] else '📭'} Address: {result['address']}")
            print(f"Balance: {result['balance_btc']} BTC ({result['balance_satoshis']} satoshis)")
    
    elif choice == "2":
        filename = input("\nEnter filename (one address per line): ").strip()
        try:
            with open(filename, 'r') as f:
                addresses = [line.strip() for line in f if line.strip()]
            
            print(f"\n🔍 Checking {len(addresses)} addresses...")
            results = checker.batch_check(addresses)
            
            funded = [r for r in results if r.get('has_funds')]
            print(f"\n✅ Found {len(funded)} addresses with funds!")
            
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found")
    
    elif choice == "3":
        print("\n🎲 Generating weak pattern keys...")
        patterns = PatternKeyGenerator.generate_weak_keys()
        
        print(f"Generated {len(patterns)} weak patterns")
        print("\nFirst 5 examples:")
        for p in patterns[:5]:
            print(f"  {p}")
        
        check = input("\nCheck these for balances? (y/n): ").strip().lower()
        if check == 'y':
            print("⚠️  This would check if anyone actually used these weak keys...")
            print("(Disabled in demo - would need proper key→address conversion)")

if __name__ == "__main__":
    main()