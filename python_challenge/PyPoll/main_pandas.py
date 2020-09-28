import pandas as pd
import pdb
import csv
import os
#python3 main.py > output.txt

try:
    pypoll_csv = os.path.join('.', 'resources', '02-Homework_03-Python_Instructions_PyPoll_Resources_election_data.csv')
    df = pd.read_csv(pypoll_csv)
except:
    print("No local file!")
    url = 'https://raw.githubusercontent.com/David-Coy/HW03/master/python_challenge/PyPoll/resources/02-Homework_03-Python_Instructions_PyPoll_Resources_election_data.csv'
    df = pd.read_csv(url)



print(df)

print('Election Results \n')
#The total number of votes cast
total_voters = len(df['Voter ID'].unique())
print(f'Total Voters: {total_voters}')
#A complete list of candidates who received votes
candidates_unique = len(df['Candidate'].unique())

#The percentage of votes each candidate won
#The total number of votes each candidate won
vote_summary = df['Candidate'].value_counts()
#df_new = pd.DataFrame(columns =['Candidate', 'Percent', 'Votes'])
df_new = pd.DataFrame()
for candidate in df['Candidate'].unique():
    candidate_votes = vote_summary[candidate]
    print(f'{candidate}: {candidate_votes/total_voters*100:.3f}% ({candidate_votes})')
    '''
    dict = {'Candidate': [candidate],
            'Percent':[candidate_votes/total_voters*100],
            'Votes':[candidate_votes]}
    '''
    df_temp = pd.DataFrame.from_dict({'Candidate': [candidate],
            'Percent':[candidate_votes/total_voters*100],
            'Votes':[candidate_votes]})
    df_new = pd.concat([df_new,df_temp])
    
#The winner of the election based on popular vote.
#df.loc[df['Change in Profit/Losses'] == greatest_dec]['Date'].values[0]
#df_new.loc[df_new['Percent'] == df_new['Percent'].max()]
winner = df_new.loc[df_new['Percent'] == df_new['Percent'].max()]['Candidate'].values[0]
print(f'Winner: {winner}')


