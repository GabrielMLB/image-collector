"""
Author: Madruga
Date: 06/07/2022

Params:
path: Path where images will be saved
time: Time interval (in seconds) that images will be saved

Usage:
python3 main.py --path /media/usb-drive/images --time 300
"""

from realsense import Realsense
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description='Image collector')
parser.add_argument("-p", "--path", type=str, help='path to save images')
parser.add_argument("-t", "--time", type=int, default=300, help="time to save images")
args = parser.parse_args()


def main():
    now = datetime.now().strftime("%c")
    config = {
        "day": now,
        "path": args.path,
        "time": args.time
    }
    print(" ")
    print(f"Params:")
    print(config)
    print(" ")

    camera = Realsense()
    camera.save_frames(args.path, args.time)


if __name__ == '__main__':
    main()
