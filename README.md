# Pearc2020 - VizPipeline1
# Helping parents protect their children from COVID-19

> This project was written for a Hackathon hosted by Science Gateways Community Institute to show parents the correlation between public schools and covid cases.


We used APIs to get data from the schools and from the covid reporting. The following APIs were used:<br>
kaggle <br>
arcgis.com

And the code uses plotly, dash, pandas to create a webpage that shows the following graphs:
<img src="https://raw.githubusercontent.com/BranRitz/Pearc20VizPipeline/master/schools.png" alt="Schools">
<img src="https://raw.githubusercontent.com/BranRitz/Pearc20VizPipeline/master/covidcases.png" alt="Covid Cases by county">


A slider was also implemented to look back in time at cases for each county in the past up to 30 days.

# How to see it work
1. Either fork or clone this repo to your own machine
2. Install Pip for python
3. In a terminal/command line, run the following scripts: <br>
    "pip install json" <br>
    "pip install datetime" <br>
    "pip install request"<br>
    "pip install dash==1.14.0"<br>
    "pip install plotly==4.9.0"<br>
    "pip install kaggle"<br>


