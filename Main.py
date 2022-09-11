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

st.set_page_config(
    page_title = "Baseball Stats",
    page_icon = "⚾",
    layout = "wide")

st.title("Baseball Sabermetrics")
st.sidebar.success("Filters")
HmTm = st.sidebar.selectbox(label = "Select the Home Team", options = pb.teams().query("yearID == 2021")["name"].unique())
AwTm = st.sidebar.selectbox(label = "Select the Away team", options = pb.teams().query("yearID == 2021")["name"].unique())

start_date = str(st.sidebar.date_input(label = "Enter the start date"))
end_date = str(st.sidebar.date_input(label = "Enter the end date"))
pitcher1 = st.sidebar.selectbox(label = "Select the pitcher1",
                       options = pb.fg_pitching_data(start_season = 2020, end_season = 2022)["Name"].unique())

pitcher2 = st.sidebar.selectbox(label = "Select the pitcher2",
                       options = pb.fg_pitching_data(start_season = 2020, end_season = 2022)["Name"].unique())

pt_dict = pd.read_csv("Pitch_types.csv").set_index("Abb").to_dict()["Full"]

col1, col2 = st.columns((1,1))

with col1:
    st.subheader(f"Pitching stats for {pitcher1}")                  
    st.write(pb.pitching_stats(start_season = int(start_date[0:4]), end_season = int(end_date[0:4])).query(f"Name == '{pitcher1}'")[[
        "Season","Name","Team","Age","WAR","ERA","FIP","xFIP","K/9","HR/9","AVG","WHIP","BABIP",
        "GB/FB",]])
    pitcher1_df = pb.statcast_pitcher(player_id = pb.playerid_lookup(pitcher1.split(" ")[1],pitcher1.split(" ")[0])["key_mlbam"].values[0],
                    start_dt = start_date, end_dt = end_date)
    pitcher1_df.replace(pt_dict, inplace = True)
    



with col2 : 
    st.subheader(f"Pitching stats for {pitcher2}")
    st.write(pb.pitching_stats(start_season = int(start_date[0:4]), end_season = int(end_date[0:4])).query(f"Name == '{pitcher2}'")[[
        "Season","Name","Team","Age","WAR","ERA","FIP","xFIP","K/9","HR/9","AVG","WHIP","BABIP",
        "GB/FB",]])
    pitcher2_df = pb.statcast_pitcher(player_id = pb.playerid_lookup(pitcher2.split(" ")[1],pitcher2.split(" ")[0])["key_mlbam"].values[0],
                    start_dt = start_date, end_dt = end_date)
    pitcher2_df.replace(pt_dict, inplace = True)




tab1,tab2 = st.tabs(["T1 : X1", "T2 : X2"])


with tab1:


    st.write(pitcher2_df.head(3))
    fig1 = alt.Chart(pitcher2_df).mark_bar().encode(x = "pitch_type",y = 'count(*):Q')
    st.altair_chart(fig1)
    
with tab2:

    fig2 = alt.Chart(pitcher1_df).mark_bar().encode(x = "pitch_type",y = 'count(*):Q')
    st.altair_chart(fig2)



