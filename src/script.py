import os
%matplotlib inline
import json
import scipy.stats as stats
from pandas.io.json import json_normalize
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle, ConnectionPatch
from matplotlib.offsetbox import  OffsetImage
import squarify
from functools import reduce
plt.style.use('default')
font = {'weight': 'bold',
        'size':   16}
plt.rc('font', **font)





def match_to_pandas_events(match):
    with open(f'../data/events/{match}') as data_file:    
        data = json.load(data_file)
    return pd.json_normalize(data, sep = "_")
def match_to_pandas_lineups(match):
    with open(f'../data/lineups/{match}') as data_file:    
        data = json.load(data_file)
    return pd.json_normalize(data, sep = "_")



laliga_dict = {}
for filename in os.listdir('../data/matches/11'):
    laliga_dict[filename] = pd.json_normalize(json.load(open('../data/matches/11' + '/' + filename)),sep="_")
    
    
    
laliga_merged_matches = pd.concat(laliga_dict.values(),ignore_index = True)



laliga_last_season = laliga_merged_matches.query('season_season_id == [4]')
laliga_last_season.reset_index()
laliga_matchids = list(laliga_last_season['match_id'])
for idx,i in enumerate(laliga_matchids):
    laliga_matchids[idx] = str(i)
    

    
    

laliga_lastseason_events = {}
for filename in os.listdir('../data/events'):
        if filename[:-5] not in laliga_matchids:
            continue
        laliga_lastseason_events[int(filename[:-5])] = match_to_pandas_events(filename)

        

    
laliga_last_season.set_index('match_id', inplace=True)
laliga_last_season['events'] = laliga_last_season.index.map(laliga_lastseason_events)



# code from https://towardsdatascience.com/advanced-sports-visualization-with-pandas-matplotlib-and-seaborn-9c16df80a81b
def draw_pitch(ax):
    # focus on only half of the pitch
    #Pitch Outline & Centre Line
    Pitch = Rectangle([0,0], width = 120, height = 80, fill = False)
    #Left, Right Penalty Area and midline
    LeftPenalty = Rectangle([0,22.3], width = 14.6, height = 35.3, fill = False)
    RightPenalty = Rectangle([105.4,22.3], width = 14.6, height = 35.3, fill = False)
    midline = ConnectionPatch([60,0], [60,80], "data", "data")

    #Left, Right 6-yard Box
    LeftSixYard = Rectangle([0,32], width = 4.9, height = 16, fill = False)
    RightSixYard = Rectangle([115.1,32], width = 4.9, height = 16, fill = False)


    #Prepare Circles
    centreCircle = plt.Circle((60,40),8.1,color="black", fill = False)
    centreSpot = plt.Circle((60,40),0.71,color="black")
    #Penalty spots and Arcs around penalty boxes
    leftPenSpot = plt.Circle((9.7,40),0.71,color="black")
    rightPenSpot = plt.Circle((110.3,40),0.71,color="black")
    leftArc = Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")
    
    element = [Pitch, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle, 
               centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc]
    for i in element:
        ax.add_patch(i)
        

        
def auto_matchlist_locations(match_ids): 
    d = {}
    for i in match_ids:
        home = laliga_last_season['home_team_home_team_name'].loc[int(i)]
        away = laliga_last_season['away_team_away_team_name'].loc[int(i)]
        home_loc = laliga_last_season['events'][int(i)].loc[(laliga_last_season['events'][int(i)]['possession_team_name'] == home),['location']].dropna(subset=['location'])['location']
        away_loc = laliga_last_season['events'][int(i)].loc[(laliga_last_season['events'][int(i)]['possession_team_name'] == away),['location']].dropna(subset=['location'])['location']
        d[(home,away)] = (home_loc,away_loc)
    return d
event_locos_lastseason = auto_matchlist_locations(laliga_matchids)