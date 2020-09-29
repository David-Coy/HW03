import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import pdb
import csv
#python3 main.py > output.txt
#https://stackoverflow.com/questions/43891391/pandas-dataframe-read-skipping-line-xxx-expected-x-fields-saw-y
#url = "https://gt.bootcampcontent.com/GT-Coding-Boot-Camp/gt-atl-data-pt-09-2020-u-c/raw/master/02-Homework/03-Python/Instructions/PyBank/Resources/budget_data.csv"
#inpFile = pd.read_csv(url, sep='\t', error_bad_lines= False,quoting=csv.QUOTE_NONE)
#pdb.set_trace()

with open('file.txt', 'w') as f:
    # Path to collect data from the Resources folder
    pybank_csv = os.path.join('.', 'resources', '02-Homework_03-Python_Instructions_PyBank_Resources_budget_data.csv')

    #The total number of months included in the dataset
    count_months = 0
    with open(pybank_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        next(csv_reader)# Skips the header row
        for row in csv_reader:
            count_months = count_months + 1
            message = f'Total Months: {count_months}'
    print(message, file=f)
    print(message)

    #The net total amount of "Profit/Losses" over the entire period
    net_profit = 0
    with open(pybank_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        next(csv_reader)# Skips the header row
        for row in csv_reader:
            net_profit = net_profit + float(row[1])
    message = f'Total: ${net_profit:.0f}'
    print(message, file=f)
    print(message)

    #The average of the changes in "Profit/Losses" over the entire period
    with open(pybank_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        next(csv_reader)# Skips the header row
        old = 0
        change_profit=[]
        for row in csv_reader:
            change_profit.append(float(row[1]) - old)
            old = float(row[1])
    message = f'Total: ${sum(change_profit[1:])/(len(change_profit)-1):.2f}' 
    print(message, file=f)
    print(message)
    
    #The greatest increase in profits (date and amount) over the entire period
    with open(pybank_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        next(csv_reader)# Skips the header row
        old = 0
        change_profit=[]
        max_change = 0
        date = ''
        for row in csv_reader:
            change_profit = float(row[1]) - old
            old = float(row[1])
            if change_profit > max_change:
                max_change = change_profit
                date = row[0]
    message = f'Greatest Increase in Profits: {date} $({max_change:.0f})' 
    print(message, file=f)
    print(message)

    #The greatest decrease in losses (date and amount) over the entire period
    with open(pybank_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        next(csv_reader)# Skips the header row
        old = 0
        change_profit=[]
        max_dec = 0
        date = ''
        for row in csv_reader:
            change_profit = float(row[1]) - old
            old = float(row[1])
            if change_profit < max_dec:
                max_dec = change_profit
                date = row[0]
    message = f'Greatest Decrease in Profits: {date} $({max_dec:.0f})' 
    print(message, file=f)
    print(message)
    f.close()