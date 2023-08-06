#!/usr/bin/python3
import sys
import os
import subprocess
try: import cv2
except ImportError: pass
try: from mss import mss
except ImportError: pass
from pynput.mouse import Controller
import keyboard
from time import sleep

from .import config


def catch_screen(iteration: int):
    if not config.do_catch_screen:
        return
    if 'mss' not in sys.modules:
        return

    with mss() as scr:
        scr.shot(mon=-1, output=f"scr_{iteration}.png")


def catch_camera(iteration: int, cam):
    if not config.do_catch_camera:
        return
    if 'cv2' not in sys.modules:
        return

    r, frame = cam.read()
    cv2.imwrite(f"cam_{iteration}.png", frame)


def catch(iteration: int, cam) -> None:
    catch_camera(iteration, cam)
    catch_screen(iteration)

    sleep(config.delay)


def main() -> None:
    mouse = Controller()
    if config.lock_mode == "free":
        initial_pos = mouse.position
    elif config.lock_mode == "fixed":
        initial_pos = (config.lock_x,
                       config.lock_y)
        mouse.position = initial_pos
    else:
        raise TypeError

    cam = cv2.VideoCapture(0)
    
    times = config.times
    i = times
    while True:
        if mouse.position != initial_pos:
            catch(i - times, cam)
            times -= 1
            if not times:
                if config.do_execute_script:
                    subprocess.run(config.executable)
                break

        if keyboard.is_pressed(config.close_hotkey):
            break

def start():
    if config.open_hotkey is not None:
        while True:
            if keyboard.is_pressed(config.open_hotkey):
                break
    main()


if __name__ == "__main__":
    start()
