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

############################################################ Public variables

# paths
project_path = os.path.dirname(__file__) or '.'
data_path = os.path.join(project_path, "data.csv")

############################################################ Public functions




############################################################ MAIN ############################################################

############################################################ load data

st.write("This is the data:")

df = pd.read_csv(data_path, sep = "\t")
st.write(df)

st.write("Now comes the interactive part...")




