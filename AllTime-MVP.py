import requests
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import os
import time
import numpy as np
import openpyxl
from tabulate import tabulate

dframes = []
year = 2022
mvp_domain = "https://www.basketball-reference.com/awards/mvp.html"
def create_dataframe(domain):
    #Categories_mvp
    playername = []
    age =[]
    team = []
    min_played_per_game = []
    ppg = []
    num_games = []
    total_rebounds_per_game= []
    apg = []
    blocks = []
    steals = []
    point3_perc = []
    field_goal_perc = [] #11
    year_won = []
    maxDataSetSize = 77
    categories = [playername, age, team, min_played_per_game, ppg, num_games,total_rebounds_per_game, apg, blocks, steals, point3_perc , field_goal_perc,year_won]
    mvp_stats_request = requests.get(mvp_domain)
    mvp_stats_soup = BeautifulSoup(mvp_stats_request.content, 'html.parser')
    def getDataStat(tag, category, arr):
        tempTag = mvp_stats_soup.findAll(tag, {"data-stat": category})
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
            data_stat_tag = 'age'
        elif categories.index(cat) == 2 :
            data_stat_tag = 'team_id'
        elif categories.index(cat) == 4:
            data_stat_tag = 'pts_per_g'
        elif categories.index(cat) ==6 :
            data_stat_tag = 'trb_per_g'
        elif categories.index(cat) ==7 :
            data_stat_tag = 'ast_per_g'
        elif categories.index(cat) ==5 :
            data_stat_tag = 'g'
        elif categories.index(cat) ==3 :
            data_stat_tag = 'mp_per_g'
        elif categories.index(cat) == 8:
            data_stat_tag = 'blk_per_g'
        elif categories.index(cat) == 9:
            data_stat_tag = 'stl_per_g'
        elif categories.index(cat) == 10:
            data_stat_tag = 'fg3_pct'
        elif categories.index(cat) ==11 :
            data_stat_tag = 'fg_pct'
        else:
            data_stat_tag = None
        getDataStat("td", data_stat_tag, cat)

    year = mvp_stats_soup.findAll("th", {"data-stat": "season","class":"left"})
    for y in range(len(year)):
        yeartext = year[y].find('a').text
        year_won[y] = yeartext

    #pads with NaNs to make sure that all arrays (that makes the dataframes) are thew same length
    for cat in categories:
        if len(cat)<=maxDataSetSize:
            for i in range(maxDataSetSize-len(cat)):
                cat.append(None)



    df = pd.DataFrame({'Player': playername,
                       'Age': age,
                       'Year Won': year_won,
                       'Team': team,
                       'Minutes Per Game': min_played_per_game,
                       'Points Per Game (PPG)': ppg,
                       'Games Played': num_games,
                       'Total Rebounds Per Game (DRPG)': total_rebounds_per_game,
                       'Assists Per Game (APG)': apg,
                       'Blocks': blocks,
                       'Steals': steals,
                       '%3': point3_perc,
                       'Field Goals Perc%': field_goal_perc
                       })
    i=0
    filename = ("DataFrame"+str(i))
    i=i+1
    df.to_csv(filename)
    print(tabulate(df, headers='keys'))

create_dataframe(mvp_domain)