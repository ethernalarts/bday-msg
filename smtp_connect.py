
import smtplib
import os

user = os.environ['HOTMAIL_ACCT']
password = os.environ['HOTMAIL_PSWD']

def connect():
    # make the server variable global so other 
    # functions in the program can call it
    global server
    
    # open a connection with the smtplib library
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)

    # identify yourself to the server
    server.ehlo()

    # secure the connection
    server.starttls()

    # send the email
    server.login(user, password)
    

connect()