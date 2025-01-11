import subprocess
import threading
import signal
from rich import print
import sys
import os

compressed_comment = "compressed"
partial_file = "tmp"


lock = threading.Lock()
currentCompressProc = None
currentVideoDst = None

def handle(signum, frame):
    with lock:
        if currentCompressProc != None:
            os.killpg(os.getpgid(currentCompressProc.pid), signal.SIGKILL) 
            os.remove(currentVideoDst)
            print(f"[bold cyan]Removed partially compressed {currentVideoDst}.[/bold cyan]")

    sys.exit(0)

signal.signal(signal.SIGINT, handle)

# Expect two %s; First one is source, second is dest
command = open("command.txt", "r").read().strip()


def has_been_compressed(src) -> bool:
    """Check the "Comment" tag metadata of the video to see if this tool
    already compressed it."""

    process = subprocess.Popen(["exiftool", "-Comment", src], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    raw_out = process.stdout.read().decode("utf-8")

    if len(raw_out) == 0:
        return False

    return compressed_comment in raw_out.split(":")[-1]

def mark_as_compressed(src):
    process = subprocess.Popen(["exiftool", '-overwrite_original', f'-Comment="{compressed_comment}"', src], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()

def compress(src, dst) -> int:
    """Halting function that compresses a video, returns return code of
    finished function."""

    global currentVideoDst
    global currentCompressProc

    process = subprocess.Popen(command % (src, dst), shell=True, preexec_fn=os.setsid)

    with lock:
        currentVideoDst = dst
        currentCompressProc = process

    process.wait()

    return process.returncode


def main():
    file = "2019_10_02_6ec9b1538574ec7.mp4"
    if has_been_compressed(file):
        print(f"[bold green]{file} has already been compressed.")
        sys.exit(0)
    else:
        print(f"[cyan]{file} hasn't been compressed. Compressing...")

    _, ext = os.path.splitext(file)
    returncode = compress(file, partial_file + ext)
    if returncode == 0:
        og_size = os.path.getsize(file)
        compressed_size = os.path.getsize(partial_file + ext)

        mark_as_compressed(partial_file + ext)
        os.replace(partial_file + ext, file)
        print(f"[bold green]{file} has been compressed. It's {round((compressed_size / og_size) * 100)}% the size.")
    else:
        print("[bold red]Compress failed.[/bold red]")


