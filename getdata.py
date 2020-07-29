## Functions to get COVID/population/school data from the web
import plotly.graph_objects as go

import numpy as np
import requests
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import json
from io import open

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
    covidcases = np.genfromtxt('./covid_us_county.csv', delimiter=',')
    popdata = np.genfromtxt('./us_county.csv', delimiter=',')
    popdata = popdata[popdata[:,0].argsort()]

    # delete nan
    # TODO: add code to delete nan and get most recent covid cases
    n = popdata.shape(0)-1
    while popdata[n][0].isNaN():    # delete all the FIPS-less data by iterating from the bottom to the top
        popdata = np.delete(popdata, (n), axis=0)
        n = n-1


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
    school_name_arr = []
    street_addr_arr = []
    state_arr = []
    city_arr = []
    county_arr = []
    lat_arr = []
    lon_arr = []
    zip_arr = []
    fips_arr = []
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
        
        #np.concatenate(schoolarr, school.values())  # adding the values of the school to the array

    diction = {"name": school_name_arr, "street": street_addr_arr, "city": city_arr, 
        "county_name": county_arr, "fips": fips_arr, "state":state_arr, "zip": zip_arr, "lat": lat_arr, "lon": lon_arr}
    return json.dumps(diction)

schoollist = pullpublicschool()
myfile = open("schools.json", "w")
myfile.write(schoollist.decode("utf-8"))
## THIS LINE DON"T WORK
df = pd.read_json(open("schools.json", "r"),lines=True)
fips = df[u'fips'][0]
values = range(len(fips))

fig = ff.create_choropleth(fips=fips, values=values)
fig.layout.template = None
fig.show()
# fig = go.Figure()
# for i in range(len(df[u'fips'][0])):
#     print (df[u'fips'][0][i])
#      fig.add_trace(go.Scattergeo(
#          locationmode = 'USA-states',
#          lon = df[u"lon"][0][i],
#         lat = df["data"]['lat'][i],
#         text = df["data"]['name'][i],
#         marker = dict(
#             size = 1,
#             color = "black",
#             line_color='rgb(40,40,40)',
#             line_width=0.5,
#             sizemode = 'area'
#         ),
#         name = df["data"]["name"][i]))

fig.show()

# fips = []
# values = []
# for s in schoollist:
#     pass

# fig = px.create_choropleth(
#     fips=fips, values=values, scope=['Florida'], show_state_data=True,
#     colorscale=colorscale, binning_endpoints=endpts, round_legend_values=True,
#     plot_bgcolor='rgb(229,229,229)',
#     paper_bgcolor='rgb(229,229,229)',
#     legend_title='Population by County',
#     county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
#     exponent_format=True,
# )
# fig.show()

pullcovid()

