import os
import time
import yaml
import keyboard
from Nentria_lib import cryptomanager, syncmanager
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

main()