import os
import subprocess
import sys
import threading
import webview
import time

from flask import Flask, request, render_template, redirect

app = Flask(__name__)

mode = 'app'

# window.destroy()
# window.minimize()

chocolatey_apps = {
    # Game Launchers
    'steam': 'steam',
    'epicgames': 'epicgameslauncher',
    'ubisoftconnect': 'ubisoft-connect',
    'eadesktop': 'ea-app',
    # Social Apps
    'discord': 'discord',
    'signal': 'signal',
    'whatsapp': 'whatsapp',
    # Entertainment
    'spotify': 'spotify',
    'stremio': 'stremio',
    'mpv': 'mpv',
    'vlc': 'vlc',
    # Tools
    'wincompose': 'wincompose',
    'powertoys': 'powertoys',
    'iobitunlocker': 'io-unlocker',
    'everything': 'everything',
    'windirstat': 'windirstat',
    'tcnoaccount': 'tcno-acc-switcher',
    # Files
    'qbittorrent': 'qbittorrent',
    'winrar': 'winrar',
    'fdm': 'freedownloadmanger',
    'megasync': 'megasync',
    'audacity': 'audacity',
    'paintnet': 'paint.net',
    'blender': 'blender',
    # Hardware Apps
    'ngenuity': 'hyperx-ngenuity',
    'vigem': 'vigembus',
    'paragonpartition': 'partition-manager',
    # Other
    'firefox': 'firefox',
    'malwarebytes': 'malwarebytes',
    'obs': 'obs-studio',
    'parsec': 'parsec',
    'python': 'python',
    'pycharm': 'pycharm-community',
    'tor': 'tor-browser'
}


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def checkChocoVersion():
    try:
        choco_version = subprocess.run(["choco", "-v"],
                                       capture_output=True)
    except FileNotFoundError:
        choco_version = None
    print(choco_version)
    return choco_version


@app.route("/chocoinstall", methods=['GET'])
def InstallChoco():
    subprocess.run(["choco", "-v"],
                   capture_output=True)
    # choco_version = checkChocoVersion()
    # if choco_version is None:
    #     print("Installation Failed")
    return redirect("/", code=302)


# checkChocoVersion()


@app.route("/", methods=['GET', 'POST'])
def index():
    selected_programs = []
    if request.method == 'POST':
        selected_programs = request.form.getlist('selected_programs')
        print(selected_programs)

    return render_template('index.html', selected_programs=selected_programs)


@app.route("/shutdown", methods=['GET'])
def shutdown_server():
    time.sleep(0.2)
    window.destroy()
    return ""


@app.route("/minimize", methods=['GET'])
def minimize_app():
    window.minimize()
    return ""


def start_flask():
    app.run(host="127.0.0.1", port=7707)


if __name__ == "__main__":
    if mode == "app":
        t = threading.Thread(target=start_flask)
        t.daemon = True
        t.start()

        window = webview.create_window("Quick Easy Installer", "http://127.0.0.1:7707/", width=1400, height=818,
                                       resizable=False, frameless=True)
        webview.start()
    elif mode == 'webpage':
        app.run(host="127.0.0.1", port=7707)

    sys.exit()
