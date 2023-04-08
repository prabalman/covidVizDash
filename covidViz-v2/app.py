import dash
from dash import html, dcc, Input, Output, State, html
import dash_daq as daq
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from plotly.subplots import make_subplots
from urllib.request import urlopen
import numpy as np
import dash_bootstrap_components as dbc

# Dataframes for all data files go here
# Data for foot traffic using Safegraph Patterns
df = pd.read_csv("./data/stcombRel.csv", dtype={"REGION": str})
txp = pd.read_csv("./data/combRel.csv", dtype={"FIPS": str})
txp["FIPS"] = txp["FIPS"].str.zfill(5)

#Surprise data for choropleth
# Traffic-deaths-cases
surp1= pd.read_csv("./data/surprise-ratio_traffic_deaths-cases.csv", dtype = {"fips": str})
surp1["fips"]= surp1["fips"].str.zfill(5)
surp1.fillna(0)

# Traffic-cases
surp2= pd.read_csv("./data/surprise-traffic_cases.csv", dtype = {"fips": str})
surp2["fips"]= surp1["fips"].str.zfill(5)
surp2.fillna(0)

# POI data from SafeGraph Core Places
dfnaics = pd.read_csv("./data/naics.csv")

# NYTimes Covid Metrics
nytstate = pd.read_csv("./data/NYTSTATE.csv")
nytstate["DATE"] = pd.to_datetime(nytstate["DATE"]).dt.date

# Vaccination information from CDC
cdc = pd.read_csv("./data/stvacpopcdc.csv")

# JSON file for mapping counties on choropleths
f = open("./data/geojson-counties-fips.json")
counties = json.load(f)

# Map data
cd_cases_pop = pd.read_csv("./final-data/county-data/case-population.csv", dtype={"FIPS": str})
cd_cases_traffic = pd.read_csv("./final-data/county-data/case-traffic.csv", dtype={"FIPS": str})
cd_deaths_pop = pd.read_csv("./final-data/county-data/death-population.csv", dtype={"FIPS": str})
cd_deaths_traffic = pd.read_csv("./final-data/county-data/death-traffic.csv", dtype={"FIPS": str})
cd_traffic_pop = pd.read_csv("./final-data/county-data/traffic-population.csv", dtype={"FIPS": str})

cs_cases_pop = pd.read_csv("./final-data/county-surprise/case-population.csv", dtype={"FIPS": str})
cs_cases_traffic = pd.read_csv("./final-data/county-surprise/case-traffic.csv", dtype={"FIPS": str})
cs_deaths_pop = pd.read_csv("./final-data/county-surprise/death-population.csv", dtype={"FIPS": str})
cs_deaths_traffic = pd.read_csv("./final-data/county-surprise/death-traffic.csv", dtype={"FIPS": str})
cs_traffic_pop = pd.read_csv("./final-data/county-surprise/traffic-population.csv", dtype={"FIPS": str})

sd_cases_pop = pd.read_csv("./final-data/state-data/case-population.csv", dtype={"FIPS": str})
sd_cases_traffic = pd.read_csv("./final-data/state-data/case-traffic.csv", dtype={"FIPS": str})
sd_deaths_pop = pd.read_csv("./final-data/state-data/death-population.csv", dtype={"FIPS": str})
sd_deaths_traffic = pd.read_csv("./final-data/state-data/death-traffic.csv", dtype={"FIPS": str})
sd_traffic_pop = pd.read_csv("./final-data/state-data/traffic-population.csv", dtype={"FIPS": str})

ss_cases_pop = pd.read_csv("./final-data/state-surprise/case-population.csv", dtype={"FIPS": str})
ss_cases_traffic = pd.read_csv("./final-data/state-surprise/case-traffic.csv", dtype={"FIPS": str})
ss_deaths_pop = pd.read_csv("./final-data/state-surprise/death-population.csv", dtype={"FIPS": str})
ss_deaths_traffic = pd.read_csv("./final-data/state-surprise/death-traffic.csv", dtype={"FIPS": str})
ss_traffic_pop = pd.read_csv("./final-data/state-surprise/traffic-population.csv", dtype={"FIPS": str})

# -------------- VARIABLES -------------- #
year = ["202001","202002","202003","202004","202005","202006","202007","202008","202009","202010","202011","202012","202101","202102","202103","202104","202105","202106","202107","202108","202109","202110"]
yearInt = [202001,202002,202003,202004,202005,202006,202007,202008,202009,202010,202011,202012,202101,202102,202103,202104,202105,202106,202107,202108,202109,202110]
yearMark = {
    202001: {},
    202002: {},
    202003: {},
    202004: {},
    202005: {},
    202006: {},
    202007: {},
    202008: {},
    202009: {},
    202010: {},
    202011: {},
    202012: {},
    202101: {},
    202102: {},
    202103: {},
    202104: {},
    202105: {},
    202106: {},
    202107: {},
    202108: {},
    202109: {},
    202110: {},
}

# yearDict = [
#     {'label': "01.2020", 'value': '1'},
#     {'label': "02.2020", 'value': '2'},
#     {'label': "02.2020", 'value': '3'},
#     {'label': "02.2020", 'value': '4'},
#     {'label': "02.2020", 'value': '5'},
#     {'label': "02.2020", 'value': '6'},
#     {'label': "02.2020", 'value': '7'},
# ]

yearDict = {
    1: "01.2020",
    2: "02.2020",
    3: "03.2020",
    4: "04.2020",
    5: "05.2020",
    6: "06.2020",
    7: "07.2020",
}

west = ['04', '08', '32', '35', '49', '56', '02', '06', '15', '41', '53']
midwest = ['17', '18', '26', '39', '55', '19', '20', '27', '29', '31', '38', '46']
south = ['10', '12', '13', '24', '37', '45', '51', '54', '01', '21', '28', '47', '05', '22', '40', '48']
northeast = ['09', '23', '25', '33', '44', '50', '34', '36', '42']
# west = '04|08|32'

states = [
    {'label': 'USA', 'value': '00'},
    {'label': 'Alabama', 'value': '01'},
    {'label': 'Alaska', 'value': '02'},
    {'label': 'Arizona', 'value': '04'},
    {'label': 'Arkansas', 'value': '05'},
    {'label': 'California', 'value': '06'},
    {'label': 'Colorado', 'value': '08'},
    {'label': 'Connecticut', 'value': '09'},
    {'label': 'Delaware', 'value': '10'},
    {'label': 'Florida', 'value': '12'},
    {'label': 'Georgia', 'value': '13'},
    {'label': 'Hawaii', 'value': '15'},
    {'label': 'Idaho', 'value': '16'},
    {'label': 'Illinois', 'value': '17'},
    {'label': 'Indiana', 'value': '18'},
    {'label': 'Iowa', 'value': '19'},
    {'label': 'Kansas', 'value': '20'},
    {'label': 'Kentucky', 'value': '21'},
    {'label': 'Louisiana', 'value': '22'},
    {'label': 'Maine', 'value': '23'},
    {'label': 'Maryland', 'value': '24'},
    {'label': 'Massachusetts', 'value': '25'},
    {'label': 'Michigan', 'value': '26'},
    {'label': 'Minnesota', 'value': '27'},
    {'label': 'Mississippi', 'value': '28'},
    {'label': 'Missouri', 'value': '29'},
    {'label': 'Montana', 'value': '30'},
    {'label': 'Nebraska', 'value': '31'},
    {'label': 'Nevada', 'value': '32'},
    {'label': 'New Hampshire', 'value': '33'},
    {'label': 'New Jersey', 'value': '34'},
    {'label': 'New Mexico', 'value': '35'},
    {'label': 'New York', 'value': '36'},
    {'label': 'North Carolina', 'value': '37'},
    {'label': 'North Dakota', 'value': '38'},
    {'label': 'Ohio', 'value': '39'},
    {'label': 'Oklahoma', 'value': '40'},
    {'label': 'Oregon', 'value': '41'},
    {'label': 'Pennsylvania', 'value': '42'},
    {'label': 'Rhode Island', 'value': '44'},
    {'label': 'South Carolina', 'value': '45'},
    {'label': 'South Dakota', 'value': '46'},
    {'label': 'Tennessee', 'value': '47'},
    {'label': 'Texas', 'value': '48'},
    {'label': 'Utah', 'value': '49'},
    {'label': 'Vermont', 'value': '50'},
    {'label': 'Virginia', 'value': '51'},
    {'label': 'Washington', 'value': '53'},
    {'label': 'West Virginia', 'value': '54'},
    {'label': 'Wisconsin', 'value': '55'},
    {'label': 'Wyoming', 'value': '56'},
    # {'label': 'West', 'value': west},
    # {'label': 'Midwest', 'value': midwest},
    # {'label': 'Northeast', 'value': northeast},
    # {'label': 'South', 'value': south},
]

models = [
    {'label': "Case vs. population", "value": "cases_pop"},
    {'label': "Case vs. traffic", 'value': "cases_traffic"},
    {'label': "Death vs. population", 'value': "deaths_pop"},
    {'label': "Death vs. traffic", 'value': "deaths_traffic"},
    {'label': "Traffic vs. population", 'value': "traffic_pop"},
]

# models = {
    # 1: {"label": "Case vs. population"},
    # 2: {"label": "Case vs. traffic"},
    # 3: {"label": "Death vs. population"},
    # 4: {"label": "Death vs. traffic"},
    # 5: {"label": "Traffic vs. population"}
# }
colors = ["#ffffff", "#e5e5ff", "#7f7fff", "#0000ff", "#000019"]
dfnaics["text"] = dfnaics["state"] + " has " + (dfnaics["naicscnt"]).astype(str)+" POIs"
limits = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 53)]
scale = 1000
external_scripts = ["https://d3js.org/d3.v7.min.js"]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
appTitle = "Bayesian surprise during Covid-19"
description = "The primary purpose of visualization is the discovery of new information and patterns. As our aim is to coalesce data points from different domains and infer correlation through patterns that arise from the data, we try to depict bulk information in a presentable and coherent manner. Being able to visualize multiple sources of data in aggregation opens new doorways to stack information to derive new knowledge from independent datasets. A major aim we have is to integrate features from multiple visualization techniques such as state and county-level choropleths, bubble charts and offer Bayesian Surprise using different combinations of these data points.  We also add conventional statistical charts with added interactivity and custom functionality to produce more effective Time-Series visualization."
colorScales = px.colors.named_colorscales()
defaultColor = [{"value": "YlOrRd", "label": "Default color"}]
all_states = ss_cases_pop.STATENM.unique()
# stateDropdown = dcc.Dropdown(
#     id='stateDropdown',
#     options=defaultState + [x for x in all_states],
#     value=['USA'],
#     searchable=True)
# stateDropdown = dcc.Dropdown(
#     id='stateDropdown',
#     options=[x for x in states],
#     value='01',
#     searchable=True)
selectionStates = dcc.Dropdown(
    id='stateSelection',
    options=[{'label': x, 'value': x} for x in all_states],
    value=['Ohio', 'Virginia', 'New York', 'Alaska'],
    multi=True,
    searchable=True)
radioAbsRel = dcc.Dropdown(
    id='abs-rel-picker',
    options=[{'label': 'Abs-FootTraffic', 'value': 'Abs'}, {'label': 'Rel-FootTraffic', 'value': 'Rel'}],
    value='Abs',
    searchable=False)
radioNaics = dcc.Dropdown(
    id='abs-rel-naics',
    options=[{'label': 'Abs-POI', 'value': '2'}, {'label': 'Rel-POI', 'value': '1'}, {'label': 'Hide-POI', 'value': '0'}],
    searchable=False,
    value='0')
about = html.Div(id="about", children=[
    html.P("Data Sources:"),    
    html.P("Safe Graph, NYTimes, CDC, Data World"),
    html.P("Data Disclaimer:"),    
    html.P("Governments often revise data or report a single-day large increase in cases or deaths from unspecified days without historical revisions, which can cause an irregular pattern in the daily reported figures. The Times is excluding these anomalies from seven-day averages when possible. For agencies that do not report data every day, variation in the schedule on which cases or deaths are reported, such as around holidays, can also cause an irregular pattern in averages. The Times uses an adjustment method to vary the number of days included in an average to remove these irregularities."),
])

slider_year = dcc.Slider(1, 26, id="sliderYear",
    marks={
        1: "20' Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
        13: "21' Jan",
        14: "Feb",
        15: "Mar",
        16: "Apr",
        17: "May",
        18: "Jun",
        19: "Jul",
        20: "Aug",
        21: "Sep",
        22: "Oct",
        23: "Nov",
        24: "Dec",
        25: "22' Jan",
        26: "Feb",
    },
    value=13,
    step=None,
)

# -------------- LAYOUT -------------- #
app.title = "CoViz19"
app.layout = html.Div(
    [
        html.Header(appTitle, id="title"),
        html.Main(
           [
                # html.Nav(description, id="description"),
                html.Article(
                    [
                        html.Div(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5("Filters", className="card-title"),
                                        html.Div([
                                            "Select a colormap",
                                            dcc.Dropdown(
                                                id='colorscale',
                                                options=defaultColor+[{"value": x, "label": x} for x in colorScales],
                                                value="YlOrRd",
                                                searchable=True
                                            )
                                        ]),
                                        html.Div([
                                            "Select a state",
                                            dcc.Dropdown(
                                                id='statesDropdown',
                                                options=[x for x in states],
                                                value='00',
                                                searchable=True
                                            )
                                        ]),
                                        html.Div([
                                            "Select a model",
                                            dcc.Dropdown(
                                                id='surpriseDropdown',
                                                options=[x for x in models],
                                                value="cases_pop"
                                            )
                                        ]),
                                    ]
                                ),
                            ),
                            className="settings"
                        ),
                        slider_year,
                        html.Div(className="maps", children=[
                            dcc.Graph(id="map_original", className="map"),
                            dcc.Graph(id="map_surprise", className="map"),
                        ]),
                        # selectionStates,
                        # html.Div(id="lineCharts", children=[
                        #     dcc.Graph(id="line-chart-case", className="lineChart"),
                        #     dcc.Graph(id="line-chart-death", className="lineChart"),
                        #     dcc.Graph(id="line-chart-vac", className="lineChart")
                        # ], className="settings")
                    ]
                ),
           ]
        ),
    ],
    className="wrapper"

    # children=[
    #     html.Div(children=intro),
    #
    #     # html.Div(children=accordion),
    #     # html.Div(id="headerContainer", children=appTitle),
    #     # html.Div(className="container", children=menu),
    #     html.Div(children=[maps, lineCharts, buttonsYear]),
    #     html.Div(children=[about])
    # ]
)

# lineChartCase, lineChartDeath, lineChartVaccine


# -------------- APP -------------- #

@app.callback([
    Output("map_original", "figure"),
    Output("map_surprise", "figure")],
    [Input("sliderYear", "value"),
     Input("colorscale", "value"),
     Input("statesDropdown", "value"),
     Input("surpriseDropdown", "value")]
)

def display_choropleth(year, scale, state, surpriseModel):
    year = str(year)

    if state == "00":
        if surpriseModel == "cases_pop":
            sub_map1 = sd_cases_pop['STATENM']
            sub_map2 = ss_cases_pop['STATENM']
            sub_map1_z = sd_cases_pop
            sub_map2_z = ss_cases_pop

        elif surpriseModel == "cases_traffic":
            sub_map1 = sd_cases_traffic['STATENM']
            sub_map2 = ss_cases_traffic['STATENM']
            sub_map1_z = sd_cases_traffic
            sub_map2_z = ss_cases_traffic

        elif surpriseModel == "deaths_pop":
            sub_map1 = sd_deaths_pop['STATENM']
            sub_map2 = ss_deaths_pop['STATENM']
            sub_map1_z = sd_deaths_pop
            sub_map2_z = ss_deaths_pop

        elif surpriseModel == "deaths_traffic":
            sub_map1 = sd_deaths_traffic['STATENM']
            sub_map2 = ss_deaths_traffic['STATENM']
            sub_map1_z = sd_deaths_traffic
            sub_map2_z = ss_deaths_traffic

        elif surpriseModel == "traffic_pop":
            sub_map1 = sd_traffic_pop['STATENM']
            sub_map2 = ss_traffic_pop['STATENM']
            sub_map1_z = sd_traffic_pop
            sub_map2_z = ss_traffic_pop

        map1 = go.Figure(
            data=go.Choropleth(
                locations=sub_map1,
                colorscale=scale,
                autocolorscale=False,
                z=sub_map1_z[year],
                locationmode="USA-states",
                marker_line_color="white",
                # colorbar_title=year,
                colorbar=dict(orientation='h', thickness=10, y=-0.4),
            )
        )

        map1.update_layout(
            title_text="ORIGINAL MAP: " + (surpriseModel),
            height=400,
            geo=dict(
                scope="usa",
                projection=go.layout.geo.Projection(type="albers usa"),
                showlakes=False,
                lakecolor="rgb(255, 255, 255)"
            ),
            legend_x=-0.1,
            legend_y=0
        )

        map2 = go.Figure(
            data=go.Choropleth(
                locations=sub_map2,
                colorscale=scale,
                autocolorscale=False,
                # z=np.log(sub_map2_z[year]),
                z=sub_map2_z[year],
                locationmode="USA-states",
                marker_line_color="white",
                # colorbar_title=year,
                colorbar=dict(orientation='h', thickness=10, y=-0.4),
            )
        )

        map2.update_layout(
            title_text="SURPRISE MAP: " + (surpriseModel),
            height=400,
            geo=dict(
                scope="usa",
                projection=go.layout.geo.Projection(type="albers usa"),
                showlakes=False,
                lakecolor="rgb(255, 255, 255)",
            ),
            legend_x=-0.1,
            legend_y=0
        )

        return map1, map2

    else:
        if surpriseModel == "cases_pop":
            sub_map3 = cd_cases_pop[cd_cases_pop['FIPS'].str[:2].str.contains(state)]
            sub_map4 = cs_cases_pop[cs_cases_pop['FIPS'].str[:2].str.contains(state)]
        elif surpriseModel == "cases_traffic":
            sub_map3 = cd_cases_traffic[cd_cases_traffic['FIPS'].str[:2].str.contains(state)]
            sub_map4 = cs_cases_traffic[cs_cases_traffic['FIPS'].str[:2].str.contains(state)]
        elif surpriseModel == "deaths_pop":
            sub_map3 = cd_deaths_pop[cd_deaths_pop['FIPS'].str[:2].str.contains(state)]
            sub_map4 = cs_deaths_pop[cs_deaths_pop['FIPS'].str[:2].str.contains(state)]
        elif surpriseModel == "deaths_traffic":
            sub_map3 = cd_deaths_traffic[cd_deaths_traffic['FIPS'].str[:2].str.contains(state)]
            sub_map4 = cs_deaths_traffic[cs_deaths_traffic['FIPS'].str[:2].str.contains(state)]
        elif surpriseModel == "traffic_pop":
            sub_map3 = cd_traffic_pop[cd_traffic_pop['FIPS'].str[:2].str.contains(state)]
            sub_map4 = cs_traffic_pop[cs_traffic_pop['FIPS'].str[:2].str.contains(state)]

        map3 = px.choropleth(
            sub_map3,
            geojson=counties,
            locations='FIPS',
            color=year,
            color_continuous_scale=scale,
            scope="usa",
            hover_name='FIPS',
            labels={'FIPS': 'Fips'},
            title="ORIGINAL MAP: " + (surpriseModel),
            fitbounds='locations',
        )

        map3.update_coloraxes(
            colorbar=dict(orientation='h', thickness=10, y=-0.4),
        )

        map4 = px.choropleth(
            sub_map4,
            geojson=counties,
            locations='FIPS',
            color=year,
            color_continuous_scale=scale,
            scope="usa",
            hover_name='FIPS',
            labels={'FIPS': 'Fips'},
            title="SURPRISE MAP: " + (surpriseModel),
            fitbounds='locations',
        )

        map4.update_coloraxes(
            colorbar_title=year,
            colorbar=dict(orientation='h', thickness=10, y=-0.4),
        )

        return map3, map4

# @app.callback(
#     [Output("line-chart-case", "figure"),
#      Output("line-chart-death", "figure"),
#      Output("line-chart-vac", "figure")],
#     [Input("stateSelection", "value")]
# )
#
# def update_line_chart(STATES):
#     mask = nytstate.STATE.isin(STATES)
#     maskCDC = cdc.STATE.isin(STATES)
#     line1 = px.line(nytstate[mask], x="DATE", y="CASES", color="STATE", title="COVID-19 CASE COUNT BY STATES")
#     line2 = px.line(nytstate[mask], x="DATE", y="DEATHS", color="STATE", title="COVID-19 DEATH COUNT BY STATES")
#     line3 = px.line(cdc[maskCDC], x="DATE", y="VACPOPN", color="STATE", title="COVID-19 VACCINATION-RATE BY STATES")
#
#     return line1, line2, line3

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True) # , port = 80