#!/usr/bin/env python3
"""
🔧 MODULAR BITCOIN RECOVERY TOOLKIT
Personal Memory Reconstruction & Blockchain Forensics

Building modular tools for legitimate recovery and research.
Each tool is standalone but works together as a system.
"""

import hashlib
import itertools
import os
import re
import json
from pathlib import Path
from datetime import datetime

# ============================================================================
# MODULE 1: MNEMONIC REBUILDER
# ============================================================================

class MnemonicRebuilder:
    """
    Reconstruct partial or forgotten seed phrases using linguistic modeling
    and entropy scoring.
    """
    
    # BIP39 wordlist (partial - full list has 2048 words)
    BIP39_WORDLIST = [
        "abandon", "ability", "able", "about", "above", "absent", "absorb",
        "abstract", "absurd", "abuse", "access", "accident", "account",
        "accuse", "achieve", "acid", "acoustic", "acquire", "across", "act",
        "action", "actor", "actress", "actual", "adapt", "add", "addict",
        "address", "adjust", "admit", "adult", "advance", "advice", "aerobic",
        "affair", "afford", "afraid", "again", "age", "agent", "agree", "ahead",
        "aim", "air", "airport", "aisle", "alarm", "album", "alcohol", "alert",
        "alien", "all", "alley", "allow", "almost", "alone", "alpha", "already",
        "also", "alter", "always", "amateur", "amazing", "among", "amount",
        "amused", "analyst", "anchor", "ancient", "anger", "angle", "angry",
        "animal", "ankle", "announce", "annual", "another", "answer", "antenna",
        "antique", "anxiety", "any", "apart", "apology", "appear", "apple",
        "approve", "april", "arch", "arctic", "area", "arena", "argue", "arm",
        "armed", "armor", "army", "around", "arrange", "arrest", "arrive",
        "arrow", "art", "artefact", "artist", "artwork", "ask", "aspect",
        "assault", "asset", "assist", "assume", "asthma", "athlete", "atom",
        "attack", "attend", "attitude", "attract", "auction", "audit", "august",
        "aunt", "author", "auto", "autumn", "average", "avocado", "avoid",
        "awake", "aware", "away", "awesome", "awful", "awkward", "axis",
        # ... (truncated for space)
    ]
    
    @staticmethod
    def find_similar_words(partial_word):
        """
        Find BIP39 words that match partial input
        """
        matches = []
        partial_lower = partial_word.lower()
        
        for word in MnemonicRebuilder.BIP39_WORDLIST:
            # Exact match
            if word == partial_lower:
                matches.append({"word": word, "confidence": 1.0, "type": "exact"})
            # Starts with
            elif word.startswith(partial_lower):
                matches.append({"word": word, "confidence": 0.8, "type": "prefix"})
            # Contains
            elif partial_lower in word:
                matches.append({"word": word, "confidence": 0.5, "type": "contains"})
        
        return matches
    
    @staticmethod
    def rebuild_from_fragments(known_words, missing_positions, theme_hints=None):
        """
        Rebuild seed phrase from partial information
        
        Args:
            known_words: dict {position: word}
            missing_positions: list of positions with missing words
            theme_hints: optional list of theme words for context
        """
        print("\n🧩 MNEMONIC REBUILDER")
        print("=" * 60)
        
        print(f"\nKnown words: {len(known_words)}")
        print(f"Missing positions: {len(missing_positions)}")
        
        # Show what we have
        total_positions = max(list(known_words.keys()) + missing_positions) + 1
        
        print(f"\nPhrase structure ({total_positions} words):")
        for i in range(total_positions):
            if i in known_words:
                print(f"  {i+1:2d}. ✅ {known_words[i]}")
            else:
                print(f"  {i+1:2d}. ❓ [unknown]")
        
        # Calculate combinations
        if len(missing_positions) <= 3:
            combinations = 2048 ** len(missing_positions)
            print(f"\n🎯 Combinations to test: {combinations:,}")
            
            if combinations < 10000:
                print("✅ Feasible to brute force")
            elif combinations < 1000000:
                print("⚠️  Moderate difficulty - may take hours")
            else:
                print("❌ Too many combinations - need more words")
        else:
            print(f"\n❌ Too many missing words ({len(missing_positions)})")
            print("   Need to remember at least 1-2 more")
        
        # If theme hints provided, suggest likely words
        if theme_hints:
            print(f"\n💡 Based on themes: {', '.join(theme_hints)}")
            print("   Suggested words:")
            
            suggestions = []
            for theme in theme_hints:
                matches = MnemonicRebuilder.find_similar_words(theme)
                suggestions.extend([m['word'] for m in matches[:3]])
            
            for word in set(suggestions[:10]):
                print(f"   - {word}")
        
        return {
            "total_positions": total_positions,
            "known_count": len(known_words),
            "missing_count": len(missing_positions),
            "feasibility": "HIGH" if len(missing_positions) <= 2 else "LOW"
        }
    
    @staticmethod
    def validate_checksum(words):
        """
        Validate BIP39 checksum (simplified - real implementation uses SHA256)
        """
        # In production: decode words, verify checksum bits
        # For now: basic validation
        return len(words) in [12, 15, 18, 21, 24]


# ============================================================================
# MODULE 2: WALLET SCANNER
# ============================================================================

class WalletScanner:
    """
    Scan addresses or patterns across blockchain for balances and activity
    """
    
    def __init__(self):
        self.checked_addresses = []
        self.results = []
    
    def check_address_pattern(self, pattern, limit=10):
        """
        Check addresses matching a pattern
        
        Args:
            pattern: Address pattern (e.g., "1Bitcoin*")
            limit: Max addresses to check
        """
        print("\n🔍 WALLET SCANNER")
        print("=" * 60)
        print(f"Pattern: {pattern}")
        print(f"Checking up to {limit} addresses...")
        
        # In production: generate addresses from pattern
        # Here: demonstrate concept
        
        print("\nGenerating addresses from pattern...")
        addresses = self._generate_pattern_addresses(pattern, limit)
        
        results = []
        for i, addr in enumerate(addresses, 1):
            print(f"\n[{i}/{limit}] {addr}")
            
            # In production: actual blockchain API call
            # Here: simulated check
            balance = self._check_balance(addr)
            tx_count = self._check_transactions(addr)
            
            result = {
                "address": addr,
                "balance": balance,
                "transactions": tx_count,
                "active": tx_count > 0
            }
            
            results.append(result)
            
            if balance > 0:
                print(f"  💰 Balance: {balance} BTC")
            if tx_count > 0:
                print(f"  📊 Transactions: {tx_count}")
        
        return results
    
    def _generate_pattern_addresses(self, pattern, limit):
        """Generate addresses from pattern"""
        # Simplified: in reality would use proper address derivation
        addresses = []
        for i in range(limit):
            addr = pattern.replace("*", str(i).zfill(3))
            addresses.append(addr)
        return addresses
    
    def _check_balance(self, address):
        """Check balance (simulated - use real API in production)"""
        # In production: blockchain.info API or similar
        return 0.0
    
    def _check_transactions(self, address):
        """Check transaction count (simulated)"""
        return 0
    
    def scan_known_addresses(self, address_list):
        """
        Batch scan a list of known addresses
        """
        print("\n📋 BATCH ADDRESS SCAN")
        print("=" * 60)
        print(f"Scanning {len(address_list)} addresses...\n")
        
        results = []
        for addr in address_list:
            result = {
                "address": addr,
                "balance": self._check_balance(addr),
                "transactions": self._check_transactions(addr)
            }
            results.append(result)
        
        # Summary
        total_balance = sum(r['balance'] for r in results)
        active_count = sum(1 for r in results if r['transactions'] > 0)
        
        print(f"\n📊 SUMMARY:")
        print(f"  Total addresses: {len(results)}")
        print(f"  Active addresses: {active_count}")
        print(f"  Total balance: {total_balance} BTC")
        
        return results


# ============================================================================
# MODULE 3: ENTROPY SANDBOX
# ============================================================================

class EntropySandbox:
    """
    Local testbed for testing phrase permutations against wallet files
    or public addresses without triggering alarms.
    """
    
    def __init__(self):
        self.test_results = []
    
    def test_phrase_variations(self, base_phrase, variations):
        """
        Test variations of a phrase locally
        
        Args:
            base_phrase: The base phrase to vary
            variations: List of variation strategies
        """
        print("\n🧪 ENTROPY SANDBOX")
        print("=" * 60)
        print(f"Base phrase: '{base_phrase}'")
        print(f"Testing {len(variations)} variation strategies...\n")
        
        candidates = self._generate_variations(base_phrase, variations)
        
        print(f"Generated {len(candidates)} candidate phrases")
        print("\nTesting each candidate...")
        
        results = []
        for i, candidate in enumerate(candidates[:20], 1):  # Limit for demo
            key = self._phrase_to_key(candidate)
            address = self._key_to_address(key)
            
            result = {
                "phrase": candidate,
                "key": key[:16] + "...",
                "address": address,
                "tested": True
            }
            
            results.append(result)
            
            if i <= 5:  # Show first 5
                print(f"{i}. '{candidate}' → {address}")
        
        print(f"\n... and {len(candidates) - 5} more variations")
        
        return results
    
    def _generate_variations(self, base, strategies):
        """Generate phrase variations"""
        variations = [base]
        
        for strategy in strategies:
            if strategy == "lowercase":
                variations.append(base.lower())
            elif strategy == "uppercase":
                variations.append(base.upper())
            elif strategy == "title":
                variations.append(base.title())
            elif strategy == "nospace":
                variations.append(base.replace(" ", ""))
            elif strategy == "numbers":
                # Try appending common numbers
                for num in ["123", "2024", "1", "0"]:
                    variations.append(base + num)
        
        return list(set(variations))  # Remove duplicates
    
    def _phrase_to_key(self, phrase):
        """Convert phrase to key (brain wallet style)"""
        return hashlib.sha256(phrase.encode()).hexdigest()
    
    def _key_to_address(self, key):
        """Convert key to address (simplified)"""
        # In production: proper ECDSA + Base58Check
        addr_hash = hashlib.sha256(key.encode()).hexdigest()[:33]
        return f"1{addr_hash}"
    
    def test_against_target(self, phrases, target_address):
        """
        Test if any phrase generates target address
        """
        print(f"\n🎯 Testing {len(phrases)} phrases against target")
        print(f"Target: {target_address}\n")
        
        for i, phrase in enumerate(phrases, 1):
            key = self._phrase_to_key(phrase)
            addr = self._key_to_address(key)
            
            if addr == target_address:
                print(f"✅ MATCH FOUND at position {i}!")
                print(f"   Phrase: '{phrase}'")
                return {"found": True, "phrase": phrase, "position": i}
        
        print("❌ No matches found")
        return {"found": False}


# ============================================================================
# MODULE 4: METADATA MINER
# ============================================================================

class MetadataMiner:
    """
    Scan local files for anything that smells like keys, addresses, or
    wallet-related data.
    """
    
    def __init__(self):
        self.findings = []
    
    def scan_directory(self, path, file_types=None):
        """
        Scan directory for crypto-related metadata
        
        Args:
            path: Directory to scan
            file_types: List of file extensions to check (None = all text files)
        """
        print("\n🔬 METADATA MINER")
        print("=" * 60)
        print(f"Scanning: {path}\n")
        
        if file_types is None:
            file_types = ['.txt', '.json', '.log', '.md', '.csv', '.dat']
        
        findings = []
        scan_path = Path(path)
        
        if not scan_path.exists():
            print(f"❌ Path does not exist: {path}")
            return []
        
        # Scan files
        file_count = 0
        for file_path in scan_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in file_types:
                file_count += 1
                results = self._scan_file(file_path)
                findings.extend(results)
        
        print(f"\n📊 SCAN COMPLETE")
        print(f"  Files scanned: {file_count}")
        print(f"  Potential findings: {len(findings)}")
        
        if findings:
            print("\n🎯 FINDINGS:")
            for finding in findings[:10]:  # Show first 10
                print(f"\n  File: {finding['file']}")
                print(f"  Type: {finding['type']}")
                print(f"  Content: {finding['content'][:50]}...")
        
        return findings
    
    def _scan_file(self, file_path):
        """Scan individual file for crypto patterns"""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Pattern matching
            patterns = {
                "bitcoin_address": r'1[A-HJ-NP-Za-km-z1-9]{25,34}',
                "hex_key": r'[0-9a-fA-F]{64}',
                "seed_word": r'\b(' + '|'.join(MnemonicRebuilder.BIP39_WORDLIST[:50]) + r')\b',
                "private_key_label": r'(private[_\s]key|priv[_\s]key|secret)',
            }
            
            for pattern_name, pattern in patterns.items():
                matches = re.findall(pattern, content)
                
                for match in matches:
                    findings.append({
                        "file": str(file_path),
                        "type": pattern_name,
                        "content": match if isinstance(match, str) else match[0]
                    })
        
        except Exception as e:
            pass  # Skip files that can't be read
        
        return findings
    
    def scan_for_wallet_files(self, path):
        """Find common wallet file types"""
        print("\n💼 WALLET FILE SCANNER")
        print("=" * 60)
        
        wallet_patterns = [
            'wallet.dat',
            '*.wallet',
            'bitcoin.conf',
            'electrum*',
            '*.aes.json',
        ]
        
        found_wallets = []
        scan_path = Path(path)
        
        for pattern in wallet_patterns:
            matches = list(scan_path.rglob(pattern))
            found_wallets.extend(matches)
        
        print(f"Found {len(found_wallets)} potential wallet files:\n")
        for wallet in found_wallets:
            print(f"  📄 {wallet}")
        
        return found_wallets


# ============================================================================
# MAIN INTERFACE
# ============================================================================

def main():
    print("=" * 70)
    print("🔧 MODULAR BITCOIN RECOVERY TOOLKIT")
    print("=" * 70)
    print("\nPersonal Memory Reconstruction & Blockchain Forensics")
    print("Each tool is legitimate on its own. Together, they're a system.\n")
    
    print("Available Modules:")
    print("  1. Mnemonic Rebuilder - Reconstruct partial seed phrases")
    print("  2. Wallet Scanner - Check addresses for balances/activity")
    print("  3. Entropy Sandbox - Test phrase variations locally")
    print("  4. Metadata Miner - Scan files for wallet clues")
    print("  5. Run Demo (All Modules)")
    print()
    
    choice = input("Select module (1-5): ").strip()
    
    if choice == "1":
        print("\n" + "="*70)
        print("MNEMONIC REBUILDER DEMO")
        print("="*70)
        
        # Example: User remembers 10 of 12 words
        known = {
            0: "abandon", 1: "ability", 2: "able",
            3: "about", 4: "above", 5: "absent",
            6: "absorb", 7: "abstract", 
            # Missing positions 8, 9
            10: "access", 11: "accident"
        }
        missing = [8, 9]
        
        rebuilder = MnemonicRebuilder()
        rebuilder.rebuild_from_fragments(known, missing, theme_hints=["abuse", "account"])
    
    elif choice == "2":
        scanner = WalletScanner()
        
        # Demo: Check a pattern
        scanner.check_address_pattern("1Bitcoin*", limit=5)
    
    elif choice == "3":
        sandbox = EntropySandbox()
        
        # Demo: Test variations
        variations = ["lowercase", "uppercase", "numbers"]
        sandbox.test_phrase_variations("MyPassword", variations)
    
    elif choice == "4":
        miner = MetadataMiner()
        
        # Demo: Scan current directory
        print("\nEnter directory to scan (or '.' for current):")
        scan_dir = input("> ").strip() or "."
        
        miner.scan_directory(scan_dir)
    
    elif choice == "5":
        print("\n🎬 RUNNING COMPLETE DEMO\n")
        
        # Module 1: Mnemonic Rebuilder
        print("="*70)
        print("MODULE 1: MNEMONIC REBUILDER")
        print("="*70)
        known = {0: "abandon", 1: "ability", 10: "access", 11: "accident"}
        missing = [2, 3, 4, 5, 6, 7, 8, 9]
        MnemonicRebuilder().rebuild_from_fragments(known, missing)
        
        input("\nPress Enter to continue...")
        
        # Module 2: Wallet Scanner
        print("\n" + "="*70)
        print("MODULE 2: WALLET SCANNER")
        print("="*70)
        WalletScanner().check_address_pattern("1Demo*", limit=3)
        
        input("\nPress Enter to continue...")
        
        # Module 3: Entropy Sandbox
        print("\n" + "="*70)
        print("MODULE 3: ENTROPY SANDBOX")
        print("="*70)
        EntropySandbox().test_phrase_variations("test", ["lowercase", "numbers"])
        
        input("\nPress Enter to continue...")
        
        # Module 4: Metadata Miner
        print("\n" + "="*70)
        print("MODULE 4: METADATA MINER")
        print("="*70)
        print("(Skipping file scan in demo)")
        
        print("\n" + "="*70)
        print("✅ ALL MODULES DEMONSTRATED")
        print("="*70)

if __name__ == "__main__":
    main()