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
from selenium.webdriver.support.ui import Select

year =2022
amount_of_data_frames = 1
dframes =[]
driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")

#DOMAIN'S
main_players_stat_domain = "https://www.basketball-reference.com/leagues/NBA_2022_per_game.html"        #0
totalpoints_player_domain = "https://www.basketball-reference.com/leagues/NBA_2022_totals.html"         #1
player_plusminus_domain = "https://www.basketball-reference.com/leagues/NBA_2022_advanced.html"         #2
team_victories_domain = "https://www.basketball-reference.com/leagues/NBA_2022.html"                    #3
full_player_points_domain = "https://www.espn.com/nba/standings/_/season/2022/group/league"             #4 *** Different Button Class - might consider selenium ***
check_if_player_is_allstar_domain = "https://www.basketball-reference.com/allstar/NBA_2022.html"        #5 *** Different Button Class ***
won_conference_team_domain = "https://blog.ticketcity.com/nba/nba-finals-champions/"                    #6
domains = [main_players_stat_domain,totalpoints_player_domain,player_plusminus_domain,team_victories_domain,full_player_points_domain,check_if_player_is_allstar_domain,won_conference_team_domain]
def create_dataframe(main_players_stat_domain,totalpoints_player_domain,player_plusminus_domain,team_victories_domain,full_player_points_domain,check_if_player_is_allstar_domain,won_conference_team_domain):
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
    maxDataSetSize = 812
    categories = [playername,position,age,team,salary,won_conference,victories_in_season,allpoints,ppg,team_conference_rank,is_allstar,plusminus,orpg,drpg,apg,games_played,minutes_per_game,blocks,steals, point3_perc, point2_perc,east_rank, west_rank, total_mvp, year]
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
    currentYear = int(selectedYear[:4])+1
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


    #pads with NaNs to make sure that all arrays (that makes the dataframes) are thew same length
    for cat in categories:
        if len(cat)<=maxDataSetSize:
            for i in range (maxDataSetSize-len(cat)):
                cat.append(None)


    #Creates the DataFrame

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

    won_conference_team_request = requests.get("https://www.landofbasketball.com/championships/year_by_year.htm")
    won_conference_team_soup = BeautifulSoup(won_conference_team_request.content, "html.parser")
    wonConference = won_conference_team_soup.findAll("div", {"class": "rd-100 a-center a-right-sm margen-r5 wpx-170"})
    lostConference = won_conference_team_soup.findAll("div", {"class": "rd-100 a-center a-left-sm wpx-170"})
    w = []
    l = []
    for i in wonConference:
        winningTeam = i.find('a').text
        w.append(winningTeam)
    for i in lostConference:
        losingTeam = i.find('a').text
        l.append(losingTeam)

    df.loc[df['Team'] == get_team_abbreviation(w[2022-currentYear]), 'Won Conference'] = 1
    df.loc[df['Team'] == get_team_abbreviation(l[2022-currentYear]), 'Won Conference'] = 1
    #df.loc[df['Player'] != name, 'Won Conference'] = 0


    return df

#Accessing the previous years pages


dframes.append(create_dataframe(domains[0],domains[1],domains[2],domains[3],domains[4],domains[5],domains[6]))
# #Selenium
for dfs in range(amount_of_data_frames):
    i=0
    for i in range(4):
        driver.get(domains[i])
        link = driver.find_element_by_css_selector('a.button2.prev').get_attribute('href')
        domains[i] = link
    i=i+1
    #fourth site
    year = year -(dfs+1)
    link = "https://www.espn.com/nba/standings/_/season/"+str(year)+"/group/league"
    domains[i] = link
    i=i+1
    #fifth site
    driver.get(domains[i])
    link = driver.find_element_by_css_selector('a.button2').get_attribute('href')
    domains[i] = link
    dframes.append(create_dataframe(domains[0],domains[1],domains[2],domains[3],domains[4],domains[5],domains[6]))
    driver.quit()
    #sixth site - Not needed - its a list for all years back conference winners and losers

domains[0] = "https://www.basketball-reference.com/leagues/NBA_2020_per_game.html"
domains[1] = "https://www.basketball-reference.com/leagues/NBA_2020_totals.html"
domains[2] = "https://www.basketball-reference.com/leagues/NBA_2020_advanced.html"
domains[3] = "https://www.basketball-reference.com/leagues/NBA_2020.html"
domains[4] = "https://www.espn.com/nba/standings/_/season/2020/group/league"
domains[5] = "https://www.basketball-reference.com/allstar/NBA_2020.html"
dframes.append(create_dataframe(domains[0],domains[1],domains[2],domains[3],domains[4],domains[5],domains[6]))
i=0
for df in dframes:
    filename = ("DataFrame"+str(i))
    i=i+1
    df.to_csv(filename)
    print(tabulate(df, headers='keys'))
    print("****************************************************************************************************************************************************************************************************************")

# i=0
# for i in range(4):
#     driver.get(domains[i])
#     link = driver.find_element_by_css_selector('a.button2.prev').get_attribute('href')
#     domains[i] = link
# i=i+1
# #fourth site
# year = year -2
# link = "https://www.espn.com/nba/standings/_/season/"+str(year)+"/group/league"
# domains[i] = link
# i=i+1
# #fifth site
# driver.get(domains[i])
# link = driver.find_element_by_css_selector('a.button2').get_attribute('href')
# domains[i] = link
# driver.quit()
