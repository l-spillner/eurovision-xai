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

############################################################ Public variables

############################################################ Public functions




############################################################ MAIN ############################################################

if balloons:
	st.balloons()

st.markdown("Thank you for participating in our study!")

st.write("If you had fun and/or want to support our research, please consider sharing our study with people you know. You can copy the text below:")

st.info("Here's a link to a research study on working with Artificial Intelligence to judge the quality of Eurovision Song Contest participants:   \n   [link here]")

