import nacl.secret
import nacl.utils
import hashlib, base64

def generate_pin(text: str) -> str:
    """Hash input into a 6-digit PIN"""
    hash_obj = hashlib.sha256(text.encode())  
    hash_int = int(hash_obj.hexdigest(), 16)  
    pin = str(hash_int % 1000000).zfill(6)  # Ensure 6 digits
    return pin

def pin_to_key(pin: str) -> bytes:
    """Convert PIN to a 32-byte key"""
    # Hash the PIN to get a 32-byte key using SHA-256
    hash_obj = hashlib.sha256(pin.encode())  
    return hash_obj.digest()  # Return raw 32-byte hash

class SimpleEncryptor:
    def __init__(self, key: bytes):
        """Initialize with a 32-byte encryption key"""
        if len(key) != 32:
            raise ValueError("Encryption key must be exactly 32 bytes.")
        self.box = nacl.secret.SecretBox(key)

    def encrypt(self, message: str) -> str:
        """Encrypt a message and return a base64-encoded ciphertext with nonce"""
        encrypted = self.box.encrypt(message.encode())
        return base64.b64encode(encrypted).decode()  # Store nonce with encrypted message

    def decrypt(self, encrypted_message: str) -> str:
        """Decrypt a base64-encoded ciphertext with nonce and return the original message"""
        encrypted_bytes = base64.b64decode(encrypted_message)
        return self.box.decrypt(encrypted_bytes).decode()

# Example usage
if __name__ == "__main__":
    password = input("Password > ")
    if password == "":
        pin = input("PIN > ")
    else:
        pin = generate_pin(password)
        print(f"Generated PIN: {pin}")
    
    # Convert PIN to key using SHA-256 hash (32 bytes)
    key = pin_to_key(pin)
    print(f"Key (32 bytes): {key.hex()}")  # Print key as hex for clarity
    
    if input("Encrypt or Decrypt > ").lower() == "encrypt":
        encryptor = SimpleEncryptor(key)
        message = input("Message > ")
        encrypted_message = encryptor.encrypt(message)
        print(f"Encrypted: {encrypted_message}")
    else:
        encryptor = SimpleEncryptor(key)
        encrypted_message = input("Encrypted message > ")
        decrypted_message = encryptor.decrypt(encrypted_message)
        print(f"Decrypted: {decrypted_message}")
