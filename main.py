import requests
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import os
import time
import numpy as np
import openpyxl
from tabulate import tabulate
import selenium
from selenium import webdriver


#Selenium
# driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
# driver.get('https://www.basketball-reference.com/leagues/NBA_2022_per_game.html')
# anchor = driver.find_element_by_css_selector('a.button2.prev')
# # Retrieve the link
# link = anchor.get_attribute('href')
# driver.close()
# print(link)


##DOMAIN LIST
main_players_stat_domain = "https://www.basketball-reference.com/leagues/NBA_2022_per_game.html"        #1
totalpoints_player_domain = "https://www.basketball-reference.com/leagues/NBA_2022_totals.html"         #2
player_plusminus_domain = "https://www.basketball-reference.com/leagues/NBA_2022_advanced.html"         #3
team_victories_domain = "https://www.basketball-reference.com/leagues/NBA_2022.html"                    #4
full_player_points_domain = "https://www.espn.com/nba/standings/_/season/2022/group/league"             #5
check_if_player_is_allstar_domain = "https://www.basketball-reference.com/allstar/NBA_2022.html"        #6


#Main Player-Statistics pull
main_players_stats_request = requests.get(main_players_stat_domain)
main_players_stats_soup = BeautifulSoup(main_players_stats_request.content,'html.parser')


#Categories
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
point3_perc = []
point2_perc = []
east_rank = []
west_rank = []
total_mvp = []
year = [] #24



categories = [playername,position,age,team,salary,won_conference,victories_in_season,allpoints,ppg,team_conference_rank,is_allstar,plusminus,orpg,drpg,apg,games_played,minutes_per_game,blocks,steals, point3_perc, point2_perc,east_rank, west_rank, total_mvp, year]


# Maybe consider adding cluch for more data
maxDataSetSize = 812
def getDataStat(tag,category,arr):
    tempTag = main_players_stats_soup.findAll(tag,{"data-stat":category})
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
    elif categories.index(cat) == 19:
        data_stat_tag = 'fg3_pct'
    elif categories.index(cat) == 20:
        data_stat_tag = 'fg2_pct'
    else:
        data_stat_tag = None
    getDataStat("td", data_stat_tag, cat)

# getDataStat("td","player",playername)
# getDataStat("td","pos",position)

#insert selected year to array
selectedYear = (main_players_stats_soup.find("div",{"id":"meta"})).find('span').text
for i in range(maxDataSetSize):
    year[i] = selectedYear






#Takes the full points of a player in a team
totalpoints_player_request = requests.get(totalpoints_player_domain)
totalpoints_player_soup = BeautifulSoup(totalpoints_player_request.content,'html.parser')
tempTag = totalpoints_player_soup.findAll("td", {"data-stat": "pts"})
k =0
for i in tempTag:
    allpoints[k] = (i.text.strip())
    k = k+1
#takes the plusminus of a player in a team
player_plusminus_request = requests.get(player_plusminus_domain)
player_plusminus_soup = BeautifulSoup(player_plusminus_request.content,'html.parser')
tempTag = player_plusminus_soup.findAll("td", {"data-stat": "bpm"})
k = 0
for i in tempTag:
    plusminus[k] = (i.text.strip())
    k = k+1

value_by_team_dict = {
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
        "Washington Wizards": "WAS",
        #extraordinary abbr
        "LA Clippers":  "LAC"

    }
    return team_abbreviations.get(team_name, "None")

def updateTeamVictoriesDict():
    team_victories_request = requests.get(team_victories_domain)
    team_victories_soup = BeautifulSoup(team_victories_request.content, 'html.parser')
    team_stats = team_victories_soup.findAll("tr", {"class": "full_table"})
    for t in team_stats:
        name = (t.find("th",{"data-stat":'team_name'})).find('a').text
        win = (t.find("td",{"data-stat":'wins'})).text
        # print(get_team_abbreviation(name))
        # print(win)
        value_by_team_dict[get_team_abbreviation(name)] = win

updateTeamVictoriesDict()

def updateDfWinByTeam():
    df.loc[df['Team'].isin(value_by_team_dict.keys()), 'Victories in Season'] = df['Team'].map(value_by_team_dict)














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
                     'Steals': steals,
                     '%3': point3_perc,
                     '%2': point2_perc,
                     'year': year
                    })

updateDfWinByTeam()

#Takes the full points of a player in a team
full_player_points_request = requests.get(full_player_points_domain)
full_player_points_soup = BeautifulSoup(full_player_points_request.content,'html.parser')
tempTag = full_player_points_soup.findAll("span", {"class": "dn show-mobile"})
rank = 1
for i in tempTag:
    t=i.find('abbr')
    name = (t['title'])
    value_by_team_dict[get_team_abbreviation(name)] = rank
    rank = rank +1

df.loc[df['Team'].isin(value_by_team_dict.keys()), 'Team Conference Rank'] = df['Team'].map(value_by_team_dict)



#getAllstar column
check_if_player_is_allstar_request = requests.get(check_if_player_is_allstar_domain)
check_if_player_is_allstar_soup = BeautifulSoup(check_if_player_is_allstar_request.content,'html.parser')
thTags = check_if_player_is_allstar_soup.findAll("th", {"data-stat": "player","csk":True})
for th in thTags:
    name = th.find('a').text
    df.loc[df['Player'] == name, 'Is All-Star'] = 1
    #df.loc[df['Player'] != name, 'Is All-Star'] = 0


#getWonConference column
df.loc[df['Team'] == "BOS", 'Won Conference'] = 1
df.loc[df['Team'] == "GSW", 'Won Conference'] = 1
#df.loc[df['Player'] != name, 'Won Conference'] = 0

print(tabulate(df, headers='keys'))