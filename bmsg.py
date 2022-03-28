''' This program goes through a csv file of staff details.
It returns a list of those that have birthdays and sends
Birthday Felicitation Email(s) to them.
AUTHOR: Uwa V. Isibor, March 2022
CLIENT: Edo State Ministry of Industry, Trade and Cooperatives '''

from datetime import date
import time
import pandas as pd
import random
import smtplib, os
import sys

from email.mime.text import MIMEText
from dotenv import load_dotenv
from win10toast import ToastNotifier

load_dotenv()

host = os.getenv('EMAIL_HOST')
port = os.getenv('EMAIL_PORT')
user = os.getenv('EMAIL_HOST_USER')
password = os.getenv('EMAIL_PASSWORD')
prog_admin = os.getenv('ADMIN_EMAIL')

# for desktop notification
toast = ToastNotifier()


# Program Logic

def bdaycheck():
    data = pd.read_csv("stafflist.csv")

    current_day = date.today().day
    current_month = date.today().month

    details = []

    print("\nChecking...\n")

    time.sleep(2)

    # check if the month and day of a row is equal to
    # the current month and current day
    for row in range(len(data)):
        if((data.iloc[row][' month'] == current_month) and (data.iloc[row][' day'] == current_day)):

            sn = row
            email = data.iloc[row][' email'].lstrip()
            firstname = data.iloc[row]['first_name']
            lastname = data.iloc[row][' last_name'].lstrip()
            number = data.iloc[row][' phone_number'].lstrip()
            
            details.append([sn, firstname, lastname, email, number])
    
    if (len(details) == 0):
        print("No birthdays today. Goodbye. \n")

        time.sleep(1)

        sys.exit()
    else:
        print("We have birthday(s) today:\n")
        
        for i in range(len(details)):
            print(f"{sn+2}. {firstname} {lastname} \n")

        time.sleep(2)

        print("Connecting...\n")

        time.sleep(2)

        try:
            connect(details)
            
        except Exception as e:
            print(f"Connection failed. Reason: {e} \n")


def connect(details):
    global server

    # open a connection
    server = smtplib.SMTP(host, port)

    # identify yourself to the server
    server.ehlo()

    # secure the connection
    server.starttls()

    server.login(user, password)

    print("Connected.\n")

    time.sleep(2)

    sendmail(details)


def sendmail(details):

    for i in range(len(details)):

        # open a random html file out of the three files that exists
        with open(f"./templates/inlinecard_{random.randint(1, 1)}.html") as bday_msg:

            card_contents = bday_msg.read()

        card_msg = card_contents.replace("[NAME]", f"{details[i][1]} {details[i][2]}")
        to_email = details[i][3]

        msg = MIMEText(card_msg, 'html')
        msg["From"] = "Ministry of Industry Trade and Cooperatives <bladesofsteel2009@hotmail.com>"
        msg["To"] = to_email
        msg["Subject"] = f"Happy Birthday {details[i][1]} {(details[i][2]).rstrip()}!!"

        try:
            print(f"Sending Birthday felicitations to {details[i][1]} {details[i][2]}({details[i][3]})... \n")

            server.send_message(msg)

            print(f"Birthday Felicitation sent \n")

        except Exception as e:
            print(f"Message not sent to {details[i][1]} {details[i][2]} ({details[i][3]}) \
                REASON: {e} \n\n")  

    print("Closing server...\n")

    time.sleep(2)

    server.close()

    print("Goodbye. \n")
    
    toast.show_toast("Email Sent!",
                     f"{details[i][1]} {details[i][2]} was sent an e-mail",
                     threaded=True,
                     icon_path=None,
                     duration=6)

    while toast.notification_active():
        time.sleep(0.2)

    sys.exit()


# launch the program
bdaycheck()
