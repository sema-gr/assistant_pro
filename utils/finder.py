import os
import platform
import subprocess

def find_app_path(app_name):
    if platform.system() != "Windows":
        return None

    if app_name.lower().endswith(".exe"):
        app_name = app_name[:-4]

    try:
        result = subprocess.run(
            ["where", app_name],
            capture_output=True,
            text=True
        )

        if result.returncode == 0 and result.stdout.strip():
            path = result.stdout.strip().split("\n")[0].strip()
            if os.path.exists(path):
                return path
    except:
        pass

    search_dirs = [
        os.environ.get("ProgramFiles", "C:\\Program Files"),
        os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
        os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32"),
        os.path.expanduser("~/AppData/Local/Programs"),
        os.path.expanduser("~/AppData/Roaming"),
    ]

    for root_dir in search_dirs:
        if not os.path.exists(root_dir):
            continue

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.lower() == app_name.lower() + ".exe":
                    return os.path.join(root, file)

            # обмеження глибини
            if root.count(os.sep) - root_dir.count(os.sep) > 3:
                dirs[:] = []

    return None