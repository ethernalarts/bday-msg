# This program goes through a csv file of staff details.
# It returns a list of those that have birthdays and sends 
# Birthday Felicitation Email(s) to them.
# AUTHOR: Uwa V. Isibor, March 2022
# CLIENT: Edo State Ministry of Industry, Trade and Cooperatives


############## Imports ##############

from datetime import  date
import pandas as pd
import random
import time
import smtplib
import os
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


############## Program Logic ##############

def bdaycheck():
    # read the file
    data = pd.read_csv("stafflist.csv")

    # current day and month
    current_day = date.today().day
    current_month = date.today().month

    # a list to hold the detail(s) retrieved from rows that have the
    # current day as birthdays incase there are more than one celebrant
    details = list()

    # effects
    print("\nChecking...\n")

    # effects
    time.sleep(2)

    # loop through the pandas DataFrame
    for row in range(len(data)):

        # check if the month and day of a row is equal to
        # the current month and current day
        if((data.iloc[row][' month'] == current_month) and (data.iloc[row][' day'] == current_day)):

            # retrieve the email from the row and save it in the variable, cemail
            cemail = data.iloc[row][' email'].lstrip()

            # retrieves the first name from the row and save it in the variable, cfirstname
            cfirstname = data.iloc[row]['first_name']

            # retrieves the last name from the row and save it in the variable, clastname
            clastname = data.iloc[row][' last_name'].lstrip()

            # retrieve the number from the row and save it in the variable, cnumber
            cnumber = data.iloc[row][' phone_number'].lstrip()

            # put them into the details list
            details.append([cemail, cfirstname, clastname, cnumber])

    if (len(details) == 0):
        # confirmatory message        
        print("No birthdays today. Goodbye. \n")

        # time delay of 1 second
        time.sleep(1)

        # terminates the program
        sys.exit()

    else:
        # confirmatory message
        print("We have birthday(s) today:..\n")
        
        # print the names of the celebrants
        for i in range(len(details)):
            print(f"{i+1}. {details[i][1]} {details[i][2]} \n")
        
        # time delay of 2 seconds        
        time.sleep(2)
        
        # status message
        print("Connecting...")
        
        # time delay of 2 seconds        
        time.sleep(2)

        try:
            # opens an smtp connection
            connect(details)

        except Exception as e:
            # effects
            print(f"Connection failed. Reason: {e} \n")


def connect(details):
    # make the "server" variable global so other
    # functions in the program can call it
    global server

    # open a connection with the smtplib library
    server = smtplib.SMTP(host, port)

    # identify yourself to the server
    server.ehlo()

    # secure the connection
    server.starttls()

    # log in
    server.login(user, password)

    # confirmatory message
    print("Connected.\n")

    # effects
    time.sleep(2)

    # call the sendmail function and pass the details list to it
    sendmail(details)


def sendmail(details):

    # loop through the birthday celebrants list
    for i in range(len(details)):

        # open a random html file out of the three files that exists
        with open(f"./templates/inlinecard_{random.randint(1, 1)}.html") as bday_msg:

            # reading the file
            card_contents = bday_msg.read()

            # replace the html [NAME] tag with the actual name on the data
            card_msg = card_contents.replace("[NAME]", f"{details[i][1]} {details[i][2]}")
            to_email = details[i][0]

            # create the msg
            msg = MIMEText(card_msg, 'html')
            msg["From"] = "Ministry of Industry Trade and Cooperatives <bladesofsteel2009@hotmail.com>"
            msg["To"] = to_email
            msg["Subject"] = f"Happy Birthday {details[i][1]} {details[i][2]}!!"

        try:
            print(f"Sending Birthday felicitations to {details[i][1]} {details[i][2]} ({details[i][0]})... \n")

            # send the email
            server.send_message(msg)

            # confirmatory message
            print(f"Birthday Felicitation sent \n")

        except Exception as e:
            # error message
            print(f"Message not sent to {details[i][1]} {details[i][2]} <{details[i][0]}> \
                  REASON: {e} \n\n")

    
    # confirmatory message
    print("Closing server...\n")

    # time before sever closes
    time.sleep(2)

    # close the server
    server.close()

    # confirmatory message
    print("Goodbye. \n")


# launch the program
bdaycheck()
