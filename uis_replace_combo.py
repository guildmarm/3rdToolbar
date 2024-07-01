import os
import shutil
import sys
import psutil
import tkinter as tk
from tkinter import messagebox

def get_install_location():
    install_location = os.path.expandvars(r'%APPDATA%\\SWG Infinity\\Live')
    return install_location

def check_game_install(directory):
    if not os.path.exists(directory):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"The directory {directory} does not exist. Please make sure that you are using the Infinity 2.0 Launcher OR that SWG Infinity has been installed.")
        sys.exit(1)

def check_game_running(process_names):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() in [name.lower() for name in process_names]:
            return True
    return False

def read_cfg_file():
    cfg_directory = get_install_location()
    check_game_install(cfg_directory)
    cfg_file_path = os.path.join(cfg_directory, "installDirectory.cfg")
    
    with open(cfg_file_path, 'r') as file:
        data = file.read().strip()
    return data

def get_directories():
    target_directory = read_cfg_file()
    profiles_directory = os.path.join(target_directory, "profiles")
    if not os.path.exists(profiles_directory):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "Please run the game at least once before running this script")
        sys.exit(1)
    return target_directory, profiles_directory

def find_uis_files(directory):
    uis_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".uis"):
                uis_files.append(os.path.join(root, file))
    return uis_files

def copy_and_replace_uis_files(profiles_directory, template_file):
    uis_files = find_uis_files(profiles_directory)
    for file_path in uis_files:
        target_directory, file_name = os.path.split(file_path)
        new_file_path = os.path.join(target_directory, file_name)
        shutil.copy(template_file, new_file_path)
        print(f"Copied and replaced {file_path} with {new_file_path}")

def copy_ui_file(target_directory, ui_file):
    ui_directory = os.path.join(target_directory, "ui")
    if not os.path.exists(ui_directory):
        os.makedirs(ui_directory)
    new_file_path = os.path.join(ui_directory, "ui_ground_hud_toolbar.inc")
    shutil.copy(ui_file, new_file_path)
    print(f"Copied {ui_file} to {new_file_path}")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    try:
        process_names = ["SWGEmu.exe", "SwgClient.exe", "SwgClient_r.exe"]
        if check_game_running(process_names):
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", "Please close Star Wars Galaxies before running this script.")
            sys.exit(1)

        install_location = get_install_location()
        check_game_install(install_location)

        target_directory, profiles_directory = get_directories()

        template_file = resource_path("1000000000000000.uis")
        ui_file = resource_path("ui_ground_hud_toolbar.inc")

        if not os.path.exists(template_file):
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"Template file {template_file} not found.")
            sys.exit(1)

        if not os.path.exists(ui_file):
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"UI file {ui_file} not found.")
            sys.exit(1)

        copy_and_replace_uis_files(profiles_directory, template_file)
        copy_ui_file(target_directory, ui_file)

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Information", ".uis file conversion complete and UI file copied.")

    except PermissionError:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Permission Denied", "Permission Denied. Please run the script as an administrator.")
        sys.exit(1)

if __name__ == "__main__":
    main()