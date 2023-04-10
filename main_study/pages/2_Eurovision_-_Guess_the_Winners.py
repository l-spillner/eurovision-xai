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
from collections import Counter

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

############################################################ Public variables

# paths
project_path = os.path.dirname(__file__) or '.'
data_path = os.path.join(project_path, "data.csv")

############################################################ Public functions




############################################################ MAIN ############################################################

st.markdown("### Winner or Loser?")

st.markdown('''Here you can see 10 randomly chosen Eurovision candidate songs. Your task is to choose for each song whether it will be a winner (first place) or a loser (last place).
Below, you can see for each song which country the singer is from, read the lyrics, and listen to a 20 second preview of the song itself. All of the songs are in the native language of their country. As the songs are chosen randomly, there are not necessarily five winners and five losers. Hint: Scroll down in the lyrics to read the rest!

As a thank you for participating in our study, you get a betting budget of 5€. You will wager 50ct on each choice - in the end, you will get the money only for those songs that you predicted correctly. If you get all songs correct, you can get 5€.

You now have X minutes to pick your winning songs:


---''')

############################################################ load data

df = st.session_state.data

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

st.sidebar.write("Your choices so far:")
#st.sidebar.write(Counter(user_predictions.values()))
counts = Counter(user_predictions.values())
st.sidebar.write("Winners:", counts["WINNER"])
st.sidebar.write("Losers:", counts["LOSER"])
if not (counts["WINNER"] + counts["LOSER"] == 10):
	st.sidebar.write('You need to make a choice for all 10 songs.')
else:
	st.sidebar.write(f'You have picked {counts["WINNER"]} winners and {counts["LOSER"]} losers!   \n Are you happy with your selection?   \n If yes, click "Continue".')

	st.session_state.user_predictions = user_predictions

	next_page = st.sidebar.button("Continue")
	if next_page:
	    switch_page("AI_Review")



