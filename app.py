# importing all the required libraries
import dash
from dash import dcc
from dash import html
import pandas as pd
import time
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dayGetter import get_day

# Setting the template for the graph to a pre-defined plotly theme.
pio.templates.default = 'plotly'

# Starting the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Title for the website.
app.title = "TraffikTrak"

bestTime = ""
bestDay = ""
currentCount = ""

# Reading data from Google Sheets using Pandas through URLs as CSV files and storing as data frames.

#DONE
building_1_Current = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1REqhOuo6PhOqWs4qzfPx-gxJxJ0Fo6pL-rTVRFJT2-g/export?gid=667215098&format=csv", index_col=None)

#===============================

#DONE
building_1_Previous = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1TI1BKUzVo8runnVTvOg_ttk1WLl_PZElSQWET47ZNt8/export?gid=1822509596&format=csv",  index_col=None)

    #========================#

    #DONE
building_2_Current = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1h6bhhrMoAH87XcDubpT3aDHZ15rMQtV7Mde9HpnlpIw/export?gid=1935197477&format=csv", index_col=None)
#=================
    #DONE
building_2_Previous = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1FnH-qETthx7KswRv5SzahfZBmzHu4S54rIwZ3pU5DwM/export?gid=1967637644&format=csv", index_col=None)
#====================

#DONE 
building_3_Previous = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/12g8vo8p1YrxhCvd_HHbXQyzzNSEdhZFsUH5pGgowpB0/export?gid=579500192&format=csv", index_col=None)
#===============
    
#DONE
building_3_Current = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1eb3U8CfhFE5Iwh_Oq35OsJFqOOGuysOmLKrcB8TQK64/export?gid=112750822&format=csv", index_col=None)
#============

#DONE
week1 = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1rry9FKiQjwThEt9k-i2Z51IJmT-Gx-98Xc2iLqk2j8I/export?format=csv", index_col=None)
#=============

# Approximate areas of buildings obtained through Google Maps measuring app.

building_1_Area = 14519
building_2_Area = 13576
building_3_Area = 6028

# Using dayGetter.py to obtain the day of the week.
day = get_day()[0]

daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# This is where the HTML5 is incorporated through the .layout backbone of plotly.
app.layout = html.Div(
    children=[
        html.Div([
            # Logo and title.
            html.Div(id="title"),
            html.Img(src="assets/TraffikTrak_Logo.png",
                     height="120", width="170"),
            html.H1("TraffikTrak")

        ]),
        #Introductory message.
        html.H4("""                -Simple and catchy, focusing on tracking crowd.-""",
                    title='Introduction to TraffikTrak',
                className='text_area'),

        html.Div(children=[
            html.Div([

                # Dropdown to select from the establishment that user would like to view data for.
                dcc.Dropdown(
                    id="buildingSelector",
                    options=[
                        {"label": "Building 2", "value": "Building 2"},
                        {"label": "Building 1",
                            "value": "Building 1"},
                        {"label": "Building 3", "value": "Building 3"}
                    ],
                    placeholder="Select a Building",
                    clearable=False,
                    className='dropdown',
                    searchable=False,
                    # Default selected establishment in this code is YMCA-Shawnessy (customizable).
                    value = "Building 1"
                ),

                # Dropdown to select the day of the week as another required filter.
                dcc.Dropdown(
                    # id that will link dropdown menu to input for callbacks.
                    id="daySelector",  
                    # Creating labels and values for the labels that are linked to the csv file.
                    options=[  
                        {"label": "Saturday", "value": "Saturday"},
                        {"label": "Sunday", "value": "Sunday"},
                        {"label": "Monday", "value": "Monday"},
                        {"label": "Tuesday", "value": "Tuesday"},
                        {"label": "Wednesday", "value": "Wednesday"},
                        {"label": "Thursday", "value": "Thursday"},
                        {"label": "Friday", "value": "Friday"}
                    ],
                    # Enables multiple graphs to be displayed and overlayed for better comparison.
                    multi=True,
                    # Default value is set to the current day of the week.
                    value=day,  
                    placeholder="Select a Day",
                    searchable=False,
                    clearable=True,
                    className='dropdown',
                ),

                # Slider for selecting which week's information is to be viewed. For demo purposes, both weeks are pre-filled,
                # however upon deployment, the weekly information will be filled as time progresses.
                dcc.Slider(id="weekGetter",
                           min=1,
                           max=2,
                           # Default value is set to display previous week information.
                           value=1,
                           marks={
                               1: {'label': 'Previous Week', 'style': {'color': 'black'}},
                               2: {'label': 'Current Week', 'style': {'color': 'black'}},
                           },
                           className='slider',
                           )
            ], className="left_side"),

            # Div element for the graph. The id is used as output in the callback according to the filters selected.
            html.Div([
                dcc.Graph(id='ourGraph'),  
            ], className="right_side"),
        ], className="side_by_side"),

        # The div element which contains the general information displayed based on the filters selected
        html.Div(children = [
        html.Div([
            html.P(id="generalInfo", children=True),
        ], className = 'left_side2'),
        html.Div([
            html.H4('Select a range below using the slider to determine the day which has the least traffic in the specified time:', className = 'selectRangeText'),
            html.Div([
            html.H5('From:', title='Range (From)', className='from'),
            html.H5('To:', title='Range (To)', className='to'),
            ], className = 'FromToTitle'),
            dcc.RangeSlider(
            min = 6,
            max = 23,
            value=[6, 23],
            id = "predictiveDay",
            marks={
                6: {'label': '6:00',},
                7: {'label': '7:00',},
                8: {'label': '8:00',},
                9: {'label': '9:00',},
                10: {'label': '10:00',},
                11: {'label': '11:00',},
                12: {'label': '12:00',},
                13: {'label': '13:00',},
                14: {'label': '14:00',},
                15: {'label': '15:00',},
                16: {'label': '16:00',},
                17: {'label': '17:00',},
                18: {'label': '18:00',},
                19: {'label': '19:00',},
                20: {'label': '20:00',},
                21: {'label': '21:00',},
                22: {'label': '22:00',},
                23: {'label': '23:00',},
                },
            ),
            html.P(id = 'predictBestDay', children = True)
        ], className = "right_side2"),
        ], className = 'side_by_side2'),

    ],
    # Added styling to be able to display side by side for a better user experience.
    id="mainContainer", style={"display": "flex", "flex-direction": "column"})

# First callback. This is to display the graph based on the inputs selected.
@app.callback(
    Output('ourGraph', 'figure'),  
    Input('daySelector', 'value'),
    Input('weekGetter', 'value'),
    Input('buildingSelector', 'value')
)
def update_graph(day, week, building):
    # Changing the CSV based on the building selected.
    sheetToReadFrom_Previous = building_1_Previous
    sheetToReadFrom_Current = building_1_Current
    if building == "Building 2":
        sheetToReadFrom_Previous = building_2_Previous
        sheetToReadFrom_Current = building_2_Current
    elif building == "Building 3":
        sheetToReadFrom_Previous = building_3_Previous
        sheetToReadFrom_Current = building_3_Current

    # If nothing is selected, don't display anything.
    if len(day) == 0:
        day = "None"

    # X-axis of graph is Time of Day from csv file, and the y-axis is the day(s) that are selected.
    if week == 1:
        fig = px.line(sheetToReadFrom_Previous, x="Time of Day", y=day,
                      title="Number of People in Building at Different Times")
    if week == 2:
        fig = px.line(sheetToReadFrom_Current, x="Time of Day", y=day,
                      title="Number of People in Building at Different Times")

    # Updating y-axis title and the legend title.
    fig.update_layout(yaxis_title="Number of People")
    fig.update_layout(legend_title="Day of Week")
    return fig

    # Second callback to the paragraph tag where the output is dependent of the filters chosen by the user.
@app.callback(
    Output('generalInfo', 'children'),
    Input('daySelector', 'value'),
    Input('buildingSelector', 'value')
)
def update_info(day, building):
    buildingArea = building_1_Area
    #Determining which Google Sheets to read from based on the input of the building
    #With Walmart-Shawnessy as the current default.
    sheetToReadFrom_Previous = building_1_Previous
    if building == "Building 2":
        sheetToReadFrom_Previous = building_2_Previous
        buildingArea = building_2_Area
    elif building == "Building 3":
        sheetToReadFrom_Previous = building_3_Previous
        buildingArea = building_3_Area
    oneDay = True
    if len(day) != 1:
        oneDay = False
    if isinstance(day, str) == True:
        oneDay = True
    if oneDay == False:
        return "Select a day to display general information about it."
    else:
        #This returns a string which provides the user the day in the previous week which contained the least number of people in total.
        indexOfSuggestedDay = dayWithLeast(day, building, sheetToReadFrom_Previous)
        liveCounter = displayLiveCounter(day, building, sheetToReadFrom_Previous)
        return f"""Currently, there are {displayLiveCounter(day, building, sheetToReadFrom_Previous):.0f} people in {building}.\nAccording to last week's data, the day with the least number of visitors in {building} was: {daysOfWeek[indexOfSuggestedDay]}.\nEach current visitor in {building} has {buildingArea/liveCounter:.0f} m²/person space."""

@app.callback(
    Output('predictBestDay', 'children'),
    Input('buildingSelector', 'value'),
    Input('predictiveDay', 'value')
)
def predictiveDayUpdate(building, timeSelected):
    timeSelected = [f"{timeSelected[0]}:00", f"{timeSelected[1]}:00"]
    sheetToReadFrom_Previous = building_1_Previous
    if building == "Building 2":
        sheetToReadFrom_Previous = building_2_Previous
    elif building == "Building 3":
        sheetToReadFrom_Previous = building_3_Previous
    return f"""Based on your inputs, {daysOfWeek[predictiveRange(building, sheetToReadFrom_Previous, timeSelected)]} was the day 
                last week in which there were the fewest number of people in {building}."""

def dayWithLeast(day, building, sheetToReadFrom_Previous):
    prevmon = sheetToReadFrom_Previous['Monday'].sum()
    prevtue = sheetToReadFrom_Previous['Tuesday'].sum()
    prevwed = sheetToReadFrom_Previous['Wednesday'].sum()
    prevthu = sheetToReadFrom_Previous['Thursday'].sum()
    prevfri = sheetToReadFrom_Previous['Friday'].sum()
    prevsat = sheetToReadFrom_Previous['Saturday'].sum()
    prevsun = sheetToReadFrom_Previous['Sunday'].sum()
    bigday = (prevmon, prevtue, prevwed, prevthu, prevfri, prevsat, prevsun)
    dayIndex = bigday.index(min(bigday))
    return dayIndex

def displayLiveCounter(day, building, sheetToReadFrom_Previous):
    #Finding the total number of lines so as to read the most recent counter value
    lastLine = len(sheetToReadFrom_Previous)

    #Based on the day, get the column number to read from a specific cell
    if day == "Monday":
        dayIndex = 1
    elif day == "Tuesday":
        dayIndex = 2
    elif day == "Wednesday":
        dayIndex = 3
    elif day == "Thursday":
        dayIndex = 4
    elif day == "Friday":
        dayIndex = 5
    elif day == "Saturday":
        dayIndex = 6
    elif day == "Sunday":
        dayIndex = 7
    else:
        dayIndex = 8
    #Returning the most recent counter value
    return sheetToReadFrom_Previous.iloc[1046 - 1, dayIndex]

def predictiveRange(building, sheetToReadFrom_Previous, timeSelected):
    input1="{x}".format(x=timeSelected[0])
    input2="{y}".format(y=timeSelected[1])

    prevmonT = pd.DataFrame(sheetToReadFrom_Previous['Monday'])
    prevmonT.loc[input1:input2]
    a = prevmonT.sum()

    prevtueT = pd.DataFrame(sheetToReadFrom_Previous['Tuesday'])
    prevtueT.loc[input1:input2]
    b = prevtueT.sum()

    prevwedT = pd.DataFrame(sheetToReadFrom_Previous['Wednesday'])
    prevwedT.loc[input1:input2]
    c = prevwedT.sum()

    prevthuT = pd.DataFrame(sheetToReadFrom_Previous['Thursday'])
    prevthuT.loc[input1:input2]
    d = prevthuT.sum()

    prevfriT = pd.DataFrame(sheetToReadFrom_Previous['Friday'])
    prevfriT.loc[input1:input2]
    e = prevfriT.sum()

    prevsatT = pd.DataFrame(sheetToReadFrom_Previous['Saturday'])
    prevsatT.loc[input1:input2]
    f = prevsatT.sum()

    prevsunT = pd.DataFrame(sheetToReadFrom_Previous['Sunday'])
    prevsunT.loc[input1:input2]
    g = prevsunT.sum()

    bestOptions = (float(a.to_string(index = False)),float(b.to_string(index = False)),
                    float(c.to_string(index = False)),float(d.to_string(index = False)),
                        float(e.to_string(index = False)),float(f.to_string(index = False)),float(g.to_string(index = False)))

    bestOption = bestOptions.index(min(bestOptions))

    return bestOption

# Running it
if __name__ == "__main__":
    app.run_server(debug=False, port=5000)
