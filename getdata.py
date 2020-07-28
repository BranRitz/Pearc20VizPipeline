## Functions to get COVID/population/school data from the web

import numpy as np
import requests

def refreshdata():
    '''
    Function to update the data periodically.
    :return:
    '''

def pullcovid():
    '''
    Function to pull COVID/population data once. Needs to run every time data is updated.
    :return:
    '''

def pullpublicschool():
    '''
    Function to pull school location data. Only needs to run once (how often do new schools get added?)
    :return:
    '''
    # Need: county FIPS, latitude, longitude, school name, school id
    schooldata = requests.get("https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/Public_School_Location_201819/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json")
    schooldata.json()     # school data is now a dictionary
    schoollist = schooldata["fields"]   # dictionary of all the schools

    print(schoollist)

    for school in schoollist:
        
