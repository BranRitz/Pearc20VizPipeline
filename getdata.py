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
    Get data with Kaggle API
    :return:
    '''


def pullpublicschool():
    '''
    Function to pull school location data. Only needs to run once
    :return:
    '''

    # Need: county FIPS, latitude, longitude, school name, school id
    schooldata = requests.get("https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/Public_School_Location_201819/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json")
    schooldata.json()     # school data is now a dictionary
    schoollist = schooldata["features"]   # dictionary of all the schools

    schoolarr = np.array(schoollist[1].keys())  # Header of array is names of the attributes

    for school in schoollist:
        np.concatenate(schoolarr, school.values())  # adding the values of the school to the array
