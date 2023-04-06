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

st.set_page_config(layout="wide")

# paths
project_path = os.path.dirname(__file__) or '.'
data_path = os.path.join(project_path, "data.csv")

############################################################ Public functions




############################################################ MAIN ############################################################

st.markdown("### [BETA] Review your choices with AI4Eurovision!")

st.markdown('''Before submitting your selection, you can review your choices with our AI-based winner prediction tool.
Our AI predicts whether a song will be a winner or a loser at Eurovision based on the arist and their country of origin, as well as the lyrics of the song.
It takes into account over 50 years of Eurovision history! 
	
The AI model utilizes Machine Learning and so-called Large Language Models (in this case, GPT4 by OpenAI) to analyse the songtext and decide whether or not it is likely to speak to typical Eurovision audiences based on voting patterns in the past.
An explanation of the AI decision is provided, so that you can see what its prediction is based on.

Please go through your selection again, and look at the AI predictions. Your prize will depend on the final selection you make here. You are free to change - or not change - as many of your choices as you like.



---''')

############################################################ load data

df = st.session_state.data
songs = st.session_state.songs
user_predictions = st.session_state.user_predictions

df["user_prediction"] = pd.Series(user_predictions)

############################################################ generate AI predictions

# for now, I only have one explanation for each, so I just base the prediction on which one I have an explanation for
# because of this, the ai doesn't always predict five winners and five losers
# later we should change this accordingly 

ai_prediction = df.loc[songs]
ai_incorrect = {key:("WINNER" if value else "LOSER") for key, value in pd.Series.to_dict(ai_prediction[ai_prediction["explanation_correct"].isna()]["is_last"]).items()}
ai_correct = {key:("WINNER" if value else "LOSER") for key, value in pd.Series.to_dict(ai_prediction[ai_prediction["explanation_incorrect"].isna()]["is_last"] == False).items()}
ai_prediction = ai_correct
ai_prediction.update(ai_incorrect)
df["ai_prediction"] = pd.Series(ai_prediction)
#st.write(ai_prediction)
#st.write(df)

############################################################ display songs 

final_user_predictions = {}

for s in songs:

	col1, col2, col3 = st.columns([2, 5, 3])

	song = df.loc[s]
	lyrics = song["lyrics"].replace("\n", "   \n") 

	with col1:

		st.write("Your first prediction was:", user_predictions[s])

		choice = st.radio("Winner or loser?", ["WINNER", "LOSER"], key = str(s), index = 0 if user_predictions[s] == "WINNER" else 1)

		final_user_predictions[s] = choice

		#if choice == "WINNER":
		#	st.success("You predict: Winner!")
		#elif choice == "LOSER":
		#	st.error("You predict: Loser")

	with col2:

		if choice == "LOSER":
			st.error(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
			#with st.expander(lyrics.split("\n")[0] + "[...]"):
				#st.error(f'{lyrics}')
			components.html(
				#f"""
				#<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
				#<div class="overflow-auto">{lyrics}</div>	
				#<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
				#<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
				#<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>				
				#"""
	f"""
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <div class="overflow-auto">{lyrics}</div>
    """
				)
		elif choice == "WINNER":
			st.success(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
			with st.expander(lyrics.split("\n")[0] + "[...]"):
				st.success(f'{lyrics}')

		#elif choice == "LOSER":
		#	st.error(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
		#	with st.expander(lyrics.split("\n")[0] + "[...]"):
		#		st.error(f'{lyrics}')

	with col3:

		st.write("This is where the audio goes.")
		components.html(
			"""
			<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/6bk11TH82XrT5QUC1gDw9A?utm_source=generator" width="250" height="150" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
			)

	ai_choice = ai_prediction[s]
	ai_explanation = df.loc[s, "explanation_correct"] if isinstance(df.loc[s, "explanation_correct"], str) else df.loc[s, "explanation_incorrect"]
	st.markdown(f'AI prediction: {ai_choice}')
	st.markdown(f'*Explanation*:   \n {ai_explanation}')

	st.markdown("---")

st.sidebar.write("Your choices so far:")
#st.sidebar.write(Counter(user_predictions.values()))
st.sidebar.write("Winners:", Counter(user_predictions.values())["WINNER"])
st.sidebar.write("Losers:", Counter(user_predictions.values())["LOSER"])
if not (Counter(user_predictions.values())["WINNER"] == 5 and Counter(user_predictions.values())["LOSER"] == 5):
	st.sidebar.write('You need to pick 5 winners and 5 losers.')
else:
	st.sidebar.write('You have picked 5 winner and 5 losers!   \n Are you happy with your selection?   \n If yes, click "Continue".')



