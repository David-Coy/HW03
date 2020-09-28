import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import pdb
import csv
python3 main.py > output.txt
#https://stackoverflow.com/questions/43891391/pandas-dataframe-read-skipping-line-xxx-expected-x-fields-saw-y
#url = "https://gt.bootcampcontent.com/GT-Coding-Boot-Camp/gt-atl-data-pt-09-2020-u-c/raw/master/02-Homework/03-Python/Instructions/PyBank/Resources/budget_data.csv"
#inpFile = pd.read_csv(url, sep='\t', error_bad_lines= False,quoting=csv.QUOTE_NONE)
#pdb.set_trace()

# Path to collect data from the Resources folder
pybank_csv = os.path.join('.', 'resources', '02-Homework_03-Python_Instructions_PyBank_Resources_budget_data.csv')
df = pd.read_csv(pybank_csv)



#The total number of months included in the dataset
total_months =len(df["Date"].str.extract(r'([a-zA-Z]{3})')[0])#Total non-unique Months found
print(f'Total Months: {total_months}')
#len(df["Date"].str.extract(r'([a-zA-Z]{3})')[0].unique())#Unique Months found


#The net total amount of "Profit/Losses" over the entire period
net_total = df["Profit/Losses"].sum()
print(f'Total: ${net_total}')


#The average of the changes in "Profit/Losses" over the entire period
df['Change in Profit/Losses'] = df['Profit/Losses'].diff()
average_change = df['Change in Profit/Losses'].sum()/(total_months-1)
print(f'Average Change: ${average_change}')


#The greatest increase in profits (date and amount) over the entire period
greatest_inc = df['Change in Profit/Losses'].max()
greatest_inc_date = df.loc[df['Change in Profit/Losses'] == greatest_inc]['Date'].values[0]
print(f'Greatest Increase in Profits: {greatest_inc_date} (${greatest_inc})')


#The greatest decrease in losses (date and amount) over the entire period
greatest_dec = df['Change in Profit/Losses'].min()
greatest_dec_date = df.loc[df['Change in Profit/Losses'] == greatest_dec]['Date'].values[0]
print(f'Greatest Increase in Profits: {greatest_dec_date} (${greatest_dec})')
#pdb.set_trace()