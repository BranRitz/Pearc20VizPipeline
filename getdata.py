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
    todaycases = covidcases[covidcases["date"] > "2020-07-26"]

    return todaycases, popdata

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
        myfile.write(schoollist)

    df = pd.read_json(open("schools.json", "r"), lines=True)

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

    fig.show()


generateSchoolMap()
pullcovid()

