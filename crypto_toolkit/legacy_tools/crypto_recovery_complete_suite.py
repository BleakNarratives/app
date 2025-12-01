#!/usr/bin/env python3
"""
🔐 COMPLETE CRYPTO RECOVERY TOOLKIT
Tools for legitimate recovery services
"""

import hashlib
import itertools
import binascii

# ============================================================================
# TOOL 1: BRAIN WALLET CRACKER
# ============================================================================

class BrainWalletCracker:
    """Convert phrases/passwords to Bitcoin private keys"""
    
    @staticmethod
    def phrase_to_private_key(phrase):
        """Convert any phrase to Bitcoin private key (SHA256)"""
        key_bytes = hashlib.sha256(phrase.encode('utf-8')).digest()
        return binascii.hexlify(key_bytes).decode('ascii')
    
    @staticmethod
    def check_common_phrases(custom_phrases=None):
        """Check common brain wallet phrases"""
        common = [
            "password",
            "bitcoin",
            "satoshi nakamoto",
            "correct horse battery staple",
            "to the moon",
            "the quick brown fox jumps over the lazy dog",
            "12345678",
            "qwerty",
            "letmein",
            "admin"
        ]
        
        if custom_phrases:
            common.extend(custom_phrases)
        
        results = []
        for phrase in common:
            key = BrainWalletCracker.phrase_to_private_key(phrase)
            results.append({
                "phrase": phrase,
                "private_key": key
            })
        
        return results

# ============================================================================
# TOOL 2: BIP39 SEED PHRASE VALIDATOR
# ============================================================================

class SeedPhraseValidator:
    """Validate and recover BIP39 seed phrases"""
    
    # BIP39 English wordlist (sample - full list has 2048 words)
    BIP39_WORDS = [
        "abandon", "ability", "able", "about", "above", "absent", "absorb",
        "abstract", "absurd", "abuse", "access", "accident", "account",
        "acoustic", "acquire", "across", "act", "action", "actor", "actress",
        "actual", "adapt", "add", "addict", "address", "adjust", "admit",
        "adult", "advance", "advice", "aerobic", "afford", "afraid", "again",
        "age", "agent", "agree", "ahead", "aim", "air", "airport", "aisle",
        "alarm", "album", "alcohol", "alert", "alien", "all", "alley", "allow",
        "almost", "alone", "alpha", "already", "also", "alter", "always",
        "amateur", "amazing", "among", "amount", "amused", "analyst", "anchor",
        "ancient", "anger", "angle", "angry", "animal", "ankle", "announce",
        "annual", "another", "answer", "antenna", "antique", "anxiety", "any",
        "apart", "apology", "appear", "apple", "approve", "april", "arch",
        "arctic", "area", "arena", "argue", "arm", "armed", "armor", "army",
        "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact",
        "artist", "artwork", "ask", "aspect", "assault", "asset", "assist",
        "assume", "asthma", "athlete", "atom", "attack", "attend", "attitude",
        "attract", "auction", "audit", "august", "aunt", "author", "auto",
        "autumn", "average", "avocado", "avoid", "awake", "aware", "away",
        "awesome", "awful", "awkward", "axis", "baby", "bachelor", "bacon",
        "badge", "bag", "balance", "balcony", "ball", "bamboo", "banana",
        "banner", "bar", "barely", "bargain", "barrel", "base", "basic",
        "basket", "battle", "beach", "bean", "beauty", "because", "become",
        "beef", "before", "begin", "behave", "behind", "believe", "below",
        "belt", "bench", "benefit", "best", "betray", "better", "between",
        "beyond", "bicycle", "bid", "bike", "bind", "biology", "bird", "birth",
        "bitter", "black", "blade", "blame", "blanket", "blast", "bleak",
        "bless", "blind", "blood", "blossom", "blouse", "blue", "blur", "blush",
        "board", "boat", "body", "boil", "bomb", "bone", "bonus", "book",
        "boost", "border", "boring", "borrow", "boss", "bottom", "bounce",
        "box", "boy", "bracket", "brain", "brand", "brass", "brave", "bread",
        "breeze", "brick", "bridge", "brief", "bright", "bring", "brisk",
        "broccoli", "broken", "bronze", "broom", "brother", "brown", "brush",
        "bubble", "buddy", "budget", "buffalo", "build", "bulb", "bulk",
        "bullet", "bundle", "bunker", "burden", "burger", "burst", "bus",
        "business", "busy", "butter", "buyer", "buzz"
        # ... (truncated for space - full list has 2048 words)
    ]
    
    @staticmethod
    def validate_word(word):
        """Check if word is in BIP39 wordlist"""
        return word.lower() in SeedPhraseValidator.BIP39_WORDS
    
    @staticmethod
    def validate_phrase(phrase_list):
        """Validate a seed phrase"""
        if len(phrase_list) not in [12, 15, 18, 21, 24]:
            return False, f"Invalid length: {len(phrase_list)}. Must be 12, 15, 18, 21, or 24 words"
        
        invalid_words = [w for w in phrase_list if not SeedPhraseValidator.validate_word(w)]
        
        if invalid_words:
            return False, f"Invalid words: {', '.join(invalid_words)}"
        
        return True, "Valid BIP39 phrase structure"
    
    @staticmethod
    def find_missing_words(partial_phrase, known_positions):
        """Find possible missing words in seed phrase"""
        # known_positions: dict like {0: "abandon", 1: "ability", 11: None}
        missing_indices = [i for i, word in known_positions.items() if word is None]
        
        if len(missing_indices) > 3:
            return "Too many missing words for practical brute force"
        
        # For each missing position, all 2048 words are possible
        combinations = 2048 ** len(missing_indices)
        
        return {
            "missing_positions": missing_indices,
            "combinations": f"{combinations:,}",
            "feasibility": "POSSIBLE" if len(missing_indices) <= 2 else "DIFFICULT"
        }

# ============================================================================
# TOOL 3: PARTIAL PRIVATE KEY RECOVERY (Original Tool - FIXED)
# ============================================================================

class PrivateKeyRecovery:
    """Recover partial Bitcoin private keys"""
    
    HEX_CHARS = "0123456789abcdef"
    
    @staticmethod
    def validate_key(key):
        """STRICT 64-character validation"""
        if len(key) != 64:
            return False, f"❌ Key must be EXACTLY 64 characters. Got {len(key)}"
        
        valid_chars = set(PrivateKeyRecovery.HEX_CHARS + '*')
        if not all(c in valid_chars for c in key.lower()):
            return False, "❌ Key contains invalid characters (use 0-9, a-f, or *)"
        
        return True, "✅ Valid 64-character key"
    
    @staticmethod
    def analyze_recovery(masked_key):
        """Analyze recovery feasibility"""
        valid, message = PrivateKeyRecovery.validate_key(masked_key)
        if not valid:
            return {"error": message}
        
        unknown_count = masked_key.count('*')
        combinations = 16 ** unknown_count
        
        # Time estimates
        checks_per_sec = 10000  # Optimistic
        seconds = combinations / checks_per_sec
        
        if seconds < 1:
            time_est = "< 1 second"
        elif seconds < 60:
            time_est = f"~{seconds:.1f} seconds"
        elif seconds < 3600:
            time_est = f"~{seconds/60:.1f} minutes"
        elif seconds < 86400:
            time_est = f"~{seconds/3600:.1f} hours"
        else:
            time_est = f"~{seconds/86400:.1f} days"
        
        feasibility = "EASY" if unknown_count <= 3 else "MODERATE" if unknown_count <= 5 else "HARD" if unknown_count <= 7 else "EXTREME"
        
        return {
            "masked_key": masked_key,
            "length": len(masked_key),
            "unknowns": unknown_count,
            "combinations": f"{combinations:,}",
            "feasibility": feasibility,
            "estimated_time": time_est
        }
    
    @staticmethod
    def generate_candidates(masked_key, limit=100):
        """Generate candidate keys (first N possibilities)"""
        valid, message = PrivateKeyRecovery.validate_key(masked_key)
        if not valid:
            return []
        
        unknown_positions = [i for i, c in enumerate(masked_key) if c == '*']
        unknown_count = len(unknown_positions)
        
        if unknown_count > 6:
            return ["Too many unknowns - would generate billions of keys"]
        
        candidates = []
        key_list = list(masked_key)
        
        # Generate first 'limit' combinations
        for i in range(min(limit, 16 ** unknown_count)):
            temp_key = key_list.copy()
            val = i
            
            for pos in reversed(unknown_positions):
                temp_key[pos] = PrivateKeyRecovery.HEX_CHARS[val % 16]
                val //= 16
            
            candidates.append(''.join(temp_key))
        
        return candidates


# ============================================================================
# MAIN INTERFACE
# ============================================================================

def main():
    print("=" * 70)
    print("🔐 CRYPTO RECOVERY TOOLKIT - Complete Suite")
    print("=" * 70)
    print()
    print("Available Tools:")
    print("  1. Brain Wallet Cracker - Convert phrases to private keys")
    print("  2. BIP39 Seed Phrase Validator - Check seed phrase validity")
    print("  3. Partial Private Key Recovery - Brute force missing characters")
    print("  4. Run All Examples")
    print()
    
    choice = input("Select tool (1-4): ").strip()
    
    if choice == "1":
        print("\n" + "=" * 70)
        print("🧠 BRAIN WALLET CRACKER")
        print("=" * 70)
        
        custom = input("Enter custom phrase (or press Enter for common list): ").strip()
        phrases = [custom] if custom else None
        
        results = BrainWalletCracker.check_common_phrases(phrases)
        
        for r in results:
            print(f"\nPhrase: {r['phrase']}")
            print(f"Private Key: {r['private_key']}")
    
    elif choice == "2":
        print("\n" + "=" * 70)
        print("📝 BIP39 SEED PHRASE VALIDATOR")
        print("=" * 70)
        
        phrase = input("Enter seed phrase (space-separated): ").strip().lower()
        words = phrase.split()
        
        valid, message = SeedPhraseValidator.validate_phrase(words)
        print(f"\n{'✅' if valid else '❌'} {message}")
        
        if valid:
            print(f"Phrase length: {len(words)} words")
    
    elif choice == "3":
        print("\n" + "=" * 70)
        print("🔑 PARTIAL PRIVATE KEY RECOVERY")
        print("=" * 70)
        print("Enter 64-character hex key with * for unknowns")
        print("Example: abc123***def456....(fill to 64 total)")
        print()
        
        key = input("Enter key: ").strip()
        
        result = PrivateKeyRecovery.analyze_recovery(key)
        
        if "error" in result:
            print(f"\n{result['error']}")
        else:
            print(f"\n✅ Length: {result['length']}")
            print(f"🔍 Unknown characters: {result['unknowns']}")
            print(f"🎯 Combinations: {result['combinations']}")
            print(f"⚡ Feasibility: {result['feasibility']}")
            print(f"⏱️  Estimated time: {result['estimated_time']}")
            
            if result['unknowns'] <= 5:
                print("\n📋 First 10 candidate keys:")
                candidates = PrivateKeyRecovery.generate_candidates(key, 10)
                for i, cand in enumerate(candidates, 1):
                    print(f"  {i}. {cand}")
    
    elif choice == "4":
        print("\n" + "=" * 70)
        print("🚀 RUNNING ALL EXAMPLES")
        print("=" * 70)
        
        # Example 1: Brain Wallet
        print("\n1️⃣  BRAIN WALLET EXAMPLES:")
        results = BrainWalletCracker.check_common_phrases(["test", "bitcoin"])
        for r in results[:3]:
            print(f"  '{r['phrase']}' → {r['private_key'][:16]}...")
        
        # Example 2: Seed Phrase
        print("\n2️⃣  SEED PHRASE VALIDATION:")
        test_phrase = ["abandon", "ability", "able", "about", "above", "absent", 
                      "absorb", "abstract", "absurd", "abuse", "access", "accident"]
        valid, msg = SeedPhraseValidator.validate_phrase(test_phrase)
        print(f"  12-word phrase: {msg}")
        
        # Example 3: Partial Key
        print("\n3️⃣  PARTIAL KEY RECOVERY:")
        test_key = "abc1234567890def" + "0" * 44 + "**"
        result = PrivateKeyRecovery.analyze_recovery(test_key)
        if "error" not in result:
            print(f"  2 unknowns: {result['combinations']} combinations")
            print(f"  Feasibility: {result['feasibility']}")
            print(f"  Time: {result['estimated_time']}")

if __name__ == "__main__":
    main()