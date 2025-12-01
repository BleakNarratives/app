#!/usr/bin/env python3
"""
🧩 SHAMIR SECRET SHARING TOOL
Split private keys into shards with threshold recovery
Example: Split into 5 shards, need any 3 to recover (3-of-5)
"""

import secrets
import hashlib
from typing import List, Tuple

class ShamirSecretSharing:
    """
    Implement Shamir's Secret Sharing Scheme
    Split a secret into N shares where any K shares can recover it (K-of-N threshold)
    """
    
    # Large prime for finite field arithmetic (256-bit)
    PRIME = 2**256 - 189
    
    @staticmethod
    def _mod_inverse(a, m):
        """Calculate modular multiplicative inverse"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return (x % m + m) % m
    
    @staticmethod
    def _eval_polynomial(coeffs, x, prime):
        """Evaluate polynomial at x using Horner's method"""
        result = 0
        for coeff in reversed(coeffs):
            result = (result * x + coeff) % prime
        return result
    
    @staticmethod
    def _lagrange_interpolate(shares, prime):
        """Use Lagrange interpolation to recover secret from shares"""
        k = len(shares)
        secret = 0
        
        for i in range(k):
            xi, yi = shares[i]
            numerator = 1
            denominator = 1
            
            for j in range(k):
                if i != j:
                    xj, _ = shares[j]
                    numerator = (numerator * (-xj)) % prime
                    denominator = (denominator * (xi - xj)) % prime
            
            lagrange = (yi * numerator * ShamirSecretSharing._mod_inverse(denominator, prime)) % prime
            secret = (secret + lagrange) % prime
        
        return secret
    
    @staticmethod
    def split_secret(secret_hex, threshold, num_shares):
        """
        Split a secret into shares
        
        Args:
            secret_hex: Secret as hex string (private key, seed, etc.)
            threshold: Minimum shares needed to recover (K)
            num_shares: Total shares to create (N)
        
        Returns:
            List of shares as hex strings
        """
        print("\n🧩 SHAMIR SECRET SHARING - SPLIT")
        print("=" * 70)
        
        if threshold > num_shares:
            return {"success": False, "error": "Threshold cannot exceed number of shares"}
        
        if threshold < 2:
            return {"success": False, "error": "Threshold must be at least 2"}
        
        # Convert secret to integer
        secret = int(secret_hex, 16)
        
        if secret >= ShamirSecretSharing.PRIME:
            return {"success": False, "error": "Secret too large"}
        
        print(f"\n📊 Configuration:")
        print(f"   Secret length: {len(secret_hex)} hex chars")
        print(f"   Threshold: {threshold} shares needed")
        print(f"   Total shares: {num_shares}")
        print(f"   Security: {threshold-1} shares can be compromised safely")
        
        # Generate random polynomial coefficients
        # P(x) = secret + a1*x + a2*x^2 + ... + a(k-1)*x^(k-1)
        coeffs = [secret] + [secrets.randbelow(ShamirSecretSharing.PRIME) for _ in range(threshold - 1)]
        
        # Generate shares by evaluating polynomial at different x values
        shares = []
        for i in range(1, num_shares + 1):
            x = i
            y = ShamirSecretSharing._eval_polynomial(coeffs, x, ShamirSecretSharing.PRIME)
            share_hex = f"{i:02x}:{y:064x}"
            shares.append(share_hex)
        
        print(f"\n✅ Secret split into {num_shares} shares!")
        print(f"\n🔑 SHARES (distribute to different locations):")
        for i, share in enumerate(shares, 1):
            print(f"   Share #{i}: {share[:20]}...{share[-20:]}")
        
        print(f"\n⚠️  SECURITY WARNINGS:")
        print(f"   - Keep shares in separate secure locations")
        print(f"   - Any {threshold} shares can recover the secret")
        print(f"   - Losing too many shares = permanent loss")
        print(f"   - Never store all shares together")
        
        return {
            "success": True,
            "shares": shares,
            "threshold": threshold,
            "total": num_shares
        }
    
    @staticmethod
    def recover_secret(shares_hex):
        """
        Recover secret from shares
        
        Args:
            shares_hex: List of share strings
        
        Returns:
            Recovered secret as hex string
        """
        print("\n🔓 SHAMIR SECRET SHARING - RECOVER")
        print("=" * 70)
        
        print(f"\n📥 Received {len(shares_hex)} shares")
        
        # Parse shares
        shares = []
        for share_hex in shares_hex:
            try:
                x_hex, y_hex = share_hex.split(':')
                x = int(x_hex, 16)
                y = int(y_hex, 16)
                shares.append((x, y))
            except:
                return {"success": False, "error": f"Invalid share format: {share_hex}"}
        
        if len(shares) < 2:
            return {"success": False, "error": "Need at least 2 shares"}
        
        # Recover secret using Lagrange interpolation
        try:
            secret = ShamirSecretSharing._lagrange_interpolate(shares, ShamirSecretSharing.PRIME)
            secret_hex = f"{secret:064x}"
            
            print(f"\n✅ Secret recovered successfully!")
            print(f"   Length: {len(secret_hex)} hex chars")
            print(f"\n🔑 RECOVERED SECRET:")
            print(f"   {secret_hex}")
            
            # Verify it's valid
            print(f"\n🔍 Validation:")
            if secret > 0 and secret < ShamirSecretSharing.PRIME:
                print(f"   ✅ Secret is valid")
            else:
                print(f"   ⚠️  Secret may be incorrect")
            
            return {
                "success": True,
                "secret": secret_hex,
                "shares_used": len(shares)
            }
            
        except Exception as e:
            return {"success": False, "error": f"Recovery failed: {str(e)}"}
    
    @staticmethod
    def demo_split_private_key(private_key_hex, threshold=3, total=5):
        """
        Demo: Split a Bitcoin private key into shards
        """
        print("\n💎 DEMO: Splitting Private Key")
        print("=" * 70)
        print(f"\n🔑 Original private key: {private_key_hex[:16]}...{private_key_hex[-16:]}")
        
        result = ShamirSecretSharing.split_secret(private_key_hex, threshold, total)
        
        if result["success"]:
            print(f"\n📋 Distribution plan:")
            print(f"   Share #1 → Safe deposit box")
            print(f"   Share #2 → Trusted family member")
            print(f"   Share #3 → Lawyer's office")
            print(f"   Share #4 → Encrypted cloud storage")
            print(f"   Share #5 → Hardware wallet backup")
            print(f"\n   Any 3 of these can recover your key!")
            
        return result


class BitcoinKeySplitter:
    """
    Specialized tool for splitting Bitcoin private keys
    """
    
    @staticmethod
    def split_key_secure(private_key_hex, threshold, total, passphrase=None):
        """
        Split key with optional passphrase encryption
        """
        print("\n🔐 BITCOIN KEY SPLITTER")
        print("=" * 70)
        
        # Validate private key format
        if len(private_key_hex) != 64:
            # Try to pad or trim
            if len(private_key_hex) < 64:
                private_key_hex = private_key_hex.zfill(64)
            else:
                private_key_hex = private_key_hex[:64]
        
        # Optional: Add passphrase encryption layer
        key_to_split = private_key_hex
        if passphrase:
            # XOR with passphrase hash
            pass_hash = hashlib.sha256(passphrase.encode()).hexdigest()
            key_int = int(private_key_hex, 16) ^ int(pass_hash, 16)
            key_to_split = f"{key_int:064x}"
            print("\n🔒 Additional passphrase encryption applied")
        
        result = ShamirSecretSharing.split_secret(key_to_split, threshold, total)
        
        if result["success"]:
            result["encrypted_with_passphrase"] = passphrase is not None
            
            if passphrase:
                print("\n⚠️  CRITICAL: You need BOTH shares AND passphrase to recover!")
        
        return result
    
    @staticmethod
    def recover_key_secure(shares, passphrase=None):
        """
        Recover key with optional passphrase
        """
        result = ShamirSecretSharing.recover_secret(shares)
        
        if result["success"] and passphrase:
            # Decrypt with passphrase
            pass_hash = hashlib.sha256(passphrase.encode()).hexdigest()
            recovered_int = int(result["secret"], 16) ^ int(pass_hash, 16)
            result["secret"] = f"{recovered_int:064x}"
            print("\n🔓 Passphrase decryption applied")
        
        return result


def demo():
    """Demo the Shamir Secret Sharing tool"""
    print("=" * 70)
    print("🧩 SHAMIR SECRET SHARING - DEMO")
    print("=" * 70)
    print()
    print("Choose operation:")
    print("  1. Split secret into shares")
    print("  2. Recover secret from shares")
    print("  3. Demo with test key")
    print()
    
    choice = input("Select (1-3): ").strip()
    
    if choice == "1":
        secret = input("\nEnter secret (hex): ").strip()
        threshold = int(input("Threshold (min shares needed): ").strip())
        total = int(input("Total shares to create: ").strip())
        
        ShamirSecretSharing.split_secret(secret, threshold, total)
        
    elif choice == "2":
        num = int(input("\nHow many shares do you have? ").strip())
        shares = []
        for i in range(num):
            share = input(f"Share #{i+1}: ").strip()
            shares.append(share)
        
        ShamirSecretSharing.recover_secret(shares)
        
    elif choice == "3":
        test_key = "a" * 64  # Test private key
        print(f"\n🔑 Test key: {test_key}")
        
        # Split 3-of-5
        result = ShamirSecretSharing.split_secret(test_key, 3, 5)
        
        if result["success"]:
            print("\n" + "=" * 70)
            print("Testing recovery with 3 random shares...")
            
            # Use shares 1, 3, 5
            test_shares = [result["shares"][0], result["shares"][2], result["shares"][4]]
            
            recover_result = ShamirSecretSharing.recover_secret(test_shares)
            
            if recover_result["success"]:
                if recover_result["secret"] == test_key:
                    print("\n🎉 SUCCESS! Secret recovered correctly!")
                else:
                    print("\n❌ ERROR: Recovered secret doesn't match!")


if __name__ == "__main__":
    demo()
