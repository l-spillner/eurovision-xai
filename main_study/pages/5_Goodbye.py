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

no_sidebar_style = """
	<style>
        div[data-testid="stSidebarNav"] {pointer-events: none; cursor: default; height = 200px}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

############################################################ Public variables

############################################################ Public functions




############################################################ MAIN ############################################################

st.markdown("Thank you for participating in our study")