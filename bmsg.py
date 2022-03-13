# This program goes through a csv file of staff names, emails, phone numbers
# and birthdays, checks for those whose birthday might be today and sends a
# Birthday Felicitation email(s) to them
# Created by Uwa V. Isibor, March 2022


############## Imports ##############

# import port_check
import datetime as dtime
import pandas as pd
import random
import time
import smtplib, os

from email.mime.text import MIMEText
from img_sources.gif_images import gif_images
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('EMAIL_HOST')
port = os.getenv('EMAIL_PORT')
user = os.getenv('EMAIL_HOST_USER')
password = os.getenv('EMAIL_PASSWORD')


############## Program Logic ##############

def connect():    
    # make the server variable global so other 
    # functions in the program can call it
    global server
    
    # open a connection with the smtplib library
    server = smtplib.SMTP(host, port)

    # identify yourself to the server
    server.ehlo()

    # secure the connection
    server.starttls()

    # send the email
    server.login(user, password)   
     
      
def bdaycheck():
    # read the data
    data = pd.read_csv("birthdays.csv")

    # current day and month
    current_day = dtime.datetime.now().day
    current_month = dtime.datetime.now().month

    # a list to hold the detail(s) retrieved from rows that have the
    # current day as birthdays incase there are more than one celebrant
    details = []

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

            # retrieve the number from the row and save it in the variable, celebnumber
            cnumber = data.iloc[row][' phone_number'].lstrip()

            # put them all into a list
            tmp = [cemail, cfirstname, clastname, cnumber]
            details.append(tmp)       
    
    # open an smtp connection
    connect()
    
    # call the sendmail function and pass the details list to itd
    sendmail (details)

    

def sendmail(details):
    # loop through the filtered birthday list
    for i in range(len(details)):

        # open a random html file out of the three files that exists
        with open(f"./templates/letter_{random.randint(1, 1)}.html") as bday_msg:

            # reading the file
            msg_contents = bday_msg.read()

            # replace the html [NAME] tag with the actual name on the data
            the_msg = msg_contents.replace("[NAME]", f"{details[i][1]} {details[i][2]}")
            the_email = details[i][0]

            # replace the GIF image with one from the imported python files
            the_msg = the_msg.replace("[GIF IMAGE]", random.choice(gif_images))

            # create the msg
            msg = MIMEText(the_msg, 'html')
            msg["From"] = "Ministry of Industry Trade and Cooperatives <bladesofsteel2009@hotmail.com>"
            msg["To"] = the_email
            msg["Subject"] = f"Happy Birthday {details[i][1]} {details[i][2]}!!"            
        
        
        try:
            # displays whom the message is being sent to
            print('')
            print(f"Sending birthday felicitation to {details[i][0]}... \n")

            # send the email
            server.send_message(msg)

            # print a confirmation if message was sent successfully
            print(f"Birthday Felicitation sent \n")                       

        except Exception as e:

            # print an error message if message failed to send
            print(f"Message not sent to {details[i][0]} \n \
                  REASON: {e} \n\n")
            
            # update the program admin if message failed to deliver
            server.send_message(msg["From"], 'neutrolysis@gmail.com', message=f"Birthday Felicitation message \
                                    to {details[i][1]} <{details[i][0]}> failed to deliver")

    # time before sever closes
    time.sleep(5)
    
    
    # close the server
    server.close()
    print("Goodbye \n")  


# initiate the program
bdaycheck()