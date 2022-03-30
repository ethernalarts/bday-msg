
from datetime import date
import time
import pandas as pd
import sys


def bdaycheck():
    data = pd.read_csv("stafflist.csv")

    current_day = date.today().day
    current_month = date.today().month
    
    counter = 0

    print("\nChecking...\n")

    time.sleep(2)

    # check if the 'month' and 'day' of a row is equal to
    # the current month and current day
    for row in range(len(data)):
                    
        if((data.iloc[row][' month'] == current_month) and (data.iloc[row][' day'] == current_day)):
            if counter == 0:
                print("We have birthday(s) today: \n")
                counter = counter + 1
                time.sleep(1)

            print(f"S/N: {row + 2}")
            print(f"First Name: {data.iloc[row]['first_name']}")  
            print(f"Last Name: {data.iloc[row][' last_name'].strip()}")
            print(f"Email: {data.iloc[row][' email'].strip()}")
            print(f"Phone Number: {data.iloc[row][' phone_number'].strip()}")
            print('')
        
        elif(counter == 0) and (row == 132):
            sys.exit("No birthdays today. Goodbye \n")
        else:
            pass               

    sys.exit()

bdaycheck()
