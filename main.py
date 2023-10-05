import os
import subprocess
import sys
import threading
import webview
import time
import requests
import ctypes

from flask import Flask, request, render_template, redirect, Response

app = Flask(__name__)

display_log = []
SSE_message = ""

chocolatey_apps = {
    # Game Launchers
    'steam': ['steam', 'Steam'],
    'epicgames': ['epicgameslauncher', 'Epic Games Launcher'],
    'ubisoftconnect': ['ubisoft-connect', 'Ubisoft Connect'],
    'eadesktop': ['ea-app', 'EA Desktop App'],
    # Social Apps
    'discord': ['discord', 'Discord'],
    'signal': ['signal', 'Signal'],
    'whatsapp': ['whatsapp', 'WhatsApp'],
    # Entertainment
    'spotify': ['spotify', 'Spotify'],
    'stremio': ['stremio', 'Stremio'],
    'mpv': ['mpv', 'MPV'],
    'vlc': ['vlc', 'VLC Media Player'],
    # Tools
    'wincompose': ['wincompose', 'WinCompose'],
    'powertoys': ['powertoys', 'Microsoft PowerToys'],
    'iobitunlocker': ['io-unlocker', 'IOBitUnlocker'],
    'everything': ['everything', 'Everything'],
    'windirstat': ['windirstat', 'WinDirStat'],
    'tcnoaccount': ['tcno-acc-switcher', 'TCNO Account Switcher'],
    # Files
    'qbittorrent': ['qbittorrent', 'qBittorrent'],
    'winrar': ['winrar', 'WinRAR'],
    'fdm': ['freedownloadmanger', 'Free Download Manager'],
    'megasync': ['megasync', 'MegaSync'],
    'audacity': ['audacity', 'Audacity'],
    'paintnet': ['paint.net', 'Paint.NET'],
    'blender': ['blender', 'Blender'],
    # Hardware Apps
    'ngenuity': ['hyperx-ngenuity', 'HyperX Ngenuity'],
    'vigem': ['vigembus', 'ViGEM Bus Driver'],
    'paragonpartition': ['partition-manager', 'Paragon Partition Manager'],
    # Other
    'firefox': ['firefox', 'Firefox'],
    'malwarebytes': ['malwarebytes', 'Malwarebytes'],
    'obs': ['obs-studio', 'OBS Studio'],
    'parsec': ['parsec', 'Parsec'],
    'python': ['python', 'Python'],
    'pycharm': ['pycharm-community', 'Pycharm Community Edition'],
    'git': ['git', 'Git'],
    'tor': ['tor-browser', 'Tor Browser']
}


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def uac_elevation():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1) # Needs to be changed to sys.argv[1:] in build !!or not ig
        print(is_admin())
        if not is_admin():
            shutdown_server()


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
    SSE_message = 'Progressbar: ' + str(percentage) + '%'


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
    # subprocess.run(["powershell.exe", "-NoProfile", "-InputFormat", "None", "-ExecutionPolicy", "Bypass", "-Command",
    #                 f"iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"],
    #                check=True)
    # choco_version = checkChocoVersion()
    # if choco_version is None:
    #     print("Choco Installation Failed")
    return redirect("/", code=302)


def updateDisplayLog(message, message_type='normal'):
    global SSE_message
    display_log.append([message, message_type])
    print(display_log[-1])
    SSE_message = f'DisplayLog Append: {message_type}: {message}'


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
            percentage_per_program = int(round(100 / len(selected_programs)))
            for program in selected_programs:
                if program in chocolatey_apps:
                    # Choco install app
                    updateDisplayLog(f'Installing {chocolatey_apps[program][1]}...')
                    result = subprocess.run(["choco", "install", chocolatey_apps[program][0], '-y'], capture_output=True)
                    print(result)
                    if result.returncode == 0:
                        print(f"Successfully installed {chocolatey_apps[program][1]}!")
                    else:
                        print(f"Failed to install {chocolatey_apps[program][1]}.")
                        print(result.stderr)
                else:

                    # Battery Mode Installation #
                    if program == 'batterymode':
                        release_info = requests.get(
                            "https://api.github.com/repos/tarcode-apps/BatteryMode/releases/latest",
                            allow_redirects=True)
                        print(release_info.json())
                        for asset in release_info.json()["assets"]:
                            print(asset["name"])
                            if asset["name"] == "BatteryModeInstaller64.exe":
                                updateDisplayLog("Downloading BatteryMode...")
                                installer = requests.get(asset["browser_download_url"], allow_redirects=True)
                                print(resource_path('installers\\BatteryModeInstaller64.exe'))
                                open(resource_path('installers\\BatteryModeInstaller64.exe'), 'wb').write(
                                    installer.content)
                                updateDisplayLog("Installing BatteryMode...")
                                installer_log = subprocess.run(
                                    [resource_path("installers/BatteryModeInstaller64.exe"), "/VERYSILENT"],
                                    capture_output=True)
                            else:
                                updateDisplayLog(
                                    "BatteryMode Installer not found in github repo, please create an issue "
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
                                updateDisplayLog("Installing Safe Exam Browser...")
                                open(resource_path('installers\\SEBInstaller.exe'), 'wb').write(installer.content)
                                installer_log = subprocess.run(
                                    [resource_path("installers/SEBInstaller.exe"), "/install /quiet /norestart"],
                                    capture_output=True)  # Test necessary
                            else:
                                updateDisplayLog(
                                    "Safe Exam Browser Installer not found in github repo, please create an issue "
                                    "on the QuEI github repo", message_type="Error")
                    # BattleNet Installation
                    elif program == 'battlenet':
                        updateDisplayLog("Downloading BattleNet...")
                        release_info = requests.get(
                            "https://downloader.battle.net/download/getInstallerForGame?os=win&gameProgram"
                            "=BATTLENET_APP&version=Live",
                            allow_redirects=True)
                        open(resource_path('installers\\BattleNetInstaller.exe'), 'wb').write(release_info.content)
                        updateDisplayLog("Installing BattleNet...")
                        installer_log = subprocess.run(
                            [resource_path("installers/BattleNetInstaller.exe"),
                             "--lang=enUS --installpath=\"C:\Program Files (x86)\Battle.net"],
                            capture_output=True)  # Test necessary
                current_percentage = + percentage_per_program
                updateProgressbar(current_percentage)

            updateDisplayLog("Done")

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
    # uac_elevation()
    window = webview.create_window("Quick Easy Installer", "http://127.0.0.1:7707/", width=1400, height=818,
                                   resizable=False, frameless=True, easy_drag=False)

    webview.start()

    sys.exit()
