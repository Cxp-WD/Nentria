SAFE_FILE = "DO_NOT_DELETE_PASSWORD_MANAGER.safe"
LOCAL_FILE = "DO_NOT_DELETE_PASSWORD_MANAGER.safe"

PASSOWRD = "password123" # Default password for now

from Nentria_lib import *
import keyboard, yaml, os, time

tempkey = cryptomanager.generate_key(PASSOWRD)

def main():
    if not os.path.isfile(".settings.yml"):
        auth_file = input("Type $make to create a auth file\nDefault Auth > ")
        with open(".settings.yml", 'w') as file:
            if auth_file == "$make":
                print("a")
                syncmanager.authenticate_and_upload(safe_name=SAFE_FILE)
            settings = {'default_auth': f'{auth_file}'}
            yaml.dump(settings, file)
            default_auth = settings.get('default_auth')
    else:
        with open(".settings.yml", 'r') as file:
            settings = yaml.safe_load(file)
            default_auth = settings.get('default_auth')
            syncmanager.authenticate_and_upload(auth_file=default_auth, safe_name=SAFE_FILE)
    print("Nentria CLI")
    if not os.path.isfile(LOCAL_FILE):
        with open(LOCAL_FILE, 'w') as file:
            file.write("")
    while True:
        if keyboard.is_pressed('f1'):
            print("Passwords")
            if os.path.isfile(LOCAL_FILE) and os.path.getsize(LOCAL_FILE) > 0:
                with open(LOCAL_FILE, 'r') as file:  # Open the file in text mode
                    encrypted_content = file.read().strip()  # Read and strip any extra whitespace
                    print(cryptomanager.decrypt_message(encrypted_content, key=tempkey))
            else:
                print("No passwords found.")
            time.sleep(0.1)
        elif keyboard.is_pressed('f2'):
            print("Add Password")
            with open(LOCAL_FILE, 'w') as file:  # Use 'w' to write in text mode
                password = input("Enter Password: ")
                encrypted_password = cryptomanager.encrypt_message(password, tempkey)
                file.write(encrypted_password + '\n')  # Write string directly

main()