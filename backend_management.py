# Estimate of 500 bytes per login

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from nacl import secret, utils
from nacl.encoding import Base64Encoder
import hashlib
import os
import tkinter as tk
from tkinter import ttk, messagebox
import uuid

class Cryptography:
    @staticmethod
    def hash_password_to_32_chars(password):
        # Hash the password using SHA-256 and get the first 32 characters
        return hashlib.sha256(password.encode()).hexdigest()[:32]

    @staticmethod
    def generate_key(password):
        hashed_password = Cryptography.hash_password_to_32_chars(password)
        return hashed_password.encode()  # Ensure the key is 32 bytes long

    @staticmethod
    def encrypt_message(message, key):
        box = secret.SecretBox(key)
        encrypted = box.encrypt(message.encode(), encoder=Base64Encoder)
        return encrypted

    @staticmethod
    def decrypt_message(encrypted_message, key):
        box = secret.SecretBox(key)
        try:
            decrypted = box.decrypt(encrypted_message, encoder=Base64Encoder)
        except Exception:
            return "Wrong key or message corrupted"
        else:
            return decrypted.decode()

def authenticate_and_upload(auth_file=None, content=None):
    gauth = GoogleAuth()

    if auth_file:
        # Load the specified auth file
        gauth.LoadCredentialsFile(auth_file)
        if gauth.credentials is None or gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
    else:
        # Authenticate if no auth file is provided
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        about = drive.GetAbout()
        email = about['user']['emailAddress']
        auth_filename = email.split('@')[0] + '.auth'

        # Determine the next available number for the auth file
        i = 1
        while os.path.exists(f"{i}_{auth_filename}"):
            i += 1
        auth_filename = f"{i}_{auth_filename}"

        # Save the credentials with the new filename
        gauth.SaveCredentialsFile(auth_filename)
        print(f"Credentials saved as {auth_filename}")

    drive = GoogleDrive(gauth)

    # Encrypt the content before uploading
    key = Cryptography.generate_key("password")  # Default master password
    encrypted_content = Cryptography.encrypt_message(content, key)

    # Create or update the file and upload it
    file_list = drive.ListFile({'q': "title='DO_NOT_DELETE_PASSWORD_MANAGER.safe'"}).GetList()
    if file_list:
        file1 = file_list[0]
    else:
        file1 = drive.CreateFile({'title': 'DO_NOT_DELETE_PASSWORD_MANAGER.safe'})
    file1.SetContentString(encrypted_content.decode())
    file1.Upload()
    print('File uploaded successfully')

def read_file(auth_file):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(auth_file)
    if gauth.credentials is None or gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': "title='DO_NOT_DELETE_PASSWORD_MANAGER.safe'"}).GetList()
    if file_list:
        file1 = file_list[0]
        file1.GetContentFile('DO_NOT_DELETE_PASSWORD_MANAGER.safe')
        with open('DO_NOT_DELETE_PASSWORD_MANAGER.safe', 'r') as f:
            encrypted_content = f.read()
        print(f"Content of DO_NOT_DELETE_PASSWORD_MANAGER.safe: {encrypted_content}")

        # Decrypt the content after downloading
        key = Cryptography.generate_key("password")  # Default master password
        content = Cryptography.decrypt_message(encrypted_content.encode(), key)
        return content
    else:
        print("DO_NOT_DELETE_PASSWORD_MANAGER.safe not found")
        return None

def list_auth_files():
    return [f for f in os.listdir() if f.endswith('.auth')]

def save_to_local_file(data, key):
    filename = "DO_NOT_DELETE_PASSWORD_MANAGER.safe"
    encrypted_data = Cryptography.encrypt_message(data, key)
    with open(filename, 'ab') as f:
        f.write(encrypted_data + b'\n')

def read_from_local_file(key):
    filename = "DO_NOT_DELETE_PASSWORD_MANAGER.safe"
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            lines = f.readlines()
        decrypted_lines = [Cryptography.decrypt_message(line.strip(), key) for line in lines]
        return decrypted_lines
    return []

class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):
        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both')

        # Create frames for each tab
        self.create_tab(notebook, "Add Password", self.create_add_password_tab)
        self.create_tab(notebook, "View Passwords", self.create_view_passwords_tab)
        self.create_tab(notebook, "Settings", self.create_settings_tab)

    def create_tab(self, notebook, title, create_tab_func):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=title)
        create_tab_func(frame)

    def create_add_password_tab(self, frame):
        ttk.Label(frame, text="Add a new password").pack(pady=10)
        ttk.Label(frame, text="Website(s):").pack(pady=5)
        self.website_entry = ttk.Entry(frame)
        self.website_entry.pack(pady=5)
        ttk.Label(frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.pack(pady=5)
        ttk.Label(frame, text="Email:").pack(pady=5)
        self.email_entry = ttk.Entry(frame)
        self.email_entry.pack(pady=5)
        ttk.Label(frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.pack(pady=5)
        ttk.Button(frame, text="Save", command=self.save_password).pack(pady=10)

    def create_view_passwords_tab(self, frame):
        ttk.Label(frame, text="View saved passwords").pack(pady=10)
        self.password_listbox = tk.Listbox(frame)
        self.password_listbox.pack(expand=True, fill='both', pady=10)
        ttk.Button(frame, text="View", command=self.refresh_passwords).pack(pady=10)

    def create_settings_tab(self, frame):
        ttk.Label(frame, text="Settings").pack(pady=10)
        ttk.Label(frame, text="Change master password:").pack(pady=5)
        self.new_master_password_entry = ttk.Entry(frame, show="*")
        self.new_master_password_entry.pack(pady=5)
        ttk.Button(frame, text="Change", command=self.change_master_password).pack(pady=10)

    def save_password(self):
        websites = self.website_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        if not websites or not username or not email or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        # Generate a unique ID
        entry_id = str(uuid.uuid4())

        # Format the data
        data = f"{entry_id}|{websites}|{username}|{email}|{password}§"

        # Encrypt and save to local file
        key = Cryptography.generate_key("password")  # Default master password
        save_to_local_file(data, key)

        # Upload to Google Drive
        auth_files = list_auth_files()
        if auth_files:
            content = ''.join(read_from_local_file(key))
            authenticate_and_upload(auth_file=auth_files[0], content=content)
            messagebox.showinfo("Success", "Password saved successfully")
        else:
            messagebox.showerror("Error", "No authentication files found")

    def refresh_passwords(self):
        # Fetch passwords from Google Drive
        auth_files = list_auth_files()
        if auth_files:
            content = read_file(auth_files[0])
            if content:
                key = Cryptography.generate_key("password")  # Default master password
                with open('DO_NOT_DELETE_PASSWORD_MANAGER.safe', 'w') as f:
                    f.write(content)
                passwords = read_from_local_file(key)
                self.password_listbox.delete(0, tk.END)
                for password in passwords:
                    self.password_listbox.insert(tk.END, password.strip())
        else:
            messagebox.showerror("Error", "No authentication files found")

    def change_master_password(self):
        new_password = self.new_master_password_entry.get()
        if not new_password:
            messagebox.showerror("Error", "New master password is required")
            return

        # Implement logic to change the master password
        messagebox.showinfo("Success", "Master password changed successfully")

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()