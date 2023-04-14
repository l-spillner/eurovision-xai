############################################################ SETUP ############################################################

############################################################ Imports

import os
import sys
import io
import streamlit as st
import streamlit.components.v1 as components
from annotated_text import annotated_text
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
c_green = "#AD9"
c_red = "#FA9"

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

# paths
data_path = os.path.join(st.session_state.project_path, "data.csv")

switch_label = {"WINNER":"LOSER", "LOSER":"WINNER"}

############################################################ Public functions




############################################################ MAIN ############################################################

############################################################ load data

try:
	df = st.session_state.data
	songs = st.session_state.songs
	user_predictions = st.session_state.user_predictions
	group = st.session_state.group
	#filename = st.session_state.filename
except:
	switch_page("Home")

df["true_label"] = ["WINNER" if not l else "LOSER" for l in df["is_last"]]
df["user_prediction"] = pd.Series(user_predictions)

############################################################ Explain setup

xai = ""
if group == 1:
	xai = "An explanation of the AI decision is provided, so that you can see what its prediction is based on."

st.markdown("### Review your choices with ABBA-cadabra!")

st.markdown(f'''Before submitting your selection, you can review your choices with our AI-based winner prediction tool.
Our AI predicts whether a song will be a winner or a loser at Eurovision based on the arist and their country of origin, as well as the lyrics of the song.
It takes into account over 50 years of Eurovision history. 
	
The AI model utilizes Machine Learning and so-called Large Language Models (in this case, GPT4 by OpenAI) to analyse the songtext and decide whether or not it is likely to speak to typical Eurovision audiences based on voting patterns in the past.
{xai}

Please go through your selection again, and look at the AI predictions. Your place on the leaderboards will depend on the final selection you make here. You are free to change - or not change - as many of your choices as you like.



---''')

############################################################ generate AI predictions

sample_df = df.loc[songs]

# count how often user is right
user_accuracy = list(sample_df[sample_df["true_label"] == sample_df["user_prediction"]].index)

if not "ai_predictions" in st.session_state:

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

	st.session_state.ai_predictions = ai_prediction

else:
	ai_prediction = st.session_state.ai_predictions

sample_df["ai_prediction"] = pd.Series(ai_prediction)
#st.write("DEBUG:")
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

		st.write("Your first prediction was:", user_predictions[s])
		#if user_predictions[s] == "WINNER":
		#	annotated_text((user_predictions[s], "", c_green))
		#else:
		#	annotated_text((user_predictions[s], "", c_red))

		st.write("")
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

	colB1, colB2 = st.columns([2, 8])

	with colB2:

		ai_choice = ai_prediction[s]

		if (ai_choice == df.loc[s, "true_label"]):
			ai_explanation = df.loc[s, "explanation_correct"]
		else:
			ai_explanation = df.loc[s, "explanation_incorrect"]

		#ai_explanation = df.loc[s, "explanation_correct"] if isinstance(df.loc[s, "explanation_correct"], str) else df.loc[s, "explanation_incorrect"]

		if ai_choice == "WINNER":
			annotated_text("AI prediction: ", (ai_choice, "", c_green))
		else:
			annotated_text("AI prediction: ", (ai_choice, "", c_red))

		#st.markdown(f'AI prediction: {ai_choice}')
		st.write("")
		#if ai_choice == final_user_predictions[s]:
		#	with st.expander("Explanation"):
		#		st.markdown(f'{ai_explanation}')
		#else:
		if st.session_state.group == 1:
			st.markdown(f'*Explanation*:   \n {ai_explanation}')

	st.markdown("---")

sample_df["final_user_prediction"] = pd.Series(final_user_predictions)
st.session_state.final_data = sample_df
agrees = list(sample_df[sample_df["ai_prediction"] == sample_df["final_user_prediction"]].index)
agree_counter = len(agrees)

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
counts = Counter(final_user_predictions.values())
st.sidebar.write("Winners:", counts["WINNER"])
st.sidebar.write("Losers:", counts["LOSER"])
if not (counts["WINNER"] + counts["LOSER"] == 10):
	st.sidebar.write('You need to make a choice for all 10 songs.')
else:
	st.sidebar.write(f'You have picked {counts["WINNER"]} winners and {counts["LOSER"]} losers!   \n ABBA-cadabra agrees with {agree_counter} of your choices.   \n    \n Are you happy with your selection?   \n If yes, click "Continue" at the bottom of the page.')
	st.session_state.final_user_predictions = final_user_predictions
	enable_next_page_button = True


next_page = st.button("Continue", disabled = not enable_next_page_button, key = 3)
if next_page:
	id = 0
	while os.path.exists(str(st.session_state.group) + '_' + str(id)+'.csv'):
		id = id + 1
	filename = str(st.session_state.group) + '_' + str(id) + '.csv'
	st.session_state.filename = filename
	for k in user_predictions.keys():
		with open(filename, 'a+') as f:
			isLast = df.loc[k]["is_last"]
			f.write(f"{k},{isLast},{user_predictions[k]},{final_user_predictions[k]}\n")
	switch_page("Questionnaire")

	# next_page = st.sidebar.button("Continue", key = 3)
	# if next_page:
	# 	for k in user_predictions.keys():
	# 		with open(filename, 'a+') as f:
	# 			isLast = df.loc[k]["is_last"]
	# 			f.write(f"{k},{isLast},{user_predictions[k]}\n")
	

# debug info in sidebar:

#st.sidebar.write("DEBUG - REMOVE FOR FINAL VERSION:r")
#st.sidebar.write("User accuracy:", len(user_accuracy))
#st.sidebar.write("Ai will try to misinform for:", len(ai_misinform))
#st.sidebar.write("In total, AI will be wrong for:", len(ai_wrong))


