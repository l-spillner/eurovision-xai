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

# stuff that's put in a streamlit container gets a light grey background
st.markdown(
    """ <style>
            div[data-testid="stHorizontalBlock"]{
                background-color: #F0F2F6 !important;
                padding: 10px !important;
                border-radius: 5px !important;
            }
        </style>
        """,
    unsafe_allow_html=True
)

# hides page nav in sidebar
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {pointer-events: none; cursor: default;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# questionnaire - horizontal or vertical likert

likert_horizontal = True
if likert_horizontal:
    label_vis = "collapsed"
else:
    label_vis = "visible"

# randomize trust questions

likert_random_order = True

############################################################ Public variables

# paths
data_path = os.path.join(st.session_state.project_path, "data.csv")

switch_label = {"WINNER":"LOSER", "LOSER":"WINNER"}

############################################################ Public functions




############################################################ MAIN ############################################################

filename = st.session_state.filename

st.markdown("Please help us evaluate the performance of the ABBA-cadabra AI by answering the following questions.")

with st.form(key='my_form'):

    q1 = st.radio("Do you think our AI will successfully predict the winner of the Eurovision Song Contest 2023?", ["", "VERY LIKELY", "LIKELY", "NEUTRAL", "UNLIKELY", "VERY UNLIKELY"])
    q2 = st.radio("Do you watch/follow the Eurovision Song Contest?", ["", "EVERY YEAR", "MOST YEARS", "SOMETIMES", "RARELY", "NEVER"])
    q3 = st.radio("Were you familiar with any of the songs in the study?", ["", "YES", "NO"])
    #if q3 == "YES":
    q3b = st.text_input('If yes, which songs were you familiar with?')
    #else:
    #    q3b = None
    q4 = st.radio("Are you in any way familiar with AI?", ["", "YES", "NO"])
    #if q4 == "YES":
    q4b = st.text_input('If yes, how have you come in contact with AI?')
    #else:
    #    q4b = None
    q5 = st.text_input('How old are you?')
    q6 = st.radio("What gender do you identify as?", ["", "FEMALE", "MALE", "OTHER"])

    if not st.session_state.group == 0:

        q7 = st.text_input('What do you think is the basis for the AI\'s answer?')

        q8 = st.radio('Did the explanations given by the AI seem plausible to you?', ["", "YES", "NO"])
        q8b = st.text_input('Why?')

    st.write("Please rate the following statements:")

    likert_questions = {
        "rel_1": "The system always provides the advice I require to make my decision",
        "rel_2": "The system performs reliably",
        "rel_5": "The system analyzes problems consistently",
        "com_1": "The system uses appropriate methods to reach decisions",
        "com_2": "The system has sound knowledge about this kind of problem built into it",
        "com_3": "The advice the system produces is as good as that which a highly competent person could produce",
        "com_5": "The system makes use of all the knowledge and information available to it to produce its solution to the problem",
        "fai_1": "I believe advice from the system even though I don't know for certain that it is correct",
        "fai_2": "When I am uncertain I believe the system rather than myself",
        "fai_3": "If I am not sure about a decision, I have faith that the system will provide the best solution",
        "fai_4": "When the system gives unusual advice I am confident that the advice is correct",
        "fai_5": "Even if I have no reason to expect the system will be able to solve a difficult problem, I still feel certain that it will",
    }

    likert_results = {}

    likert_question_keys = list(likert_questions.keys())
    if likert_random_order:
        if not "likert_question_keys" in st.session_state:
            random.shuffle(likert_question_keys)
            st.session_state.likert_question_keys = likert_question_keys
        else:
            likert_question_keys = st.session_state.likert_question_keys

        

    for key in likert_question_keys:
        with st.container():
            col_likert1, col_likert2 = st.columns([5,8], gap = "large")
            with col_likert1:
                st.write(likert_questions[key])
            with col_likert2:
                likert_results[key] = st.radio(likert_questions[key], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal, key = key)
            #st.write("---")

    # rel_1 = st.radio(likert_questions["rel_1"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # rel_2 = st.radio(likert_questions["rel_2"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #rel_3 = st.radio("The system responds the same way under the same conditions at different times", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #rel_4 = st.radio("I can rely on the system to function properly", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # rel_5 = st.radio(likert_questions["rel_5"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # com_1 = st.radio(likert_questions["com_1"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # com_2 = st.radio(likert_questions["com_2"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # com_3 = st.radio(likert_questions["com_3"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #com_4 = st.radio("The system correctly uses the information I enter", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # com_5 = st.radio(likert_questions["com_5"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #und_1 = st.radio("I understand what will happen the next time I use the system because I understand how it behaves", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #und_2 = st.radio("I understand how the system will assist me with decisions I have to make", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #und_3 = st.radio("Although I may not know exactly how the system works, I know how to use it to make decisions about the problem", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #und_4 = st.radio("It is easy to follow what the system does", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #und_5 = st.radio("I recognize what I should do to get the advice I need from the system the next time I use it", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # fai_1 = st.radio(likert_questions["fai_1"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # fai_2 = st.radio(likert_questions["fai_2"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # fai_3 = st.radio(likert_questions["fai_3"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # fai_4 = st.radio(likert_questions["fai_4"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # fai_5 = st.radio(likert_questions["fai_5"], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #per_1 = st.radio("I would feel a sense of loss if the system was unavailable and I could no longer use it", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #per_2 = st.radio("I feel a sense of attachment to using the system", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #per_3 = st.radio("I find the system suitable to my style of decision making", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #per_4 = st.radio("I like using the system for decision making", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)
    # #per_5 = st.radio("I have a personal preference for making decisions with the system", ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal)

    #st.write("Something something did everything sound like bullshit?")
    #bullshit_answer = st.text_area("", label_visibility = "collapsed")

    submit_button = st.form_submit_button(label='Submit')

#st.write(q1, likert_results)

if submit_button:
    if any(a == "" for a in likert_results.values()) or any(a == "" for a in [q1, q2, q3, q4, q5, q6]) or (st.session_state.group == 1 and any(a == 0 for a in [q7, q8])):
        st.error("Please answer all the questions!")
    else:
        with open(filename, 'a+') as f:
            f.write(f"{1},{q1}\n")
            f.write(f"{2},{q2}\n")
            f.write(f"{3},{q3}, {q3b}\n")
            f.write(f"{4},{q4}, {q4b}\n")
            f.write(f"{5},{q5}\n")
            f.write(f"{6},{q6}\n")
            if st.session_state.group == 1:
                f.write(f"{7},{q7}\n")
                f.write(f"{8},{q8}, {q8b}\n")
            for k in likert_question_keys:
                f.write(f"{k},{likert_results[key]}\n")
        switch_page("Goodbye")

#next_page = st.button("Send results", key = 4)
#if next_page:
		#write results to file
#	switch_page("Goodbye")