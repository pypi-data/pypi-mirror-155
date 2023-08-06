import os
import sys
import time
import subprocess

dermatillo_dir = os.path.dirname(os.path.realpath(__file__))


class Platform:
    def __init__(self, name, config_file_dir, service_name, service_file_dir, service_file_path, data_dir):
        self.name = name

        self.config_file_dir = config_file_dir
        self.config_file_path = os.path.join(self.config_file_dir, "config.json")

        self.service_name = service_name
        self.service_file_dir = service_file_dir
        self.service_file_path = service_file_path

        self.data_dir = data_dir

    class NotImplemented(Exception):
        pass

    def service_active(self):
        raise self.NotImplemented

    def set_service(self):
        raise self.NotImplemented

    def remove_service(self):
        raise self.NotImplemented

    def start_service(self):
        raise self.NotImplemented

    def stop_service(self):
        raise self.NotImplemented


class Linux(Platform):
    def __init__(self):
        home_dir = os.path.expanduser("~")
        config_file_dir = os.path.join(home_dir, ".config/dermatillo")

        service_name = "dermatillo"
        service_file_dir = os.path.join(home_dir, ".config/systemd/user")
        service_file_path = os.path.join(service_file_dir, f"{service_name}.service")

        data_dir = os.path.join(home_dir, ".local/share/dermatillo")

        super().__init__("Linux", config_file_dir, service_name, service_file_dir, service_file_path, data_dir)

    def service_active(self, quiet=False):
        if subprocess.call(["systemctl", "--user", "is-active", "--quiet", self.service_name]) == 0:
            if not quiet:
                print("\033[92mService is active.\033[0m")
            return True
        else:
            if not quiet:
                print("\033[91mService is inactive.\033[0m")
            return False

    def set_service(self):
        self.remove_service()

        os.makedirs(self.service_file_dir, exist_ok=True)
        with open(self.service_file_path, "w") as file:
            file.write("[Unit]\n")
            file.write("Description=Dermatillo systemd service\n")
            file.write("After=network.target\n")
            file.write("\n[Service]\n")
            file.write("Type=simple\n")
            file.write(f"ExecStart={sys.executable} "
                       f"{os.path.join(dermatillo_dir, 'run.py')}\n")
            file.write("RestartSec=5\n")
            file.write("Restart=always\n")
            file.write("\n[Install]\n")
            file.write("WantedBy=default.target\n")

        os.environ["DERMATILLO_SETUP"] = "0"
        systemd_setup = [
            ["systemctl", "--user", "enable", self.service_name],
            ["systemctl", "--user", "daemon-reload"],
            ["systemctl", "--user", "start", self.service_name]
        ]
        success = [subprocess.call(cmd) == 0 for cmd in systemd_setup]

        if all(success):
            time.sleep(3)
            print("\n\033[92mDermatillo systemd service enabled. It should be reported as active."
                  "\nClose status with 'q'.\033[0m")
            subprocess.run(["systemctl", "status", "--user", self.service_name])
        else:
            print("\n\033[91mDermatillo systemd service set-up failed!\033[0m")

    def remove_service(self):
        subprocess.run(["systemctl", "--user", "stop", self.service_name])
        subprocess.run(["systemctl", "--user", "disable", self.service_name])
        subprocess.run(["systemctl", "--user", "daemon-reload"])
        subprocess.run(["systemctl", "--user", "reset-failed"])

    def start_service(self):
        subprocess.run(["systemctl", "--user", "start", self.service_name])

    def stop_service(self):
        if self.service_active(quiet=True):
            return subprocess.call(["systemctl", "--user", "stop", self.service_name]) == 0
        else:
            return False


class MacOS(Platform):
    def __init__(self):
        home_dir = os.path.expanduser("~")
        dermatillo_data_dir = os.path.join(home_dir, ".dermatillo")

        service_name = "com.dermatillo.run"
        service_file_dir = os.path.join(home_dir, "Library/LaunchAgents")
        service_file_path = os.path.join(service_file_dir, f"{service_name}.plist")

        super().__init__(
            "macOS", dermatillo_data_dir, service_name, service_file_dir, service_file_path, dermatillo_data_dir)

    def service_active(self, quiet=False):
        if self.service_name in subprocess.check_output(["launchctl", "list"]).decode("utf-8"):
            if not quiet:
                print("\033[92mService is active.\033[0m")
            return True
        else:
            if not quiet:
                print("\033[91mService is inactive.\033[0m")
            return False

    def set_service(self):
        self.stop_service()

        os.makedirs(self.service_file_dir, exist_ok=True)
        with open(self.service_file_path, "w") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
                       '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
            file.write('<plist version="1.0">\n')
            file.write('<dict>\n')
            file.write('    <key>Label</key>\n')
            file.write(f'    <string>{self.service_name}</string>\n')
            file.write('    <key>ProgramArguments</key>\n')
            file.write('    <array>\n')
            file.write(f'        <string>{sys.executable}</string>\n')
            file.write(f'        <string>{os.path.join(dermatillo_dir, "run.py")}</string>\n')
            file.write('    </array>\n')
            file.write('    <key>KeepAlive</key>\n')
            file.write('    <true/>\n')
            file.write('</dict>\n')
            file.write('</plist>\n')

        os.environ["DERMATILLO_SETUP"] = "0"
        self.start_service()
        print("\n\033[92mDermatillo launchd service enabled. Checking if active ...")
        time.sleep(1)
        self.service_active()

    def remove_service(self):
        subprocess.call(["launchctl", "unload", "-w", self.service_file_path])

    def start_service(self):
        subprocess.call(["launchctl", "load", "-w", self.service_file_path])

    def stop_service(self):
        if self.service_active(quiet=True):
            return subprocess.call(["launchctl", "unload", self.service_file_path]) == 0
        else:
            return False


def check_platform():
    if sys.platform in ["linux", "darwin"]:
        return sys.platform
    else:
        print("\n\033[91mDermatillo is available only for Linux and macOS.\033[0m")
        sys.exit(0)


def get_platform():
    this_platform = check_platform()
    if this_platform == "linux":
        return Linux()
    elif this_platform == "darwin":
        return MacOS()
    assert False


platform = get_platform()
