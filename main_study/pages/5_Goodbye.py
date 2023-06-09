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

# optional celebratory balloons
balloons = True

st.set_page_config(layout="centered")
c_green = "#AD9"
c_red = "#FA9"

# hides page nav in sidebar
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

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

############################################################ Public variables

############################################################ Public functions




############################################################ MAIN ############################################################

try:
	data_path = os.path.join(st.session_state.project_path, "data.csv")
	leader_path = os.path.join(st.session_state.project_path, "leaderboards.txt")
	sample_df = st.session_state.final_data
	st.session_state.reroute_error = True
except:
    switch_page("Home")

if balloons and not "saved_line" in st.session_state:
	st.balloons()

st.markdown("Thank you for participating in our study!")

############################################################ Leaderboards

leaderboards = []
with open(leader_path) as file:
	leaderboards = file.readlines()
	leaderboards = [l.split() for l in leaderboards if not l.strip() == ""]

#st.write(leaderboards)

leaderboards = [[item[0], int(item[1])] for item in leaderboards]
leaderboards = sorted(leaderboards, key = lambda x: x[1], reverse = True)

# calculate final user accuracy
user_accuracy = len(list(sample_df[sample_df["true_label"] == sample_df["final_user_prediction"]].index))
#st.write(user_accuracy)

#user_accuracy = 1

st.write(f"Congratulations: Your prediction was correct for {user_accuracy} songs 🥳   \n   These are the best scores so far:")

#st.write(f"there are {len(leaderboards)} places taken")

your_place = 1
while your_place <= len(leaderboards) and leaderboards[your_place-1][1] > user_accuracy:
	#st.write(your_place)
	#st.write(f"person at index {your_place-1} is better than you")
	your_place += 1
	#st.write("thus your place is now", your_place)

#st.write(your_place)
#st.write(len(leaderboards))

# generate output with first three and one each before and after user place
if not "output" in st.session_state:
	output = []
	ellipsis = False
	for i, item in enumerate(leaderboards):
		if i < your_place-2 and i < 3:
			output.append({"Place":str(i+1), "Name":item[0], "Score":str(item[1])})
		if not ellipsis and i < your_place-2 and i >= 3:
			output.append({"Place":"...", "Name":"...", "Score":"..."})
			ellipsis = True
		if i == your_place-2:
			output.append({"Place":str(i+1), "Name":item[0], "Score":str(item[1])})
		if i == your_place-1:
			output.append({"Place":str(i+1), "Name":"YOU", "Score":str(user_accuracy)})
			output.append({"Place":str(i+2), "Name":item[0], "Score":str(item[1])})
		if i == your_place:
			output.append({"Place":"...", "Name":"...", "Score":"..."})
	if your_place == len(leaderboards)+1:
		output.append({"Place":str(i+2), "Name":"YOU", "Score":str(user_accuracy)})
	st.session_state.output = output
else:
	output = st.session_state.output
	if "name" in st.session_state:
		for i, line in enumerate(output):
			print("line")
			if line["Name"] == "YOU":
				print("replace")
				output[i]["Name"] = st.session_state.name

		
df_lb = pd.DataFrame(output)
df_lb = df_lb.style.apply(lambda x: ['background: lightgreen' 
                                  if (x["Name"] == 'YOU')
                                  else '' for i in x], axis=1)
st.table(df_lb)

st.write("Do you want to enter you results on our leaderboards? Future participants will be able to see your score and the name you chose. If yes, enter a nickname here and click Submit:")
name = st.text_input("Your nickname:", max_chars = 5)
submit_name = st.button("Submit")

if not "saved_line" in st.session_state:
	with open(leader_path, "r") as file:
		lines = [l for l in file.readlines() if not l.strip() == ""]
	#st.write(lines)
	#st.write(len(lines))
	st.session_state.saved_line = len(lines)
	lines.append("\nANON" + " " + str(user_accuracy))
	with open(leader_path, "w") as file:
		file.writelines(lines)

	#st.write(st.session_state.saved_line)

if submit_name:
	if not name.isalnum():
		st.error("Sorry, your name can only contain letters and numbers.")
	else:
		st.success("Success! Your Score has been saved under your name: " + name)
		with open(leader_path) as file:
			lines = [l for l in file.readlines() if not l.strip() == ""]
		#st.write(lines)
		lines[st.session_state.saved_line] = name + " " + str(user_accuracy) + "\n"
		print("Troubleshooting lines:")
		for l in lines:
			print(l.replace("\n", "|****|"))
		#st.write(lines)
		with open(leader_path, "w") as file:
			file.writelines(lines)
		st.session_state.name = name

#st.write(leaderboards)

############################################################ Share

st.write("---")

st.write("If you had fun and/or want to support our research, please consider sharing our study with people you know. You can copy the text below:")

st.code("Here's a link to a research study on working with Artificial Intelligence \nto judge the quality of Eurovision Song Contest participants:\n\n    abba-cadabra.uni-bremen.de", language = "excelFormula")

