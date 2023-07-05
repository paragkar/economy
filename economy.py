#importing libraries
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np
from collections import OrderedDict
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
import plotly
import pandas as pd
import plotly.figure_factory as ff
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
from datetime import datetime
import datetime as dt 
import calendar
import time

from PIL import Image

from dateutil import relativedelta

import re

from collections import defaultdict

from dateutil.relativedelta import relativedelta

import io
import msoffcrypto

import pickle
from pathlib import Path
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

from deta import Deta


#Set page layout here
st.set_page_config(layout="wide")


#--------hide streamlit style and buttons--------------

hide_st_style = '''
				<style>
				#MainMenu {visibility : hidden;}
				footer {visibility : hidder;}
				header {visibility :hidden;}
				<style>
				'''
st.markdown(hide_st_style, unsafe_allow_html =True)


@st.cache_resource
def loadecofile():

	password = st.secrets["db_password"]

	excel_content = io.BytesIO()

	with open("economic_data.xlsx", 'rb') as f:
		excel = msoffcrypto.OfficeFile(f)
		excel.load_key(password)
		excel.decrypt(excel_content)

	#loading data from excel file
	xl = pd.ExcelFile(excel_content)
	sheet = xl.sheet_names
	df = pd.read_excel(excel_content, sheet_name=sheet)

	return df

df = loadecofile()

dfcpi = df["CPI"]

dfcpi["Date"] = pd.to_datetime(dfcpi["Date"])

dfcpi["Date"] = [x.date() for x in list(dfcpi["Date"])]

dfcpi = dfcpi.set_index("Date")

cpi_sub_dict = df["CPI_Sub_Map"].set_index("SubCat").to_dict()["SubCatCode"]

cpi_main_dict = df["CPI_Main_Map"].set_index("MainCat").to_dict()["MainCatCode"]

dfcpi = dfcpi.replace(cpi_sub_dict)

dfcpi = dfcpi.replace(cpi_main_dict)

dfrural = dfcpi.reset_index().pivot(index="SubCat", columns ="Date", values ="RuralIndex").dropna(axis=0)

dfrural = dfrural.sort_values(dfrural.columns[-1], ascending = False)

data = [go.Heatmap(
		z=dfrural.values,
        x=dfrural.columns,
        y=dfrural.index,
		xgap = 1,
		ygap = 1,
		hoverinfo ='text',
		text = dfrural.values,
		colorscale="Picnic",
			# texttemplate="%{text}",
			textfont={"size":10},
			reversescale=True,
			),
		]
			
#Ploting the heatmap for all the above three options

fig = go.Figure(data=data)

fig.update_layout(uniformtext_minsize=12, 
				  uniformtext_mode='hide', 
				  xaxis_title=None, 
				  yaxis_title=None, 
				  yaxis_autorange='reversed',
				  font=dict(size=12),
				  template='simple_white',
				  paper_bgcolor=None,
				  height=600, 
				  width=1200,
				  margin=dict(t=80, b=50, l=50, r=50, pad=0),
				  yaxis=dict(
		        	  tickmode='array'),
				  xaxis = dict(
				  side = 'top',
				  tickmode = 'linear',
				  # tickangle=xdtickangle,
				  # dtick = xdtickval), 
				))

st.plotly_chart(fig, use_container_width=True) # for heatmaps








