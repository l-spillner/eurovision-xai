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

no_sidebar_style = """
	<style>
        div[data-testid="stSidebarNav"] {pointer-events: none; cursor: default;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

############################################################ Public variables

# paths
project_path = os.path.dirname(__file__) or '.'
data_path = os.path.join(project_path, "data.csv")

############################################################ Public functions




############################################################ MAIN ############################################################

############################################################ load data

df = pd.read_csv(data_path, sep = "\t", index_col = 0)
st.session_state.data = df

# show of hide data for debug
if False:

	st.write("This is the data:")
	st.write(df)

	st.write("But participants won't actually see this; it's just for us to check. Instead, they only see the lower part:")
	st.write("---")

st.write("# ABBA-cadabra!")

st.markdown("Blablabla, explanation goes here. Something something your data.")

next_page = st.button("Start", key = 1)
if next_page:
	   switch_page("Eurovision_-_Guess_the_Winners")




