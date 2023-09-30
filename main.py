import os
import subprocess
import sys
import threading
import webview
import time
import requests

from flask import Flask, request, render_template, redirect, Response

app = Flask(__name__)

display_log = []
SSE_message = ""

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

def updateProgressbar(percentage):
    global SSE_message
    SSE_message = 'Progressbar: '+ percentage +'%'

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


def updateDisplayLog(message, message_type='normal'):
    display_log.append(message)
    print(display_log[-1])


@app.route('/sse')
def sse():
    def event_stream():
        while True:
            yield f"data: {SSE_message}\n\n"
            time.sleep(1)  # Simulate updates every 1 second

    return Response(event_stream(), content_type='text/event-stream')


@app.route("/", methods=['GET', 'POST'])
def index():
    selected_programs = []
    if request.method == 'POST':
        selected_programs = request.form.getlist('selected_programs')
        print(selected_programs)
        if selected_programs:
            percentage_per_program = int(round(100/len(selected_programs)))
            current_percentage = 0
            for program in selected_programs:
                if program in chocolatey_apps:
                    pass  # Choco install app
                else:

                    # Battery Mode Installation #
                    if program == 'batterymode':
                        release_info = requests.get("https://api.github.com/repos/tarcode-apps/BatteryMode/releases/latest",
                                                    allow_redirects=True)
                        print(release_info.json())
                        for asset in release_info.json()["assets"]:
                            print(asset["name"])
                            if asset["name"] == "BatteryModeInstaller64.exe":
                                updateDisplayLog("Downloading BatteryMode...")
                                installer = requests.get(asset["browser_download_url"], allow_redirects=True)
                                print(resource_path('installers\\BatteryModeInstaller64.exe'))
                                open(resource_path('installers\\BatteryModeInstaller64.exe'), 'wb').write(installer.content)
                                updateDisplayLog("Installing BatteryMode...")
                                installer_log = subprocess.run(
                                    [resource_path("installers/BatteryModeInstaller64.exe"), "/VERYSILENT"],
                                    capture_output=True)
                            else:
                                updateDisplayLog("BatteryMode Installer not found in github repo, please create an issue "
                                                 "on the QuEI github repo", message_type="Error")

                    # Safe Exam Browser Installation #
                    elif program == 'seb':
                        release_info = requests.get(
                            "https://api.github.com/repos/SafeExamBrowser/seb-win-refactoring/releases/latest",
                            allow_redirects=True)
                        print(release_info.json())
                        for asset in release_info.json()["assets"]:
                            print(asset["name"])
                            if asset["name"][-16:] == "_SetupBundle.exe":
                                updateDisplayLog("Downloading Safe Exam Browser...")
                                installer = requests.get(asset["browser_download_url"], allow_redirects=True)
                                print(resource_path('installers\\SEBInstaller.exe'))
                                open(resource_path('installers\\SEBInstaller.exe'), 'wb').write(installer.content)
                                # Install SEB Using:  SEB_w.x.y.z_SetupBundle.exe /install /quiet /norestart
                current_percentage = + percentage_per_program
                updateProgressbar(current_percentage)

    return render_template('index.html', selected_programs=selected_programs)


@app.route("/shutdown", methods=['GET'])
def shutdown_server():
    time.sleep(0.2)
    window.destroy()
    return ""


@app.route("/minimize", methods=['GET'])
def minimize_app():
    window.minimize()
    global SSE_message
    SSE_message = 'Progressbar: 40%'
    return ""





def start_flask():
    app.run(host="127.0.0.1", port=7707)


if __name__ == "__main__":
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()
    print(resource_path("/"))
    window = webview.create_window("Quick Easy Installer", "http://127.0.0.1:7707/", width=1400, height=818,
                                   resizable=False, frameless=True)
    webview.start()

    sys.exit()
