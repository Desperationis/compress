# compress
compress recursively searches a directory for .mp4 and .mov files and compresses them with ffmpeg, or any other tool you'd want to use. 

## Install
First install exiftool and ffmpeg via `sudo apt-get install exiftool ffmpeg`, then install the package locally by running:
```
python3 -m build .
pip3 install dist/*.whl
```

Or, you can also just run the package with `python3 -m compress [folder]`.

## Usage
Let's say you had a folder that looks like this:
```
folder/
    image.png
    my_video.mp4
    sub_dir/
        VID_2234.MOV
        VID_2234.mov
        ...
    ...
```

`python3 -m compress folder/` finds every .mp4, .mov, .MOV, and .MP4 file, and checks to see if the `Comment=` metadata contains "compressed". If it does, it skips the file and no processing is done. If it doesn't, then the tool will run the command in `command.txt`, replacing the first `%s` with the original file and the second `%s` with a temporary file. 

While it's compresing, you can exit out of the tool via CTRL+C and your data won't get overidden. 


