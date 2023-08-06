import os
import subprocess
import cv2
import sys
import json
import time
import click
import sounddevice as sd


def check_platform():
    if sys.platform not in ["linux", "darwin"]:
        print("\n\033[91mDermatillo is available only on Unix.\033[0m")
        sys.exit(0)


def get_choice(options):
    answer = None
    while answer not in options:
        answer = input(f"\033[93m{' | '.join(options)} (type in)\n\033[0m")
    return answer


def get_boolean_answer(question):
    answer = None
    while answer not in ["y", "n"]:
        answer = input(f"\033[93m{question} (y/n)\033[0m")
    return answer == "y"


def select_item(prompt, iterable):
    while True:
        try:
            return iterable[int(input(f"\033[93m{prompt}\033[0m"))]
        except (ValueError, IndexError):
            continue


class Config:
    def __init__(self):
        self.config_file_dir = os.path.join(os.path.expanduser("~"), ".config/dermatillo")
        self.config_file_path = os.path.join(self.config_file_dir, "config.json")
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, "r") as file:
                self.dict = json.load(file)
        else:
            default_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files/config.json")
            with open(default_config_path, "r") as file:
                self.dict = json.load(file)

    def save(self):
        os.makedirs(self.config_file_dir, exist_ok=True)
        with open(self.config_file_path, "w") as file:
            json.dump(self.dict, file)


class NaturalOrderGroup(click.Group):
    def list_commands(self, ctx):
        return self.commands.keys()


@click.group(cls=NaturalOrderGroup)
def entry():
    pass


def get_video_sources():
    def query_video_source(source_id):
        if source_id in selected_video_sources:
            print(f"\n\033[91m{source_id} is already selected!\033[0m")
            return

        video_capture = VideoCapture(source_id)
        try:
            video_capture.start(time_out=3)
        except (video_capture.NotAvailable, video_capture.TimeOutExceeded):
            print(f"\n\033[91mnot available: {source_id}\033[0m")
            return

        choice = None
        while choice not in ["add", "skip"]:
            print(f"\n{source_id}")
            choice = get_choice(["add", "test", "skip"])
            if choice == "add":
                selected_video_sources.append(source_id)
            elif choice == "test":
                print("displaying camera image ...")
                shape = video_capture.get_frame().data.shape
                print(shape)
                scale = 500 / shape[0]
                dsize = (int(shape[1] * scale), int(shape[0] * scale))
                cv2.namedWindow(source_id)
                cv2.moveWindow(source_id, 100, 100)
                start = time.time()
                while time.time() - start < 3:
                    cv2.imshow(
                        source_id, cv2.resize(cv2.cvtColor(video_capture.get_frame().data, cv2.COLOR_RGB2BGR), dsize))
                    _ = cv2.waitKey(20)
                cv2.destroyAllWindows()
        video_capture.stop()

    os.environ["DERMATILLO_CONFIG"] = "1"
    from dermatillo.video_capture import VideoCapture

    selected_video_sources = []
    # ioreg grep -i cam
    if sys.platform == "linux":
        v4l_dir = "/dev/v4l/by-path"
        local_video_sources = sorted(os.listdir(v4l_dir))
        for local_source_id in local_video_sources:
            query_video_source(os.path.join(v4l_dir, local_source_id))

    add_network = get_boolean_answer("\nDo you want to add network camera?")
    while add_network:
        query_video_source(input("\033[93m  Please provide IP address:\n  \033[0m"))
        add_network = get_boolean_answer("\nDo you want to add another network camera?")

    if sys.platform == "linux" and len(selected_video_sources) == 0:
        print(f"\n\033[91mPlease provide at least one video source!\033[0m")
        return get_video_sources()
    return selected_video_sources


def get_audio_output():
    def get_selection():
        available_audio_output = []
        print("\nAvailable audio output devices:")
        n = 0
        for device in sd.query_devices():
            if device["max_output_channels"] > 0:
                crop_idx = device["name"].find("(hw:")
                if crop_idx == -1:
                    name = device["name"]
                else:
                    name = device["name"][:crop_idx]
                available_audio_output.append(name)
                if name == "default":
                    print(f"  {n}: {name}  <--- recommended")
                else:
                    print(f"  {n}: {name}")
                n += 1
        print()
        return select_item("Please provide index of selected audio output device: ", available_audio_output)

    os.environ["DERMATILLO_CONFIG"] = "1"
    from dermatillo.utils import Alarm

    audio_output = get_selection()
    choice = None
    while choice not in ["add"]:
        print(f"\n{audio_output}")
        choice = get_choice(["add", "test", "change"])
        if choice == "test":
            alarm = Alarm(audio_output)
            alarm.start()
            print("playing alarm signal ...")
            alarm.trigger()
        elif choice == "change":
            audio_output = get_selection()

    return audio_output


def do_config():
    def confirm_config(prompt):
        video_sources = configuration.dict["VIDEO_SOURCES"]
        audio_output_device = configuration.dict["AUDIO_OUTPUT_DEVICE"]
        if len(video_sources) > 0:
            print("\nvideo sources:")
            for i, video_source_id in enumerate(video_sources):
                print(f"  {i}: {video_source_id}")
            print(f"\naudio output device:\n  {audio_output_device}")
            if get_boolean_answer(prompt) is False:
                sys.exit(0)

    configuration = Config()
    confirm_config("\nDo you want to overwrite current I/O set-up?")

    service_stopped = False
    if sys.platform == "linux":
        service_stopped = subprocess.check_call(["systemctl", "--user", "stop", "dermatillo"]) == 0

    configuration.dict["VIDEO_SOURCES"] = get_video_sources()
    configuration.dict["AUDIO_OUTPUT_DEVICE"] = get_audio_output()
    confirm_config("\nDo you want to continue with this I/O set-up?")
    configuration.save()

    if service_stopped:
        subprocess.run(["systemctl", "--user", "start", "dermatillo"])

    if get_boolean_answer("\nDo you want to set Dermatillo as a service?"):
        create_systemd()
        
    print("\n\033[92mConfiguration completed.\033[0m")


@click.command()
def config():
    check_platform()
    do_config()


def create_systemd():
    if sys.platform != "linux":
        print("Service set-up is currently available on Linux only.")
        return

    remove_systemd()
    configuration = Config()
    video_sources = configuration.dict["VIDEO_SOURCES"]
    audio_output_device = configuration.dict["AUDIO_OUTPUT_DEVICE"]
    if len(video_sources) == 0 or audio_output_device == "":
        print("\nPlease run a configuration first.")
        do_config()
    else:
        systemd_dir = os.path.join(os.path.expanduser("~"), ".config/systemd/user")
        os.makedirs(systemd_dir, exist_ok=True)
        with open(os.path.join(systemd_dir, "dermatillo.service"), "w") as service_file:
            service_file.write("[Unit]\n")
            service_file.write("Description=Dermatillo systemd service\n")
            service_file.write("After=network.target\n")
            service_file.write("\n[Service]\n")
            service_file.write("Type=simple\n")
            service_file.write(f"ExecStart={sys.executable} "
                               f"{os.path.join(os.path.dirname(os.path.realpath(__file__)), 'run.py')}\n")
            service_file.write("RestartSec=5\n")
            service_file.write("Restart=always\n")
            service_file.write("\n[Install]\n")
            service_file.write("WantedBy=default.target\n")

        os.environ["DERMATILLO_CONFIG"] = "0"

        systemd_setup = [
            ["systemctl", "--user", "enable", "dermatillo"],
            ["systemctl", "--user", "daemon-reload"],
            ["systemctl", "--user", "start", "dermatillo"]
        ]
        success = [subprocess.check_call(cmd) == 0 for cmd in systemd_setup]
        if all(success):
            time.sleep(3)
            print("\n\033[92mDermatillo systemd service enabled. It should be reported as active."
                  "\nClose status with 'q'.\033[0m")
            subprocess.run(['systemctl', 'status', '--user', 'dermatillo'])
        else:
            print("\n\033[91mDermatillo systemd service set-up failed!\033[0m")


def remove_systemd():
    subprocess.run(["systemctl", "--user", "stop", "dermatillo"])
    subprocess.run(["systemctl", "--user", "disable", "dermatillo"])
    subprocess.run(["systemctl", "--user", "daemon-reload"])
    subprocess.run(["systemctl", "--user", "reset-failed"])


@click.command()
def service_set():
    check_platform()
    create_systemd()


@click.command()
def service_status():
    print("\n\033[92mClose status with 'q'.\033[0m")
    subprocess.run(['systemctl', 'status', '--user', 'dermatillo'])


@click.command()
def service_remove():
    remove_systemd()


@click.command()
def run():
    from dermatillo.run import entry
    entry()


@click.command(help="-t [minutes]")
@click.option("-t")
def halt(t: str):
    try:
        time_out = int(t)
    except (TypeError, ValueError):
        print("run 'dermatillo halt -t [minutes]'")
        sys.exit(1)
    if time_out > 720 and not get_boolean_answer(f"Do you wish to halt Dermatillo for {time_out} minutes?"):
        sys.exit(0)
    os.environ["DERMATILLO_CONFIG"] = "1"
    from dermatillo.utils import mission_control
    mission_control.halt(time_out)


@click.command()
def log():
    pass


@click.command()
def defaults():
    pass


@click.command()
def version():
    import dermatillo
    print(f"{dermatillo.__name__}-{dermatillo.__version__}")


@click.command()
def legal():
    from dermatillo.config import DERMATILLO_DIR
    print("Copyright (c) 2022 by Jan Grzybek, lyre_embassy_0n@icloud.com")
    print("All Rights Reserved.\n")
    input("Press ENTER to print out LICENSE text")
    print()
    with open(os.path.join(DERMATILLO_DIR, "files/LICENSE"), "r") as f:
        print(f.read())


entry.add_command(config)
entry.add_command(service_set)
entry.add_command(service_status)
entry.add_command(service_remove)
entry.add_command(run)
entry.add_command(halt)
entry.add_command(log)
entry.add_command(defaults)
entry.add_command(version)
entry.add_command(legal)
