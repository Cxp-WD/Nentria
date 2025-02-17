import os
#import Nentria_sync as syncmanager
import nacl.secret
import nacl.utils
import hashlib, base64
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Cloud():
    def __init__(self, auth_file=None):
        self.gauth = GoogleAuth()
        self.drive = None
        self.authenticate(auth_file)

    def authenticate(self, auth_file=None):
        if auth_file: # Load the specified auth file
            self.gauth.LoadCredentialsFile(auth_file)
            try:
                if self.gauth.credentials is None or self.gauth.access_token_expired: self.gauth.Refresh()
                else: self.gauth.Authorize()
            except Exception:
                self.gauth.LocalWebserverAuth()
                self.save_credentials(auth_file)
        else: # Authenticate if no auth file is provided
            self.gauth.LocalWebserverAuth()
            self.save_credentials(auth_file)
        self.drive = GoogleDrive(self.gauth)

    def save_credentials(self, auth_file):
        about = self.drive.GetAbout()
        email = about['user']['emailAddress']
        auth_filename = email.split('@')[0] + '.auth'

        # Determine the next available number for the auth file
        i = 1
        while os.path.exists(f"{i}_{auth_filename}"):
            i += 1
        print(f"Saving credentials to {i}_{auth_filename}")

        # Save the credentials with the new filename
        self.gauth.SaveCredentialsFile(f"{i}_{auth_filename}")

    def upload(self, safe_name, content="Empty"):
        # Create a file and upload it
        file1 = self.drive.CreateFile({f'title': safe_name})  # Create a file with the title 'Hello.txt'
        file1.SetContentString(content)  # Set content of the file
        file1.Upload()

    def delete(self, safe_name):
        # Load the file to be deleted
        file_list = self.drive.ListFile({'q': f"title='{safe_name}'"}).GetList()
        if file_list:
            file1 = file_list[0]
            file1.Delete()  # Delete the uploaded file
            print(f"Deleted file: {safe_name}")
        else:
            print(f"File not found: {safe_name}")

    def read(self, read_file):
        file_list = self.drive.ListFile({'q': f"title='{read_file}'"}).GetList()
        if file_list:
            file1 = file_list[0]
            file1.GetContentFile(read_file)
            with open(read_file, 'r') as f:
                content = f.read()
            return content
        else: return "404"

class Cryptography:
    def hash(data): 
        return hashlib.sha256(data.encode()).hexdigest()

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
    def load_creds(auth_file):
        auth_ids = []
        for auths in Credentials.list_creds():
            auth_ids.append(auths.split("_"))
        # Example variable and search string
        variable = " ".join(auth_ids[0])  # Assuming you want to search in the first auth_id
        search_string = auth_file

        try:
            # Find the index of the search string
            index = variable.index(search_string)
    
            # Find the next entry after the search string
            next_entry_start = index + len(search_string) + 1  # Adjust to skip the underscore
            next_entry_end = variable.find(" ", next_entry_start)
    
            if next_entry_end == -1:
                next_entry_end = len(variable)
    
            next_entry = variable[next_entry_start:next_entry_end]

        except ValueError:
            print(f"'{search_string}' not found in the variable.")

        return Cloud(f"{auth_file}_{next_entry}")

    def save_creds():
        x=0
    
    def list_creds(): return [f for f in os.listdir() if f.endswith('.auth')]

class FileManagement:
    def add_entry():
        x=0

    def list_entries():
        x=0

    def delete_entry():
        x=0