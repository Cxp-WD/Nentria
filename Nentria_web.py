import os
import nacl.secret
import nacl.utils
import hashlib
import base64
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import threading
import logging
from flask import Flask, request, jsonify
from pypress import *

# ------------------------------
# Backend Library Implementation
# ------------------------------

class Cloud():
    def __init__(self, auth_file=None):
        self.gauth = GoogleAuth()
        self.drive = None
        self.authenticate(auth_file)

    def authenticate(self, auth_file=None):
        if auth_file:  # Load the specified auth file
            self.gauth.LoadCredentialsFile(auth_file)
            try:
                if self.gauth.credentials is None or self.gauth.access_token_expired:
                    self.gauth.Refresh()
                else:
                    self.gauth.Authorize()
            except Exception:
                self.gauth.LocalWebserverAuth()
                self.save_credentials(auth_file)
        else:
            self.gauth.LocalWebserverAuth()
            self.save_credentials(auth_file)
        self.drive = GoogleDrive(self.gauth)
        return "Authenticated Cloud instance."

    def save_credentials(self, auth_file):
        about = self.drive.GetAbout()
        email = about['user']['emailAddress']
        auth_filename = email.split('@')[0] + '.auth'
        i = 1
        while os.path.exists(f"{i}_{auth_filename}"):
            i += 1
        filename = f"{i}_{auth_filename}"
        self.gauth.SaveCredentialsFile(filename)
        return f"Saved credentials to {filename}"

    def upload(self, safe_name, content="Empty"):
        file1 = self.drive.CreateFile({'title': safe_name})
        file1.SetContentString(content)
        file1.Upload()
        return f"Uploaded file '{safe_name}'."

    def delete(self, safe_name):
        file_list = self.drive.ListFile({'q': f"title='{safe_name}'"}).GetList()
        if file_list:
            file1 = file_list[0]
            file1.Delete()
            return 200
        else:
            return 404

    def read(self, read_file):
        file_list = self.drive.ListFile({'q': f"title='{read_file}'"}).GetList()
        if file_list:
            file1 = file_list[0]
            file1.GetContentFile(read_file)
            with open(read_file, 'r') as f:
                content = f.read()
            return content
        else:
            return "404"

class Cryptography:
    @staticmethod
    def hash(data): 
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def generate_pin(text: str) -> str:
        hash_obj = hashlib.sha256(text.encode())  
        hash_int = int(hash_obj.hexdigest(), 16)  
        pin = str(hash_int % 1000000).zfill(6)
        return pin

    @staticmethod
    def pin_to_key(pin: str) -> bytes:
        hash_obj = hashlib.sha256(pin.encode())  
        return hash_obj.digest()

    def generate_key(self, key: bytes):
        if len(key) != 32:
            raise ValueError("Encryption key must be exactly 32 bytes.")
        self.box = nacl.secret.SecretBox(key)
        return "Encryption key set."

    def encrypt(self, message: str) -> str:
        encrypted = self.box.encrypt(message.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt(self, encrypted_message: str) -> str:
        encrypted_bytes = base64.b64decode(encrypted_message)
        return self.box.decrypt(encrypted_bytes).decode()

class Credentials:
    @staticmethod
    def load_creds(auth_file):
        auth_ids = []
        for auths in Credentials.list_creds():
            auth_ids.append(auths.split("_"))
        # Use first credential list as an example.
        if not auth_ids:
            return 404
        variable = " ".join(auth_ids[0])
        search_string = auth_file
        try:
            index = variable.index(search_string)
            next_entry_start = index + len(search_string) + 1
            next_entry_end = variable.find(" ", next_entry_start)
            if next_entry_end == -1:
                next_entry_end = len(variable)
            next_entry = variable[next_entry_start:next_entry_end]
        except ValueError:
            return 404
        return Cloud(f"{auth_file}_{next_entry}")
    
    @staticmethod
    def list_creds():
        return [f for f in os.listdir() if f.endswith('.auth')]

# ------------------------------
# API Key Configuration
# ------------------------------

API_KEYS = [
    'NY2cGqHberCNRnRd8VC1ujywBU7mXyHtrj8DKaevVMYu2DX4Bg96vPKn7zacP6EJ'
]

# ------------------------------
# Flask Application & Endpoints
# ------------------------------

app = Flask(__name__)

def check_api_key():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, jsonify({"error": "Missing or invalid Authorization header"}), 401
    api_key = auth_header.split(" ")[1]
    if api_key not in API_KEYS:
        return None, jsonify({"error": "Unauthorized"}), 401
    return api_key, None, None

# ----- Cloud Endpoints -----

@app.route("/daemon/cloud/init", methods=["GET"])
def cloud_init():
    """Initialize a Cloud instance; optionally with auth_file."""
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    auth_file = request.args.get("auth_file")
    try:
        cloud = Cloud(auth_file)
        # cloud.authenticate() is called inside __init__
        return jsonify({"result": "Cloud instance initialized and authenticated."})
    except Exception as e:
        return jsonify({"error": f"Cloud initialization failed: {str(e)}"}), 500

@app.route("/daemon/cloud/save_credentials", methods=["GET"])
def cloud_save_credentials():
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    auth_file = request.args.get("auth_file")
    if not auth_file:
        return jsonify({"error": "Missing 'auth_file' parameter."}), 400
    try:
        cloud = Cloud(auth_file)
        result = cloud.save_credentials(auth_file)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": f"Saving credentials failed: {str(e)}"}), 500

@app.route("/daemon/cloud/upload", methods=["GET"])
def cloud_upload():
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    safe_name = request.args.get("safe_name")
    if not safe_name:
        return jsonify({"error": "Missing 'safe_name' parameter."}), 400
    content = request.args.get("content", "Empty")
    auth_file = request.args.get("auth_file")  # optional
    try:
        cloud = Cloud(auth_file)
        result = cloud.upload(safe_name, content)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route("/daemon/cloud/delete", methods=["GET"])
def cloud_delete():
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    safe_name = request.args.get("safe_name")
    if not safe_name:
        return jsonify({"error": "Missing 'safe_name' parameter."}), 400
    try:
        cloud = Cloud()
        res = cloud.delete(safe_name)
        if res == 200:
            return jsonify({"result": f"Deleted file '{safe_name}'."})
        else:
            return jsonify({"error": f"File '{safe_name}' not found."}), 404
    except Exception as e:
        return jsonify({"error": f"Deletion failed: {str(e)}"}), 500

@app.route("/daemon/cloud/read", methods=["GET"])
def cloud_read():
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    read_file = request.args.get("read_file")
    if not read_file:
        return jsonify({"error": "Missing 'read_file' parameter."}), 400
    try:
        cloud = Cloud()
        content = cloud.read(read_file)
        if content == "404":
            return jsonify({"error": f"File '{read_file}' not found."}), 404
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": f"Read failed: {str(e)}"}), 500

# ----- Cryptography Endpoints -----

@app.route("/daemon/crypto/hash", methods=["GET"])
def crypto_hash():
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    data = request.args.get("data")
    if not data:
        return jsonify({"error": "Missing 'data' parameter."}), 400
    try:
        hashed = Cryptography.hash(data)
        return jsonify({"hash": hashed})
    except Exception as e:
        return jsonify({"error": f"Hashing failed: {str(e)}"}), 500

@app.route("/daemon/crypto/generate_pin", methods=["GET"])
def crypto_generate_pin():
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    text = request.args.get("text")
    if not text:
        return jsonify({"error": "Missing 'text' parameter."}), 400
    try:
        pin = Cryptography.generate_pin(text)
        return jsonify({"pin": pin})
    except Exception as e:
        return jsonify({"error": f"PIN generation failed: {str(e)}"}), 500

@app.route("/daemon/crypto/pin_to_key", methods=["GET"])
def crypto_pin_to_key():
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    pin = request.args.get("pin")
    if not pin:
        return jsonify({"error": "Missing 'pin' parameter."}), 400
    try:
        key_bytes = Cryptography.pin_to_key(pin)
        return jsonify({"key": key_bytes.hex()})
    except Exception as e:
        return jsonify({"error": f"PIN-to-key conversion failed: {str(e)}"}), 500

@app.route("/daemon/crypto/encrypt", methods=["GET"])
def crypto_encrypt():
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    message = request.args.get("message")
    key_hex = request.args.get("key")
    if not message or not key_hex:
        return jsonify({"error": "Missing 'message' or 'key' parameter."}), 400
    try:
        if len(key_hex) != 64:
            return jsonify({"error": "Key must be a 64-character hex string (32 bytes)."}), 400
        key_bytes = bytes.fromhex(key_hex)
        crypto = Cryptography()
        crypto.generate_key(key_bytes)
        encrypted_message = crypto.encrypt(message)
        return jsonify({"encrypted_message": encrypted_message})
    except Exception as e:
        return jsonify({"error": f"Encryption failed: {str(e)}"}), 500

@app.route("/daemon/crypto/decrypt", methods=["GET"])
def crypto_decrypt():
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    encrypted_message = request.args.get("encrypted_message")
    key_hex = request.args.get("key")
    if not encrypted_message or not key_hex:
        return jsonify({"error": "Missing 'encrypted_message' or 'key' parameter."}), 400
    try:
        if len(key_hex) != 64:
            return jsonify({"error": "Key must be a 64-character hex string (32 bytes)."}), 400
        key_bytes = bytes.fromhex(key_hex)
        crypto = Cryptography()
        crypto.generate_key(key_bytes)
        decrypted_message = crypto.decrypt(encrypted_message)
        return jsonify({"decrypted_message": decrypted_message})
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 500

# ----- Credentials Endpoints -----

@app.route("/daemon/credentials/load_creds", methods=["GET"])
def credentials_load():
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    auth_file = request.args.get("auth_file")
    if not auth_file:
        return jsonify({"error": "Missing 'auth_file' parameter."}), 400
    try:
        result = Credentials.load_creds(auth_file)
        if result == 404:
            return jsonify({"error": "Credentials not found."}), 404
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": f"Loading credentials failed: {str(e)}"}), 500

@app.route("/daemon/credentials/list_creds", methods=["GET"])
def credentials_list():
    _, err_resp, status = check_api_key()
    if err_resp:
        return err_resp, status
    try:
        creds = Credentials.list_creds()
        return jsonify({"credentials": creds})
    except Exception as e:
        return jsonify({"error": f"Listing credentials failed: {str(e)}"}), 500

# ----- General Daemon Endpoint -----

@app.route("/daemon/", methods=["GET"])
def daemon():
    return "Daemon is running!", 200

# ------------------------------
# Pypress Server for Serving Static Files
# ------------------------------
pypress_app = Server()
webserver.host(pypress_app, folder='www')

def run_flask_app():
    app.run(port=5050)

def run_pypress_app():
    launch(pypress_app, port=8080)

# ------------------------------
# Run Both Servers in Separate Threads
# ------------------------------
if __name__ == "__main__":
    t1 = threading.Thread(target=run_flask_app)
    t2 = threading.Thread(target=run_pypress_app)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
