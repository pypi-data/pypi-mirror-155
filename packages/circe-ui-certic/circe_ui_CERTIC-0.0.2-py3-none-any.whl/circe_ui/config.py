import os
from pathlib import Path
from multiprocessing import cpu_count
import sys
from dotenv import load_dotenv

sys.path.append(os.getcwd())
load_dotenv("{}/.env".format(os.getcwd()))

CONFIG = {
    "CIRCEUI_HOST": "127.0.0.1",
    "CIRCEUI_PORT": 8001,
    "CIRCEUI_DEBUG": False,
    "CIRCEUI_WORKERS": cpu_count() if os.name != "nt" else 1,
    "CIRCEUI_WORKING_DIR": "{}/.circeui/".format(Path.home()),
    "CIRCEUI_CRYPT_KEY": "you should really change this",
    "CIRCEUI_REMOVE_USER_FILES_DELAY": 7200,
    "CIRCEUI_CIRCE_ENDPOINT": "http://circe.unicaen.fr/",
    "CIRCEUI_CIRCE_APP": "acme",
    "CIRCEUI_CIRCE_KEY": "acme",
}

for key in CONFIG.keys():
    try:
        val = os.environ[key]
        if key in [
            "CIRCEUI_DEBUG",
        ]:
            CONFIG[key] = True if val == "1" else False
        elif key in ["CIRCEUI_PORT"]:
            CONFIG[key] = int(val)
        else:
            CONFIG[key] = val
    except KeyError:
        pass


os.makedirs("{}/done/".format(CONFIG["CIRCEUI_WORKING_DIR"]), exist_ok=True)
os.makedirs("{}/web_ui_sessions/".format(CONFIG["CIRCEUI_WORKING_DIR"]), exist_ok=True)
