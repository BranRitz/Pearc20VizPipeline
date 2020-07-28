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
    Function to pull school location data. Only needs to run once
    :return:
    '''

    # Need: county FIPS, latitude, longitude, school name, school id
    schooldata = requests.get("https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/Public_School_Location_201819/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json")
    schools = schooldata.json()     # school data is now a dictionary

    schoollist = schools["features"]   # dictionary of all the schools
   
    # schoolarr = np.array(schoollist[0].keys())  # Header of array is names of the attributes
    schoolarr = []
    for school in schoollist:
        attr = school["attributes"]
        school_name = attr["NAME"]
        street_addr = attr["STREET"]
        city = attr["CITY"]
        county = attr["NMCNTY"]
        state = attr["STATE"]
        zip_code = attr["ZIP"]
        lat = attr["LAT"]
        lon = attr["LON"]
        select_school_data = [school_name, street_addr, city, county, state, zip_code, lat, lon]
        schoolarr.append(select_school_data)
        print(select_school_data) 
        #np.concatenate(schoolarr, school.values())  # adding the values of the school to the array

    return schoolarr
pullpublicschool()