
from datetime import date
import time
import pandas as pd
import sys


def bdaycheck():
    data = pd.read_csv("stafflist.csv")

    current_day = date.today().day
    current_month = date.today().month

    print("\nChecking...\n")

    time.sleep(2)

    # check if the month and day of a row is equal to
    # the current month and current day
    for row in range(len(data)):
        if((data.iloc[row][' month'] == current_month) and (data.iloc[row][' day'] == current_day)):

            print(f"{row + 2}. {data.iloc[row]['first_name']} {data.iloc[row][' last_name']} \n")
        
        else:
            pass    

    sys.exit()

bdaycheck()
