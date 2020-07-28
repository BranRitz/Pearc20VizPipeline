## Functions to get COVID/population/school data from the web

import numpy
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

    # Need: county FIPS, latitude, longitude, school name, school id
    covidpop = requests.get("https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/Public_School_Location_201819/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json")
    covidpop.json()


def pullpublicschool():
    '''
    Function to pull school location data. Only needs to run once (how often do new schools get added?)
    :return:
    '''