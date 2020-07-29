## Functions to get COVID/population/school data from the web
import plotly.graph_objects as go
import dash
import numpy as np
import requests
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
import pandas as pd
import json
from io import open
from os import path
from datetime import datetime, timedelta

import os
from zipfile import ZipFile
app = dash.Dash(__name__)

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

    date = datetime.date(datetime.now() - timedelta(days=2))  # get today's date

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

def pullpublicschool(covid):
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
    schooldata = requests.get("https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/Public_School_Location_201819/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json")
    for state in states:

        schooldata = requests.get(
            "https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/Public_School_Location_201819/FeatureServer/0/query?where=STATE%20%3D%20'" + state + "'&outFields=NAME,STREET,CITY,STATE,ZIP,CNTY,NMCNTY,LAT,LON&outSR=4326&f=json")
        schools = schooldata.json()  # school data is now a dictionary

        schoollist = schools["features"]  # dictionary of all the schools

        # schoolarr = np.array(schoollist[0].keys())  # Header of array is names of the attributes

        for school in schoollist:
            attr = school["attributes"]
            fips = str(attr["CNTY"])
            query = "fips =='"+attr["CNTY"]+"'"
            name = str(attr["NAME"])
           # print(str(covid.query(query)["cases"].values[0]))
            text = name + "<br>Cases in county: " + str(covid.query(query)["cases"].values[0])
            school_name_arr.append(text)
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


def generateSchoolMap(covid):
    # load data first time only
    if (not path.exists("schools.json")):
        schoollist = pullpublicschool(covid)
        myfile = open("schools.json", "w")
        myfile.write(schoollist)

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

    #fig.write_html("temp1.html", auto_open=True)

    return fig

covid_today, case_dict, pop = pullcovid()
fig = generateSchoolMap(covid_today)

response = requests.get('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json')
counties = response.json()

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
#fig2.write_html("temp2.html", auto_open=True)


def layout_for_site(fig1, fig2):
    app.title = "Covid Data"

    app.layout = html.Div(children=[
        html.Div([

            html.H1("Public Schools K-12"),
            dcc.Graph(
                id="current-graph2",
                figure=fig1),
        ]),


            html.Div([
                html.Div([
                    html.Span('Select Date:'),
                ], className='Grid-cell',
                ),
                dcc.Slider(
                    id='case_slider',
                    min=1,
                    max=30,
                    step=1,
                    value=30
                ),
            ], className='Grid-cell',
            ),
            html.Div([
                html.H1("Covid Cases per County"),
                dcc.Graph(
                    id="current-graph",
                    figure=fig2),
            ]),
    ])


    @app.callback(
        dash.dependencies.Output('current-graph', 'figure'),
        [dash.dependencies.Input('case_slider','value')])
    def update_output(value):
        # Update fig2
        currtime = timedelta(days=30-value)
        print(currtime)
        today = datetime.date(datetime.today())-timedelta(days=1)
        print(today)
        #todaycases = case_dict["date" == str(today-currtime)]
        print(case_dict)
        var = None
        for case,df in case_dict.items():
            print(case)
            if case == str(today-currtime):
                var = df

        fig2 = px.choropleth(var, geojson=counties, locations='fips', color='cases',
                             range_color=(0, 5000),
                             scope='usa',
                             color_continuous_scale="rainbow"
                             )
        return fig2



layout_for_site(fig, fig2)
# @app.callback(
#     dash.dependencies.Output('current-graph', 'figure'),
#     [dash.dependencies.Input('ngram-dropdown', 'value'),
#     dash.dependencies.Input('date-slider', 'value')]
# )
# def update_output(ngram, date_index):
#     pass


if __name__ == '__main__':
    app.run_server(debug=True)