import threading
import os
import sys
import logging
from flask import Flask
from pypress import *
from Nentria_lib import *

# === Silence Flask/Werkzeug ===
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # or logging.CRITICAL to silence even more

# Redirect stdout and stderr (for the "Running on..." messages)
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# === Flask App (Daemon) ===
flask_app = Flask(__name__)

@flask_app.route("/daemon", methods=["GET"])
def daemon():
    return "Daemon is running!", 200

def run_flask_app():
    flask_app.run(port=5050)

# === Pypress App ===
pypress_app = Server()
webserver.host(pypress_app, folder='www')

def run_pypress_app():
    launch(pypress_app, port=8080)

# === Run both in threads ===
t1 = threading.Thread(target=run_flask_app); t2 = threading.Thread(target=run_pypress_app)
t1.start(); t2.start()
t1.join(); t2.join()