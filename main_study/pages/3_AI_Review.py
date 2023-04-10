############################################################ SETUP ############################################################

############################################################ Imports

import os
import sys
import io
import streamlit as st
import streamlit.components.v1 as components
from annotated_text import annotated_text

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

switch_label = {"WINNER":"LOSER", "LOSER":"WINNER"}

############################################################ Public functions




############################################################ MAIN ############################################################

st.markdown("### [BETA] Review your choices with ABBA-cadabra!")

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

df["true_label"] = ["WINNER" if not l else "LOSER" for l in df["is_last"]]
df["user_prediction"] = pd.Series(user_predictions)

############################################################ generate AI predictions

sample_df = df.loc[songs]

# count how often user is right
user_accuracy = list(sample_df[sample_df["true_label"] == sample_df["user_prediction"]].index)

# if user is right less than half the time, put AI to 50% and decide randomly
if len(user_accuracy) < 5:
	ai_correct = random.sample(songs, 5)
	ai_prediction = {s:(df.loc[s, "true_label"] if s in ai_correct else switch_label[df.loc[s, "true_label"]]) for s in songs}

# otherwise, put ai to 50% and make sure that there are some instances where the user was right in which the ai should be wrong
else:
	# how many of the songs that the user predicted correctly should the AI predict incorrectly? lets say half?
	ai_num_misinform = int(len(user_accuracy)/2)
	# out of the ones where the user was right, pick this many
	ai_misinform = random.sample(list(sample_df[sample_df["true_label"] == sample_df["user_prediction"]].index), ai_num_misinform)
	# out of the ones where the user was wrong, pick some more for the ai to be wrong so that it's five in total
	if ai_num_misinform < 5:
		ai_other_wrong = random.sample(list(sample_df[sample_df["true_label"] != sample_df["user_prediction"]].index), 5-ai_num_misinform)
		ai_wrong = ai_misinform + ai_other_wrong
	else:
		ai_wrong = ai_misinform

	ai_prediction = {s:(df.loc[s, "true_label"] if not s in ai_wrong else switch_label[df.loc[s, "true_label"]]) for s in songs}

sample_df["ai_prediction"] = pd.Series(ai_prediction)
#st.write(user_accuracy)
#st.write(ai_prediction)
#st.write(sample_df)

############################################################ display songs 

final_user_predictions = {}

for s in songs:

	col1, col2, col3 = st.columns([2, 5, 3])

	song = df.loc[s]
	#lyrics = song["lyrics"].replace("\n", "   \n") 
	lyrics = song["lyrics"].replace("\\n", "<br>") 
	spotifyLink = song["spotify_url"]

	with col1:

		st.write("Your first prediction was:")
		if user_predictions[s] == "WINNER":
			annotated_text((user_predictions[s], "", "#8FD07D"))
		else:
			annotated_text((user_predictions[s], "", "#FBAB9D"))

		choice = st.radio("Winner or loser?", ["", "WINNER", "LOSER"], key = str(s), index = 1 if user_predictions[s] == "WINNER" else 2)

		final_user_predictions[s] = choice

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

		# if choice == "LOSER":
		# 	st.error(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
		# 	#components.html("""<div style="overflow-y: scroll; height:400px;">{lyrics}</div>""")
		# 	#with st.expander(lyrics.split("\n")[0] + "[...]"):
		# 		#st.error(f'{lyrics}')
		# 	components.html(
		# 		f"""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
		# 		<div class="overflow-auto p-3 mb-3 mb-md-0 me-md-3 bg-dark text-white" style="max-height: 150px;">{lyrics}</div>""")
		# elif choice == "WINNER":
		# 	st.success(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
		# 	#with st.expander(lyrics.split("\n")[0] + "[...]"):
		# 	#	st.success(f'{lyrics}')
		# 	components.html(
		# 		f"""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
		# 		<div class="overflow-auto p-3 mb-3 mb-md-0 me-md-3 bg-dark text-white" style="max-height: 150px;">{lyrics}</div>""")

		#elif choice == "LOSER":
		#	st.error(f'**{song["song"]}**   \n by *{song["performer"]}* from {song["to_country"]}')
		#	with st.expander(lyrics.split("\n")[0] + "[...]"):
		#		st.error(f'{lyrics}')

	with col3:

		components.html(
			f"""
			<iframe style="border-radius:12px" src="{spotifyLink}" width="250" height="250" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>""", height = 260
			)

	ai_choice = ai_prediction[s]
	ai_explanation = df.loc[s, "explanation_correct"] if isinstance(df.loc[s, "explanation_correct"], str) else df.loc[s, "explanation_incorrect"]

	if ai_choice == "WINNER":
		annotated_text("AI prediction: ", (ai_choice, "", "#8FD07D"))
	else:
		annotated_text("AI prediction: ", (ai_choice, "", "#FBAB9D"))

	#st.markdown(f'AI prediction: {ai_choice}')
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



