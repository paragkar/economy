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

#function for enabling data for the figure object
def data(df,colorscale,texttemplate, hovertext):
	data = [go.Heatmap(
		z=df.values,
        x=df.columns,
        y=df.index,
		xgap = 1,
		ygap = 1,
		hoverinfo ='text',
		text = hovertext,
		# text = dfindex.values,
		colorscale=colorscale,
		showscale=False,
		texttemplate=texttemplate,
		textfont={"size":8},
		# reversescale=True,
						),
			]
	return data

#function for updating the layout of the figure for the data object of cpi
def figupdatecpi(fig, df, dates, x_title_dict, selected_feature,height, tickvals, hoverlabel_bgcolor, sort_by_date):
	fig.update_layout(uniformtext_minsize=14, 
					  uniformtext_mode='hide', 
					  xaxis_title= "<span style='text-decoration: underline; color: red;'>"+x_title_dict[selected_feature]+\
					  				" (Sort Date - "+str(sort_by_date)+")",
					  xaxis_title_font=dict(size=18),
					  yaxis_title=None, 
					  yaxis_autorange='reversed',
					  font=dict(size=10),
					  template='simple_white',
					  paper_bgcolor=None,
					  height=height, 
					  width=1200,
					  margin=dict(t=40, b=0, l=50, r=50, pad=0),
					  yaxis=dict(
			        	  tickmode='array',
			        	  ticktext =["<b>"+x+"<b>" for x in list(df.index)],
					  	  tickfont=dict(size=12)),
					  xaxis = dict(
					  side = 'top',
					  tickmode = 'array',
					  tickvals = tickvals,
					  tickformat='%b-%y',
					  tickangle=-45,
					  dtick = 0), 
					)
	#drawing a rectangle around the heatmap
	fig.update_xaxes(fixedrange=True,showline=True,linewidth=1.2,linecolor='black', mirror=True)
	fig.update_yaxes(fixedrange=True,showline=True, linewidth=1.2, linecolor='black', mirror=True)
	#coloring the hoverbox
	fig.update_traces(hoverlabel=dict(bgcolor=hoverlabel_bgcolor,font=dict(size=12, color='white')))


#function for updating the layout of the figure for the data object for general index cpi
def figupdatecpigen(fig, df, dates, x_title_dict, selected_feature, height, tickvals, hoverlabel_bgcolor):
	fig.update_layout(uniformtext_minsize=14, 
					  uniformtext_mode='hide', 
					  xaxis_title= "<span style='text-decoration: underline; color: red;'>"+x_title_dict[selected_feature],
					  xaxis_title_font=dict(size=18),
					  yaxis_title=None, 
					  yaxis_autorange='reversed',
					  font=dict(size=10),
					  template='simple_white',
					  paper_bgcolor=None,
					  height=height, 
					  width=1100,
					  margin=dict(t=80, b=25, l=50, r=50, pad=0),
					  yaxis=dict(
			        	  ticktext =[],
			        	  tickvals =[],
					  	  ticks =""),
					  xaxis = dict(
					  side = 'top',
					  tickmode = 'array',
					  tickvals = tickvals,
					  tickformat='%b-%y',
					  tickangle=-45,
					  dtick = 0), 
					)
	#drawing a rectangle around the heatmap
	fig.update_xaxes(fixedrange=True,showline=True,linewidth=1.2,linecolor='black', mirror=True)
	fig.update_yaxes(fixedrange=True,showline=True, linewidth=1.2, linecolor='black', mirror=True)
	fig.update_traces(hoverlabel=dict(bgcolor=hoverlabel_bgcolor,font=dict(size=12, color='white')))


#function for updating the layout of the figure for the data object of gst
def figupdategst(fig, df, dates, x_title_dict,height, tickvals, hoverlabel_bgcolor, sort_by_date):
	fig.update_layout(uniformtext_minsize=14, 
					  uniformtext_mode='hide', 
					  # xaxis_title= "<span style='text-decoration: underline; color: red;'>"+x_title_dict[selected_feature]+\
					  # 				" (Sort Date - "+str(sort_by_date)+")",
					  xaxis_title_font=dict(size=18),
					  yaxis_title=None, 
					  yaxis_autorange='reversed',
					  font=dict(size=10),
					  template='simple_white',
					  paper_bgcolor=None,
					  height=height, 
					  width=1200,
					  margin=dict(t=40, b=0, l=50, r=50, pad=0),
					  yaxis=dict(
			        	  tickmode='array',
			        	  ticktext =["<b>"+x+"<b>" for x in list(df.index)],
					  	  tickfont=dict(size=12)),
					  xaxis = dict(
					  side = 'top',
					  tickmode = 'array',
					  tickvals = tickvals,
					  tickformat='%b-%y',
					  tickangle=-45,
					  dtick = 0), 
					)
	#drawing a rectangle around the heatmap
	fig.update_xaxes(fixedrange=True,showline=True,linewidth=1.2,linecolor='black', mirror=True)
	fig.update_yaxes(fixedrange=True,showline=True, linewidth=1.2, linecolor='black', mirror=True)
	#coloring the hoverbox
	fig.update_traces(hoverlabel=dict(bgcolor=hoverlabel_bgcolor,font=dict(size=12, color='white')))

#function for updating the layout of the figure for the data object for total in gst
def figupdategsttot(fig, df, dates, x_title_dict, height, tickvals, hoverlabel_bgcolor):
	fig.update_layout(uniformtext_minsize=14, 
					  uniformtext_mode='hide', 
					  # xaxis_title= "<span style='text-decoration: underline; color: red;'>"+x_title_dict[selected_feature],
					  xaxis_title_font=dict(size=18),
					  yaxis_title=None, 
					  yaxis_autorange='reversed',
					  font=dict(size=10),
					  template='simple_white',
					  paper_bgcolor=None,
					  height=height, 
					  width=1100,
					  margin=dict(t=80, b=25, l=50, r=50, pad=0),
					  yaxis=dict(
			        	  ticktext =[],
			        	  tickvals =[],
					  	  ticks =""),
					  xaxis = dict(
					  side = 'top',
					  tickmode = 'array',
					  tickvals = tickvals,
					  tickformat='%b-%y',
					  tickangle=-45,
					  dtick = 0), 
					)
	#drawing a rectangle around the heatmap
	fig.update_xaxes(fixedrange=True,showline=True,linewidth=1.2,linecolor='black', mirror=True)
	fig.update_yaxes(fixedrange=True,showline=True, linewidth=1.2, linecolor='black', mirror=True)
	fig.update_traces(hoverlabel=dict(bgcolor=hoverlabel_bgcolor,font=dict(size=12, color='white')))



#function for creating hovertext for cpi
# @st.cache_resource
def htext_cpi(dfindex, dfinflation, dfinfweighted,datano):
	if datano==1:
		dfanchor = dfindex.copy()
	if datano==2:
		dfanchor = dfinflation.copy()
	if datano==3:
		dfanchor = dfinfweighted.copy()
	hovertext = []
	for yi, yy in enumerate(dfanchor.index):
		hovertext.append([])
		for xi, xx in enumerate(dfanchor.columns):
			
			price_index = dfindex.loc[yy,xx]
			price_inflation = dfinflation.loc[yy, xx]
			weighted_inflation = dfinfweighted.loc[yy,xx]
			hovertext[-1].append(
					    'Date: {}\
					     <br>Sub Catagory : {}\
					     <br>Price Index: {}\
					     <br>Price Inflation: {} %\
					     <br>Weighted Inflation: {} basis pts'


				     .format(
					    xx,
					    yy,
					    price_index,
					    round(price_inflation,1),
					    round(weighted_inflation,1),
					    )
					    )
	return hovertext


#function for creating hovertext for gst
# @st.cache_resource
def htext_gst(dfcgsts, dfsgst, dfigst,dfcess,datano):
	if datano==1:
		dfanchor = dfcgsts.copy()
	if datano==2:
		dfanchor = dfsgst.copy()
	if datano==3:
		dfanchor = dfigst.copy()
	if datano==4:
		dfanchor = dfcess.copy()
	hovertext = []
	for yi, yy in enumerate(dfanchor.index):
		hovertext.append([])
		for xi, xx in enumerate(dfanchor.columns):
			
			cgst= dfcgsts.loc[yy,xx]
			sgst = dfsgst.loc[yy, xx]
			igst = dfigst.loc[yy,xx]
			cess = dfcess.loc[yy,xx]
			hovertext[-1].append(
					    'Date: {}\
					     <br>State : {}\
					     <br>CGST: {} Rs Cr\
					     <br>SGST: {} Rs Cr\
					     <br>IGST {} Rs Cr\
					     <br>CESS {} Rs Cr'

				     .format(
					    xx,
					    yy,
					    cgst,
					    sgst,
					    igst,
					    cess,
					    )
					    )
	return hovertext


#Loading the datafile
df = loadecofile()

#making a selection for financial metric
selected_metric = st.sidebar.selectbox("Select a Metric", ["CPI India", "CPI States", "GST India"])

if selected_metric == "CPI India":

	dfcpi = df["CPI"]

	cpi_sub_dict = df["CPI_Sub_Map"].set_index("SubCat").to_dict()["SubCatCode"]

	cpi_main_dict = df["CPI_Main_Map"].set_index("MainCat").to_dict()["MainCatCode"]

	dfcpi = dfcpi.replace(cpi_sub_dict)

	dfcpi = dfcpi.replace(cpi_main_dict)

	index = "SubCat"

	aggmetric ="General"

	col1width = 0.35

if selected_metric == "CPI States":

	dfcpi = df["CPI_States"]

	cpi_states_dict = df["States_Code_Map"].set_index("State").to_dict()["Code"]

	dfcpi = dfcpi.replace(cpi_states_dict)

	index = "State"

	aggmetric = "IND"

	col1width = 0.000000001 


if selected_metric in ["CPI India", "CPI States"]:

	if selected_metric == "CPI India":

		dfcpi = df["CPI"]

		cpi_sub_dict = df["CPI_Sub_Map"].set_index("SubCat").to_dict()["SubCatCode"]

		cpi_main_dict = df["CPI_Main_Map"].set_index("MainCat").to_dict()["MainCatCode"]

		dfcpi = dfcpi.replace(cpi_sub_dict)

		dfcpi = dfcpi.replace(cpi_main_dict)

		index = "SubCat"

		aggmetric ="General"

		col1width = 0.35

	if selected_metric == "CPI States":

		dfcpi = df["CPI_States"]

		cpi_states_dict = df["States_Code_Map"].set_index("State").to_dict()["Code"]

		dfcpi = dfcpi.replace(cpi_states_dict)

		index = "State"

		aggmetric = "IND"

		col1width = 0.000000001 

	dfcpi =dfcpi.replace("-", np.nan)

	dfcpi["Date"] = pd.to_datetime(dfcpi["Date"])

	dfcpi["Date"] = [x.date() for x in list(dfcpi["Date"])]

	dfcpi = dfcpi.set_index("Date")

	selected_feature = st.sidebar.selectbox("Select an Index", ["RuralIndex","UrbanIndex", "CombIndex"])

	selected_weights_dict = {"RuralIndex":"RuralWeights", "UrbanIndex":"UrbanWeights", "CombIndex":"CombWeights"}

	dfindex = dfcpi.reset_index().pivot(index=index, columns ="Date", values =selected_feature).dropna(axis=0)

	dfweights = dfcpi.reset_index().pivot(index=index, columns ="Date", values =selected_weights_dict[selected_feature]).dropna(axis=0)/100

	dfinflation = (((dfindex - dfindex.shift(12,axis=1))/dfindex.shift(12,axis=1))*100).round(1)

	#slider for selecting the range of dates 
	start_date, end_date = st.select_slider("Select Range of Dates", 
						options = list(dfindex.columns), value =(dfindex.columns[-18],dfindex.columns[-1]))

	#defining the tabs for rendering the heatmaps for different features
	tab1, tab2, tab3 = st.tabs(["Price Index", "Price Inflation", "Weighted Inflation"])

	#calculating the difference in number of months between selected dates
	delta = relativedelta(end_date, start_date)

	no_of_months = delta.years * 12 + delta.months

	#selecting the date for filtering the dataframe
	date_range_list = get_selected_date_list(list(dfindex.columns), start_date, end_date)

	#filtering the dataframe with the selected range of dates
	dfindex = dfindex[date_range_list] #filter the dataframe with the selected dates
	dfinflation = dfinflation[date_range_list] #filter the dataframe with the selected dates
	dfweights = dfweights[date_range_list]

	#calculating the dataframe for measuring the contribution of items to the total inflation (basis points)
	dfinfweighted = (dfinflation*dfweights)*100

	#selecting the date for sorting the dataframe
	sort_by_date = st.sidebar.selectbox("Select Sorting Date", sorted(list(dfindex.columns), reverse = True), 0)

	#sorting the dataframe with the selected dates
	dfindex = dfindex.sort_values(sort_by_date, ascending = False)
	dfinflation = dfinflation.sort_values(sort_by_date, ascending = False)
	dfinfweighted = dfinfweighted.sort_values(sort_by_date, ascending = False)

	#selecting the dates for list on the xaxis of the heatmap
	dates = dfindex.columns

	#selecting the years for list on the xaxis when selected dates goes beyond chosen value of 36
	years = sorted(list(set([x.year for x in list(dfindex.columns)])))

	#dictionary for defining the title of the heatmaps renders on the screen
	x_axis_title_dict1 = {"RuralIndex":"<b>Indian CPI Rural Trend<b>", "UrbanIndex":"<b>Indian CPI Urban Trend<b>", "CombIndex":
						"<b>Indian CPI Combined Trend<b>"}
	x_axis_title_gen_dict1 = {"RuralIndex":"<b>Indian CPI General Rural Trend<b>", "UrbanIndex":"<b>Indian CPI General Urban Trend<b>", "CombIndex":
						"<b>Indian CPI General Combined Trend<b>"}
	x_axis_title_dict2 = {"RuralIndex":"<b>Indian CPI Rural % Inflation Trend<b>", "UrbanIndex":"<b>Indian CPI Urban % Inflation Trend<b>", "CombIndex":
						"<b>Indian CPI Combined % Inflation Trend<b>"}
	x_axis_title_gen_dict2 = {"RuralIndex":"<b>Indian CPI Rural % General Inflation Trend<b>", "UrbanIndex":"<b>Indian CPI Urban % General Inflation Trend<b>", "CombIndex":
						"<b>Indian CPI Combined % General Inflation Trend<b>"}
	x_axis_title_dict3 = {"RuralIndex":"<b>Indian CPI Rural (Basis Points) Contribution to Overall Inflation<b>", 
						  "UrbanIndex":"<b>Indian CPI Urban (Basis Points) Contribution to Overall Inflation<b>", 
						  "CombIndex": "<b>Indian CPI Combined (Basis Points) Contribution to Overall Inflation<b>"}
	x_axis_title_gen_dict3 = {"RuralIndex":"<b>Indian CPI Rural Total Inflation Trend (Basis Points)<b>", 
						      "UrbanIndex":"<b>Indian CPI Urban Total Inflation Trend (Basis Points)<b>", 
						      "CombIndex": "<b>Indian CPI Combined Total Inflation Trend (Basis Points)<b>"}

	#the logic for seleting the texttemplete and tickvals if date range goes beyond a number of months
	if no_of_months <= 36:
		texttemplate ="%{z:.1f}"
		tickvals = dates
	else:
		texttemplate =""
		tickvals = years

	#preparing the dataframe for general items for total to be listed below each heatmap
	genindex = dfindex.loc[aggmetric,:].reset_index().T
	dfindex = dfindex.drop(aggmetric)
	genindex.columns = list(genindex.loc["Date",:])
	genindex=genindex.drop("Date")


	geninflation = dfinflation.loc[aggmetric,:].reset_index().T
	dfinflation = dfinflation.drop(aggmetric)
	geninflation.columns = list(geninflation.loc["Date",:])
	geninflation=geninflation.drop("Date")


	geninfweighted = dfinfweighted.loc[aggmetric,:].reset_index().T
	dfinfweighted = dfinfweighted.drop(aggmetric)
	geninfweighted.columns = list(geninfweighted.loc["Date",:])
	geninfweighted=geninfweighted.drop("Date")


	#dropping na if all rows are zero
	dfindex = dfindex.replace(0,np.nan).dropna(axis=0, how='all')
	dfinflation = dfinflation.replace(0,np.nan).dropna(axis=0, how='all')
	dfinfweighted = dfinfweighted.replace(0,np.nan).dropna(axis=0, how='all')


	#preparing hovertext for each dataframe
	hovertext1 = htext_cpi(dfindex, dfinflation, dfinfweighted,1)
	hovertext2 = htext_cpi(dfindex, dfinflation, dfinfweighted,2)
	hovertext3 = htext_cpi(dfindex, dfinflation, dfinfweighted,3)
	hovertextgen1 = htext_cpi(genindex, geninflation, geninfweighted,1)
	hovertextgen2 = htext_cpi(genindex, geninflation, geninfweighted,2)
	hovertextgen3 = htext_cpi(genindex, geninflation, geninfweighted,3)
	hoverlabel_bgcolor = "#000000" #subdued black


	#calculating data for individual figures of heatmaps
	data1 = data(dfindex,"Rainbow",texttemplate, hovertext1)
	data2 = data(dfinflation,"Rainbow",texttemplate, hovertext2)
	data3 = data(dfinfweighted,"Rainbow",texttemplate, hovertext3)
	datagen1 = data(genindex,"Rainbow",texttemplate, hovertextgen1)
	datagen2 = data(geninflation,"Rainbow",texttemplate, hovertextgen2)
	datagen3 = data(geninfweighted,"Rainbow",texttemplate, hovertextgen3)


	#defining the figure object of individual heatmaps
	fig1 = go.Figure(data=data1)
	fig2 = go.Figure(data=data2)
	fig3 = go.Figure(data=data3)
	figgen1 = go.Figure(data=datagen1)
	figgen2 = go.Figure(data=datagen2)
	figgen3 = go.Figure(data=datagen3)


	#updating the figure of individual heatmaps
	figupdatecpi(fig1, dfindex, dates, x_axis_title_dict1, selected_feature, 650, tickvals, hoverlabel_bgcolor, sort_by_date)
	figupdatecpi(fig2, dfindex, dates, x_axis_title_dict2, selected_feature, 650, tickvals, hoverlabel_bgcolor, sort_by_date)
	figupdatecpi(fig3, dfindex, dates, x_axis_title_dict3, selected_feature, 650, tickvals, hoverlabel_bgcolor, sort_by_date)
	figupdatecpigen(figgen1, genindex, dates, x_axis_title_gen_dict1, selected_feature, 150, tickvals,hoverlabel_bgcolor)
	figupdatecpigen(figgen2, geninflation, dates, x_axis_title_gen_dict2, selected_feature, 150, tickvals, hoverlabel_bgcolor)
	figupdatecpigen(figgen3, geninfweighted, dates, x_axis_title_gen_dict3, selected_feature, 150, tickvals, hoverlabel_bgcolor)

	#Final plotting of various charts on the output page
	style = "<style>h3 {text-align: left;}</style>"
	with tab1:
		st.plotly_chart(fig1, use_container_width=True)
		if selected_metric == "CPI India":
			col1,col2 = st.columns([col1width,14]) #create collumns of uneven width
			col2.plotly_chart(figgen1, use_container_width=True)
		if selected_metric == "CPI States":
			st.plotly_chart(figgen1, use_container_width=True)
	with tab2:
		st.plotly_chart(fig2, use_container_width=True)
		if selected_metric == "CPI India":
			col1,col2 = st.columns([col1width,14]) #create collumns of uneven width
			col2.plotly_chart(figgen2, use_container_width=True)
		if selected_metric == "CPI States":
			st.plotly_chart(figgen2, use_container_width=True)
	with tab3:
		st.plotly_chart(fig3, use_container_width=True)
		if selected_metric == "CPI India":
			col1,col2 = st.columns([col1width,14]) #create collumns of uneven width
			col2.plotly_chart(figgen3, use_container_width=True)
		if selected_metric == "CPI States":
			st.plotly_chart(figgen3, use_container_width=True)

if selected_metric == "GST India":

	dfgst = df["GST"]

	gst_state_dict = df["GST_State_Map"].set_index("State").to_dict()["StateCode"]

	dfgst = dfgst.replace(gst_state_dict)

	dfgst["Date"] = pd.to_datetime(dfgst["Date"])

	dfgst["Date"] = [x.date() for x in list(dfgst["Date"])]

	dfgst = dfgst.set_index("Date")

	dfgst['Amount'] = pd.to_numeric(dfgst['Amount'], errors='coerce')

	dfcgsts = dfgst[dfgst["Type"]=="CGSTS"].drop(columns = "Type").reset_index().groupby(["Date","State"])["Amount"].sum().reset_index()
	dfsgst = dfgst[dfgst["Type"]=="SGST"].drop(columns = "Type").reset_index().groupby(["Date","State"])["Amount"].sum().reset_index()
	dfigst = dfgst[dfgst["Type"]=="IGST"].drop(columns = "Type").reset_index().groupby(["Date","State"])["Amount"].sum().reset_index()
	dfcess = dfgst[dfgst["Type"]=="CESS"].drop(columns = "Type").reset_index().groupby(["Date","State"])["Amount"].sum().reset_index()

	dfcgsts = dfcgsts.pivot(index = "State", columns = "Date", values = "Amount")
	dfsgst = dfsgst.pivot(index = "State", columns = "Date", values = "Amount")
	dfigst = dfigst.pivot(index = "State", columns = "Date", values = "Amount")
	dfcess = dfcess.pivot(index = "State", columns = "Date", values = "Amount")

	start_date, end_date = st.select_slider("Select Range of Dates", 
						options = list(dfcgsts.columns), value =(dfcgsts.columns[-18],dfcgsts.columns[-1]))

	#calculating the difference in number of months between selected dates
	delta = relativedelta(end_date, start_date)

	no_of_months = delta.years * 12 + delta.months

	#selecting the date for filtering the dataframe
	date_range_list = get_selected_date_list(list(dfcgsts.columns), start_date, end_date)

	#filtering the dataframe with the selected range of dates
	dfcgsts = dfcgsts[date_range_list].replace(np.nan,0).round(1)
	dfsgst = dfsgst[date_range_list].replace(np.nan,0).round(1)
	dfigst = dfigst[date_range_list].replace(np.nan,0).round(1)
	dfcess = dfcess[date_range_list].replace(np.nan,0).round(1)

	#selecting the date for sorting the dataframe
	sort_by_date = st.sidebar.selectbox("Select Sorting Date", sorted(list(dfcgsts.columns), reverse = True), 0)

	#sorting the dataframe with the selected dates
	dfcgsts = dfcgsts.sort_values(sort_by_date, ascending = False)
	dfsgst = dfsgst.sort_values(sort_by_date, ascending = False)
	dfigst = dfigst.sort_values(sort_by_date, ascending = False)
	dfcess = dfcess.sort_values(sort_by_date, ascending = False)

	dfcgststotal = dfcgsts.sum(axis=0).to_frame().T
	dfsgsttotal = dfsgst.sum(axis=0).to_frame().T
	dfigsttotal = dfigst.sum(axis=0).to_frame().T
	dfcesstotal = dfcess.sum(axis=0).to_frame().T

	st.write(dfcesstotal)

	#selecting the dates for list on the xaxis of the heatmap
	dates = dfcgsts.columns

	#selecting the years for list on the xaxis when selected dates goes beyond chosen value of 36
	years = sorted(list(set([x.year for x in list(dfcgsts.columns)])))


	#the logic for seleting the texttemplete and tickvals if date range goes beyond a number of months
	if no_of_months <= 36:
		texttemplate ="%{z:.1f}"
		tickvals = dates
	else:
		texttemplate =""
		tickvals = years

	#preparing hovertext for each dataframe
	hovertext1 = htext_gst(dfcgsts, dfsgst, dfigst,dfcess,1)
	hovertext2 = htext_gst(dfcgsts, dfsgst, dfigst,dfcess,2)
	hovertext3 = htext_gst(dfcgsts, dfsgst, dfigst,dfcess,3)
	hovertext4 = htext_gst(dfcgsts, dfsgst, dfigst,dfcess,4)
	hovertexttot1 = htext_gst(dfcgststotal, dfsgsttotal, dfigsttotal,dfcesstotal,1)
	hovertexttot2 = htext_gst(dfcgststotal, dfsgsttotal, dfigsttotal,dfcesstotal,2)
	hovertexttot3 = htext_gst(dfcgststotal, dfsgsttotal, dfigsttotal,dfcesstotal,3)
	hovertexttot4 = htext_gst(dfcgststotal, dfsgsttotal, dfigsttotal,dfcesstotal,4)
	hoverlabel_bgcolor = "#000000" #subdued black


	#calculating data for individual figures of heatmaps
	data1 = data(dfcgsts,"Rainbow",texttemplate, hovertext1)
	data2 = data(dfsgst,"Rainbow",texttemplate, hovertext2)
	data3 = data(dfigst,"Rainbow",texttemplate, hovertext3)
	data4 = data(dfcess,"Rainbow",texttemplate, hovertext4)
	datatot1 = data(dfcgststotal,"Rainbow",texttemplate, hovertexttot1)
	datatot2 = data(dfsgsttotal,"Rainbow",texttemplate, hovertexttot2)
	datatot3 = data(dfigsttotal,"Rainbow",texttemplate, hovertexttot3)
	datatot4 = data(dfcesstotal,"Rainbow",texttemplate, hovertexttot4)


	#defining the figure object of individual heatmaps
	fig1 = go.Figure(data=data1)
	fig2 = go.Figure(data=data2)
	fig3 = go.Figure(data=data3)
	fig4 = go.Figure(data=data4)
	figtot1 = go.Figure(data=datatot1)
	figtot2 = go.Figure(data=datatot2)
	figtot3 = go.Figure(data=datatot3)
	figtot4 = go.Figure(data=datatot4)


	#dictionary for defining the title of the heatmaps renders on the screen
	x_axis_title_dict1 = {"RuralIndex":"<b>Indian CPI Rural Trend<b>", "UrbanIndex":"<b>Indian CPI Urban Trend<b>", "CombIndex":
						"<b>Indian CPI Combined Trend<b>"}
	x_axis_title_gen_dict1 = {"RuralIndex":"<b>Indian CPI General Rural Trend<b>", "UrbanIndex":"<b>Indian CPI General Urban Trend<b>", "CombIndex":
						"<b>Indian CPI General Combined Trend<b>"}
	x_axis_title_dict2 = {"RuralIndex":"<b>Indian CPI Rural % Inflation Trend<b>", "UrbanIndex":"<b>Indian CPI Urban % Inflation Trend<b>", "CombIndex":
						"<b>Indian CPI Combined % Inflation Trend<b>"}
	x_axis_title_gen_dict2 = {"RuralIndex":"<b>Indian CPI Rural % General Inflation Trend<b>", "UrbanIndex":"<b>Indian CPI Urban % General Inflation Trend<b>", "CombIndex":
						"<b>Indian CPI Combined % General Inflation Trend<b>"}
	x_axis_title_dict3 = {"RuralIndex":"<b>Indian CPI Rural (Basis Points) Contribution to Overall Inflation<b>", 
						  "UrbanIndex":"<b>Indian CPI Urban (Basis Points) Contribution to Overall Inflation<b>", 
						  "CombIndex": "<b>Indian CPI Combined (Basis Points) Contribution to Overall Inflation<b>"}
	x_axis_title_gen_dict3 = {"RuralIndex":"<b>Indian CPI Rural Total Inflation Trend (Basis Points)<b>", 
						      "UrbanIndex":"<b>Indian CPI Urban Total Inflation Trend (Basis Points)<b>", 
						      "CombIndex": "<b>Indian CPI Combined Total Inflation Trend (Basis Points)<b>"}

	x_axis_title_dict4 = {"RuralIndex":"<b>Indian CPI Rural (Basis Points) Contribution to Overall Inflation<b>", 
						  "UrbanIndex":"<b>Indian CPI Urban (Basis Points) Contribution to Overall Inflation<b>", 
						  "CombIndex": "<b>Indian CPI Combined (Basis Points) Contribution to Overall Inflation<b>"}
	x_axis_title_gen_dict4 = {"RuralIndex":"<b>Indian CPI Rural Total Inflation Trend (Basis Points)<b>", 
						      "UrbanIndex":"<b>Indian CPI Urban Total Inflation Trend (Basis Points)<b>", 
						      "CombIndex": "<b>Indian CPI Combined Total Inflation Trend (Basis Points)<b>"}


	#updating the figure of individual heatmaps
	figupdategst(fig1, dfcgsts, dates, x_axis_title_dict1, 650, tickvals, hoverlabel_bgcolor, sort_by_date)
	figupdategst(fig2, dfcgsts, dates, x_axis_title_dict2, 650, tickvals, hoverlabel_bgcolor, sort_by_date)
	figupdategst(fig3, dfcgsts, dates, x_axis_title_dict3, 650, tickvals, hoverlabel_bgcolor, sort_by_date)
	figupdategst(fig4, dfcgsts, dates, x_axis_title_dict4, 650, tickvals, hoverlabel_bgcolor, sort_by_date)
	figupdategsttot(figtot1, dfcgststotal, dates, x_axis_title_gen_dict1, 150, tickvals,hoverlabel_bgcolor)
	figupdategsttot(figtot2, dfsgsttotal, dates, x_axis_title_gen_dict2, 150, tickvals, hoverlabel_bgcolor)
	figupdategsttot(figtot3, dfigsttotal, dates, x_axis_title_gen_dict3, 150, tickvals, hoverlabel_bgcolor)
	figupdategsttot(figtot4, dfcesstotal, dates, x_axis_title_gen_dict3, 150, tickvals, hoverlabel_bgcolor)


	#Final plotting of various charts on the output page
	style = "<style>h3 {text-align: left;}</style>"
	st.plotly_chart(fig1, use_container_width=True)
	st.plotly_chart(figtot1, use_container_width=True)











