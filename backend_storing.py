# filepath: /c:/Users/Admin/Documents/Koding/PASSWOWN/back-end.py
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from nacl import secret, utils
from nacl.encoding import Base64Encoder
import hashlib
import os

def hash_password_to_32_chars(password):
    # Hash the password using SHA-256 and get the first 32 characters
    return hashlib.sha256(password.encode()).hexdigest()[:32]

def generate_key(password):
    hashed_password = hash_password_to_32_chars(password)
    return hashed_password.encode()  # Ensure the key is 32 bytes long

def encrypt_message(message, key):
    box = secret.SecretBox(key)
    encrypted = box.encrypt(message.encode(), encoder=Base64Encoder)
    return encrypted

def decrypt_message(encrypted_message, key):
    box = secret.SecretBox(key)
    try:
        decrypted = box.decrypt(encrypted_message, encoder=Base64Encoder)
    except Exception:
        return "Wrong key or message corrupted"
    else:
        return decrypted.decode()

def decrypt_using_backup(encrypted_message, password):
    key = password.ljust(32)[:32].encode()  # Ensure the key is 32 bytes long
    return decrypt_message(encrypted_message, key)

def authenticate_and_upload(auth_file=None):
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

    # Create a file and upload it
    file1 = drive.CreateFile({f'title': input("Name > ")})  # Create a file with the title 'Hello.txt'
    file1.SetContentString(input("Content > "))  # Set content of the file
    file1.Upload()  # Upload the file
    print('File uploaded successfully')

def read_file(auth_file):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(auth_file)
    if gauth.credentials is None or gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': "title='Hello.txt'"}).GetList()
    if file_list:
        file1 = file_list[0]
        file1.GetContentFile('Hello.txt')
        with open('Hello.txt', 'r') as f:
            content = f.read()
        print(f"Content of Hello.txt: {content}")
    else:
        print("Hello.txt not found")

def list_auth_files():
    return [f for f in os.listdir() if f.endswith('.auth')]

def upload_menu():
    while True:
        print("Upload Menu")
        print("0. Authenticate and Save Credentials")
        auth_files = list_auth_files()
        for i, auth_file in enumerate(auth_files, start=1):
            print(f"{i}. Upload File using {auth_file}")
        print(f"{len(auth_files) + 1}. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '0':
            authenticate_and_upload()
        elif choice.isdigit() and 1 <= int(choice) <= len(auth_files):
            authenticate_and_upload(auth_files[int(choice) - 1])
        elif choice == str(len(auth_files) + 1):
            break
        else:
            print("Invalid choice. Please try again.")

def read_menu():
    while True:
        print("Read Menu")
        auth_files = list_auth_files()
        for i, auth_file in enumerate(auth_files, start=1):
            print(f"{i}. Read File using {auth_file}")
        print(f"{len(auth_files) + 1}. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice.isdigit() and 1 <= int(choice) <= len(auth_files):
            read_file(auth_files[int(choice) - 1])
        elif choice == str(len(auth_files) + 1):
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    try:
        while True:
            print("Quantum Secure Vault CLI")
            print("1. Upload Menu")
            print("2. Read Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                upload_menu()
            elif choice == '2':
                read_menu()
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()