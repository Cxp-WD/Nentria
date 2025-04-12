import os
import time
import yaml
import keyboard
from Archive.Nentria_lib import cryptomanager, syncmanager
import uuid

SAFE_FILE = "DO_NOT_DELETE_PASSWORD_MANAGER.safe"
LOCAL_FILE = "NentriaData/vaults/DO_NOT_DELETE_PASSWORD_MANAGER.safe"
PASSWORD = ""  # Default password for now

current_vault = None
list_of_vaults = []
tempkey, salt = cryptomanager.generate_key(PASSWORD)

if not os.path.isdir("NentriaData"):
    os.mkdir("NentriaData")
if not os.path.isdir("NentriaData/vaults"):
    os.mkdir("NentriaData/vaults")
if not os.path.isdir("NentriaData/keys"):
    os.mkdir("NentriaData/keys")

for vault in os.listdir("NentriaData/vaults/"):
    list_of_vaults.append(vault)

def create_vault():
    global current_vault, tempkey, salt
    vault_name = input("Enter vault name: ")
    password = input("Enter vault password: ")
    tempkey, salt = cryptomanager.generate_key(password)
    vault_path = f"NentriaData/vaults/{vault_name}.safe"
    with open(vault_path, 'w') as file:
        file.write("")
    list_of_vaults.append(vault_path)
    current_vault = vault_path
    print(f"Vault '{vault_name}' created and selected.")

def switch_vault():
    global current_vault, tempkey, salt
    print("Available vaults:")
    for i, vault in enumerate(list_of_vaults, start=1):
        print(f"{i}. {vault}")
    choice = int(input("Select vault number: ")) - 1
    if 0 <= choice < len(list_of_vaults):
        current_vault = list_of_vaults[choice]
        password = input("Enter vault password: ")
        tempkey, salt = cryptomanager.generate_key(password)
        print(f"Switched to vault: {current_vault}")
    else:
        print("Invalid choice.")

def main():
    if not os.path.isfile(".settings.yml"):
        auth_file = input("Type $make to create an auth file\nDefault Auth > ")
        with open(".settings.yml", 'w') as file:
            if auth_file == "$make":
                syncmanager.authenticate_and_upload(safe_name=SAFE_FILE)
                auth_file = "default.auth"  # Set a default auth file name
                syncmanager.authenticate_and_upload(safe_name=SAFE_FILE, auth_file=auth_file)
            settings = {'default_auth': f'{auth_file}'}
            yaml.dump(settings, file)
            default_auth = settings.get('default_auth')
    else:
        with open(".settings.yml", 'r') as file:
            settings = yaml.safe_load(file)
            default_auth = settings.get('default_auth')
            if not os.path.isfile(default_auth):
                syncmanager.authenticate_and_upload(safe_name=SAFE_FILE, auth_file=default_auth)
            else:
                syncmanager.authenticate_and_upload(auth_file=default_auth, safe_name=SAFE_FILE)
    print("Nentria CLI")
    if not os.path.isfile(LOCAL_FILE):
        with open(LOCAL_FILE, 'w') as file:
            file.write("")
    while True:
        if keyboard.is_pressed('alt+1'):
            print("Passwords")
            if os.path.isfile(current_vault) and os.path.getsize(current_vault) > 0:
                with open(current_vault, 'r') as file:  # Open the file in text mode
                    encrypted_content = file.read().strip()  # Read and strip any extra whitespace
                    print(cryptomanager.decrypt_message(encrypted_content, key=tempkey))
            else:
                print("No passwords found.")
            time.sleep(0.1)
        elif keyboard.is_pressed('alt+2'):
            print("Add Password")
            with open(current_vault, 'w') as file:  # Use 'w' to write in text mode
                password = input("Enter Password: ")
                encrypted_password = cryptomanager.encrypt_message(password, tempkey)
                file.write(encrypted_password.decode() + '\n')  # Write string directly
            time.sleep(0.1)
        elif keyboard.is_pressed('alt+0'):
            switch_vault()
            time.sleep(0.1)
        elif keyboard.is_pressed('alt+3'):
            create_vault()
            time.sleep(0.1)
# This is a command line version of Nentria.
# Useful for understanding how everything work.

SAFE_FILE = "DO_NOT_DELETE_PASSWORD_MANAGER.safe"

from NTM import Credentials,Cryptography,Cloud # Contains core functions
import base64

error_codes = [404,403]
hashed_password = None

def upload_file(cloud, safe_name, content):
    cloud.upload(safe_name, content)

def list_entries(cloud):
    if read_file(cloud, SAFE_FILE) == "": return "Empty"

def add_entry(cloud):
    if list_entries(cloud) == "Empty": empty_file = True
    print("Only one field are required")
    username = input("Username = ")
    email = input("Email = ")
    password = input("Password = ")
    totp_key = input("ToTP = ")
    passkey = input("Passkey = ")
    note = input("Note = ")
    urls = input("Urls = ")
    if empty_file:
        content = f"U^{username}^E^{email}^P^{password}^T^{totp_key}^K^{passkey}^N^{note}^W^{urls}"
        upload_file(cloud, SAFE_FILE, Cryptography.encrypt())

def edit_entry():
    x=0

def delete_entry():
    x=0

def delete_file(cloud):
    safe_name = input("Enter the name of the file to delete: ")
    status = cloud.delete(safe_name)
    if status == 200:
        print(f"File '{safe_name}' deleted successfully.")
    else:
        print(f"File '{safe_name}' not found.")

def read_file(cloud, read_file):
    content = cloud.read(read_file)
    if content != "404": return content
    else: return None

def main():
    for cred in Credentials.list_creds(): print(cred) # Lists authenticated users

    userid = input("User > ")
    if userid != "":
        temp = Credentials.load_creds(userid)

        if temp in error_codes: print(f"Failed to load user: {userid}")
        else: print(f"Loading user: {userid}")
        if temp not in error_codes:
            cloud = temp

            if not read_file(cloud, SAFE_FILE):
                upload_file(cloud, SAFE_FILE, "")
                while True:
                    security_password = input("Setup Wizard\nSet new pasword = ")
                    double_check = input("Type once again = ")
                    if security_password == double_check: 
                        print(f"This is your vault pin: {Cryptography.generate_pin(security_password)}")
                        break
                    else: print("\n\nPasswords dont match\n\n")
            else:
                global hashed_password
                if hashed_password:
                    security_pin = input("Leave empty to use password\nEnter PIN = ")
                    if security_pin == "":
                        security_password = input("Enter password = ")
                        security_pin = Cryptography.generate_pin(security_password)
                else:
                    security_password = input("This action requires using the password\nEnter password = ")
            security_pin = Cryptography.generate_pin(security_password)
            hashed_pin = Cryptography.hash(security_pin)
            hashed_password = Cryptography.hash(security_password)
            encryption_password = Cryptography.pin_to_key(hashed_password+hashed_pin)
            cryptography_instance = Cryptography()
            cryptography_instance.generate_key(encryption_password)
            encryption_key = cryptography_instance.box
            readable_key = base64.b64encode(encryption_key._key).decode('utf-8')
            print(f"For emergencies decrypt the safe using NaCL with this key: {readable_key}")

            print(f"Nentria - Commandline Utility\n\nSigned in as {userid}\n\n1 : list\n2 : delete\n3 : add\n4 : edit\n5 : signout\n6 : exit")
            while True:
                action = input("\n> ").strip().lower()
                if action == "1": list_entries(cloud)
                elif action == "2": delete_entry(cloud)
                elif action == "3": add_entry(cloud)
                elif action == "4": edit_entry(cloud)
                elif action == "5": main()
                elif action == "6": break
                else: print("Invalid action. Please choose again.")
    else: Credentials.authenticate(Cloud)
main()