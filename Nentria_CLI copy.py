# This is a command line version of Nentria.
# Useful for understanding how everything work.

from NTM import Credentials,Cryptography,Cloud,FileManagement # Contains core functions

error_codes = [404,403]

def upload_file(cloud):
    safe_name = input("Enter the name of the file to upload: ")
    content = input("Enter the content of the file: ")
    cloud.upload(safe_name, content)
    print(f"File '{safe_name}' uploaded successfully.")

def delete_file(cloud):
    safe_name = input("Enter the name of the file to delete: ")
    status = cloud.delete(safe_name)
    if status == 200:
        print(f"File '{safe_name}' deleted successfully.")
    else:
        print(f"File '{safe_name}' not found.")

def read_file(cloud):
    read_file = input("Enter the name of the file to read: ")
    content = cloud.read(read_file)
    if content != "404":
        print(f"Content of '{read_file}':\n{content}")
    else:
        print(f"File '{read_file}' not found.")

def main():
    for cred in Credentials.list_creds(): print(cred) # Lists authenticated users

    userid = input("User > ")
    if userid != "":
        temp = Credentials.load_creds(userid)

        if temp in error_codes: print(f"Failed to load user: {userid}")
        else: print(f"Succesfully loaded user: {userid}")
        if temp not in error_codes:
            cloud = temp
            while True:
                print("\nOptions: upload, delete, read, exit")
                action = input("Choose an action: ").strip().lower()
                if action == "upload":
                    upload_file(cloud)
                elif action == "delete":
                    delete_file(cloud)
                elif action == "read":
                    read_file(cloud)
                elif action == "exit":
                    break
                else:
                    print("Invalid action. Please choose again.")
    else:
        Credentials.authenticate(Cloud)

main()