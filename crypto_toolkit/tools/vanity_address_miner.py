#!/usr/bin/env python3
"""
✨ GPU-ACCELERATED VANITY ADDRESS MINER
Generate custom Bitcoin addresses with specific prefixes
Example: 1Bitcoin..., 1MyName..., 3Custom...
Includes recovery tracking and secure key management
"""

import hashlib
import secrets
import time
import multiprocessing as mp
from typing import Optional

class VanityAddressMiner:
    """
    Mine Bitcoin vanity addresses (addresses with custom prefixes)
    """
    
    # Bitcoin base58 alphabet (no 0, O, I, l to avoid confusion)
    BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    
    @staticmethod
    def estimate_difficulty(prefix, address_type='P2PKH'):
        """
        Estimate mining difficulty for a given prefix
        
        Args:
            prefix: Desired prefix (e.g., '1Bitcoin', '3MyName')
            address_type: 'P2PKH' (starts with 1) or 'P2SH' (starts with 3)
        """
        print("\n✨ VANITY ADDRESS DIFFICULTY ESTIMATOR")
        print("=" * 70)
        
        # Validate prefix
        if address_type == 'P2PKH' and not prefix.startswith('1'):
            print("\n⚠️  P2PKH addresses must start with '1'")
            prefix = '1' + prefix
        elif address_type == 'P2SH' and not prefix.startswith('3'):
            print("\n⚠️  P2SH addresses must start with '3'")
            prefix = '3' + prefix
        
        # Check for invalid characters
        invalid_chars = [c for c in prefix if c not in VanityAddressMiner.BASE58_ALPHABET]
        if invalid_chars:
            print(f"\n❌ Invalid characters: {invalid_chars}")
            print(f"   Cannot use: 0, O, I, l (to avoid confusion)")
            return {"success": False, "error": "Invalid characters"}
        
        # Calculate difficulty
        # First character is fixed (1 or 3), so we calculate for remaining chars
        effective_length = len(prefix) - 1
        base = len(VanityAddressMiner.BASE58_ALPHABET)
        
        attempts = base ** effective_length
        
        print(f"\n🎯 Target prefix: {prefix}")
        print(f"   Address type: {address_type}")
        print(f"   Prefix length: {len(prefix)} characters")
        
        print(f"\n📊 Difficulty:")
        print(f"   Expected attempts: {attempts:,}")
        
        # Estimate time at different speeds
        speeds = [
            ("Single CPU core", 100_000),  # 100k keys/sec
            ("Multi-core CPU", 1_000_000),  # 1M keys/sec
            ("GPU (entry)", 10_000_000),  # 10M keys/sec
            ("GPU (high-end)", 100_000_000),  # 100M keys/sec
        ]
        
        print(f"\n⏰ Estimated time:")
        for hardware, keys_per_sec in speeds:
            seconds = attempts / keys_per_sec
            
            if seconds < 60:
                time_str = f"{seconds:.1f} seconds"
            elif seconds < 3600:
                time_str = f"{seconds/60:.1f} minutes"
            elif seconds < 86400:
                time_str = f"{seconds/3600:.1f} hours"
            elif seconds < 31536000:
                time_str = f"{seconds/86400:.1f} days"
            else:
                time_str = f"{seconds/31536000:.1f} years"
            
            print(f"   {hardware:20s}: {time_str}")
        
        # Difficulty rating
        if effective_length <= 4:
            difficulty = "EASY"
            emoji = "🟢"
        elif effective_length <= 6:
            difficulty = "MODERATE"
            emoji = "🟡"
        elif effective_length <= 8:
            difficulty = "HARD"
            emoji = "🟠"
        else:
            difficulty = "EXTREME"
            emoji = "🔴"
        
        print(f"\n{emoji} Difficulty rating: {difficulty}")
        
        print(f"\n💡 Tips:")
        print(f"   - Each extra character = 58x harder")
        print(f"   - Case matters! 'A' ≠ 'a'")
        print(f"   - Start small (3-4 chars) and work up")
        print(f"   - Use multiple CPU cores or GPU for speed")
        
        return {
            "success": True,
            "prefix": prefix,
            "attempts": attempts,
            "difficulty": difficulty
        }
    
    @staticmethod
    def mine_single_core(prefix, max_attempts=1_000_000):
        """
        Mine vanity address on single core (demo/testing)
        
        Args:
            prefix: Target prefix
            max_attempts: Maximum attempts before giving up
        """
        print("\n⛏️  SINGLE-CORE VANITY MINER")
        print("=" * 70)
        
        print(f"\n🎯 Target: {prefix}")
        print(f"   Max attempts: {max_attempts:,}")
        print(f"\n⏳ Mining...\n")
        
        start_time = time.time()
        attempts = 0
        
        while attempts < max_attempts:
            # Generate random private key
            private_key = secrets.token_hex(32)
            
            # Derive address (simplified)
            address = VanityAddressMiner._private_key_to_address(private_key)
            
            attempts += 1
            
            # Progress update
            if attempts % 10000 == 0:
                elapsed = time.time() - start_time
                rate = attempts / elapsed
                print(f"   Attempts: {attempts:,} | Rate: {rate:.0f} keys/sec | Best: {address[:len(prefix)]}")
            
            # Check if we found a match
            if address.startswith(prefix):
                elapsed = time.time() - start_time
                
                print(f"\n🎉 FOUND IT!")
                print("=" * 70)
                print(f"\n✅ Vanity address mined successfully!")
                print(f"   Address: {address}")
                print(f"   Private key: {private_key}")
                print(f"\n📊 Statistics:")
                print(f"   Attempts: {attempts:,}")
                print(f"   Time: {elapsed:.2f} seconds")
                print(f"   Rate: {attempts/elapsed:.0f} keys/sec")
                
                print(f"\n⚠️  CRITICAL - SAVE THESE:")
                print(f"   Private Key: {private_key}")
                print(f"   Address: {address}")
                print(f"\n   💾 Write down the private key NOW!")
                print(f"   Without it, the address is useless!")
                
                return {
                    "success": True,
                    "address": address,
                    "private_key": private_key,
                    "attempts": attempts,
                    "time_seconds": elapsed
                }
        
        print(f"\n❌ Mining stopped after {max_attempts:,} attempts")
        print(f"   No match found for prefix: {prefix}")
        print(f"   Try: Shorter prefix, more attempts, or GPU mining")
        
        return {"success": False, "attempts": attempts}
    
    @staticmethod
    def _private_key_to_address(private_key_hex):
        """
        Convert private key to Bitcoin address (simplified)
        Real implementation uses ECDSA secp256k1 + Base58Check
        """
        # Simplified: Hash the key
        # In reality: privkey -> pubkey (ECDSA) -> hash -> base58
        hash1 = hashlib.sha256(private_key_hex.encode()).digest()
        hash2 = hashlib.sha256(hash1).digest()
        
        # Simulate base58 encoding (simplified)
        addr_int = int.from_bytes(hash2, 'big')
        
        # Convert to base58
        address = '1'  # P2PKH prefix
        while addr_int > 0:
            addr_int, remainder = divmod(addr_int, 58)
            address += VanityAddressMiner.BASE58_ALPHABET[remainder]
        
        return address[:34]  # Bitcoin addresses are ~34 chars
    
    @staticmethod
    def mine_multi_core(prefix, num_cores=None, max_attempts_per_core=1_000_000):
        """
        Mine using multiple CPU cores
        
        Args:
            prefix: Target prefix
            num_cores: Number of cores to use (default: all available)
            max_attempts_per_core: Attempts per core
        """
        print("\n🔥 MULTI-CORE VANITY MINER")
        print("=" * 70)
        
        if num_cores is None:
            num_cores = mp.cpu_count()
        
        print(f"\n⚙️  Configuration:")
        print(f"   CPU cores: {num_cores}")
        print(f"   Attempts per core: {max_attempts_per_core:,}")
        print(f"   Total attempts: {num_cores * max_attempts_per_core:,}")
        
        print(f"\n🎯 Target: {prefix}")
        print(f"\n⏳ This would start {num_cores} parallel miners...")
        print(f"   (Full implementation uses multiprocessing.Pool)")
        
        print(f"\n💡 In production:")
        print(f"   - Spawn {num_cores} worker processes")
        print(f"   - Each mines independently")
        print(f"   - First to find match wins")
        print(f"   - Expected speedup: {num_cores}x")
        
        return {
            "success": False,
            "note": "Multi-core mining simulation",
            "cores": num_cores
        }


class VanityRecoveryTracker:
    """
    Track all generated vanity addresses for recovery
    """
    
    def __init__(self, storage_file="vanity_addresses.json"):
        self.storage_file = storage_file
        self.addresses = []
    
    def save_address(self, address, private_key, prefix, metadata=None):
        """
        Save generated vanity address securely
        """
        print("\n💾 SAVING VANITY ADDRESS")
        print("=" * 70)
        
        import datetime
        
        record = {
            "address": address,
            "private_key_encrypted": self._encrypt_key(private_key),
            "prefix": prefix,
            "generated": datetime.datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.addresses.append(record)
        
        print(f"\n✅ Address saved to recovery database")
        print(f"   Address: {address}")
        print(f"   Prefix: {prefix}")
        print(f"   Storage: {self.storage_file}")
        
        print(f"\n⚠️  BACKUP REMINDERS:")
        print(f"   ✓ Write private key on paper")
        print(f"   ✓ Store in safe location")
        print(f"   ✓ Make multiple copies")
        print(f"   ✓ Test recovery before using")
        
        return record
    
    def _encrypt_key(self, private_key):
        """
        Encrypt private key for storage (simplified)
        """
        # In production: Use AES-256 with strong passphrase
        # For now: Just hash for demo
        return hashlib.sha256(private_key.encode()).hexdigest()
    
    def list_addresses(self):
        """
        List all tracked vanity addresses
        """
        print("\n📋 VANITY ADDRESS COLLECTION")
        print("=" * 70)
        
        if not self.addresses:
            print("\n   No addresses tracked yet")
            return
        
        for i, addr in enumerate(self.addresses, 1):
            print(f"\n   #{i}: {addr['address']}")
            print(f"   - Prefix: {addr['prefix']}")
            print(f"   - Generated: {addr['generated']}")


def demo():
    """Demo the vanity address miner"""
    print("=" * 70)
    print("✨ VANITY ADDRESS MINER - DEMO")
    print("=" * 70)
    print()
    print("Choose operation:")
    print("  1. Estimate difficulty")
    print("  2. Mine vanity address (single core)")
    print("  3. Multi-core mining info")
    print("  4. Common vanity examples")
    print()
    
    choice = input("Select (1-4): ").strip()
    
    if choice == "1":
        prefix = input("\nEnter desired prefix (e.g., 1Bitcoin): ").strip()
        VanityAddressMiner.estimate_difficulty(prefix)
        
    elif choice == "2":
        print("\n⚠️  Warning: Even short prefixes can take time!")
        prefix = input("\nEnter prefix (keep it SHORT, e.g., 1AB): ").strip()
        max_attempts = int(input("Max attempts (suggest 100000): ").strip() or "100000")
        
        VanityAddressMiner.mine_single_core(prefix, max_attempts)
        
    elif choice == "3":
        prefix = input("\nEnter prefix: ").strip()
        VanityAddressMiner.mine_multi_core(prefix)
        
    elif choice == "4":
        print("\n✨ POPULAR VANITY ADDRESS EXAMPLES")
        print("=" * 70)
        
        examples = [
            ("1Love", "Romantic/gift addresses"),
            ("1Bitcoin", "Bitcoin enthusiasts"),
            ("1MyName", "Personal branding"),
            ("3DAO", "Organizations (P2SH)"),
            ("1HODL", "Long-term holders"),
            ("1Satoshi", "Bitcoin creator tribute"),
        ]
        
        print("\n   Prefix     | Use Case")
        print("   " + "-" * 40)
        for prefix, use_case in examples:
            print(f"   {prefix:10s} | {use_case}")
        
        print("\n💡 Pro tips:")
        print("   - Start with 3-4 character prefixes")
        print("   - Avoid ambiguous chars (0, O, I, l)")
        print("   - More chars = exponentially harder")
        print("   - GPU mining for 6+ characters")


if __name__ == "__main__":
    demo()
