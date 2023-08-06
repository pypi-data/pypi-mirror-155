from typing import List
from shutil import which


def get_client_public_ip_address():
    """
    Reads client machine ip

    @return (string|bool) ipAddress"""
    import socket

    ipAddress = None

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ipAddress = s.getsockname()[0]
        s.close()
    except Exception:
        print("Could not resolve client ip")

    return ipAddress


def check_shell_apps_installed(shell_apps_wanted: List[str]) -> List[str]:
    """Returns list that of shell apps that stats good in current runtime sys"""
    shell_apps = []
    for app_name in shell_apps_wanted:
        app_path = which(app_name)
        if app_path is not None:
            shell_apps.append(app_name)
    return shell_apps
