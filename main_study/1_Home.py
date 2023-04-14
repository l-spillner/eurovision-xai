############################################################ SETUP ############################################################

############################################################ Imports

import os
import sys
import io
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page

import requests

import math
import pandas as pd
import numpy as np
import json
import random
import re

############################################################ Settings

st.set_page_config(layout="centered")

# hides the first option in a radio group
# note: this applies to ALL radio groups across the app; it cannot be done for an individual button!
st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """,
    unsafe_allow_html=True
)

no_sidebar_style = """
	<style>
        div[data-testid="stSidebarNav"] {pointer-events: none; cursor: default;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# hides button to close sidebar, open settings
no_button_style = """
    <style>
        button[kind="header"] {display:none;}
    </style>
"""
st.markdown(no_button_style, unsafe_allow_html=True)

############################################################ Public variables

# paths
project_path = os.path.dirname(__file__) or '.'
data_path = os.path.join(project_path, "data.csv")
leader_path = os.path.join(project_path, "leaderboards.txt")

st.session_state.project_path = project_path

############################################################ Public functions




############################################################ MAIN ############################################################

if "reroute_error" in st.session_state and st.session_state.reroute_error:
	st.warning("Sorry! The page was reloaded in your browser, which started a new session. As this site does not save any cookies, it's not possible to remember data between sessions. Please start again.")

############################################################ load data

leaderboards = []
with open(leader_path) as file:
	leaderboards = file.readlines()
	leaderboards = [l.split() for l in leaderboards if not l.strip() == ""]

#st.write(leaderboards)

# get number of participants from number of files
n_participants = len(leaderboards)
n_perfect = len([item for item in leaderboards if int(item[1]) == 10])
st.session_state.n_perfect = n_perfect
st.session_state.n_participants = n_participants

# get average performance, round down
# should we lie and max out both at 0.9?
mean_accuracy = min(round(np.mean([int(item[1]) for item in leaderboards]), 1), 9)
ai_accuracy = min(mean_accuracy + 1, 9)

df = pd.read_csv(data_path, sep = "\t", index_col = 0)
st.session_state.data = df

# show of hide data for debug
if False:

	st.write("This is the data:")
	st.write(df)

	st.write("But participants won't actually see this; it's just for us to check. Instead, they only see the lower part:")
	st.write("---")

############################################################ text

st.write("# ABBA-cadabra!")

st.markdown(
f"""
This is a research study on how Artificial Intelligence (AI) performs in a domain where human judgement is often very subjective: *music* 🎵

The **Eurovision Song Contest** will take place between May 9th and May 13th 2023. In preparation, we have trained an AI model to predict whether or not a song will perform well at the contest. 
Your first task will be to have a look at ten randomly selected songs, and decide for each song: is it more likely to win the contest, or be placed last?
Afterwards, you can review your selection with our AI tool, before submitting your final choices. Finally, we will ask you to answer a few questions about how useful the AI tool was in making your decisions.""")

st.write("Can you beat the high score? You will see how well you performed after completing the questionnaire 😉")

st.code("Number of participants so far: " + str(n_participants) + "\nAverage score: " + str(int(mean_accuracy)) + "/10")


st.markdown(
f"""
---
##### About this study:

The entire study should take up to 15-20 minutes. All your answers will be collected anonymously. We do not collect personal information, like your name or IP address. If you want, you can add your score to the leaderboards on the last page, which will not be used in our research. You are free to quit the study at any time.

The data that we collect is stored on a server of the University of Bremen, in Germany. After the study finishes, the data from all participants will be analysed together and the results might be published in future research papers. We will not publish the answers or performance of any individual participant. Please note that since your data is not linked to any personal identifying information, we will not be able to delete your data later. 

If you have any questions about this study, please contact:

Laura Spillner (laura.spillner@uni-bremen.de) or Rachel Ringe (rringe@uni-bremen.de)

If you want to proceed with the study, please click "Start"!

"""
)

next_page = st.button("Start", key = 1)
if next_page:
	   switch_page("Eurovision_-_Guess_the_Winners")




