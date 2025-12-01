#!/usr/bin/env python3
"""
🤝 MULTI-SIG ORCHESTRATOR
Create and manage complex multi-signature wallets
2-of-3, 3-of-5, or any M-of-N configuration
Perfect for partnerships, DAOs, corporate treasuries
"""

import hashlib
import secrets
import json
from typing import List, Dict
import time

class MultiSigWallet:
    """
    Create and manage multi-signature Bitcoin wallets
    """
    
    def __init__(self, required_sigs, total_keys):
        """
        Initialize multisig configuration
        
        Args:
            required_sigs: M (minimum signatures needed)
            total_keys: N (total keys in wallet)
        """
        self.m = required_sigs
        self.n = total_keys
        self.public_keys = []
        self.participants = []
        
    def create_multisig_wallet(self, participant_pubkeys, participant_names):
        """
        Create a new multisig wallet
        
        Args:
            participant_pubkeys: List of public keys (hex)
            participant_names: Names of participants
        """
        print(f"\n🤝 MULTI-SIG WALLET CREATOR")
        print("=" * 70)
        
        if len(participant_pubkeys) != self.n:
            return {"success": False, "error": f"Need exactly {self.n} public keys"}
        
        print(f"\n⚙️  Configuration:")
        print(f"   Type: {self.m}-of-{self.n} multisig")
        print(f"   Required signatures: {self.m}")
        print(f"   Total participants: {self.n}")
        
        # Store participants
        for i, (pubkey, name) in enumerate(zip(participant_pubkeys, participant_names), 1):
            self.participants.append({
                "id": i,
                "name": name,
                "pubkey": pubkey,
                "role": "signer"
            })
            print(f"\n   Participant #{i}: {name}")
            print(f"   - Public key: {pubkey[:32]}...")
        
        # Create multisig script
        script = self._create_multisig_script(participant_pubkeys)
        
        # Generate multisig address
        script_hash = hashlib.sha256(script.encode()).hexdigest()
        address = "3" + script_hash[:33]  # P2SH address (starts with 3)
        
        print(f"\n✅ Multisig wallet created!")
        print(f"   Address: {address}")
        print(f"   Script hash: {script_hash}")
        
        print(f"\n🔒 Security properties:")
        print(f"   - Requires {self.m} signatures to spend")
        print(f"   - {self.n - self.m} keys can be lost/compromised safely")
        print(f"   - No single point of failure")
        print(f"   - Collaborative control")
        
        print(f"\n🎯 Common use cases:")
        if self.m == 2 and self.n == 3:
            print(f"   2-of-3: You + Partner + Backup (escrow, business)")
        elif self.m == 2 and self.n == 2:
            print(f"   2-of-2: Requires both parties (joint account)")
        elif self.m == 3 and self.n == 5:
            print(f"   3-of-5: Board of directors, DAO treasury")
        
        wallet_data = {
            "address": address,
            "script_hash": script_hash,
            "script": script,
            "m": self.m,
            "n": self.n,
            "participants": self.participants,
            "created": int(time.time())
        }
        
        return {"success": True, "wallet": wallet_data}
    
    def _create_multisig_script(self, pubkeys):
        """
        Create Bitcoin multisig script (simplified)
        Real format: OP_M <pubkey1> <pubkey2> ... <pubkeyN> OP_N OP_CHECKMULTISIG
        """
        script_ops = [
            f"OP_{self.m}",  # Minimum signatures
        ]
        
        for pubkey in pubkeys:
            script_ops.append(f"<{pubkey}>")
        
        script_ops.extend([
            f"OP_{self.n}",  # Total keys
            "OP_CHECKMULTISIG"
        ])
        
        return ' '.join(script_ops)
    
    def create_transaction(self, wallet_data, to_address, amount_btc):
        """
        Create unsigned multisig transaction
        """
        print(f"\n📤 CREATING MULTISIG TRANSACTION")
        print("=" * 70)
        
        print(f"\n📊 Transaction details:")
        print(f"   From: {wallet_data['address']}")
        print(f"   To: {to_address}")
        print(f"   Amount: {amount_btc} BTC")
        print(f"   Required signatures: {self.m}")
        
        # Create transaction structure
        tx = {
            "version": 2,
            "inputs": [{
                "prev_tx": "input_tx_hash",
                "prev_index": 0,
                "script_sig": "",  # Will be filled with signatures
                "multisig_script": wallet_data['script']
            }],
            "outputs": [{
                "address": to_address,
                "amount_satoshis": int(amount_btc * 100000000)
            }],
            "locktime": 0
        }
        
        # Calculate transaction hash
        tx_data_str = json.dumps(tx, sort_keys=True)
        tx_hash = hashlib.sha256(tx_data_str.encode()).hexdigest()
        
        tx['tx_hash'] = tx_hash
        tx['signatures'] = []  # Will be populated by signers
        tx['signatures_needed'] = self.m
        tx['status'] = 'PENDING_SIGNATURES'
        
        print(f"\n✅ Transaction created!")
        print(f"   TX Hash: {tx_hash}")
        print(f"   Status: Pending {self.m} signatures")
        
        print(f"\n📝 Next steps:")
        print(f"   1. Share TX with {self.m} signers")
        print(f"   2. Each signer signs with their private key")
        print(f"   3. Collect all signatures")
        print(f"   4. Broadcast completed transaction")
        
        return {"success": True, "transaction": tx}
    
    def sign_transaction(self, tx, signer_privkey, signer_name):
        """
        Add a signature to the transaction
        """
        print(f"\n✍️  SIGNING TRANSACTION")
        print("=" * 70)
        
        print(f"   Signer: {signer_name}")
        print(f"   TX: {tx['tx_hash'][:32]}...")
        
        # Create signature (simplified)
        sig_data = f"{tx['tx_hash']}{signer_privkey}"
        signature = hashlib.sha256(sig_data.encode()).hexdigest()
        
        # Add signature
        tx['signatures'].append({
            "signer": signer_name,
            "signature": signature,
            "timestamp": int(time.time())
        })
        
        sigs_collected = len(tx['signatures'])
        sigs_needed = tx['signatures_needed']
        
        print(f"\n✅ Signature added!")
        print(f"   Signatures: {sigs_collected}/{sigs_needed}")
        
        if sigs_collected >= sigs_needed:
            tx['status'] = 'READY_TO_BROADCAST'
            print(f"   Status: ✅ READY TO BROADCAST")
        else:
            print(f"   Status: ⏳ Waiting for {sigs_needed - sigs_collected} more")
        
        return {"success": True, "transaction": tx}
    
    def broadcast_transaction(self, tx):
        """
        Broadcast completed multisig transaction
        """
        print(f"\n📡 BROADCASTING TRANSACTION")
        print("=" * 70)
        
        if tx['status'] != 'READY_TO_BROADCAST':
            return {
                "success": False,
                "error": f"Transaction not ready (status: {tx['status']})"
            }
        
        sigs = len(tx['signatures'])
        required = tx['signatures_needed']
        
        if sigs < required:
            return {
                "success": False,
                "error": f"Not enough signatures ({sigs}/{required})"
            }
        
        print(f"\n✅ Verification passed!")
        print(f"   Signatures: {sigs}/{required}")
        print(f"   TX Hash: {tx['tx_hash']}")
        
        print(f"\n📡 Broadcasting to network...")
        print(f"   (In production: send to Bitcoin nodes)")
        
        tx['status'] = 'BROADCASTED'
        tx['broadcast_time'] = int(time.time())
        
        print(f"\n🎉 Transaction broadcasted successfully!")
        print(f"   TX ID: {tx['tx_hash']}")
        print(f"   Monitor: blockchain.info/tx/{tx['tx_hash']}")
        
        return {"success": True, "tx_id": tx['tx_hash']}


class CorporateTreasury:
    """
    Specialized multisig for corporate/DAO treasuries
    """
    
    @staticmethod
    def create_treasury(company_name, board_members, approval_threshold):
        """
        Create corporate treasury with role-based access
        
        Args:
            company_name: Organization name
            board_members: List of {name, pubkey, role}
            approval_threshold: Percentage needed (e.g., 60 for 60%)
        """
        print(f"\n🏛️  CORPORATE TREASURY SETUP")
        print("=" * 70)
        
        print(f"\n🏢 Organization: {company_name}")
        print(f"   Board members: {len(board_members)}")
        print(f"   Approval threshold: {approval_threshold}%")
        
        # Calculate M-of-N from percentage
        total_members = len(board_members)
        required_sigs = max(2, int(total_members * approval_threshold / 100))
        
        print(f"\n📊 Multisig configuration:")
        print(f"   Type: {required_sigs}-of-{total_members}")
        print(f"   Required approvals: {required_sigs} members")
        
        # Create multisig wallet
        wallet = MultiSigWallet(required_sigs, total_members)
        
        pubkeys = [m['pubkey'] for m in board_members]
        names = [m['name'] for m in board_members]
        
        result = wallet.create_multisig_wallet(pubkeys, names)
        
        if result['success']:
            treasury = result['wallet']
            treasury['company_name'] = company_name
            treasury['approval_threshold'] = approval_threshold
            treasury['governance'] = {
                "voting_system": "multisig",
                "proposal_lifetime": "7 days",
                "emergency_threshold": f"{required_sigs}-of-{total_members}"
            }
            
            print(f"\n🎯 Governance rules:")
            print(f"   - All spending requires {required_sigs} board signatures")
            print(f"   - Proposals valid for 7 days")
            print(f"   - Emergency procedures: same threshold")
            
            print(f"\n📋 Board members:")
            for member in board_members:
                print(f"   - {member['name']} ({member.get('role', 'Board Member')})")
            
            return {"success": True, "treasury": treasury}
        
        return result


class EscrowService:
    """
    2-of-3 multisig escrow (Buyer + Seller + Arbiter)
    """
    
    @staticmethod
    def create_escrow(buyer_pubkey, seller_pubkey, arbiter_pubkey, amount_btc):
        """
        Create escrow contract
        """
        print(f"\n🤝 ESCROW SERVICE - 2-OF-3 MULTISIG")
        print("=" * 70)
        
        print(f"\n📋 Escrow details:")
        print(f"   Amount: {amount_btc} BTC")
        print(f"   Type: 2-of-3 multisig")
        
        # Create 2-of-3 wallet
        wallet = MultiSigWallet(2, 3)
        
        result = wallet.create_multisig_wallet(
            [buyer_pubkey, seller_pubkey, arbiter_pubkey],
            ["Buyer", "Seller", "Arbiter"]
        )
        
        if result['success']:
            escrow = result['wallet']
            escrow['amount'] = amount_btc
            escrow['escrow_type'] = '2-of-3'
            
            print(f"\n🔒 How it works:")
            print(f"   1. Buyer sends {amount_btc} BTC to escrow address")
            print(f"   2. Seller delivers goods/services")
            print(f"   3. Release requires 2 of 3 signatures:")
            print(f"      - Happy: Buyer + Seller release to seller")
            print(f"      - Dispute: Arbiter + Winner release funds")
            print(f"      - Refund: Buyer + Arbiter release back to buyer")
            
            print(f"\n✅ Escrow address: {escrow['address']}")
            
            return {"success": True, "escrow": escrow}
        
        return result


def demo():
    """Demo the multisig orchestrator"""
    print("=" * 70)
    print("🤝 MULTI-SIG ORCHESTRATOR - DEMO")
    print("=" * 70)
    print()
    print("Choose operation:")
    print("  1. Create 2-of-3 multisig wallet")
    print("  2. Create 3-of-5 DAO treasury")
    print("  3. Create escrow (2-of-3)")
    print("  4. Full transaction flow demo")
    print()
    
    choice = input("Select (1-4): ").strip()
    
    if choice == "1":
        print("\nCreating 2-of-3 multisig wallet...")
        
        wallet = MultiSigWallet(2, 3)
        
        # Generate dummy keys
        pubkeys = [secrets.token_hex(32) for _ in range(3)]
        names = ["Alice", "Bob", "Charlie"]
        
        wallet.create_multisig_wallet(pubkeys, names)
        
    elif choice == "2":
        board = [
            {"name": "Alice CEO", "pubkey": secrets.token_hex(32), "role": "CEO"},
            {"name": "Bob CFO", "pubkey": secrets.token_hex(32), "role": "CFO"},
            {"name": "Charlie CTO", "pubkey": secrets.token_hex(32), "role": "CTO"},
            {"name": "Diana COO", "pubkey": secrets.token_hex(32), "role": "COO"},
            {"name": "Eve CMO", "pubkey": secrets.token_hex(32), "role": "CMO"},
        ]
        
        CorporateTreasury.create_treasury("TechCorp DAO", board, 60)
        
    elif choice == "3":
        buyer = secrets.token_hex(32)
        seller = secrets.token_hex(32)
        arbiter = secrets.token_hex(32)
        
        EscrowService.create_escrow(buyer, seller, arbiter, 1.5)
        
    elif choice == "4":
        print("\n🎬 FULL TRANSACTION FLOW DEMO")
        print("=" * 70)
        
        # Step 1: Create wallet
        wallet = MultiSigWallet(2, 3)
        pubkeys = [secrets.token_hex(32) for _ in range(3)]
        names = ["Alice", "Bob", "Charlie"]
        
        result = wallet.create_multisig_wallet(pubkeys, names)
        wallet_data = result['wallet']
        
        input("\nPress Enter to create transaction...")
        
        # Step 2: Create transaction
        tx_result = wallet.create_transaction(
            wallet_data,
            "1RecipientAddress...",
            0.5
        )
        tx = tx_result['transaction']
        
        input("\nPress Enter for Alice to sign...")
        
        # Step 3: First signature
        wallet.sign_transaction(tx, "alice_privkey", "Alice")
        
        input("\nPress Enter for Bob to sign...")
        
        # Step 4: Second signature
        wallet.sign_transaction(tx, "bob_privkey", "Bob")
        
        input("\nPress Enter to broadcast...")
        
        # Step 5: Broadcast
        wallet.broadcast_transaction(tx)
        
        print("\n🎉 Complete multisig transaction flow demonstrated!")


if __name__ == "__main__":
    demo()
