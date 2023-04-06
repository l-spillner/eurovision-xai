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


############################################################ Public variables

st.set_page_config(layout="centered")

# paths
project_path = os.path.dirname(__file__) or '.'
data_path = os.path.join(project_path, "data.csv")

############################################################ Public functions




############################################################ MAIN ############################################################

st.markdown("### Winner or Loser?")

st.markdown('''Here you can see 10 randomly chosen Eurovision candidate songs. 5 of these songs are winners, 5 of them are losers (meaning that they take the last place among all contestants of that year).
Your task is to chose the 5 songs that you think will be winners. If you chose correctly, you can win real prize money!

As a thank you for participating in our study, you get a betting budget of 5€. You will wager 1€ on each winner that you chose. If you are correct, you get 2€ back - if you are wrong, that money is lost. 
Therefore, if you are wrong in all five cases, you will lose your 5€. If you are right in all five cases, you get 10€ back.

You now have X minutes to pick your winning songs:


---''')

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
	#lyrics = song["lyrics"].replace("\n", "   \n") 
	lyrics = song["lyrics"].replace("\n", "<br>") 

	with col1:

		choice = st.radio("Winner or loser?", ["WINNER", "LOSER"], key = str(s), index = 1)

		user_predictions[s] = choice

		#if choice == "WINNER":
		#	st.success("You predict: Winner!")
		#elif choice == "LOSER":
		#	st.error("You predict: Loser")

	with col2:

		if choice == "LOSER":
			st.markdown(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
			components.html(
				f"""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
				<div class="overflow-auto p-3 mb-3 mb-md-0 me-md-3 bg-dark text-white" style="max-height: 150px;">{lyrics}</div>""")
			#with st.expander(lyrics.split("\n")[0] + "[...]"):
			#	st.markdown(f'{lyrics}')
		elif choice == "WINNER":
			st.success(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
			components.html(
				f"""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
				<div class="overflow-auto p-3 mb-3 mb-md-0 me-md-3 bg-dark text-white" style="max-height: 150px;">{lyrics}</div>""")
			#with st.expander(lyrics.split("\n")[0] + "[...]"):
			#	st.success(f'{lyrics}')
		#elif choice == "LOSER":
		#	st.error(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
		#	with st.expander(lyrics.split("\n")[0] + "[...]"):
		#		st.error(f'{lyrics}')

	st.markdown("---")

st.sidebar.write("Your choices so far:")
#st.sidebar.write(Counter(user_predictions.values()))
st.sidebar.write("Winners:", Counter(user_predictions.values())["WINNER"])
st.sidebar.write("Losers:", Counter(user_predictions.values())["LOSER"])
if not (Counter(user_predictions.values())["WINNER"] == 5 and Counter(user_predictions.values())["LOSER"] == 5):
	st.sidebar.write('You need to pick 5 winners and 5 losers.')
else:
	st.sidebar.write('You have picked 5 winner and 5 losers!   \n Are you happy with your selection?   \n If yes, click "Continue".')

	st.session_state.user_predictions = user_predictions

	next_page = st.sidebar.button("Continue")
	if next_page:
	    switch_page("AI_Review")



