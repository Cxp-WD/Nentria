from Archive.Nentria_lib import *

password = "1234567890"
message = "Hello World"
LOCAL_FILE = "DO_NOT_DELETE_PASSWORD_MANAGER.safe"

key = cryptomanager.generate_key(password)
with open(LOCAL_FILE, 'wb') as file: file.write(cryptomanager.encrypt_message(message, key))
with open(LOCAL_FILE, 'rb') as file: print(cryptomanager.decrypt_message(file.read(), key))