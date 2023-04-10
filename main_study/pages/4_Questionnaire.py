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

st.markdown("### Uh, Questions?")
st.markdown("Also, thanks!")