SAFE_FILE = "DO_NOT_DELETE_PASSWORD_MANAGER.safe"
LOCAL_FILE = "DO_NOT_DELETE_PASSWORD_MANAGER.safe"

PASSOWRD = "password123" # Default password for now

from Nentria_lib import *
import keyboard, yaml, os, time

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
    while True:
        if keyboard.is_pressed('f1'):
            print("Passwords")
            with open(LOCAL_FILE, 'r') as file:
                tempkey = cryptomanager.generate_key(PASSOWRD)
                #print(cryptomanager.decrypt_message(file.read(), key=tempkey))
                print(file.read())
                time.sleep(0.1)

main()