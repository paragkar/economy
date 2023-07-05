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

#function to extract a list of dates from the list using start and end date from the slider
def get_selected_date_list(listofallcolumns, start_date, end_date):
	    # Find the index of the first selected date
	    index1 = listofallcolumns.index(start_date)

	    # Find the index of the second selected date
	    index2 = listofallcolumns.index(end_date)

	    # Return a new list containing the dates from index1 to index2 (inclusive)
	    return listofallcolumns[index1:index2+1]

df = loadecofile()

dfcpi = df["CPI"]

dfcpi["Date"] = pd.to_datetime(dfcpi["Date"])

dfcpi["Date"] = [x.date() for x in list(dfcpi["Date"])]

dfcpi = dfcpi.set_index("Date")

cpi_sub_dict = df["CPI_Sub_Map"].set_index("SubCat").to_dict()["SubCatCode"]

cpi_main_dict = df["CPI_Main_Map"].set_index("MainCat").to_dict()["MainCatCode"]

dfcpi = dfcpi.replace(cpi_sub_dict)

dfcpi = dfcpi.replace(cpi_main_dict)


selected_feature = st.sidebar.selectbox("Select an Index", ["RuralIndex","UrbanIndex", "CombIndex"])

dfindex = dfcpi.reset_index().pivot(index="SubCat", columns ="Date", values =selected_feature).dropna(axis=0)

start_date, end_date = st.select_slider("Select a Range of Dates", 
					options = list(dfindex.columns), value =(dfindex.columns[-18],dfindex.columns[-1]))

delta = relativedelta(end_date, start_date)

no_of_months = delta.years * 12 + delta.months


date_range_list = get_selected_date_list(list(dfindex.columns), start_date, end_date)


dfindex = dfindex[date_range_list] #filter the dataframe with the selected dates

dfindex = dfindex.sort_values(dfindex.columns[-1], ascending = False)

dfindex = dfindex.drop("General")

years = sorted(set([x.year for x in list(dfindex.columns)]))

x_axis_title_dict = {"RuralIndex":"<b>Indian CPI Rural Index Trend<b>", "UrbanIndex":"<b>Indian CPI Urban Index Trend<b>", "CombIndex":
					"<b>Indian CPI Combined Index Trend<b>"}

if no_of_months <= 30:
	texttemplate ="%{z}"
else:
	texttemplate =""

data = [go.Heatmap(
		z=dfindex.values,
        x=dfindex.columns,
        y=dfindex.index,
		xgap = 1,
		ygap = 1,
		hoverinfo ='text',
		# text = dfindex.values,
		colorscale="Hot",
			texttemplate=texttemplate,
			textfont={"size":8},
			reversescale=True,
			),
		]
			

fig = go.Figure(data=data)

fig.update_layout(uniformtext_minsize=14, 
				  uniformtext_mode='hide', 
				  xaxis_title= x_axis_title_dict[selected_feature], 
				  yaxis_title=None, 
				  yaxis_autorange='reversed',
				  font=dict(size=10),
				  template='simple_white',
				  paper_bgcolor=None,
				  height=600, 
				  width=1200,
				  margin=dict(t=80, b=50, l=50, r=50, pad=0),
				  yaxis=dict(
		        	  tickmode='array',
		        	  ticktext =["<b>"+x+"<b>" for x in list(dfindex.index)],
				  	  tickfont=dict(size=12)),
				  xaxis = dict(
				  side = 'top',
				  tickmode = 'array',
				  tickvals = years,
				  tickformat='<b>%Y<b>',
				  tickangle=0,
				  dtick = 1), 
				)

#Drawning a black border around the heatmap chart 
fig.update_xaxes(fixedrange=True,showline=True,linewidth=1.2,linecolor='black', mirror=True)
fig.update_yaxes(fixedrange=True,showline=True, linewidth=1.2, linecolor='black', mirror=True)

st.plotly_chart(fig, use_container_width=True) # for heatmaps








