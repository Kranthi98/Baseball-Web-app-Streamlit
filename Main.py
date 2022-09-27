# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 10:24:26 2022

@author: SHIVA
"""

import streamlit as st
import pybaseball as pb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from bokeh.plotting import figure
import altair as alt
import datetime
import os
import warnings
warnings.filterwarnings('ignore')




st.set_page_config(
    page_title = "Baseball Stats",
    page_icon = "⚾",
    layout = "wide")

c1, c2 = st.columns((8,2))
with c1:
    st.title("Baseball Sabermetrics")
with c2:
    fg = st.selectbox(label = "select stat type",
    options = ["FanGraph","Pitch_Splits"], index = 0 )


exec(open('Stats_functions.py').read())



teams = pb.teams().query("yearID == 2021")["name"].unique()
HmTm = st.sidebar.selectbox(label = "Select the Home Team", options = teams)
AwTm = st.sidebar.selectbox(label = "Select the Away team", options = teams)


start_date = str(st.sidebar.date_input(label = "Enter the start date", value = datetime.date(2008, 7, 6)))
end_date = str(st.sidebar.date_input(label = "Enter the end date"))


name_split = lambda x : x.rsplit(".",1) if "." in x else x.split(" ")


pitchers = list(pd.read_csv("Pitchers_2008-present.csv").Pitchers)
pitcher1 = st.sidebar.selectbox(label = "Select the pitcher1",options = pitchers)
pitcher2 = st.sidebar.selectbox(label = "Select the pitcher2",options = pitchers)


batters = list(pd.read_csv("Batters_2008-present.csv").Batters)
HmTm_lineup = st.sidebar.multiselect(label = "select the "+HmTm +" lineup", options = batters, key = "HmTM")
AwTm_lineup = st.sidebar.multiselect(label = "select the "+AwTm +" lineup", options = batters, key = "AwTm")
pt_dict = pd.read_csv("Pitch_types.csv").set_index("Abb").to_dict()["Full"]


col1, col2 = st.columns((1,1))

with col1:
    st.subheader(f"Pitching stats for {pitcher1}")

    #if fg == "Pitch_Splits":
    pitcher1_df = (pb.statcast_pitcher(player_id = pb.playerid_lookup(name_split(pitcher1)[1].strip(),name_split(pitcher1)[0].replace(".",". ").rstrip())["key_mlbam"].values[0],
                start_dt = start_date, end_dt = end_date)
                .assign(pitch_type = lambda x : x.pitch_type.replace(pt_dict),
                events = lambda x : x.events.fillna("None")))
    st.table(stats_by_pitchtypes(pitcher1_df))
    # elif fg == "FanGraph":
    #     st.write(pb.pitching_stats(start_season = int(start_date[0:4]), end_season = int(end_date[0:4])).query(f"Name == '{pitcher1}'")[[
    #         "Season","Name","Team","Age","WAR","ERA","FIP","xFIP","K/9","HR/9","AVG","WHIP","BABIP","GB/FB",]])
     
 


with col2 : 
    st.subheader(f"Pitching stats for {pitcher2}")
    #if fg == "Pitch_Splits":
    pitcher2_df = (pb.statcast_pitcher(player_id = pb.playerid_lookup(name_split(pitcher2)[1].strip(),name_split(pitcher2)[0].replace(".",". ").rstrip())["key_mlbam"].values[0],
                start_dt = start_date, end_dt = end_date)
                .assign(pitch_type = lambda x : x.pitch_type.replace(pt_dict),
                events = lambda x : x.events.fillna("None")))
    st.table(stats_by_pitchtypes(pitcher2_df))
    # elif fg == "FanGraph":
    #     st.write(pb.pitching_stats(start_season = int(start_date[0:4]), end_season = int(end_date[0:4])).query(f"Name == '{pitcher2}'")[[
    #         "Season","Name","Team","Age","WAR","ERA","FIP","xFIP","K/9","HR/9","AVG","WHIP","BABIP","GB/FB",]])
     




tab1,tab2 = st.tabs(["Home : "+HmTm, "Away : "+AwTm])








