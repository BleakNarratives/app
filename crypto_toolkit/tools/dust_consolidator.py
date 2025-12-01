#!/usr/bin/env python3
"""
💨 DUST CONSOLIDATOR & PRIVACY ANALYZER
Combine tiny UTXOs into efficient amounts
Detect dust attacks and analyze privacy implications
"""

import hashlib
import secrets
from typing import List, Dict
import time

class DustConsolidator:
    """
    Consolidate small Bitcoin UTXOs (dust) into larger amounts
    """
    
    # Bitcoin dust threshold (546 satoshis)
    DUST_THRESHOLD = 546
    MIN_CONSOLIDATE_AMOUNT = 10000  # 10,000 satoshis minimum
    
    @staticmethod
    def analyze_utxos(utxos):
        """
        Analyze UTXOs and identify consolidation opportunities
        
        Args:
            utxos: List of {tx_hash, vout, amount_satoshis, address}
        """
        print("\n💨 UTXO DUST ANALYZER")
        print("=" * 70)
        
        if not utxos:
            print("\n❌ No UTXOs provided")
            return {"success": False, "error": "No UTXOs"}
        
        # Classify UTXOs
        dust = []  # < 546 sats (unspendable)
        small = []  # 546 - 10,000 sats (inefficient)
        medium = []  # 10k - 100k sats
        large = []  # > 100k sats
        
        total_amount = 0
        
        for utxo in utxos:
            amount = utxo['amount_satoshis']
            total_amount += amount
            
            if amount < DustConsolidator.DUST_THRESHOLD:
                dust.append(utxo)
            elif amount < DustConsolidator.MIN_CONSOLIDATE_AMOUNT:
                small.append(utxo)
            elif amount < 100000:
                medium.append(utxo)
            else:
                large.append(utxo)
        
        print(f"\n📊 UTXO Distribution:")
        print(f"   Total UTXOs: {len(utxos)}")
        print(f"   Total amount: {total_amount:,} satoshis ({total_amount/100000000:.8f} BTC)")
        print(f"\n   Classification:")
        print(f"   🚫 Dust (<546 sats): {len(dust)} UTXOs")
        print(f"   🤏 Small (546-10k): {len(small)} UTXOs")
        print(f"   🟡 Medium (10k-100k): {len(medium)} UTXOs")
        print(f"   🟢 Large (>100k): {len(large)} UTXOs")
        
        # Calculate consolidation benefit
        consolidatable = dust + small
        if consolidatable:
            consolidate_amount = sum(u['amount_satoshis'] for u in consolidatable)
            
            # Estimate fees (assume 148 bytes per input, 34 bytes per output)
            tx_size = len(consolidatable) * 148 + 34 + 10  # bytes
            fee_rate = 10  # sat/vByte (adjustable)
            estimated_fee = tx_size * fee_rate
            
            net_gain = consolidate_amount - estimated_fee
            
            print(f"\n💰 Consolidation opportunity:")
            print(f"   UTXOs to consolidate: {len(consolidatable)}")
            print(f"   Total amount: {consolidate_amount:,} sats")
            print(f"   Estimated fee: {estimated_fee:,} sats")
            print(f"   Net gain: {net_gain:,} sats")
            
            if net_gain > 0:
                print(f"   ✅ Worthwhile to consolidate!")
                recommendation = "CONSOLIDATE"
            else:
                print(f"   ❌ Not worth consolidating (fees too high)")
                recommendation = "WAIT_FOR_LOW_FEES"
        else:
            print(f"\n✅ No consolidation needed - all UTXOs are efficient")
            recommendation = "NO_ACTION"
        
        return {
            "success": True,
            "total_utxos": len(utxos),
            "dust": len(dust),
            "small": len(small),
            "medium": len(medium),
            "large": len(large),
            "total_amount": total_amount,
            "recommendation": recommendation,
            "consolidatable_utxos": consolidatable
        }
    
    @staticmethod
    def create_consolidation_tx(utxos, destination_address, fee_rate=10):
        """
        Create transaction to consolidate UTXOs
        
        Args:
            utxos: List of UTXOs to consolidate
            destination_address: Where to send consolidated amount
            fee_rate: Fee in sat/vByte
        """
        print("\n🔧 CONSOLIDATION TRANSACTION BUILDER")
        print("=" * 70)
        
        if not utxos:
            return {"success": False, "error": "No UTXOs to consolidate"}
        
        total_input = sum(u['amount_satoshis'] for u in utxos)
        
        # Calculate transaction size and fee
        tx_size = len(utxos) * 148 + 34 + 10
        fee = tx_size * fee_rate
        
        output_amount = total_input - fee
        
        if output_amount <= 0:
            return {
                "success": False,
                "error": f"Fee ({fee} sats) exceeds total input ({total_input} sats)"
            }
        
        print(f"\n📄 Transaction details:")
        print(f"   Inputs: {len(utxos)} UTXOs")
        print(f"   Total input: {total_input:,} satoshis")
        print(f"   Fee: {fee:,} satoshis ({fee_rate} sat/vByte)")
        print(f"   Output: {output_amount:,} satoshis")
        print(f"   Destination: {destination_address}")
        print(f"   TX size: ~{tx_size} bytes")
        
        # Create transaction structure
        tx = {
            "version": 2,
            "inputs": [
                {
                    "tx_hash": utxo['tx_hash'],
                    "vout": utxo['vout'],
                    "amount": utxo['amount_satoshis']
                }
                for utxo in utxos
            ],
            "outputs": [{
                "address": destination_address,
                "amount": output_amount
            }],
            "fee": fee,
            "size_bytes": tx_size
        }
        
        # Calculate TX hash
        import json
        tx_data = json.dumps(tx, sort_keys=True)
        tx_hash = hashlib.sha256(tx_data.encode()).hexdigest()
        
        tx['tx_hash'] = tx_hash
        
        print(f"\n✅ Transaction created!")
        print(f"   TX hash: {tx_hash}")
        
        print(f"\n💡 Benefits:")
        print(f"   - Reduced from {len(utxos)} UTXOs to 1 UTXO")
        print(f"   - Future transactions will be cheaper")
        print(f"   - Better for privacy (fewer inputs)")
        
        print(f"\n⏰ Best time to consolidate:")
        print(f"   - When network fees are LOW (weekends)")
        print(f"   - When you're not in a hurry")
        print(f"   - Use low priority (1-2 sat/vByte)")
        
        return {
            "success": True,
            "transaction": tx,
            "utxos_consolidated": len(utxos),
            "total_saved": output_amount
        }


class DustAttackDetector:
    """
    Detect and analyze potential dust attacks
    """
    
    @staticmethod
    def analyze_for_dust_attack(utxos, wallet_addresses):
        """
        Check if UTXOs show signs of dust attack
        
        Dust attacks send tiny amounts to link addresses together
        """
        print("\n🕵️ DUST ATTACK DETECTOR")
        print("=" * 70)
        
        suspicious_utxos = []
        
        for utxo in utxos:
            amount = utxo['amount_satoshis']
            
            # Characteristics of dust attacks:
            # 1. Very small amounts (< 1000 sats)
            # 2. Round numbers (exactly 546, 1000, etc.)
            # 3. Sent to many addresses at once
            
            is_suspicious = False
            reasons = []
            
            if amount < 1000:
                is_suspicious = True
                reasons.append("Very small amount")
            
            if amount in [546, 1000, 2000, 5000]:
                is_suspicious = True
                reasons.append("Round number (common in attacks)")
            
            # Check if you didn't expect this payment
            if 'expected' in utxo and not utxo['expected']:
                is_suspicious = True
                reasons.append("Unexpected payment")
            
            if is_suspicious:
                suspicious_utxos.append({
                    "utxo": utxo,
                    "reasons": reasons
                })
        
        print(f"\n🔍 Analysis results:")
        print(f"   Total UTXOs analyzed: {len(utxos)}")
        print(f"   Suspicious UTXOs: {len(suspicious_utxos)}")
        
        if suspicious_utxos:
            print(f"\n⚠️  POTENTIAL DUST ATTACK DETECTED!")
            print(f"\n   Suspicious transactions:")
            
            for i, item in enumerate(suspicious_utxos[:5], 1):
                utxo = item['utxo']
                print(f"\n   #{i}:")
                print(f"   - Amount: {utxo['amount_satoshis']} sats")
                print(f"   - TX: {utxo['tx_hash'][:32]}...")
                print(f"   - Reasons: {', '.join(item['reasons'])}")
            
            print(f"\n🛡️  Protection measures:")
            print(f"   1. DO NOT spend these UTXOs yet")
            print(f"   2. Use coin control to avoid them")
            print(f"   3. Consider them 'tainted' for privacy")
            print(f"   4. Label them in your wallet")
            print(f"   5. Use CoinJoin before spending")
            
            print(f"\n📚 What is a dust attack?")
            print(f"   - Attacker sends tiny amounts to many addresses")
            print(f"   - When you spend them, it links your addresses together")
            print(f"   - This breaks your privacy and anonymity")
            print(f"   - Professional attackers use this for tracking")
            
        else:
            print(f"\n✅ No dust attacks detected")
            print(f"   Your UTXOs appear normal")
        
        return {
            "success": True,
            "suspicious_count": len(suspicious_utxos),
            "suspicious_utxos": suspicious_utxos,
            "risk_level": "HIGH" if len(suspicious_utxos) > 5 else "LOW"
        }


class PrivacyAnalyzer:
    """
    Analyze transaction privacy and provide recommendations
    """
    
    @staticmethod
    def analyze_transaction_privacy(tx_inputs, tx_outputs):
        """
        Analyze privacy implications of a transaction
        """
        print("\n🕵️ PRIVACY ANALYZER")
        print("=" * 70)
        
        privacy_score = 100
        issues = []
        recommendations = []
        
        # Check 1: Too many inputs (links addresses)
        if len(tx_inputs) > 10:
            privacy_score -= 20
            issues.append("Too many inputs (links multiple addresses)")
            recommendations.append("Use coin control to select fewer inputs")
        
        # Check 2: Round number outputs (fingerprinting)
        for output in tx_outputs:
            if output['amount'] % 100000 == 0:  # Round to 0.001 BTC
                privacy_score -= 10
                issues.append("Round number output (fingerprinting risk)")
                recommendations.append("Add small random amounts to break patterns")
                break
        
        # Check 3: Address reuse
        input_addresses = [inp.get('address') for inp in tx_inputs]
        if len(input_addresses) != len(set(input_addresses)):
            privacy_score -= 30
            issues.append("Address reuse detected")
            recommendations.append("Never reuse addresses - use HD wallet")
        
        # Check 4: Change detection
        if len(tx_outputs) == 2:
            amounts = [o['amount'] for o in tx_outputs]
            if max(amounts) > min(amounts) * 10:
                privacy_score -= 15
                issues.append("Change output easily identifiable")
                recommendations.append("Consider CoinJoin or split outputs")
        
        print(f"\n🎯 Privacy Score: {privacy_score}/100")
        
        if privacy_score >= 80:
            print(f"   Rating: 🟢 EXCELLENT")
        elif privacy_score >= 60:
            print(f"   Rating: 🟡 GOOD")
        elif privacy_score >= 40:
            print(f"   Rating: 🟠 FAIR")
        else:
            print(f"   Rating: 🔴 POOR")
        
        if issues:
            print(f"\n⚠️  Privacy issues:")
            for issue in issues:
                print(f"   - {issue}")
        
        if recommendations:
            print(f"\n💡 Recommendations:")
            for rec in recommendations:
                print(f"   ✓ {rec}")
        
        print(f"\n🛡️  Advanced privacy techniques:")
        print(f"   - CoinJoin: Mix coins with others")
        print(f"   - PayJoin: Collaborative transaction")
        print(f"   - Schnorr signatures: Better privacy")
        print(f"   - Lightning Network: Off-chain transactions")
        
        return {
            "success": True,
            "privacy_score": privacy_score,
            "issues": issues,
            "recommendations": recommendations
        }


def demo():
    """Demo the dust consolidator"""
    print("=" * 70)
    print("💨 DUST CONSOLIDATOR & PRIVACY ANALYZER - DEMO")
    print("=" * 70)
    print()
    print("Choose operation:")
    print("  1. Analyze UTXOs")
    print("  2. Create consolidation transaction")
    print("  3. Detect dust attacks")
    print("  4. Analyze transaction privacy")
    print()
    
    choice = input("Select (1-4): ").strip()
    
    if choice == "1":
        # Demo with sample UTXOs
        sample_utxos = [
            {"tx_hash": secrets.token_hex(32), "vout": 0, "amount_satoshis": 500, "address": "1ABC..."},
            {"tx_hash": secrets.token_hex(32), "vout": 1, "amount_satoshis": 1000, "address": "1DEF..."},
            {"tx_hash": secrets.token_hex(32), "vout": 0, "amount_satoshis": 5000, "address": "1GHI..."},
            {"tx_hash": secrets.token_hex(32), "vout": 2, "amount_satoshis": 8000, "address": "1JKL..."},
            {"tx_hash": secrets.token_hex(32), "vout": 0, "amount_satoshis": 150000, "address": "1MNO..."},
        ]
        
        DustConsolidator.analyze_utxos(sample_utxos)
        
    elif choice == "2":
        sample_utxos = [
            {"tx_hash": secrets.token_hex(32), "vout": 0, "amount_satoshis": 5000, "address": "1ABC..."},
            {"tx_hash": secrets.token_hex(32), "vout": 1, "amount_satoshis": 6000, "address": "1DEF..."},
            {"tx_hash": secrets.token_hex(32), "vout": 0, "amount_satoshis": 7500, "address": "1GHI..."},
        ]
        
        DustConsolidator.create_consolidation_tx(
            sample_utxos,
            "1ConsolidatedAddress...",
            fee_rate=5
        )
        
    elif choice == "3":
        # Suspicious UTXOs (potential dust attack)
        suspicious = [
            {"tx_hash": secrets.token_hex(32), "vout": 0, "amount_satoshis": 546, "address": "1ABC...", "expected": False},
            {"tx_hash": secrets.token_hex(32), "vout": 1, "amount_satoshis": 1000, "address": "1DEF...", "expected": False},
            {"tx_hash": secrets.token_hex(32), "vout": 0, "amount_satoshis": 546, "address": "1GHI...", "expected": False},
        ]
        
        DustAttackDetector.analyze_for_dust_attack(suspicious, [])
        
    elif choice == "4":
        inputs = [
            {"address": "1Input1...", "amount": 50000},
            {"address": "1Input2...", "amount": 30000},
            {"address": "1Input3...", "amount": 20000},
        ]
        
        outputs = [
            {"address": "1Output1...", "amount": 100000},  # Round number
            {"address": "1Change...", "amount": 500},  # Small change
        ]
        
        PrivacyAnalyzer.analyze_transaction_privacy(inputs, outputs)


if __name__ == "__main__":
    demo()
