import os
import Nentria_sync as syncmanager
import nacl.secret
import nacl.utils
import hashlib, base64
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

class Cryptography:
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

    def generate_key(self, key: bytes):
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


class Credentials:
    def load_creds():
        x=0

    def save_creds():
        x=0
    
    def list_creds():
        return [f for f in os.listdir() if f.endswith('.auth')]

class FileManagement:
    def add_entry():
        x=0

    def list_entries():
        x=0

    def delete_entry():
        x=0

def upload_menu():
    while True:
        print("Upload Menu")
        print("0. Authenticate and Save Credentials")
        auth_files = syncmanager.list_auth_files()
        for i, auth_file in enumerate(auth_files, start=1):
            print(f"{i}. Upload File using {auth_file}")
        print(f"{len(auth_files) + 1}. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '0':
            syncmanager.authenticate_and_upload()
        elif choice.isdigit() and 1 <= int(choice) <= len(auth_files):
            syncmanager.authenticate_and_upload(auth_files[int(choice) - 1])
        elif choice == str(len(auth_files) + 1):
            break
        else:
            print("Invalid choice. Please try again.")

def read_menu():
    while True:
        print("Read Menu")
        auth_files = syncmanager.list_auth_files()
        for i, auth_file in enumerate(auth_files, start=1): print(f"{i}. Read File using {auth_file}")
        print(f"{len(auth_files) + 1}. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice.isdigit() and 1 <= int(choice) <= len(auth_files):
            syncmanager.read_file(auth_files[int(choice) - 1])
        elif choice == str(len(auth_files) + 1):
            break
        else:
            print("Invalid choice. Please try again.")
