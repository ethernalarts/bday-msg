
from datetime import date
import time
import pandas as pd
import sys


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

            email = data.iloc[row][' email'].lstrip()
            firstname = data.iloc[row]['first_name']
            lastname = data.iloc[row][' last_name'].lstrip()
            number = data.iloc[row][' phone_number'].lstrip()

            details.append([email, firstname, lastname, number])

    if (len(details) == 0):
        print("No birthdays today. Goodbye. \n")

    else:
        print("We have birthday(s) today:\n")

        for i in range(len(details)):
            print(f"{i+1}. {details[i][1]} {details[i][2]} ({details[i][0]}) {details[i][3]}\n")

    sys.exit()

bdaycheck()
