import pandas as pd
pd.options.mode.chained_assignment = None

week_no =input("What week is it?")

# File Paths to Sheets with spreads + scores
spread_dummy = r"C:\Users\jmu81\NFL Picks 2023-24\Folder\SPREADSWeek"+ week_no +".xlsx"
scores_dummy = r"C:\Users\jmu81\NFL Picks 2023-24\Folder\SCORESWeek"+ week_no +".xlsx"


spread = pd.read_excel(spread_dummy)
scores = pd.read_excel(scores_dummy)


# Cutting cities off of the team names
i = 0
for i in range(len(scores)):
    team = scores['name'][i]
    x = -1
    for counter in range(len(team)):
        z = team[x]
        if z == ' ':
            x += 1
            scores['name'][i] = team[x:]
        else:
            x = x - 1

scores.rename(columns={'name':'Team', 'score': 'Score'}, inplace=True)            

#Joining Scores and Spreads on Team Name
master = pd.merge(spread, scores, on='Team', how ='right')


master['Opponent_Score'] = None
i = 0

#Adding the Opponent_Score column to the dataframe
for i in range(len(master)):
    print(master)
    print(i)
    if i == 0:
        master['Opponent_Score'][i] = master['Score'][i+1]
        i +=1
    elif master['Team'][i] == master['Opponent'][i-1]:
        master['Opponent_Score'][i] = master['Score'][i-1]
        i += 1
    else:
        master['Opponent_Score'][i] = master['Score'][i+1]
        i += 1



i = 0
master['Result'] = None

#Assigning the result to the contest
for i in range(len(master)):
    combo = master['Score'][i] + master['Spread'][i]
    if combo > master['Opponent_Score'][i]:
        master['Result'][i] = 'W'
        i += 1
    elif  combo < master['Opponent_Score'][i]:
        master['Result'][i] = 'L'
        i += 1
    else:
        master['Result'] = 'Push'
        i += 1


master.to_excel(r"C:\Users\jmu81\NFL Picks 2023-24\Folder\MasterWeek"+ week_no + ".xlsx", index = False)
print(master)

