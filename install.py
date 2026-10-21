import subprocess
import sys

# Список сторонних библиотек, которые нужно проверить/установить
required_packages = ["requests"]

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"[!] Модуль '{package}' dont found. installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Теперь импортируем всё, что нужно для работы скрипта
import os
import sys
import time
import socket
import platform
import urllib.request
import requests

print("[+] All modules installed!")