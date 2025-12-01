#!/usr/bin/env python3
"""
🖼️ STEGANOGRAPHIC SEED ENCODER
Hide recovery phrases in images using LSB steganography
Undetectable backup method - looks like normal photos
"""

import hashlib
import secrets
from PIL import Image
import io
import numpy as np

class SteganographicEncoder:
    """
    Hide seed phrases in images using Least Significant Bit (LSB) steganography.
    The image looks identical to the human eye but contains hidden data.
    """
    
    @staticmethod
    def text_to_binary(text):
        """Convert text to binary string"""
        return ''.join(format(ord(char), '08b') for char in text)
    
    @staticmethod
    def binary_to_text(binary):
        """Convert binary string back to text"""
        chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
        return ''.join(chr(int(char, 2)) for char in chars if char)
    
    @staticmethod
    def encode_in_image(image_path, secret_text, password, output_path):
        """
        Encode secret text into an image using LSB steganography
        
        Args:
            image_path: Path to cover image (PNG/JPG)
            secret_text: Text to hide (seed phrase, private key, etc.)
            password: Encryption password
            output_path: Where to save the stego image
        
        Returns:
            dict with encoding results
        """
        print("\n🖼️  STEGANOGRAPHIC ENCODER")
        print("=" * 70)
        
        try:
            # Load image
            img = Image.open(image_path)
            img_array = np.array(img)
            
            print(f"\n📸 Image loaded: {img.size[0]}x{img.size[1]} pixels")
            print(f"   Format: {img.format}")
            print(f"   Mode: {img.mode}")
            
            # Encrypt the secret text
            key = hashlib.sha256(password.encode()).digest()
            encrypted = SteganographicEncoder._xor_encrypt(secret_text, key)
            
            # Add magic header and length
            header = "STEGSEED"
            length = len(encrypted)
            full_message = f"{header}|{length}|{encrypted}"
            
            # Convert to binary
            binary_message = SteganographicEncoder.text_to_binary(full_message)
            binary_message += '1111111111111110'  # Delimiter
            
            print(f"\n🔐 Secret encrypted: {len(secret_text)} chars")
            print(f"   Binary size: {len(binary_message)} bits")
            
            # Check capacity
            max_bits = img_array.size
            if len(binary_message) > max_bits:
                return {
                    "success": False,
                    "error": f"Image too small. Need {len(binary_message)} bits, have {max_bits}"
                }
            
            print(f"   Image capacity: {max_bits} bits")
            print(f"   Utilization: {len(binary_message)/max_bits*100:.2f}%")
            
            # Flatten image array for encoding
            flat_img = img_array.flatten()
            
            # Encode by modifying LSB
            for i, bit in enumerate(binary_message):
                flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
            
            # Reshape and save
            stego_array = flat_img.reshape(img_array.shape)
            stego_img = Image.fromarray(stego_array.astype('uint8'))
            stego_img.save(output_path, format='PNG')
            
            print(f"\n✅ Encoding complete!")
            print(f"   Saved to: {output_path}")
            print(f"\n⚠️  IMPORTANT:")
            print(f"   - Keep original image safe (needed for verification)")
            print(f"   - Remember your password!")
            print(f"   - Use PNG format (JPG compression destroys hidden data)")
            
            return {
                "success": True,
                "output_path": output_path,
                "bits_used": len(binary_message),
                "capacity": max_bits,
                "utilization": f"{len(binary_message)/max_bits*100:.2f}%"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def decode_from_image(image_path, password):
        """
        Extract hidden text from a stego image
        
        Args:
            image_path: Path to stego image
            password: Decryption password
        
        Returns:
            dict with decoded message
        """
        print("\n🔍 STEGANOGRAPHIC DECODER")
        print("=" * 70)
        
        try:
            # Load image
            img = Image.open(image_path)
            img_array = np.array(img)
            flat_img = img_array.flatten()
            
            print(f"\n📸 Image loaded: {img.size[0]}x{img.size[1]} pixels")
            
            # Extract LSBs
            binary_data = ''.join(str(pixel & 1) for pixel in flat_img)
            
            # Find delimiter
            delimiter = '1111111111111110'
            end_index = binary_data.find(delimiter)
            
            if end_index == -1:
                return {"success": False, "error": "No hidden data found"}
            
            binary_message = binary_data[:end_index]
            
            # Convert to text
            full_message = SteganographicEncoder.binary_to_text(binary_message)
            
            # Parse header
            if not full_message.startswith("STEGSEED|"):
                return {"success": False, "error": "Invalid format or corrupted data"}
            
            parts = full_message.split('|')
            if len(parts) < 3:
                return {"success": False, "error": "Corrupted data"}
            
            encrypted = '|'.join(parts[2:])
            
            # Decrypt
            key = hashlib.sha256(password.encode()).digest()
            try:
                decrypted = SteganographicEncoder._xor_decrypt(encrypted, key)
            except:
                return {"success": False, "error": "Wrong password"}
            
            print(f"\n✅ Decoding successful!")
            print(f"   Message length: {len(decrypted)} chars")
            print(f"\n📋 Recovered secret:")
            print(f"   {decrypted}")
            
            return {
                "success": True,
                "message": decrypted,
                "length": len(decrypted)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def _xor_encrypt(text, key):
        """Simple XOR encryption"""
        result = []
        for i, char in enumerate(text):
            result.append(chr(ord(char) ^ key[i % len(key)]))
        return ''.join(result)
    
    @staticmethod
    def _xor_decrypt(encrypted, key):
        """Simple XOR decryption"""
        return SteganographicEncoder._xor_encrypt(encrypted, key)
    
    @staticmethod
    def create_dummy_image(width=800, height=600, output_path="dummy.png"):
        """
        Create a dummy image for testing (colorful noise pattern)
        """
        # Create random RGB noise
        array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        img = Image.fromarray(array, 'RGB')
        img.save(output_path)
        print(f"✅ Created dummy image: {output_path} ({width}x{height})")
        return output_path


class SeedPhraseSteganographer:
    """
    Specialized tool for hiding BIP39 seed phrases in images
    """
    
    @staticmethod
    def hide_seed_phrase(seed_phrase, image_path, password, output_path):
        """
        Hide a seed phrase in an image with additional metadata
        """
        print("\n🌱 SEED PHRASE STEGANOGRAPHER")
        print("=" * 70)
        
        # Validate seed phrase
        words = seed_phrase.strip().split()
        if len(words) not in [12, 15, 18, 21, 24]:
            return {
                "success": False,
                "error": f"Invalid seed phrase length: {len(words)} words (expected 12/15/18/21/24)"
            }
        
        print(f"\n✅ Valid seed phrase: {len(words)} words")
        
        # Create metadata
        import datetime
        metadata = {
            "type": "BIP39_SEED",
            "word_count": len(words),
            "timestamp": datetime.datetime.now().isoformat(),
            "seed": seed_phrase
        }
        
        # Convert to JSON string
        import json
        json_data = json.dumps(metadata)
        
        # Encode in image
        result = SteganographicEncoder.encode_in_image(
            image_path, json_data, password, output_path
        )
        
        if result["success"]:
            print(f"\n🎉 Seed phrase successfully hidden!")
            print(f"\n💡 Recovery instructions:")
            print(f"   1. Keep the stego image file: {output_path}")
            print(f"   2. Remember password: {'*' * len(password)}")
            print(f"   3. Use decoder to extract when needed")
        
        return result
    
    @staticmethod
    def recover_seed_phrase(image_path, password):
        """
        Recover seed phrase from stego image
        """
        result = SteganographicEncoder.decode_from_image(image_path, password)
        
        if result["success"]:
            try:
                import json
                metadata = json.loads(result["message"])
                
                if metadata.get("type") == "BIP39_SEED":
                    print(f"\n🌱 Seed phrase recovered!")
                    print(f"   Words: {metadata['word_count']}")
                    print(f"   Created: {metadata['timestamp']}")
                    print(f"\n🔑 SEED PHRASE:")
                    print(f"   {metadata['seed']}")
                    
                    return {
                        "success": True,
                        "seed_phrase": metadata["seed"],
                        "word_count": metadata["word_count"],
                        "timestamp": metadata["timestamp"]
                    }
            except:
                pass
        
        return result


def demo():
    """Demo the steganographic encoder"""
    print("=" * 70)
    print("🖼️  STEGANOGRAPHIC SEED ENCODER - DEMO")
    print("=" * 70)
    print()
    print("Choose operation:")
    print("  1. Hide seed phrase in image")
    print("  2. Recover seed phrase from image")
    print("  3. Create test image")
    print()
    
    choice = input("Select (1-3): ").strip()
    
    if choice == "1":
        seed = input("\nEnter seed phrase (12-24 words): ").strip()
        image = input("Image path (or press Enter for dummy): ").strip()
        
        if not image:
            image = SteganographicEncoder.create_dummy_image(
                width=1200, height=800, output_path="/tmp/cover.png"
            )
        
        password = input("Encryption password: ").strip()
        output = input("Output path (default: stego_seed.png): ").strip() or "stego_seed.png"
        
        SeedPhraseSteganographer.hide_seed_phrase(seed, image, password, output)
        
    elif choice == "2":
        image = input("\nStego image path: ").strip()
        password = input("Password: ").strip()
        
        SeedPhraseSteganographer.recover_seed_phrase(image, password)
        
    elif choice == "3":
        width = int(input("Width (default 1200): ").strip() or "1200")
        height = int(input("Height (default 800): ").strip() or "800")
        output = input("Output path (default: test_image.png): ").strip() or "test_image.png"
        
        SteganographicEncoder.create_dummy_image(width, height, output)


if __name__ == "__main__":
    demo()
