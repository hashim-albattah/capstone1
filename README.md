# Soccer Field Heatmap Analysis of Possesion during Barcelona (Home) v Huesca (Away) for La Liga Season 2018-19
> ![messi_barca_huesca](https://i.ytimg.com/vi/Ca8K8HObeFI/maxresdefault.jpg)
> Olé, Olé, Olé, Olé 
> Fun Fact: Soccer is the only major world sport in which you can't use your hands to manipulate the ball or object of play.
## Background
Soccer has been one of the most dominant, if not the most dominant, sports in the in the world. With fans from all over the world, you can only imagine how huge of a fanbase there is. With so many countries involved, we see so many different professional leagues and teams we can count from. I've always been into soccer as a child, but slowed down a lot in college. I've always been a fan of the La Liga, especially when Ronaldo was still in the league competing with Messi. Possession has always been a topic that every coach has emphasized, in my experience. I decided to analyze the biggest win of the 2018-2019 La Liga Season, which was the Barcelona home game against Huesca. The score was 8-2, and clearly Barcelona dominated. I wanted to look into the possessions of these teams and see if I can make some insights. 
## Data
The data was obtained from StatsBomb, which is a company that collects sports data commercially. They have an open data set, of which is open to the public and can be found [here](https://github.com/statsbomb/open-data) on their github repository. It contains a lot of data, but it is split into 4 types of JSON files:
* A single JSON file for Competitions: This was just a list of the available leagues and seasons they had on the open data
* A 'matches' folder with multiple JSON files on every single match 
* An 'events folder with multiple JSON files on every single event for each match
* A folder with multiple JSON files on every lineup for each match

The data that was mainly used consisted of 'events' data, as it contained (x,y) coordinates that could be used for exploring.


## Exploratory Data Analysis
The beginning of this capstone, I struggled a lot with getting my data figured out. To be honest, it wasn't really figured out until Tuesday and workable until Wednesday. I found a lot of this was due to the fact that I was too focused on figuring out things that I could have just asked about, wasting valuable time that could have been used on figuring out more beneficial topics. I had also spent a lot of time on other datasets beforehand that were healthcare related, but were a bit out of my scope. If you look at the Jupyter Notebook, you'll see a lot of code that has been commented out, as to show my struggles initially working with the data. Once I got over this hoop, I was able to finally start graphing things in order to get a start on hypothesis testing.
### The Scope of my Data
At first, I was looking to aggregate ALL match data, plot possessions by teams, and comparing them. I realized that was ridicilously long, so I tried narrowing it down to just seasons in the La Liga. That was still way out of my scope, so I decided to reduce that to just the last season. With 34 games in a season, that was still overwhelming for me to work with. With the help of Land, I decided to lower my scope to the biggest win of that season. I was considering looking over the biggest win in every season, but with the time we have, I decided to focus first on analyzing this match. If time permitted, I would have analyzed a few more matches using what I had done for the Barcelona vs Huesca match. 
### My Journey
As we go through this, you will see how big my scope was at first. Lets follow along what I had ended up doing with the data!
#### Imported Essential Libraries
These libraries were used to manipulate the data and create visually-appealing soccer visuals using Seaborn.
```python
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
```
#### Created Dictionary with keys as Match IDs and values holding matches dataframes from all available La Liga matches, as the files were only labeled by Match IDs, then I merged all the matches.
```python
laliga_dict = {}
for filename in os.listdir('../data/matches/11'):
    laliga_dict[filename] = pd.json_normalize(json.load(open('../data/matches/11' + '/' + filename)),sep="_")
    laliga_merged_matches = pd.concat(laliga_dict.values(),ignore_index = True)
```
#### Created dataframe consisting of only La Liga matches in the last season and a list of match ids to be used to select the 'events' JSON files I wanted.
```python
laliga_last_season = laliga_merged_matches.query('season_season_id == [4]')
laliga_last_season.reset_index()
laliga_matchids = list(laliga_last_season['match_id'])
for idx,i in enumerate(laliga_matchids):
    laliga_matchids[idx] = str(i)
```
#### Created functions to be used to create a dictionary containing matchids as keys and event data for that match as values. 
```python
def match_to_pandas_events(match):
    with open(f'../data/events/{match}') as data_file:    
        data = json.load(data_file)
    return pd.json_normalize(data, sep = "_")
    
def match_to_pandas_lineups(match):
    with open(f'../data/lineups/{match}') as data_file:    
        data = json.load(data_file)
    return pd.json_normalize(data, sep = "_")
    
laliga_lastseason_events = {}
for filename in os.listdir('../data/events'):
        if filename[:-5] not in laliga_matchids:
            continue
        laliga_lastseason_events[int(filename[:-5])] = match_to_pandas_events(filename)

laliga_last_season.set_index('match_id', inplace=True)
laliga_last_season['events'] = laliga_last_season.index.map(laliga_lastseason_events)
```
#### Created function to create dictionary with tuple of home and away team names as keys and tuple of respective location data throughout that match.
```python
def auto_matchlist_locations(match_ids): 
    d = {}
    for i in match_ids:
        home = laliga_last_season['home_team_home_team_name'].loc[int(i)]
        away = laliga_last_season['away_team_away_team_name'].loc[int(i)]
        home_loc = laliga_last_season['events'][int(i)].loc[(laliga_last_season['events'][int(i)]['possession_team_name'] == home),['location']].dropna(subset=['location'])['location']
        away_loc = laliga_last_season['events'][int(i)].loc[(laliga_last_season['events'][int(i)]['possession_team_name'] == away),['location']].dropna(subset=['location'])['location']
        d[(home,away)] = (home_loc,away_loc)
    return d
event_locos_lastseason = auto_matchlist_locations(laliga_matchids
```
### Created function called soc_plot_auto_bymatch that contained another function that was found [here](https://towardsdatascience.com/advanced-sports-visualization-with-pandas-matplotlib-and-seaborn-9c16df80a81b) called drawpitch(). Purpose was to automate soccer visualizations. 
```python
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

def soc_plot_auto_bymatch(d,home,away):
    fig, axs = plt.subplots(1,2,sharex=True,sharey=True)
    fig.set_size_inches(14, 5)
    draw_pitch(axs[0]) #overlay our different objects on the first pitch
    axs[0].set_ylim(0, 80)
    axs[0].set_xlim(0, 120)
    axs[0].get_xaxis().set_visible(False)
    axs[0].get_yaxis().set_visible(False)
    axs[0].set_title(home)
    draw_pitch(axs[1]) #overlay our different objects on the second pitch
    axs[1].set_ylim(0, 80)
    axs[1].set_xlim(0, 120)
    axs[1].get_xaxis().set_visible(False)
    axs[1].get_yaxis().set_visible(False)
    axs[1].set_title(away)
    x_coord1 = [i[0] for i in d[(home,away)][0]]
    y_coord1 = [i[1] for i in d[(home,away)][0]]
    x_coord2 = [i[0] for i in d[(home,away)][1]]
    y_coord2 = [i[1] for i in d[(home,away)][1]]
    sns.kdeplot(x_coord2, y_coord2, shade = "True", color = "orange", n_levels = 30, ax=axs[1])
    sns.kdeplot(x_coord1, y_coord1, shade = "True", color = "green", n_levels = 30, ax=axs[0]);
```
#### Using soc_plot_auto_bymatch(), I plotted the Barcelona v Huesca match.
```python
soc_plot_auto_bymatch(event_locos_lastseason,'Barcelona','Huesca')
```
![soccer plot of barca v huesca](/src/images/barcelona_v_huesa_2018_2019.png)

#### Calculated Avergage Distance from Goals using Euclidean Distance.
```python
#use numpy method for euclidean disctance, then loop on it through every (x,y) point for the specific map, accumulate, and divide by len() of the iteration
#### COORDINATES FOR GOAL ARE: (120,40)
goal_loc = np.array([120,40])
#barca vs huesca... this is the BIGGEST HOME WIN of the season
#barca loop
barca_accum = []
for i in event_locos_lastseason[('Barcelona','Huesca')][0]:
    barca_accum.append(np.linalg.norm(goal_loc - np.array(i)))
barca_goaldists = np.array(barca_accum)
#huesca loop
huesca_accum = []
for i in event_locos_lastseason[('Barcelona','Huesca')][1]:
    huesca_accum.append(np.linalg.norm(goal_loc - np.array(i)))
huesca_goaldists = np.array(huesca_accum)
```
#### Plotted these distances on one-dimensional scatterplot to get an idea of what the data distribution looks like.
```python
def one_dim_scatterplot(data, ax, jitter=0.2, **options):
    ## why jitter? especially for bootstraping later
    if jitter:
        jitter = np.random.uniform(-jitter, jitter, size=data.shape)
    else:
        jitter = np.repeat(0.0, len(data))
    ax.scatter(data, jitter, **options)
    ax.yaxis.set_ticklabels([])
    ax.set_ylim([-0.24, 0.24])
    ax.tick_params(axis='both', which='major', labelsize=15)
    
fig, ax = plt.subplots(1, figsize=(12, 1))
one_dim_scatterplot(barca_goaldists, ax, s=15)

fig, ax = plt.subplots(1, figsize=(12, 1))
one_dim_scatterplot(huesca_goaldists, ax, s=15)
```
![barca goal dist](/src/images/barca_goaldist_distribution.png)
![huesca goal dist](/src/images/huesca_goaldist_distribution.png)


#### Ran a bootstrap to sample the distributions and plotted them. Found that they were not centered around 0, so I wanted to further test this.
```python
def bootstrap_samples(data,samples):
    lst = []
    for i in range(samples):
        bootstrap = np.random.choice(data, size=len(data), replace=True)
        lst.append(np.mean(bootstrap))
    return np.array(lst)
fig, ax = plt.subplots(1, figsize=(10, 4))
ax.hist(mean_diff, bins=50, density=True, color="black", alpha=0.5);
```
![bootstrapping](/src/images/bootstrap_histogram.png)
#### Ran a t-test and got a T-Test Statistic of -8.042328507143266 and a p-value of 1.1777818632104454e-15
```python
stats.ttest_ind(barca_goaldists,huesca_goaldists)
```
