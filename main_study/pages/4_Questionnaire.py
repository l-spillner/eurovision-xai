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

############################################################ Public variables

# paths
project_path = os.path.dirname(__file__) or '.'
data_path = os.path.join(project_path, "data.csv")

switch_label = {"WINNER":"LOSER", "LOSER":"WINNER"}

############################################################ Public functions




############################################################ MAIN ############################################################

filename = st.session_state.filename

st.markdown("Please help us evaluate the performance of the ABBA-cadabra AI by answering the following questions.")
q1 = st.radio("Do you think our AI will successfully predict the winner of the Eurovision Song Contest 2023?", ["", "VERY LIKELY", "LIKELY", "NEUTRAL", "UNLIKELY", "VERY UNLIKELY"])
q3 = st.radio("Do you watch/follow the Eurovision Song Contest?", ["", "EVERY YEAR", "MOST YEARS", "SOMETIMES", "RARELY", "NEVER"])
q3 = st.radio("Were you familiar with any of the songs in the study?", ["", "YES", "NO"])
if q3 == "YES":
    q3b = title = st.text_input('Which songs?')
st.write("Please rate the following statements:")
rel_1 = st.radio("The system always provides the advice I require to make my decision", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
rel_2 = st.radio("The system performs reliably", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
rel_3 = st.radio("The system responds the same way under the same conditions at different times", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
rel_4 = st.radio("I can rely on the system to function properly", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
rel_5 = st.radio("The system analyzes problems consistently", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
com_1 = st.radio("The system uses appropriate methods to reach decisions", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
com_2 = st.radio("The system has sound knowledge about this kind of problem built into it", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
com_3 = st.radio("The advice the system produces is as good as that which a highly competent person could produce", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
com_4 = st.radio("The system correctly uses the information I enter", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
com_5 = st.radio("The system makes use of all the knowledge and information available to it to produce its solution to the problem", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
und_1 = st.radio("I understand what will happen the next time I use the system because I understand how it behaves", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
und_2 = st.radio("I understand how the system will assist me with decisions I have to make", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
und_3 = st.radio("Although I may not know exactly how the system works, I know how to use it to make decisions about the problem", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
und_4 = st.radio("It is easy to follow what the system does", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
und_5 = st.radio("I recognize what I should do to get the advice I need from the system the next time I use it", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
fai_1 = st.radio("I believe advice from the system even though I don't know for certain that it is correct", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
fai_2 = st.radio("When I am uncertain I believe the system rather than myself", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
fai_3 = st.radio("If I am not sure about a decision, I have faith that the system will provide the best solution", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
fai_4 = st.radio("When the system gives unusual advice I am confident that the advice is correct", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
fai_5 = st.radio("Even if I have no reason to expect the system will be able to solve a difficult problem, I still feel certain that it will", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
per_1 = st.radio("I would feel a sense of loss if the system was unavailable and I could no longer use it", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
per_2 = st.radio("I feel a sense of attachment to using the system", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
per_3 = st.radio("I find the system suitable to my style of decision making", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
per_4 = st.radio("I like using the system for decision making", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
per_5 = st.radio("I have a personal preference for making decisions with the system", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"])
next_page = st.button("Send results")
if next_page:
		#write results to file
	switch_page("Goodbye")