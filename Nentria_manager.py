import os
import Nentria_sync as syncmanager

def load_creds():
    x=0

def save_creds():
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
