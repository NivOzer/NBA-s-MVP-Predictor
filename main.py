import requests
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import os
import time
import numpy as np
import openpyxl
from tabulate import tabulate

# df = pd.read_excel("C:\\Users\\nivoz\\Desktop\\pyprojects\\NivAndGuy\\2021-2022playerstats.xlsx")
# agedf = df.loc[:,['NAME','AGE']]

r = requests.get("https://www.basketball-reference.com/leagues/NBA_2022_per_game.html")
soup = BeautifulSoup(r.content,'html.parser')

playername = []
position = []
age = []
team = []
salary = []
won_conference = []
victories_in_season = []
allpoints = []
ppg = []
team_conference_rank = []
is_allstar = []
plusminus = []
orpg = []
drpg = []
apg = []
games_played = []
minutes_per_game = []
blocks = []
steals = []

categories = [playername,position,age,team,salary,won_conference,victories_in_season,allpoints,ppg,team_conference_rank,is_allstar,plusminus,orpg,drpg,apg,games_played,minutes_per_game,blocks,steals]


# Maybe consider adding cluch for more data
maxDataSetSize = 812
def getDataStat(tag,category,arr):
    tempTag = soup.findAll(tag,{"data-stat":category})
    if not tempTag:
        for i in range(maxDataSetSize):
            arr.append(None)
    else:
        for i in tempTag:
            arr.append(i.text.strip())

for cat in categories:
    if categories.index(cat) == 0:
        data_stat_tag = 'player'
    elif categories.index(cat) == 1:
        data_stat_tag = 'pos'
    elif categories.index(cat) == 2:
        data_stat_tag = 'age'
    elif categories.index(cat) == 3:
        data_stat_tag = 'team_id'
    elif categories.index(cat) == 4:
        data_stat_tag = 'team'
    elif categories.index(cat) == 8:
        data_stat_tag = 'pts_per_g'
    elif categories.index(cat) == 12:
        data_stat_tag = 'orb_per_g'
    elif categories.index(cat) == 13:
        data_stat_tag = 'drb_per_g'
    elif categories.index(cat) == 14:
        data_stat_tag = 'ast_per_g'
    elif categories.index(cat) == 15:
        data_stat_tag = 'g'
    elif categories.index(cat) == 16:
        data_stat_tag = 'mp_per_g'
    elif categories.index(cat) == 17:
        data_stat_tag = 'blk_per_g'
    elif categories.index(cat) == 18:
        data_stat_tag = 'stl_per_g'
    else:
        data_stat_tag = None
    getDataStat("td", data_stat_tag, cat)

# getDataStat("td","player",playername)
# getDataStat("td","pos",position)
r2 = requests.get("https://www.basketball-reference.com/leagues/NBA_2022_totals.html")
soup2 = BeautifulSoup(r2.content,'html.parser')
tempTag = soup2.findAll("td", {"data-stat": "pts"})
k =0
for i in tempTag:
    allpoints[k] = (i.text.strip())
    k = k+1


test = pd.DataFrame({'Player': playername,
                     'Position': position,
                     'Age': age,
                     'Salary': salary,
                     'Team': team,
                     'Won Conference': won_conference,
                     'Victories in Season': victories_in_season,
                     'All Points': allpoints,
                     'Points Per Game (PPG)': ppg,
                     'Team Conference Rank': team_conference_rank,
                     'Is All-Star': is_allstar,
                     'Plus/Minus': plusminus,
                     'Offensive Rebounds Per Game (ORPG)': orpg,
                     'Defensive Rebounds Per Game (DRPG)': drpg,
                     'Assists Per Game (APG)': apg,
                     'Games Played': games_played,
                     'Minutes Per Game': minutes_per_game,
                     'Blocks': blocks,
                     'Steals': steals
                    })

# print(test)

# print(f"playername: {len(playername)}")
# print(f"position: {len(position)}")
# print(f"age: {len(age)}")
# print(f"team: {len(team)}")
# print(f"salary: {len(salary)}")
# print(f"won_conference: {len(won_conference)}")
# print(f"victories_in_season: {len(victories_in_season)}")
# print(f"allpoints: {len(allpoints)}")
# print(f"ppg: {len(ppg)}")
# print(f"team_conference_rank: {len(team_conference_rank)}")
# print(f"is_allstar: {len(is_allstar)}")
# print(f"plusminus: {len(plusminus)}")
# print(f"orpg: {len(orpg)}")
# print(f"drpg: {len(drpg)}")
# print(f"apg: {len(apg)}")
# print(f"games_played: {len(games_played)}")
# print(f"minutes_per_game: {len(minutes_per_game)}")
# print(f"blocks: {len(blocks)}")
# print(f"steals: {len(steals)}")

print(tabulate(test, headers='keys'))