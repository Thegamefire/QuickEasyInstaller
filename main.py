import os
import subprocess
import sys
import threading
import webview
import time
import requests
import ctypes
import math
import pyperclip

from flask import Flask, request, render_template, redirect, Response, jsonify

app = Flask(__name__)

display_log = []
SSE_message = ""

alphabet = '0abcdefghijklmopqrstuvwxyz'  # There is no 'n' because 'n' is the split character in the package seeds
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
}  # Dictionary with the chocolatey package name and the Display Name of each choco package
application_decode_dict = {
    1: 'steam',
    2: 'epicgames',
    3: 'ubisoftconnect',
    4: 'battlenet',
    5: 'eadesktop',
    6: 'discord',
    7: 'signal',
    8: 'whatsapp',
    9: 'spotify',
    10: 'stremio',
    11: 'mpv',
    12: 'vlc',
    13: 'batterymode',
    14: 'wincompose',
    15: 'powertoys',
    16: 'iobitunlocker',
    17: 'everything',
    18: 'windirstat',
    19: 'tcnoaccount',
    20: 'qbittorrent',
    21: 'winrar',
    22: 'fdm',
    23: 'megasync',
    24: 'audacity',
    25: 'paintnet',
    26: 'blender',
    27: 'ngenuity',
    28: 'vigem',
    29: 'paragonpartition',
    30: 'firefox',
    31: 'malwarebytes',
    32: 'obs',
    33: 'parsec',
    34: 'python',
    35: 'pycharm',
    36: 'git',
    37: 'seb',
    38: 'tor'
}


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def uac_elevation():
    """ Checks if the code is run as administrator, and if it isn't it asks for admin privileges and closes if it
    doesn't get them"""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        # Needs to be changed to sys.argv[1:] in build !!or not ig
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


def get_package_seed(application_list):
    """ Get the package seed of an application list """
    seed = ''
    seed_version = '01'
    seed = seed + seed_version
    for application in application_list:
        application_number = 0
        # Get application number from dict
        for i, item in application_decode_dict.items():
            if item == application:
                application_number = i
                break

        # Convert number into seed-code
        if application_number <= 34:
            if application_number < 10:
                app_code = str(application_number)
            else:
                app_code = str(alphabet[application_number - 9])
        else:  # 2 character long code
            app_code = 'n'
            # First character in code
            if math.floor(application_number / 35) <= 9:
                app_code += str(math.floor(application_number / 35))
            else:
                app_code += str(alphabet[math.floor(application_number) - 9])
            # Second character in code
            if application_number % 35 <= 9:
                app_code += str(application_number % 35)
            else:
                app_code += str(alphabet[application_number % 35 - 9])

        seed += app_code
    return seed


def decrypt_package_seed(seed):
    """ Return the application list corresponding to a package seed """
    application_list = []
    version = seed[:2]
    seed = seed[2:]
    if version == '01':
        char_since_n = 3
        for i, char in enumerate(seed):
            application_number = 0
            if char == 'n':
                char_since_n = 0
            else:
                if not char_since_n < 2:
                    try:
                        application_number = int(char)
                    except ValueError:
                        application_number = int(alphabet.index(char) + 9)

                elif char_since_n == 0:
                    try:
                        application_number = int(char) * 35
                    except ValueError:
                        application_number = int(alphabet.index(char) + 9) * 35

                    try:
                        application_number = application_number + int(seed[i + 1])
                    except ValueError:
                        application_number = application_number + int(alphabet.index(seed[i + 1]) + 9)
                elif char_since_n == 1:
                    char_since_n += 1
                    continue
                application_list.append(application_decode_dict[application_number])
                char_since_n += 1

        return application_list


def updateProgressbar(percentage):
    """Updates the progressbar in the app"""
    global SSE_message
    SSE_message = 'Progressbar: ' + str(percentage) + '%'


def checkChocoVersion():
    """Returns the current Chocolatey version"""
    try:
        choco_version = subprocess.run(["choco", "-v"],
                                       capture_output=True)
    except FileNotFoundError:
        choco_version = None
    print(choco_version)
    return choco_version


@app.route("/copy-seed", methods=['POST'])
def copy_seed():
    print('/copy_seed got post request')
    app_list = request.get_json().get('app_list')  # Access the 'app_list' key
    print(app_list)
    pyperclip.copy(get_package_seed(app_list))
    return jsonify({'message': 'List received successfully', 'jsonp': 'false'})


@app.route("/select-package", methods=['POST'])
def selectPackage():
    package_seed = request.get_json().get('seed')
    app_list = decrypt_package_seed(package_seed)
    print(f'/select-package got post request app_list: {app_list}')
    return jsonify({'app_list': app_list})


@app.route("/chocoinstall", methods=['GET'])
def InstallChoco():
    """Installs Chocolatey, by running a powershell command"""
    # subprocess.run(["powershell.exe", "-NoProfile", "-InputFormat", "None", "-ExecutionPolicy", "Bypass", "-Command",
    #                 f"iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"],
    #                check=True)
    # choco_version = checkChocoVersion()
    # if choco_version is None:
    #     print("Choco Installation Failed")
    return redirect("/", code=302)


def updateDisplayLog(message, message_type='normal'):
    """Updates the installer Log displayed above the progressbar"""
    global SSE_message
    display_log.append([message, message_type])
    print(display_log[-1])
    SSE_message = f'DisplayLog Append: {message_type} {message}'


def installPrograms(selected_programs):
    """Installs the selected Programs"""
    global SSE_message
    if selected_programs:
        percentage_per_program = int(round(100 / len(selected_programs)))

        for program in selected_programs:

            if program in chocolatey_apps:  # Choco install app

                updateDisplayLog(f'Installing {chocolatey_apps[program][1]}...')
                result = subprocess.run(["choco", "install", chocolatey_apps[program][0], '-y'],
                                        capture_output=True)
                print(result)
                if result.returncode == 0:
                    print(f"Successfully installed {chocolatey_apps[program][1]}!")
                else:
                    print(f"Failed to install {chocolatey_apps[program][1]}: {result.stderr}")
                    print(result.stderr)

            else:  # Non-Chocolatey App

                if program == 'batterymode':  # Battery Mode Installation

                    release_info = requests.get(
                        "https://api.github.com/repos/tarcode-apps/BatteryMode/releases/latest",
                        allow_redirects=True)
                    print(release_info.json())
                    installer = None
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

                            if installer_log.returncode == 0:
                                updateDisplayLog(f"Successfully installed BatteryMode!")
                            else:
                                updateDisplayLog(f"Failed to install BatteryMode: {installer_log.stderr}",
                                                 message_type='Error')
                    if not installer:
                        updateDisplayLog(
                            "BatteryMode Installer not found in github repo, please create an issue "
                            "on the QuEI github repo", message_type="Error")

                elif program == 'seb':  # Safe Exam Browser Installation

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

                            updateDisplayLog("Installing Safe Exam Browser...")
                            installer_log = subprocess.run(
                                [resource_path("installers/SEBInstaller.exe"), "/install /quiet /norestart"],
                                capture_output=True)  # Test necessary

                            if installer_log.returncode == 0:
                                updateDisplayLog(f"Successfully installed Safe Exam Browser!")
                            else:
                                updateDisplayLog(f"Failed to install Safe Exam Browser: {installer_log.stderr}",
                                                 message_type='Error')
                        else:
                            updateDisplayLog(
                                "Safe Exam Browser Installer not found in github repo, please create an issue "
                                "on the QuEI github repo", message_type="Error")

                elif program == 'battlenet':  # BattleNet Installation

                    updateDisplayLog("Downloading BattleNet...")
                    installer = requests.get(
                        "https://downloader.battle.net/download/getInstallerForGame?os=win&gameProgram"
                        "=BATTLENET_APP&version=Live",
                        allow_redirects=True)
                    open(resource_path('installers\\BattleNetInstaller.exe'), 'wb').write(installer.content)

                    updateDisplayLog("Installing BattleNet...")
                    installer_log = subprocess.run(
                        [resource_path("installers/BattleNetInstaller.exe"),
                         "--lang=enUS --installpath=\"C:\Program Files (x86)\Battle.net"],
                        capture_output=True)  # Test necessary

                    if installer_log.returncode == 0:
                        updateDisplayLog(f"Successfully installed BattleNet Client!")
                    else:
                        updateDisplayLog(f"Failed to install BattleNet Client: {installer_log.stderr}",
                                         message_type='Error')

            current_percentage = + percentage_per_program
            updateProgressbar(current_percentage)

        updateDisplayLog("Done")
        SSE_message = "Completed Operation"


@app.route('/sse')
def sse():
    """The Server Side Eventstream"""

    def event_stream():
        while True:
            yield f"data: {SSE_message}\n\n"
            time.sleep(1)  # Simulate updates every 1 second

    return Response(event_stream(), content_type='text/event-stream')


@app.route("/", methods=['GET', 'POST'])
def index():
    selected_programs = []
    if request.method == 'POST':
        print('/ got post request')
        selected_programs = request.form.getlist('selected_programs')
        print(selected_programs)
        # installPrograms(selected_programs)

    return render_template('index.html', selected_programs=selected_programs)


@app.route("/shutdown", methods=['GET'])
def shutdown_server():
    """Closes the application"""
    time.sleep(0.2)
    window.destroy()
    return ""


@app.route("/minimize", methods=['GET'])
def minimize_app():
    """Minimizes the application to the background"""
    window.minimize()
    return ""


def start_flask():
    """Starts the flask server"""
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
