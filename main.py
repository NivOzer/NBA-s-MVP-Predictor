import requests
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import os
import time
import numpy as np
import openpyxl
from tabulate import tabulate


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


#Takes the full points of a player in a team
r2 = requests.get("https://www.basketball-reference.com/leagues/NBA_2022_totals.html")
soup2 = BeautifulSoup(r2.content,'html.parser')
tempTag = soup2.findAll("td", {"data-stat": "pts"})
k =0
for i in tempTag:
    allpoints[k] = (i.text.strip())
    k = k+1
#takes the plusminus of a player in a team
r3 = requests.get("https://www.basketball-reference.com/leagues/NBA_2022_advanced.html")
soup3 = BeautifulSoup(r3.content,'html.parser')
tempTag = soup3.findAll("td", {"data-stat": "bpm"})
k = 0
for i in tempTag:
    plusminus[k] = (i.text.strip())
    k = k+1

teamVictoriesDict = {
    "ATL": 0,
    "BOS": 0,
    "BRK": 0,
    "CHO": 0,
    "CHI": 0,
    "CLE": 0,
    "DAL": 0,
    "DEN": 0,
    "DET": 0,
    "GSW": 0,
    "HOU": 0,
    "IND": 0,
    "LAC": 0,
    "LAL": 0,
    "MEM": 0,
    "MIA": 0,
    "MIL": 0,
    "MIN": 0,
    "NOP": 0,
    "NYK": 0,
    "OKC": 0,
    "ORL": 0,
    "PHI": 0,
    "PHO": 0,
    "POR": 0,
    "SAC": 0,
    "SAS": 0,
    "TOR": 0,
    "UTA": 0,
    "WAS": 0
}

def get_team_abbreviation(team_name):
    team_abbreviations = {
        "Atlanta Hawks": "ATL",
        "Boston Celtics": "BOS",
        "Brooklyn Nets": "BRK",
        "Charlotte Hornets": "CHO",
        "Chicago Bulls": "CHI",
        "Cleveland Cavaliers": "CLE",
        "Dallas Mavericks": "DAL",
        "Denver Nuggets": "DEN",
        "Detroit Pistons": "DET",
        "Golden State Warriors": "GSW",
        "Houston Rockets": "HOU",
        "Indiana Pacers": "IND",
        "Los Angeles Clippers": "LAC",
        "Los Angeles Lakers": "LAL",
        "Memphis Grizzlies": "MEM",
        "Miami Heat": "MIA",
        "Milwaukee Bucks": "MIL",
        "Minnesota Timberwolves": "MIN",
        "New Orleans Pelicans": "NOP",
        "New York Knicks": "NYK",
        "Oklahoma City Thunder": "OKC",
        "Orlando Magic": "ORL",
        "Philadelphia 76ers": "PHI",
        "Phoenix Suns": "PHO",
        "Portland Trail Blazers": "POR",
        "Sacramento Kings": "SAC",
        "San Antonio Spurs": "SAS",
        "Toronto Raptors": "TOR",
        "Utah Jazz": "UTA",
        "Washington Wizards": "WAS"
    }
    return team_abbreviations.get(team_name, "None")

def updateTeamVictoriesDict():
    r4 = requests.get("https://www.basketball-reference.com/leagues/NBA_2023.html")
    soup4 = BeautifulSoup(r4.content, 'html.parser')
    team_stats = soup4.findAll("tr", {"class": "full_table"})
    for t in team_stats:
        name = (t.find("th",{"data-stat":'team_name'})).find('a').text
        win = (t.find("td",{"data-stat":'wins'})).text
        # print(get_team_abbreviation(name))
        # print(win)
        teamVictoriesDict[get_team_abbreviation(name)] = win

updateTeamVictoriesDict()

def updateDfWinByTeam():
    df.loc[df['Team'].isin(teamVictoriesDict.keys()), 'Victories in Season'] = df['Team'].map(teamVictoriesDict)

df = pd.DataFrame({'Player': playername,
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

updateDfWinByTeam()
print(tabulate(df, headers='keys'))
print("Version 4")