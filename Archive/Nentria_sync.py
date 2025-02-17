from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

class syncmanager():
    def authenticate_and_upload(safe_name, content="test", auth_file=None):
        gauth = GoogleAuth()

        if auth_file: # Load the specified auth file
            gauth.LoadCredentialsFile(auth_file)
            if gauth.credentials is None or gauth.access_token_expired: gauth.Refresh()
            else: gauth.Authorize()
        else: # Authenticate if no auth file is provided
            gauth.LocalWebserverAuth()
            drive = GoogleDrive(gauth)
            about = drive.GetAbout()
            email = about['user']['emailAddress']
            auth_filename = email.split('@')[0] + '.auth'

            # Determine the next available number for the auth file
            i = 1
            while os.path.exists(f"{i}_{auth_filename}"):
                i += 1

            # Save the credentials with the new filename
            gauth.SaveCredentialsFile(f"{i}_{auth_filename}")

        drive = GoogleDrive(gauth)

        # Create a file and upload it
        file1 = drive.CreateFile({f'title': safe_name})  # Create a file with the title 'Hello.txt'
        file1.SetContentString(content)  # Set content of the file
        file1.Upload()

    def read_file(auth_file, read_file):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(auth_file)
        if gauth.credentials is None or gauth.access_token_expired: gauth.Refresh()
        else: gauth.Authorize()
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile({'q': f"title='{read_file}'"}).GetList()
        if file_list:
            file1 = file_list[0]
            file1.GetContentFile(read_file)
            with open(read_file, 'r') as f:
                content = f.read()
            return content
        else: return "404"

    def list_auth_files(): return [f for f in os.listdir() if f.endswith('.auth')]