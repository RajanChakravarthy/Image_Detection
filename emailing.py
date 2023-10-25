import smtplib
import imghdr
from email.message import EmailMessage
import os
import glob
from threading import Thread

def clean_folder():
    print('Clean_folder function started.')
    files = glob.glob('images/*.png')
    for file in files:
        os.remove(file)
    print('Clean_folder function ended.')

password = os.getenv('PASSWORD')
sender = 'rajanchakravarthy@gmail.com'
receiver = 'rajanchakravarthy@gmail.com'

def send_email(image_path):
    print('Send_email function started')

    # initiates an EmailMessage object and it behaves like a dic and key have to be defined
    # key like Subject, content and attachment.
    email_message = EmailMessage()
    email_message['Subject'] = 'New Intruder detected !!'
    email_message.set_content('Hey, we just detected a new intruder. ')

    with open(image_path, mode = 'rb') as file:
        content = file.read()
    email_message.add_attachment(content, maintype='image', subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()

    print('Send_email function ended.')

    clean_thread = Thread(target=clean_folder)
    clean_thread.daemon = True
    clean_thread.start()

if __name__ == '__main__':
    send_email('images/17.png')