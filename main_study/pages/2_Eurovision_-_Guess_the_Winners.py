############################################################ SETUP ############################################################

############################################################ Imports

import os
import sys
import io
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page

import os

import requests

import math
import pandas as pd
import numpy as np
import json
import random
import re
from collections import Counter

import time

## TimeStamp

st.session_state.time2 = str(time.time())

############################################################ Settings

st.set_page_config(layout="wide")

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
        div[data-testid="stSidebarNav"] {display: none;}
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

############################################################ Public functions

    


    


############################################################ MAIN ############################################################

############################################################ load data

try:
	df = st.session_state.data
	data_path = os.path.join(st.session_state.project_path, "data.csv")
	n_perfect = st.session_state.n_perfect
	n_participants = st.session_state.n_participants
except:
	st.session_state.reroute_error = True
	switch_page("Home")

############################################################ text

st.markdown("### Winner or Loser?")

st.markdown(f'''Here you can see 10 randomly chosen Eurovision candidate songs. Your task is to choose for each song whether it will be a *winner* (first place) or a *loser* (last place).
Below, you can see for each song which country the singer is from, read the lyrics, and listen to a 20 second preview of the song itself. All of the songs are in the native language of their country. As the songs are chosen randomly, there are not necessarily five winners and five losers.

After you have completed the questionnaire, you will be able to see how many songs you predicted correctly. So far, **{st.session_state.n_perfect} out of {st.session_state.n_participants}** participants managed to get all 10 songs correct!

🔊 Remember to turn on the sound on your device so you can hear the songs. 🔊

---''')

############################################################ sort user into group

# group 0 is without explanations, 1 is with explanations

if not "group" in st.session_state:

	zeroCounter = 0
	while os.path.exists('0_' + str(zeroCounter)+'.csv'):
		zeroCounter = zeroCounter + 1
	oneCounter = 0
	while os.path.exists('1_' + str(oneCounter)+'.csv'):
		oneCounter = oneCounter + 1
	if oneCounter > zeroCounter:
		st.session_state.group = 0	
	else:
		st.session_state.group = 1
############################################################ pick ten songs randomly and mix them up; if not already done

# the way I set up the data is somewhat stupid, because I made an "is_last" column (this was necessary because some years had several losers),
# so now the winners are False and the losers are True which is a bit counterintuitive. Maybe change this later.

if not "songs" in st.session_state:

	#winners = random.sample(list(df[df["is_last"] == False & df["spotify_url"].str.contains('open.spotify.com')].index), 5)
	#losers = random.sample(list(df[df["is_last"] == True & df["spotify_url"].str.contains('open.spotify.com')].index), 5)
	#songs = winners + losers


	songs = random.sample(list(df[df["spotify_url"].str.contains('open.spotify.com')].index), 10)
	random.shuffle(songs)

	st.session_state.songs = songs

else:
	songs = st.session_state.songs

############################################################ display songs 

user_predictions = {}

for s in songs:

	#col1, col2 = st.columns([1, 3])
	col1, col2, col3 = st.columns([2, 5, 4])

	song = df.loc[s]
	#lyrics = song["lyrics"].replace("\n", "   \n") 
	lyrics = song["lyrics"].replace("\\n", "<br>") 
	spotifyLink = song["spotify_url"]

	with col1:

		choice = st.radio("Winner or loser?", ["", "WINNER", "LOSER"], key = str(s), index = 0)
		
		st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style>""", unsafe_allow_html=True)

		user_predictions[s] = choice

		#if choice == "WINNER":
		#	st.success("You predict: Winner!")
		#elif choice == "LOSER":
		#	st.error("You predict: Loser")

	with col2:

		if choice == "LOSER":
			st.error(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
			components.html(
				f"""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
				<div class="overflow-auto p-3 mb-3 mb-md-0 me-md-3 bg-light" style="max-height: 250px;">{lyrics}</div>""", height = 250) #bg-dark text-white
			#with st.expander(lyrics.split("\n")[0] + "[...]"):
			#	st.markdown(f'{lyrics}')
		elif choice == "WINNER":
			st.success(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
			components.html(
				f"""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
				<div class="overflow-auto p-3 mb-3 mb-md-0 me-md-3 bg-light" style="max-height: 250px;">{lyrics}</div>""", height = 250)
			#with st.expander(lyrics.split("\n")[0] + "[...]"):
			#	st.success(f'{lyrics}')
		else:
			st.markdown(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
			components.html(
				f"""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
				<div class="overflow-auto p-3 mb-3 mb-md-0 me-md-3 bg-light" style="max-height: 250px;">{lyrics}</div>""", height = 250)


	with col3:

		components.html(
			f"""<iframe style="border-radius:12px" src="{spotifyLink}" width="250" height="250" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>""",
			height=260) #, scrolling=True)

	st.markdown("---")

############################################################ sidebar & next page 

enable_next_page_button = False

st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")

st.sidebar.write("Your choices so far:")
#st.sidebar.write(Counter(user_predictions.values()))
counts = Counter(user_predictions.values())
st.sidebar.write("Winners:", counts["WINNER"])
st.sidebar.write("Losers:", counts["LOSER"])
if not (counts["WINNER"] + counts["LOSER"] == 10):
	st.sidebar.write('You need to make a choice for all 10 songs.')
else:
	st.sidebar.write(f'You have picked {counts["WINNER"]} winners and {counts["LOSER"]} losers!   \n Are you happy with your selection?   \n If yes, click "Continue" at the bottom of the page.')

	st.session_state.user_predictions = user_predictions
	enable_next_page_button = True
	# id = 0
	# while os.path.exists(str(id)+'.csv'):
	# 	id = id + 1 
	# filename = str(id) + '.csv'
	# st.session_state.filename = filename

next_page = st.button("Continue", disabled = not enable_next_page_button, key = 2)
if not enable_next_page_button:
	st.write("Please vote on all songs before continuing.")
if next_page:
	# 	for k in user_predictions.keys():
	# 		with open(filename, 'a+') as f:
	# 			isLast = df.loc[k]["is_last"]
	# 			f.write(f"{k},{isLast},{user_predictions[k]}\n")
	switch_page("AI_Review")



