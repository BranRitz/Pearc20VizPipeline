## Functions to get COVID/population/school data from the web
import plotly.graph_objects as go

import numpy as np
import requests
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import json
from io import open
from os import path
from datetime import datetime, timedelta

import os
from zipfile import ZipFile


def refreshdata():
    '''
    Function to update the data periodically.
    :return:
    '''

def pullcovid():
    '''
    Function to pull COVID/population data once. Needs to run every time data is updated.
    Get data with Kaggle API. Put data into numpy array
    :return:
    '''

    date = datetime.date(datetime.now() - timedelta(days=4))  # get today's date

    # Download COVID/population data from Kaggle
    os.system("kaggle datasets download -d headsortails/covid19-us-county-jhu-data-demographics")

    file_name = "covid19-us-county-jhu-data-demographics.zip"
    # extract the zip file to get the COVID/population csv files
    with ZipFile(file_name, 'r') as zip:
        zip.extractall()

    # Put csv files into numpy array
    covidcases = pd.read_csv('./covid_us_county.csv')
    popdata = pd.read_csv('./us_county.csv')

    covidcases = covidcases[["fips", "date", "cases", "deaths"]]    # only get relevant information in dataframe
    popdata = popdata[["fips", "median_age", "population"]]

    # Get only today's data for COVID
    todaycases = covidcases[covidcases["date"] == str(date)]

    # Get last 30 days of data

    timeinc = timedelta(days=1)     # decrement one day at a time
    df_case_dict = {}    # dictionary will contain dates as keys, dataframes of cases for every county as values

    for i in range(30): # go 30 days back
        df_case_dict[str(date)] = covidcases[covidcases["date"] == str(date)]
        date = date - timeinc
    todaycases.dropna(inplace=True)
    todaycases['fips'] = todaycases['fips'].astype('int64', copy=True)
    todaycases = todaycases[todaycases['fips'] < 80000].copy(deep=True)
    todaycases['fips'] = todaycases['fips'].astype('str', copy=True)
    todaycases['fips'] = todaycases['fips'].str.rjust(5, '0')

    return todaycases, df_case_dict, popdata

def pullpublicschool():
    '''
    Function to pull school location data. Only needs to run once
    :return:
    '''
    schoolarr = []
    school_name_arr = []
    street_addr_arr = []
    state_arr = []
    city_arr = []
    county_arr = []
    lat_arr = []
    lon_arr = []
    zip_arr = []
    fips_arr = []
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
              'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
              'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    # Need: county FIPS, latitude, longitude, school name, school id
    # schooldata = requests.get("https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/Public_School_Location_201819/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json")
    for state in states:

        schooldata = requests.get(
            "https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/Public_School_Location_201819/FeatureServer/0/query?where=STATE%20%3D%20'" + state + "'&outFields=NAME,STREET,CITY,STATE,ZIP,CNTY,NMCNTY,LAT,LON&outSR=4326&f=json")
        schools = schooldata.json()  # school data is now a dictionary

        schoollist = schools["features"]  # dictionary of all the schools

        # schoolarr = np.array(schoollist[0].keys())  # Header of array is names of the attributes

        for school in schoollist:
            attr = school["attributes"]
            school_name_arr.append(attr["NAME"])
            street_addr_arr.append(attr["STREET"])
            city_arr.append(attr["CITY"])
            county_arr.append(attr["NMCNTY"])
            fips_arr.append(attr["CNTY"])
            state_arr.append(attr["STATE"])
            zip_arr.append(attr["ZIP"])
            lat_arr.append(attr["LAT"])
            lon_arr.append(attr["LON"])

        # np.concatenate(schoolarr, school.values())  # adding the values of the school to the array

    diction = {"name": school_name_arr, "street": street_addr_arr, "city": city_arr,
               "county_name": county_arr, "fips": fips_arr, "state": state_arr, "zip": zip_arr, "lat": lat_arr,
               "lon": lon_arr}
    return json.dumps(diction)


def generateSchoolMap():
    # load data first time only
    if (not path.exists("schools.json")):
        schoollist = pullpublicschool()
        myfile = open("schools.json", "w")
        myfile.write(schoollist.decode("utf-8"))

    df = pd.read_json(open("schools.json", "r", encoding="utf8"), lines=True)

    # make the map
    fig = go.Figure(data=go.Scattergeo(
        lon=df['lon'][0],
        lat=df['lat'][0],
        text=df['name'][0],
        mode='markers',
    ))

    fig.update_layout(
        title='Public schools across America',
        geo_scope='usa',
    )

    fig.write_html("temp1.html", auto_open=True)



generateSchoolMap()
pullcovid()

covid_today, case_dict, pop = pullcovid()

response = requests.get('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json')
counties = response.json()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(covid_today)

fips = covid_today["fips"]



fig2 = px.choropleth(covid_today, geojson=counties, locations='fips', color='cases',
                           range_color=(0, 5000),
                           scope='usa',
                           color_continuous_scale = "rainbow"
                          )

# fig2 = ff.create_choropleth(
#     fips=fips, values=covid_today["cases"], scope=['CA', 'AZ', 'Nevada', 'Oregon', ' Idaho'],
#     county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
#     legend_title='Covid cases', title='Covid cases West Coast'
# )
fig2.write_html("temp2.html", auto_open=True)

