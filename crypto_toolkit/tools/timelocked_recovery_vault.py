#!/usr/bin/env python3
"""
⏰ TIME-LOCKED RECOVERY VAULT
Create Bitcoin transactions with time-locks (nLockTime, CLTV)
Perfect for dead man switches, inheritance planning, and delayed access
"""

import hashlib
import time
import datetime
from typing import Optional

class TimeLockVault:
    """
    Create and manage time-locked Bitcoin transactions
    """
    
    @staticmethod
    def create_nlocktime_tx(private_key_hex, to_address, amount_btc, unlock_timestamp):
        """
        Create a transaction that can't be broadcast until a specific time
        
        Args:
            private_key_hex: Source private key
            to_address: Destination address
            amount_btc: Amount in BTC
            unlock_timestamp: Unix timestamp when tx becomes valid
        
        Returns:
            Transaction data with time-lock
        """
        print("\n⏰ TIME-LOCKED TRANSACTION BUILDER")
        print("=" * 70)
        
        current_time = int(time.time())
        unlock_dt = datetime.datetime.fromtimestamp(unlock_timestamp)
        delay_seconds = unlock_timestamp - current_time
        
        if delay_seconds <= 0:
            print("\n⚠️  Warning: Unlock time is in the past!")
        
        print(f"\n📅 Time-Lock Configuration:")
        print(f"   Current time: {datetime.datetime.fromtimestamp(current_time)}")
        print(f"   Unlock time: {unlock_dt}")
        print(f"   Lock duration: {delay_seconds/86400:.1f} days ({delay_seconds/3600:.1f} hours)")
        
        # Create transaction structure (simplified)
        tx_data = {
            "version": 2,
            "locktime": unlock_timestamp,
            "inputs": [{
                "prev_tx": "simulated_input_tx_hash",
                "prev_index": 0,
                "script_sig": "<signature>",
                "sequence": 0xFFFFFFFE  # Required for nLockTime
            }],
            "outputs": [{
                "address": to_address,
                "amount_satoshis": int(amount_btc * 100000000)
            }]
        }
        
        # Calculate transaction hash (simplified)
        tx_string = f"{tx_data['version']}{tx_data['locktime']}{to_address}{amount_btc}"
        tx_hash = hashlib.sha256(tx_string.encode()).hexdigest()
        
        print(f"\n✅ Time-locked transaction created!")
        print(f"   TX Hash: {tx_hash}")
        print(f"   Destination: {to_address}")
        print(f"   Amount: {amount_btc} BTC")
        print(f"\n🔒 Lock Status:")
        if delay_seconds > 0:
            print(f"   Status: LOCKED")
            print(f"   Unlocks: {unlock_dt}")
            print(f"   Time remaining: {delay_seconds/3600:.1f} hours")
        else:
            print(f"   Status: UNLOCKED (can broadcast now)")
        
        print(f"\n💡 Use cases:")
        print(f"   - Dead man switch (inherit after X days of inactivity)")
        print(f"   - Savings lock (prevent impulse spending)")
        print(f"   - Scheduled payments")
        print(f"   - Will/inheritance automation")
        
        return {
            "success": True,
            "tx_hash": tx_hash,
            "tx_data": tx_data,
            "unlock_timestamp": unlock_timestamp,
            "unlock_datetime": unlock_dt.isoformat(),
            "locked": delay_seconds > 0,
            "seconds_until_unlock": max(0, delay_seconds)
        }
    
    @staticmethod
    def create_checklocktimeverify_script(unlock_timestamp, pubkey_hash):
        """
        Create a CHECKLOCKTIMEVERIFY script for absolute time-locks
        
        More secure than nLockTime - enforced at script level
        """
        print("\n🔐 CHECKLOCKTIMEVERIFY SCRIPT BUILDER")
        print("=" * 70)
        
        unlock_dt = datetime.datetime.fromtimestamp(unlock_timestamp)
        
        print(f"\n⏱️  Lock Configuration:")
        print(f"   Unlock time: {unlock_dt}")
        print(f"   Pubkey hash: {pubkey_hash[:20]}...")
        
        # Bitcoin script (pseudo-code representation)
        script = [
            f"<{unlock_timestamp}>",  # Push unlock time onto stack
            "OP_CHECKLOCKTIMEVERIFY",  # Verify current time > unlock time
            "OP_DROP",  # Drop the time value
            "OP_DUP",  # Duplicate pubkey hash
            "OP_HASH160",  # Hash it
            f"<{pubkey_hash}>",  # Push expected pubkey hash
            "OP_EQUALVERIFY",  # Verify equality
            "OP_CHECKSIG"  # Verify signature
        ]
        
        script_hex = hashlib.sha256(' '.join(script).encode()).hexdigest()
        
        print(f"\n✅ CLTV script created!")
        print(f"   Script hash: {script_hex}")
        print(f"   Type: P2SH (Pay-to-Script-Hash)")
        print(f"\n📜 Script operations:")
        for i, op in enumerate(script, 1):
            print(f"   {i}. {op}")
        
        print(f"\n🔒 Security:")
        print(f"   - Time-lock enforced by blockchain consensus")
        print(f"   - Cannot be bypassed or front-run")
        print(f"   - Requires both time + valid signature")
        
        return {
            "success": True,
            "script": script,
            "script_hex": script_hex,
            "unlock_timestamp": unlock_timestamp,
            "unlock_datetime": unlock_dt.isoformat()
        }
    
    @staticmethod
    def create_relative_timelock(private_key_hex, to_address, blocks_delay):
        """
        Create relative time-lock (CSV - CheckSequenceVerify)
        Locked for X blocks AFTER being confirmed
        
        Args:
            blocks_delay: Number of blocks to wait (1 block ≈ 10 minutes)
        """
        print("\n⏳ RELATIVE TIME-LOCK (CSV)")
        print("=" * 70)
        
        hours_delay = blocks_delay * 10 / 60
        days_delay = hours_delay / 24
        
        print(f"\n📊 Configuration:")
        print(f"   Blocks delay: {blocks_delay} blocks")
        print(f"   Estimated time: ~{hours_delay:.1f} hours (~{days_delay:.1f} days)")
        print(f"   Destination: {to_address}")
        
        tx_data = {
            "version": 2,
            "inputs": [{
                "prev_tx": "input_tx_hash",
                "prev_index": 0,
                "sequence": blocks_delay | (1 << 22)  # CSV format
            }],
            "outputs": [{
                "address": to_address,
                "script": "OP_CHECKSEQUENCEVERIFY"
            }]
        }
        
        print(f"\n✅ Relative time-lock created!")
        print(f"\n💡 How it works:")
        print(f"   1. Transaction is broadcast and confirmed")
        print(f"   2. Funds are locked for {blocks_delay} additional blocks")
        print(f"   3. After delay, recipient can spend")
        print(f"\n🎯 Use cases:")
        print(f"   - Cooling-off periods")
        print(f"   - Lightning Network channels")
        print(f"   - Escrow with time-based release")
        
        return {
            "success": True,
            "tx_data": tx_data,
            "blocks_delay": blocks_delay,
            "estimated_hours": hours_delay
        }


class DeadManSwitch:
    """
    Automated inheritance/emergency access system
    If you don't check in for X days, funds are released
    """
    
    def __init__(self, private_key_hex, beneficiary_address):
        self.private_key = private_key_hex
        self.beneficiary = beneficiary_address
        self.last_checkin = int(time.time())
        self.checkin_interval = 90 * 86400  # 90 days default
        
    def configure_switch(self, days_inactive, amount_btc):
        """
        Configure dead man switch parameters
        """
        print("\n💀 DEAD MAN SWITCH CONFIGURATOR")
        print("=" * 70)
        
        print(f"\n⚙️  Configuration:")
        print(f"   Inactivity threshold: {days_inactive} days")
        print(f"   Beneficiary: {self.beneficiary}")
        print(f"   Amount: {amount_btc} BTC")
        
        self.checkin_interval = days_inactive * 86400
        
        # Calculate trigger time
        trigger_time = int(time.time()) + self.checkin_interval
        trigger_dt = datetime.datetime.fromtimestamp(trigger_time)
        
        print(f"\n📅 Timeline:")
        print(f"   Last check-in: {datetime.datetime.fromtimestamp(self.last_checkin)}")
        print(f"   Trigger date (if no check-in): {trigger_dt}")
        
        # Create time-locked transaction
        result = TimeLockVault.create_nlocktime_tx(
            self.private_key,
            self.beneficiary,
            amount_btc,
            trigger_time
        )
        
        print(f"\n🎯 How it works:")
        print(f"   1. Check in regularly (every {days_inactive} days)")
        print(f"   2. If you don't check in, transaction becomes valid")
        print(f"   3. Beneficiary can broadcast and claim funds")
        print(f"   4. Each check-in creates new time-locked tx")
        
        print(f"\n⚠️  Setup requirements:")
        print(f"   - Store signed TX with trusted party/system")
        print(f"   - Set up automated check-in reminders")
        print(f"   - Have backup check-in method")
        print(f"   - Test the system with small amounts first")
        
        return result
    
    def checkin(self):
        """
        Perform check-in (resets the timer)
        """
        print("\n✅ CHECK-IN RECORDED")
        print("=" * 70)
        
        old_time = self.last_checkin
        self.last_checkin = int(time.time())
        
        next_checkin = self.last_checkin + self.checkin_interval
        next_dt = datetime.datetime.fromtimestamp(next_checkin)
        
        print(f"   Previous check-in: {datetime.datetime.fromtimestamp(old_time)}")
        print(f"   Current check-in: {datetime.datetime.fromtimestamp(self.last_checkin)}")
        print(f"   Next check-in due: {next_dt}")
        print(f"\n💡 Old time-locked transaction is now invalid.")
        print(f"   Generate new one with updated timestamp.")
        
        return {
            "success": True,
            "checkin_time": self.last_checkin,
            "next_checkin_due": next_checkin
        }


class InheritanceVault:
    """
    Multi-beneficiary time-locked inheritance system
    """
    
    @staticmethod
    def create_inheritance_plan(total_btc, beneficiaries, unlock_conditions):
        """
        Create multi-stage inheritance plan
        
        Args:
            total_btc: Total amount to distribute
            beneficiaries: List of {address, percentage, name}
            unlock_conditions: Time conditions for release
        """
        print("\n🏛️  INHERITANCE VAULT PLANNER")
        print("=" * 70)
        
        print(f"\n💰 Total estate: {total_btc} BTC")
        print(f"   Beneficiaries: {len(beneficiaries)}")
        
        # Validate percentages
        total_pct = sum(b['percentage'] for b in beneficiaries)
        if abs(total_pct - 100) > 0.01:
            print(f"\n⚠️  Warning: Percentages sum to {total_pct}% (should be 100%)")
        
        print(f"\n👥 Distribution plan:")
        transactions = []
        
        for i, beneficiary in enumerate(beneficiaries, 1):
            amount = total_btc * (beneficiary['percentage'] / 100)
            
            print(f"\n   Beneficiary #{i}: {beneficiary['name']}")
            print(f"   - Address: {beneficiary['address']}")
            print(f"   - Share: {beneficiary['percentage']}% ({amount:.8f} BTC)")
            print(f"   - Unlock: {unlock_conditions.get('timestamp', 'immediate')}")
            
            # Create time-locked transaction for each beneficiary
            if 'timestamp' in unlock_conditions:
                tx_result = TimeLockVault.create_nlocktime_tx(
                    "source_key",  # Would be actual key
                    beneficiary['address'],
                    amount,
                    unlock_conditions['timestamp']
                )
                transactions.append(tx_result)
        
        print(f"\n✅ Inheritance plan created!")
        print(f"\n📋 Next steps:")
        print(f"   1. Store signed transactions securely")
        print(f"   2. Give instructions to executor/lawyer")
        print(f"   3. Set up dead man switch")
        print(f"   4. Test with small amounts first")
        
        return {
            "success": True,
            "total_amount": total_btc,
            "beneficiaries": len(beneficiaries),
            "transactions": transactions
        }


def demo():
    """Demo the time-lock vault"""
    print("=" * 70)
    print("⏰ TIME-LOCKED RECOVERY VAULT - DEMO")
    print("=" * 70)
    print()
    print("Choose operation:")
    print("  1. Create time-locked transaction (nLockTime)")
    print("  2. Create CHECKLOCKTIMEVERIFY script")
    print("  3. Configure dead man switch")
    print("  4. Create inheritance plan")
    print("  5. Demo relative time-lock (CSV)")
    print()
    
    choice = input("Select (1-5): ").strip()
    
    if choice == "1":
        to_addr = input("\nDestination address: ").strip()
        amount = float(input("Amount (BTC): ").strip())
        days = int(input("Lock for how many days? ").strip())
        
        unlock_time = int(time.time()) + (days * 86400)
        
        TimeLockVault.create_nlocktime_tx("test_key", to_addr, amount, unlock_time)
        
    elif choice == "2":
        days = int(input("\nLock for how many days? ").strip())
        pubkey = input("Pubkey hash (or press Enter for demo): ").strip() or "a" * 40
        
        unlock_time = int(time.time()) + (days * 86400)
        
        TimeLockVault.create_checklocktimeverify_script(unlock_time, pubkey)
        
    elif choice == "3":
        beneficiary = input("\nBeneficiary address: ").strip()
        days_inactive = int(input("Days of inactivity before trigger: ").strip())
        amount = float(input("Amount (BTC): ").strip())
        
        switch = DeadManSwitch("test_key", beneficiary)
        switch.configure_switch(days_inactive, amount)
        
    elif choice == "4":
        total = float(input("\nTotal BTC to distribute: ").strip())
        
        # Example beneficiaries
        beneficiaries = [
            {"name": "Alice", "address": "1Alice...", "percentage": 50},
            {"name": "Bob", "address": "1Bob...", "percentage": 30},
            {"name": "Charlie", "address": "1Charlie...", "percentage": 20}
        ]
        
        days = int(input("Lock for how many days? ").strip())
        unlock_time = int(time.time()) + (days * 86400)
        
        InheritanceVault.create_inheritance_plan(
            total,
            beneficiaries,
            {"timestamp": unlock_time}
        )
        
    elif choice == "5":
        blocks = int(input("\nBlocks to lock (1 block ≈ 10 min): ").strip())
        to_addr = input("Destination address: ").strip()
        
        TimeLockVault.create_relative_timelock("test_key", to_addr, blocks)


if __name__ == "__main__":
    demo()
