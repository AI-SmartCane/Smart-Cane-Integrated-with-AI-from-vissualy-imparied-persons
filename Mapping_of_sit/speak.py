# speak.py — speaks the location description aloud using the Windows built-in voice (offline).
#   python speak.py 13.32592 77.12459   -> speaks one location
#   python speak.py                     -> asks for coordinates repeatedly
# Hand-off point for the stick: its audio module calls say(describe(lat, lon)).

import sys

import pyttsx3

from locator import locate


def describe(lat, lon):
    return locate(lat, lon)["description"]


def say(text):
    """Speak one sentence. A fresh engine per call stops pyttsx3 going silent after the first one."""
    print(text)
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)          # words per minute; lower is slower
    engine.say(text)
    engine.runAndWait()
    engine.stop()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        say(describe(float(sys.argv[1]), float(sys.argv[2])))
    else:
        while True:
            text = input("\nEnter latitude, longitude (blank to quit): ").strip()
            if not text:
                break
            try:
                lat, lon = (float(x) for x in text.replace(",", " ").split())
            except ValueError:
                print("Please type two numbers, e.g. 13.32592 77.12459")
                continue
            say(describe(lat, lon))