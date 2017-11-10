#!/usr/bin/env python
# Terry Davis Live-Stream Notifier v6.07
# Works with Windows, Mac, Linux, Pyhton 2 and 3
# Requires installing the "Requests" Python library (pip install requests)

import requests
import platform
from time import sleep
from os import system
from sys import stdout

def notify(opsys, title, msg, audiomsg):
    print("\n" + msg)
    if opsys == "Linux":
        system('notify-send "{}" "{}"'.format(title, msg))
        system('spd-say " {} "'.format(audiomsg))
    elif opsys == "Darwin":
        system("""osascript -e 'display notification "{}" with title "{}"'""".format(msg, title))
        system('say "{}"'.format(audiomsg))
    elif opsys == "Windows":
        system("""PowerShell -Command "Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{}');""".format(audiomsg))
        system('echo ^G') # Catch-all system beep for systems not running PowerShell
    else:
        print('\a')

def isstreaming():
    streaming, offline, failed = True, False, False
    title = "Alert"
    msg = "Terry Davis is live-streaming."
    audiomsg = "Hey faggot, Terry Davis is live-streaming."
    notify(opsys, title, msg, audiomsg)
    return streaming, offline, failed

def isoffline():
    offline, streaming, failed = True, False, False
    title = "Alert"
    msg = "Terry Davis is offline."
    audiomsg = msg
    notify(opsys, title, msg, audiomsg)
    return offline, streaming, failed

def isfail():
    failed, streaming, offline = True, False, False
    title = "Alert"
    msg = "Failed to connect to templeos.org."
    audiomsg = "Failed to connect to temple oh ess dot org."
    notify(opsys, title, msg, audiomsg)
    return failed, streaming, offline

opsys = platform.system()
streaming, offline, failed = False, False, False

while True:
    try:
        res = requests.head('http://www.templeos.org/hls/templeos.m3u8', timeout=3)
        if res.reason == "OK":
            if streaming == False:
                streaming, offline, failed = isstreaming()
            else: pass
        elif res.reason != "OK":
            if offline == False:
                offline, streaming, failed = isoffline()
            else: pass
    except:
        if failed == False:
            failed, streaming, offline = isfail()
        else:
            pass
    stdout.write('.')
    sleep(60)
