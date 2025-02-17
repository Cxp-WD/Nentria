SAFE_FILE = "DO_NOT_DELETE_PASSWORD_MANAGER.safe"
import NTM, time


for cred in NTM.Credentials.list_creds(): print(cred)
auth_file = input("Auth ID > ")


cloud = NTM.Credentials.load_creds(auth_file)
cloud.upload(SAFE_FILE, "hello world")
time.sleep(5)
cloud.delete(SAFE_FILE)