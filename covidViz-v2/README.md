# coViz19 Documentation
## A Visualization tool to understand the correlation between foot-traffic, COVID-19 metrics and Vaccination information in the US. 
> A project by Ryan Jeon and Prabal Man Dhaubhadel  

## Installation Instructions        
### Project Download

To download the project, either extract the zip file or on a terminal/command prompt,    
```
git clone https://github.com/prabalman/covidViz/
```
Change directory to the root folder using
```
cd covidViz
```  
### Environment Setup
Create a virtual environment using  
```
python -m venv venv
```

* UNIX/Mac : source venv/bin/activate  
* Windows: \venv\scripts\activate

Install all dependencies using 
```
pip install -r requirements.txt
```
### Execution  
Now, from the root folder, start the app using 
```
python app.py
```

By default, the app must launch in http://localhost:8050/  


## About the Dashboard  
### Overview  
The CoViz19 dashboard was created in the Fall of 2021 with the goal of assimilating various datasets that were released following the COVID-19 pandemic. With the goal of providing meaningful information and interaction to the user on datapoints that previously existed in separate domains. The data cornerstones for the project are Foot Traffic data by SafeGraph along with POI information, Time series information of COVID-19 metrics such as cases and deaths by NYTimes, Vaccination information in time-series format provided by the CDC. Additionally, data.world info for several crosswalks for linking data at different depths - state and county level and different labels - state code vs state name, state || county vs FIPS were used. 

### Idioms
The dashboard currently features four idioms - choropleth maps, bubble maps, line charts and pie charts.  
* **Choropleth Maps:**   Choropleth maps are widely used in the visualization of spatial data. In our context, the SafeGraph data for foot traffic during the duration of the COVID-19 pandemic has been placed on the US map at both county and state levels. The change in scope helps to vizualize hot spots and get overview of the data respectively.  
* **Bubble Maps:**  As foot traffic is closely related to POI (Points of Interest), a bubble map provides a good overview of the likelihood of people to travel to certain destinations in certain states. Overlaying this on a map helps to draw correlation with foot traffic.  
* **Line Charts:**  Strongly akin to time-series information, we used the line chart to visualize time-series data for COVID metrics as well as vaccination information. This is the simplest and most useful way to visualize the trend of a particular metric in the time domain.  
* **Pie Charts:**  We use pie charts to contextualize the portion of the population vaccinated in the world vs the US. As a leading nation in vaccine research even based on the most recent data where vaccine availability has been very wide spread, the US still edges out vs the rest of the world in terms of the number of people vaccinated.  

### Interactions  
The dashboards aims to unify all choropleths using a common **timeframe selector** . Basic interactions such as **hover**  or tooltips, **scroll** for zoom, a **state-selector** using checkboxes have been maintained. **Chart-cropping** is useful for line charts that allow zooming into specific portions of the graph. **Colormaps** and **scaling** methods have been carefully chosen to best display the available data.  
  
### Data Sources 
Here are some details about the raw data used for this project:  
* **SafeGraph:** We used the proprietary **Patterns** dataset for county-level monthly foot traffic information from [SafeGraph] (https://www.safegraph.com/) using academic access. We also used the **Core Places** dataset for generating the number of POIs available with their respective NAICS code. The raw data was over 150GB.  
* **NY Times:**  The raw data provided by [NYTimes] (https://github.com/nytimes/covid-19-data) is one of the most reliable and widely used time-series information on the COVID-19 pandemic. Available in public domain, the data is under 100 MBs in CSV format 
* **CDC:** The Centers for Disease Control and Prevention (CDC) dataset available [here](https://cdc-vaccination-history.datasette.io/) has been used for tabulating vaccination information. The dataset is about 150 MBs. 
* **Crosswalks:** Various lookup tables and crosswalks for manipulating, cross-linking and aggregating different datasets were used from their [domain](https://data.world/). Eg. FIPS to ZIP. Census data was also gathered for data normalization. 
   
### Data Pipeline  
All the data used was initially acquired in CSV format. It was dumped into a MySQL server as the central repository. Python pandas was used to handle data format issues such as null values. After file was loaded into a MySQL database, datatype manipulations and aggregations were performed. FIPS was the common column for all county level data and state code was the linking field for all state level data. Monthly groupings were performed wherever necessary. After subsequent filtering and grouping, only the data for display was exported into CSVs and called by the app directly. This was intentionally done to reduce server load and query time. The data spans across 2020 and 2021 with exceptions where data was not available or the date wasn't reached (as of Nov, 2021). 

### Source Code
The application is built on the Dash framework for Python which heavily relies on PlotlyJS under the hood for generating graphs. Several dependencies need to be met for the successful execution of this. The requirements.txt file has all packages listed. This has been explained in detail in the Environment Setup section of this Readme.  
The file structure of the repository has been outlined below
```
covidViz
│   README.md
│   app.py   
│   requirements.txt   
│
└───data
│   │   <CSV Files>
│   
└───assets
    │   <icon and CSS>

```
### Screenshots  

Screenshots from the applications have been attached for reference.   
Overview of the visualization system: Animated choropleth maps for understanding foot traffic trend in the United States.    
![Overview of the visualization system](/screenshots/timeslider.PNG) 
Absolute vs Relative data. Data can tell a very different story if it is not normalized.    
![Absolute vs Relative data](/screenshots/AbsoluteVsRelative2.PNG)  
Bubble Map showing POIs on the US Map. An attempt to draw correlation between foot traffic and POIs.    
![Bubble Map showing POIs on the US Map](/screenshots/bubbleMap.PNG)  
Tool tip interaction. Tooltips give users additional information. Tooltips, however, are supplementary.     
![Tool tip interaction](/screenshots/bubbleMapToolTip.PNG)  
Timeline cropping on line charts. This allows users to focus on a specific portion of the map and drill down into individual cases.     
![Timeline cropping on line charts](/screenshots/timelineCropping2.png) 
Pie chart of vaccination completion. A simple representation of a part as a whole concept showing the portion of population unvaccinated yet.       
![Pie chart of vaccination completion ](/screenshots/VaccinationPie.PNG) 
