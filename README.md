# Soccer Field Heatmap Analysis of Possesion during Biggest win of La Liga Season 2018-19 (Barcelona v Huesca)
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
#### Getting my Data Ready
This was the hardest part for me, as I spent most of my time working with the data.
1. Imported Essential Libraries, like Matplotlib, Pandas, Numpy, and Seaborn. These libraries were used to manipulate the data and create visually-appealing soccer visuals.

2. Biggest issue was the EDA, as the data provided from StatsBomb was very broken up. It was separated into 3 folders, with match folder containing all the available matches by league_i (found in a seperate single JSON file called 'Competitions'. The other 2 folders, 'events' and 'lineups' were the biggest obstacles because the files were labeled with their Match IDs (found in the Matches JSONs) but the Match ID was not used in the 'events' JSON files.

3. With the help of Jerome, I was able to get a working function to import these files, as they needed to be normalized with pd.json_normalize, which normalizes the semi-structured JSON data into a flat table. And with the help of Jamie, I was able to get to tweak this function to loop through all the JSONs in a specified folder. Using this, i created Dictionary with keys as Match IDs and values holding matches dataframes from all available La Liga matches, as the files were only labeled by Match IDs, then I merged all the matches.

4. I tried this for all the 'events', but this was a ridiculously huge dataset, so I decided to narrow it to just all season for La Liga. Still too big, so I decided to just focus on a single game, and then if time permitted, I would compare them to other matches. I just wanted to get at least SOME data ready.

3. Created dataframe consisting of only La Liga matches in the last season and a list of match ids to be used to select the 'events' JSON files I wanted.

4. Created functions to be used to create a dictionary containing matchids as keys and event data for that match as values. 

5. Created function to create dictionary with tuple of home and away team names as keys and tuple of respective location data throughout that match. This made it a lot easier to find the matches I needed, instead of having to find the match_id for that specific match. 

#### Creating Visuals with Prepared Data
6. Created function called soc_plot_auto_bymatch that contained another function that was found [here](https://towardsdatascience.com/advanced-sports-visualization-with-pandas-matplotlib-and-seaborn-9c16df80a81b) called drawpitch(). Purpose was to automate soccer visualizations. 

7. Using soc_plot_auto_bymatch(), I plotted the Barcelona v Huesca match. Looking at the distribution of the possessions, Barcelona clearly dominated in the attacking possesions. You can see that a lot of Huesca's possessions lied within the mid-field, probably because they were trying to hold them back as much as they can. It seems like that possessions near goal are more important than possessions elsewhere, in terms of making goals. This might be obvious, but I wanted to test the statistical significance of this. So I decided to look into the Average Distance from Goals, thanks to some guidance from Land. 
```python
soc_plot_auto_bymatch(event_locos_lastseason,'Barcelona','Huesca')
```
![soccer plot of barca v huesca](/src/images/barcelona_v_huesa_2018_2019.png)

#### Hypothesis Testing
8. Calculated Average Distance from Goals using Euclidean Distance.
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

9. Plotted these distances on one-dimensional scatterplot, with jitter, to get an idea of what the data distribution looks like. As you can see, a lot of the data points for Barca lied closer to the goal, while Huesca was further. You also see a significantly greater amount of points for Barca because of the dominance in possession that they had in that game. I wanted to further test this, so I decided to bootstrap the mean differences and plot the results on a Histogram.
![barca goal dist](/src/images/barca_goaldist_distribution.png)
![huesca goal dist](/src/images/huesca_goaldist_distribution.png)

10.  Ran a bootstrap to sample the mean differences of the distributions and plotted them. They appear to be centered around -7, which is good news because if it was centered around 0, then there really isn't that much of a Average Mean Difference amongst the teams. I wanted to further confirm the hypothesis that more dominant possessions closer to the goal correlates with a win. I'd like to emphasize that this is soley a correlation, and not a matter of causation.
![bootstrapping](/src/images/bootstrap_histogram.png)

11. To further confirm, I ran a t-test and got a T-Test Statistic of -8.042328507143266 and a p-value of 1.1777818632104454e-15. The reason I chose a t-test is because I wanted to see if the mean differences were statistically significant, and the extremely low p-value supports that. This makes sense, as you can imagine being closer to the goal means more shot opportunity, which can potentially lead to game-winning goals. 
```python
stats.ttest_ind(barca_goaldists,huesca_goaldists)
```
## Further Studies / Considerations
While the possibilities are endless with this dataset, I wanted to maybe look into a match during that season that was more contested, a better match. Huesca was having a really bad season, so it's no surprise they were dominated 8-2. It was also Barcelona's home field, so they had an additional advantage asides from having a stacked lineup. A match of maybe Atletico Madrid vs Valencia might have been nice to analyze similarily and compare to the Barca v Huesca match. In addition, I wanted to look further into how possession changed throughout the game, especially as goals were made. I had a great experience and learned a lot from this capstone. I hope to maybe even expand upon this on my own time, as the resulting visualizations were very satisfying once I was able to get them to work. 

## EXTRA
I had some time to come up with graphs of Sevilla and Barcelona, as well as ran some statistics:
![barcasevilla](/src/images/barca_sevilla.png)
![barcasevilla](/src/images/sevilla_goaldist_distribution_vs_barca.png)
![barcasevilla](/src/images/barca_goaldist_distribution_vs_sevilla.png)
![barcasevilla](/src/images/bootstrap_histogram_sev_bar.png)

Here is the T-Test Statistic: -3.887497981178525
Here is the P-Value: 0.0001031535872268295
