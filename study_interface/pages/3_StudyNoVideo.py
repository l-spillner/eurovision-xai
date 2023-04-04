############################################################ SETUP ############################################################

############################################################ Imports

import os
import sys
import io
import streamlit as st
import streamlit.components.v1 as components

import requests

import math
import pandas as pd
import numpy as np
import json
import random
import re
from collections import Counter


############################################################ Public variables

st.set_page_config(layout="centered")

# paths
project_path = os.path.dirname(__file__) or '.'
data_path = os.path.join(project_path, "data.csv")

############################################################ Public functions




############################################################ MAIN ############################################################

############################################################ load data

df = st.session_state.data

############################################################ pick ten songs randomly and mix them up; if not already done

# the way I set up the data is somewhat stupid, because I made an "is_last" column (this was necessary because some years had several losers),
# so now the winners are False and the losers are True which is a bit counterintuitive. Maybe change this later.

if not "songs" in st.session_state:

	winners = random.sample(list(df[df["is_last"] == False].index), 5)
	losers = random.sample(list(df[df["is_last"] == True].index), 5)

	songs = winners + losers
	random.shuffle(songs)

	st.session_state.songs = songs

else:
	songs = st.session_state.songs

############################################################ display songs 

user_predictions = {}

for s in songs:

	col1, col2 = st.columns([1, 3])

	song = df.loc[s]
	lyrics = song["lyrics"].replace("\n", "   \n") 

	with col1:

		choice = st.selectbox("Winner or loser?", ["", "WINNER", "LOSER"], key = str(s))

		user_predictions[s] = choice

		#if choice == "WINNER":
		#	st.success("You predict: Winner!")
		#elif choice == "LOSER":
		#	st.error("You predict: Loser")

	with col2:

		if choice == "":
			st.markdown(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
			with st.expander(lyrics.split("\n")[0] + "[...]"):
				st.markdown(f'{lyrics}')
		elif choice == "WINNER":
			st.success(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
			with st.expander(lyrics.split("\n")[0] + "[...]"):
				st.success(f'{lyrics}')
		elif choice == "LOSER":
			st.error(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
			with st.expander(lyrics.split("\n")[0] + "[...]"):
				st.error(f'{lyrics}')

	st.markdown("---")

st.sidebar.write("Your choices so far:")
#st.sidebar.write(Counter(user_predictions.values()))
st.sidebar.write("Winners:", Counter(user_predictions.values())["WINNER"])
st.sidebar.write("Losers:", Counter(user_predictions.values())["LOSER"])
if not (Counter(user_predictions.values())["WINNER"] == 5 and Counter(user_predictions.values())["LOSER"] == 5):
	st.sidebar.write('You need to pick 5 winners and 5 losers.')
else:
	st.sidebar.write('You have picked 5 winner and 5 losers!   \n Are you happy with your selection?   \n If yes, click "Continue".')
	if st.sidebar.button('Continue'):
		successcounter = 0
		for k in user_predictions.keys():
			with open('resultsNoVideo.csv', 'a+') as f:
				isLast = df.loc[k]["is_last"]
				f.write(f"{k},{isLast},{user_predictions[k]}\n")
			if not df.loc[k]["is_last"] and user_predictions[k] == "WINNER":
				successcounter = successcounter+1
			elif df.loc[k]["is_last"] and user_predictions[k] == "LOSER":
				successcounter = successcounter+1
			else:
				st.sidebar.write('You were wrong about ' + df.loc[k]["song"] + ', it was actually a winner') if user_predictions[k] == "LOSER" else st.sidebar.write('You were wrong about ' + df.loc[k]["song"] + ', it was actually a loser')
				
		st.sidebar.write('You were right about ' +  str(successcounter) + ' songs!')
			
		




