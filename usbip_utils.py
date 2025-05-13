import subprocess
import os

def list_devices():
    try:
        output = subprocess.check_output(["usbip", "list", "-l"], encoding="utf-8")
    except subprocess.CalledProcessError:
        return []

    devices = []
    current_device = {}

    for line in output.splitlines():
        line = line.strip()
        if line.startswith("- busid"):
            if current_device:
                devices.append(current_device)
            parts = line.split()
            busid = parts[2]
            current_device = {
                "busid": busid,
                "info": "",
                "bound": is_bound(busid)
            }
        elif ":" in line:
            current_device["info"] += line.strip() + " "

    if current_device:
        devices.append(current_device)

    return devices

def is_bound(busid):
    path = f"/sys/bus/usb/drivers/usbip-host/{busid}"
    return os.path.exists(path)

def bind_device(busid):
    try:
        subprocess.check_output(["usbip", "bind", "-b", busid], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Error] Failed to bind {busid}: {e.output}")
        return False

def unbind_device(busid):
    try:
        subprocess.check_output(["usbip", "unbind", "-b", busid], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Error] Failed to unbind {busid}: {e.output}")
        return False
