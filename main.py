import pandas as pd
import numpy as np
import json
from sklearn.utils import shuffle


####### TO CHANGE
comp_id = "OakvilleFallA2022"
json_path = r"data\{}.json".format(comp_id)
df_groups = pd.read_csv(r"data\A groups.csv")
#######

#notes
#removed delegates from original groups files



#json file open
f = open(json_path, encoding="utf8")
dict_json = json.load(f)

#change json to df
dict_wcifCompetitor = dict_json['persons']
df_wcifCompetitor = pd.DataFrame.from_dict(dict_wcifCompetitor)

#use group df
df_groups = df_groups.set_index('Person')
df_groups = shuffle(df_groups, random_state=12091998)

#parameters for judging
STAGE_COUNT = 9 #per colour

#find all stages available to judge
dict_stages = {}
events = []
for name, values in df_groups.iteritems():
    dict_stages[name] = pd.DataFrame(values.unique(), columns=["Group"])
    #add delimited values, and a count
    dict_stages[name][["Stage", "Group"]] = dict_stages[name]["Group"].str.split(" ", expand=True)
    dict_stages[name]["Required"] = STAGE_COUNT
    dict_stages[name]['Combined'] = dict_stages[name]['Stage'] + " " + dict_stages[name]['Group']
    dict_stages[name] = dict_stages[name].set_index('Combined')
    events.append(name)

#create df for competitor priority
df_judgeAssignment = pd.DataFrame().reindex_like(df_groups)

df_judgeAssignment["Count"] = np.nan
for event in events:
    #df_judgeAssignment[event] = jugdeAssignmentbyEvent(dict_stages[event], event, df_groups[event], df_judgeAssignment[event])
    #carried over from function
    df_stageInfo = dict_stages[event]
    
    
    event = event
    ser_groups = df_groups[event]
    ser_judgeAssignment = df_judgeAssignment[event]
    
    df_groupsDelimit = ser_groups.str.split(" ", expand=True)
    df_groupsDelimit[1] = pd.to_numeric(df_groupsDelimit[1], errors = "ignore")
    dict_maxPerStage = pd.to_numeric(df_stageInfo.groupby(["Stage"])["Group"].max(), errors = "ignore").to_dict()
    
    for index, row in df_groupsDelimit.iterrows():
        
        dummy = ""
        if row[0] == "0": #if competitor is not in event, do not account
            dummy = np.nan

        else:
            print(str(row[1]) + " --- " + str(dict_maxPerStage[row[0]]))
            if row[1] == dict_maxPerStage[row[0]]:
                dummy = row[0] + " 1" #if last group, judge group 1
                
            else:
                try:
                    dummy = row[0] + " " + str(int(row[1]+1)) #if any other group, judge group after
                except: dummy = row[0] + " " + str(row[1]+1)
        
        if dummy != np.nan:
            if df_stageInfo["Required"][dummy] > 0:
                df_stageInfo["Required"][dummy] -=1
                ser_judgeAssignment[index] = dummy
        
        if df_stageInfo["Required"].sum == 0:
            break

    df_judgeAssignment["Count"] = df_judgeAssignment[events].count(axis=1)
    df_groups["Count"] = df_judgeAssignment[events].count(axis=1)
    df_groups = df_groups.sort_values(by=["Count"], ascending = "True") #sort by lowest to highest, to force new people to judge where required
    
    
df_judgeAssignment.to_csv("data/judging_assignments_{}.csv".format(comp_id), encoding='utf-8', index=True)
df_judgeAssignmentPrint = df_judgeAssignment.fillna("")
df_judgeAssignmentPrint = df_judgeAssignment.drop("Count", axis=1)
df_judgeAssignmentPrint = df_judgeAssignmentPrint.sort_values(by=["Person"], ascending = "True")

print(df_judgeAssignmentPrint.to_markdown())

    

    




#only judge if they are within the group
#cannot judge if they are in the same number group
#keep on that specific stage if possible
#if they are group 1, automatically assign group 2, otherwise assign 1 group back
#random selection of 8 people for each group
#delegates cannot judge

#priorize lower if new competitor
#priorize higher if WCA ID age is top 35%
#priorize higher if result in event already
