from NTM import Cryptography

def generate_key(password):
    stored_pass = Cryptography.hash(password)
    pin = Cryptography.generate_pin(password)
    hashed_pin = Cryptography.hash(pin)
    combined_key = stored_pass + hashed_pin
    return combined_key[:32]  # Ensure the key is exactly 32 bytes

def encrypt(data, key):
    cryptomanager = Cryptography()
    cryptomanager.generate_key(key.encode())
    return cryptomanager.encrypt(data)

def decrypt(data, key):
    cryptomanager = Cryptography()
    cryptomanager.generate_key(key.encode())
    return cryptomanager.decrypt(data)

key = generate_key(input("Password > "))
text = input("Data > ")
encrypted = encrypt(text, key)
decrypted = decrypt(encrypted, key)
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
