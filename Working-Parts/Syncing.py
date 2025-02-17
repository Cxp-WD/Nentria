SAFE_FILE = "DO_NOT_DELETE_PASSWORD_MANAGER.safe"
import Nentria_manager, time


for cred in Nentria_manager.Credentials.list_creds(): print(cred)
auth_file = input("Auth ID > ")


cloud = Nentria_manager.Credentials.load_creds(auth_file)
cloud.upload(SAFE_FILE, "hello world")
time.sleep(5)
cloud.delete(SAFE_FILE)