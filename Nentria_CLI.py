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