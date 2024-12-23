import os
import subprocess
import random
import string
import shutil

def mount_disk(device: str) -> str | None:
    if os.path.ismount("/mnt"):
        return None

    random_dir = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    mount_point = f"/mnt/{random_dir}"

    try:
        _ = subprocess.check_call(["sudo", "mkdir", "-p", mount_point])
        _ = subprocess.check_call(["sudo", "mount", device, mount_point])

        if not os.path.ismount(mount_point):
            return None

    except Exception as e:
        return None

    return mount_point

def unmount_disk(mount_point: str) -> bool:
    try:
        if os.path.ismount(mount_point):
            _ = subprocess.check_call(["sudo", "umount", mount_point])

            if not os.path.ismount(mount_point):
                _ = subprocess.check_call(["sudo", "rmdir", mount_point])
                return True
            else:
                return False

    except Exception as e:
        return False

    return False

def check_if_linux_home(mount_point: str, user: str):
    home_dir = os.path.join(mount_point, f"/home/{user}/")
    return os.path.exists(home_dir)

def destroy_dir(src) -> bool:
    try:
        if os.path.exists(src):
            _ = subprocess.check_call(["rm", "-rf", src])
    except:
        return False


    return True

def copy_dir(src, dst) -> bool:
    try:
        _ = subprocess.check_call(["cp", "-r", src, dst])

    except:
        return False


    return True

