## Functions to get COVID/population/school data from the web
import plotly.express as px

import numpy as np
import requests
import plotly.express as px
import pandas as pd
import json

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
        fips = attr["CNTY"]
        state = attr["STATE"]
        zip_code = attr["ZIP"]
        lat = attr["LAT"]
        lon = attr["LON"]
        select_school_data = {'name':school_name, 'addr':street_addr, 'city':city, \
                    'country':county, 'state':state, 'zip':zip_code, 'lat':lat, 'lon':lon, 'fips':fips}
        schoolarr.append(select_school_data)
        #np.concatenate(schoolarr, school.values())  # adding the values of the school to the array

    return json.dumps(schoolarr)

schoollist = pullpublicschool()
myfile = open("schools.json", "w")
myfile.write(schoollist)
## THIS LINE DON"T WORKgit add -
# df = pd.read_json("/Users/ChaseBusacker/Documents/Git/Pearc20VizPipeline/schools.json")
# fips = df["fips"]

# fig = e.create_choropleth(
#     fips=fips, 
#     plot_bgcolor='rgb(229,229,229)',
#     paper_bgcolor='rgb(229,229,229)',
#     legend_title='Population by County',
#     county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
#     exponent_format=True,
# )
# fig.show()

# fips = []
# values = []
# for s in schoollist:
#     pass

# fig = e.create_choropleth(
#     fips=fips, values=values, scope=['Florida'], show_state_data=True,
#     colorscale=colorscale, binning_endpoints=endpts, round_legend_values=True,
#     plot_bgcolor='rgb(229,229,229)',
#     paper_bgcolor='rgb(229,229,229)',
#     legend_title='Population by County',
#     county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
#     exponent_format=True,
# )
# fig.show()