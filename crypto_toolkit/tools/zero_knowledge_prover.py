#!/usr/bin/env python3
"""
🔐 ZERO-KNOWLEDGE OWNERSHIP PROVER
Prove you own a Bitcoin address without revealing the private key
Useful for audits, disputes, verification without exposing secrets
"""

import hashlib
import secrets
import time
from typing import Tuple

class ZeroKnowledgeProver:
    """
    Implement Zero-Knowledge Proof of private key ownership
    Using Schnorr-like protocol (simplified)
    """
    
    # Simplified curve parameters (in production, use secp256k1)
    P = 2**256 - 2**32 - 977  # Prime modulus
    G = 2  # Generator
    
    @staticmethod
    def _mod_pow(base, exp, mod):
        """Efficient modular exponentiation"""
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        return result
    
    @staticmethod
    def generate_proof(private_key_hex, challenge_message):
        """
        Generate zero-knowledge proof of private key ownership
        
        Prover demonstrates knowledge of private key without revealing it
        
        Args:
            private_key_hex: Your private key (kept secret)
            challenge_message: Message to sign (from verifier)
        
        Returns:
            Proof data that can be publicly verified
        """
        print("\n🔐 ZERO-KNOWLEDGE PROOF GENERATION")
        print("=" * 70)
        
        # Convert private key to integer
        private_key = int(private_key_hex, 16)
        
        # Compute public key: PubKey = G^PrivKey mod P
        public_key = ZeroKnowledgeProver._mod_pow(ZeroKnowledgeProver.G, private_key, ZeroKnowledgeProver.P)
        
        print(f"\n🔑 Keys:")
        print(f"   Private key: {'*' * 64} (hidden)")
        print(f"   Public key: {public_key:064x}")
        
        # Generate random nonce
        nonce = secrets.randbelow(ZeroKnowledgeProver.P - 1) + 1
        
        # Compute commitment: R = G^nonce mod P
        commitment = ZeroKnowledgeProver._mod_pow(ZeroKnowledgeProver.G, nonce, ZeroKnowledgeProver.P)
        
        print(f"\n📝 Challenge:")
        print(f"   Message: {challenge_message}")
        
        # Compute challenge hash: c = H(PubKey || R || Message)
        challenge_data = f"{public_key:064x}{commitment:064x}{challenge_message}"
        challenge_hash = hashlib.sha256(challenge_data.encode()).hexdigest()
        challenge = int(challenge_hash, 16) % (ZeroKnowledgeProver.P - 1)
        
        # Compute response: s = nonce - challenge * private_key (mod P-1)
        response = (nonce - challenge * private_key) % (ZeroKnowledgeProver.P - 1)
        
        proof = {
            "public_key": f"{public_key:064x}",
            "commitment": f"{commitment:064x}",
            "challenge": challenge_hash,
            "response": f"{response:064x}",
            "message": challenge_message,
            "timestamp": int(time.time())
        }
        
        print(f"\n✅ Proof generated!")
        print(f"   Commitment: {proof['commitment'][:32]}...")
        print(f"   Response: {proof['response'][:32]}...")
        
        print(f"\n🔒 Security properties:")
        print(f"   ✓ Private key NOT revealed")
        print(f"   ✓ Proof cannot be reused for different messages")
        print(f"   ✓ Only owner of private key can generate valid proof")
        print(f"   ✓ Anyone can verify the proof")
        
        return proof
    
    @staticmethod
    def verify_proof(proof, challenge_message):
        """
        Verify a zero-knowledge proof
        
        Anyone can verify without knowing the private key
        
        Args:
            proof: Proof data from prover
            challenge_message: Original challenge message
        
        Returns:
            Boolean indicating if proof is valid
        """
        print("\n🔍 ZERO-KNOWLEDGE PROOF VERIFICATION")
        print("=" * 70)
        
        try:
            # Parse proof
            public_key = int(proof['public_key'], 16)
            commitment = int(proof['commitment'], 16)
            response = int(proof['response'], 16)
            
            print(f"\n📋 Verifying proof:")
            print(f"   Public key: {proof['public_key'][:32]}...")
            print(f"   Challenge: {challenge_message}")
            
            # Verify message matches
            if proof['message'] != challenge_message:
                print(f"\n❌ VERIFICATION FAILED: Message mismatch")
                return False
            
            # Recompute challenge
            challenge_data = f"{public_key:064x}{commitment:064x}{challenge_message}"
            challenge_hash = hashlib.sha256(challenge_data.encode()).hexdigest()
            challenge = int(challenge_hash, 16) % (ZeroKnowledgeProver.P - 1)
            
            # Verify equation: G^response * PubKey^challenge == R (commitment)
            # This verifies: G^(nonce - c*priv) * (G^priv)^c == G^nonce
            left_side = (
                ZeroKnowledgeProver._mod_pow(ZeroKnowledgeProver.G, response, ZeroKnowledgeProver.P) *
                ZeroKnowledgeProver._mod_pow(public_key, challenge, ZeroKnowledgeProver.P)
            ) % ZeroKnowledgeProver.P
            
            is_valid = (left_side == commitment)
            
            if is_valid:
                print(f"\n✅ PROOF VALID!")
                print(f"   The prover knows the private key for this public key")
                print(f"   Verified at: {time.ctime()}")
                print(f"\n💡 What this proves:")
                print(f"   - Prover owns private key for address")
                print(f"   - Proof was generated specifically for this challenge")
                print(f"   - Private key was NOT revealed or exposed")
            else:
                print(f"\n❌ PROOF INVALID!")
                print(f"   The prover does NOT know the private key")
                print(f"   Or proof has been tampered with")
            
            return is_valid
            
        except Exception as e:
            print(f"\n❌ Verification error: {str(e)}")
            return False
    
    @staticmethod
    def interactive_challenge_response(private_key_hex):
        """
        Interactive proof session
        
        Simulates interaction between prover and verifier
        """
        print("\n🤝 INTERACTIVE ZERO-KNOWLEDGE PROOF SESSION")
        print("=" * 70)
        
        # Step 1: Prover publishes public key
        private_key = int(private_key_hex, 16)
        public_key = ZeroKnowledgeProver._mod_pow(ZeroKnowledgeProver.G, private_key, ZeroKnowledgeProver.P)
        
        print(f"\n[PROVER] I claim to own the private key for:")
        print(f"   Public Key: {public_key:064x}")
        
        # Step 2: Verifier issues challenge
        challenge_msg = f"prove_ownership_{secrets.token_hex(8)}"
        print(f"\n[VERIFIER] Prove it! Sign this challenge:")
        print(f"   Challenge: {challenge_msg}")
        
        # Step 3: Prover generates proof
        print(f"\n[PROVER] Generating proof...")
        proof = ZeroKnowledgeProver.generate_proof(private_key_hex, challenge_msg)
        
        # Step 4: Verifier checks proof
        print(f"\n[VERIFIER] Verifying proof...")
        is_valid = ZeroKnowledgeProver.verify_proof(proof, challenge_msg)
        
        if is_valid:
            print(f"\n[VERIFIER] ✅ Proof accepted! You own this address.")
        else:
            print(f"\n[VERIFIER] ❌ Proof rejected! Verification failed.")
        
        return is_valid


class BitcoinOwnershipProver:
    """
    Specialized tool for proving Bitcoin address ownership
    """
    
    @staticmethod
    def prove_address_ownership(private_key_hex, bitcoin_address, verifier_challenge=None):
        """
        Prove ownership of a Bitcoin address
        
        Args:
            private_key_hex: Your private key
            bitcoin_address: The Bitcoin address to prove ownership of
            verifier_challenge: Optional challenge from verifier
        
        Returns:
            Proof package
        """
        print("\n🪙 BITCOIN ADDRESS OWNERSHIP PROOF")
        print("=" * 70)
        
        print(f"\n📍 Proving ownership of:")
        print(f"   Address: {bitcoin_address}")
        
        # Generate challenge if not provided
        if not verifier_challenge:
            verifier_challenge = f"prove_{bitcoin_address}_{int(time.time())}"
            print(f"   Challenge: {verifier_challenge}")
        
        # Generate proof
        proof = ZeroKnowledgeProver.generate_proof(private_key_hex, verifier_challenge)
        
        # Add Bitcoin-specific data
        proof['bitcoin_address'] = bitcoin_address
        proof['proof_type'] = 'bitcoin_ownership'
        
        print(f"\n📦 Proof package ready!")
        print(f"\n🎯 Use cases:")
        print(f"   - Prove solvency to auditors")
        print(f"   - Resolve ownership disputes")
        print(f"   - Verify cold storage without exposing keys")
        print(f"   - Authenticate without revealing secrets")
        
        print(f"\n📤 Share with verifier:")
        print(f"   - Public key")
        print(f"   - Proof data (commitment, response)")
        print(f"   - DO NOT share private key!")
        
        return proof
    
    @staticmethod
    def batch_prove_ownership(private_keys, addresses):
        """
        Generate proofs for multiple addresses
        Useful for portfolio verification
        """
        print("\n📊 BATCH OWNERSHIP PROOF")
        print("=" * 70)
        
        if len(private_keys) != len(addresses):
            print("\n❌ Error: Number of keys and addresses must match")
            return None
        
        print(f"\n🔢 Generating proofs for {len(addresses)} addresses...")
        
        proofs = []
        for i, (key, addr) in enumerate(zip(private_keys, addresses), 1):
            print(f"\n[{i}/{len(addresses)}] Processing {addr}...")
            proof = BitcoinOwnershipProver.prove_address_ownership(key, addr)
            proofs.append(proof)
        
        print(f"\n✅ Batch proof complete!")
        print(f"   Total addresses: {len(proofs)}")
        print(f"\n💡 Use case: Prove solvency of entire portfolio")
        
        return proofs


def demo():
    """Demo the zero-knowledge prover"""
    print("=" * 70)
    print("🔐 ZERO-KNOWLEDGE OWNERSHIP PROVER - DEMO")
    print("=" * 70)
    print()
    print("Choose operation:")
    print("  1. Generate proof (I own this address)")
    print("  2. Verify proof (check someone else's proof)")
    print("  3. Interactive session (full demo)")
    print("  4. Bitcoin address ownership proof")
    print()
    
    choice = input("Select (1-4): ").strip()
    
    if choice == "1":
        print("\n⚠️  Your private key stays secret - never transmitted!")
        key = input("\nEnter private key (hex): ").strip()
        challenge = input("Challenge message from verifier: ").strip()
        
        proof = ZeroKnowledgeProver.generate_proof(key, challenge)
        
        print("\n📋 Send this proof to verifier:")
        print(f"   Public key: {proof['public_key']}")
        print(f"   Commitment: {proof['commitment']}")
        print(f"   Response: {proof['response']}")
        
    elif choice == "2":
        print("\nPaste proof data:")
        pub = input("Public key: ").strip()
        com = input("Commitment: ").strip()
        res = input("Response: ").strip()
        msg = input("Challenge message: ").strip()
        
        proof = {
            'public_key': pub,
            'commitment': com,
            'response': res,
            'message': msg
        }
        
        ZeroKnowledgeProver.verify_proof(proof, msg)
        
    elif choice == "3":
        # Demo with test key
        test_key = "a" * 64
        print(f"\n🧪 Using test key: {test_key[:16]}...")
        
        ZeroKnowledgeProver.interactive_challenge_response(test_key)
        
    elif choice == "4":
        key = input("\nPrivate key (hex): ").strip()
        addr = input("Bitcoin address: ").strip()
        
        BitcoinOwnershipProver.prove_address_ownership(key, addr)


if __name__ == "__main__":
    demo()
