import plotly.graph_objects as go
import plotly.express as px
import os
import warnings
import pyodbc
from datetime import date, datetime

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
#import urllib.parse




warnings.filterwarnings('ignore')

#csv_file_path = 'Path to the CSV file/page_by_session90-2.csv'


def load_data(targeted_actions=['question_loaded','questionnaire_finish']):
    """
    input:
    - targeted_actions = list of strings ex: 'question_loaded' This is the action we need to analyze

    output:
    Pandas dataframe containing analytics data from the SQL DB

    """

    if "DATABASE_PARAMS" not in os.environ:
        raise RuntimeError("Environment variable DATABASE_PARAMS not detected")

    sqlconn = pyodbc.connect(os.environ["DATABASE_PARAMS"])

    #for each targeted action, only load in that data
    #SELECT * FROM analytics_data WHERE (action = 'question_loaded') OR (action = 'questionnaire_finish')

    begin_str = "SELECT * FROM analytics_data WHERE (action = '"
    fill_str = "') OR (action = '"
    middle_str = fill_str.join(targeted_actions)
    final_str = "')"
    complete_query = begin_str+middle_str+final_str

    data_of_interest = pd.read_sql(complete_query, sqlconn)


    return data_of_interest


def question_id_to_question_number(question_id):
    """
    Converts question_id to question_number but only works properly if using data with 
    question_ids from 1-10 and if questionnaire has question_ids presented from high to low.
    
    input:
    - question_id = question_id from the personal values quiz

    output:
    - question_number = number from 1 to 10 that should correspond to the position the question was displayed in the quiz
    """
    question_id = pd.to_numeric(question_id)
    if question_id > 10 and question_id < 21:
      question_number = 31 - question_id
    elif question_id > 0 and question_id < 11:
      question_number = 11 - question_id
    else:
      question_number = None

    return question_number

def question_id_from_value(value):
    """
    Converts question_id to question_number but only works properly if using data with 
    question_ids from 1-10 and if questionnaire has question_ids presented from high to low.
    
    input:
    - question_id = question_id from the personal values quiz

    output:
    - question_number = number from 1 to 10 that should correspond to the position the question was displayed in the quiz
    """
    if ":" in value:
      split = value.split(":")
      question_id = pd.to_numeric(split[0])
      question_number = pd.to_numeric(split[1])
    else:
      question_id = pd.to_numeric(value)

    return question_id

def question_number_from_value(value):
    """
    Converts question_id to question_number but only works properly if using data with 
    question_ids from 1-10 and if questionnaire has question_ids presented from high to low.
    
    input:
    - question_id = question_id from the personal values quiz

    output:
    - question_number = number from 1 to 10 that should correspond to the position the question was displayed in the quiz
    """
    if ":" in value:
      split = value.split(":")
      question_id = pd.to_numeric(split[0])
      question_number = pd.to_numeric(split[1])
    else:
      question_id = pd.to_numeric(value)
      question_number = question_id_to_question_number(question_id) 

    return question_number


def parse_columns_native_formats(df):
    """
    input:
    - df = Pandas dataframe containing analytics_data

    output:
    Same dataframe with columns converted to numeric and datetime

    1 - Converts value (Question_ID) to numeric value
    2 - Converts the event_timestamp to Pandas datetime format

    """
    df.loc[df["action"]=="questionnaire_finish", "value"] = "0:0"
    #df['value'] = pd.to_numeric(df['value'])
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])

    #convert value column to appropriate split terms (if just number without ":" in it convert to numeric)
    #if value column has ":" in it then split into separate column 
    df["question_id"] = df.apply(lambda row: question_id_from_value(row.value), axis=1) #value if no ":", and if ":" present then use the value to the left of the ":"
    df["question_number"] = df.apply(lambda row: question_number_from_value(row.value), axis=1) #if no ":" and under 11 then subtract from 10 otherwise blank, and if ":" present then use the value to the right of the ":"

#analytics = load_data(csv_file_path, ['question_loaded','questionnaire_finish'])
#analytics = load_data(['question_loaded','questionnaire_finish'])
#parse_columns_native_formats(analytics)


def compute_time_differences(df, session_id, timestamp, difference_column):
    """
	Computes the difference in seconds of consecutive timepoints in the data, grouped by session_id.

	input: 
	- df = Pandas dataframe from previous function
	- session_id = Questionnaire_Session_ID in this case. Can also be session_uuid
	- timestamp = The original event timestamp in the analytics data
	- difference_column = To store the extracted seconds/minutes from the interval. Seconds in this case

	output:
	 pandas dataframe with additional column 'difference_column' that is the time interval between consecutive timepoints
     
     1 - Converts event_timestamp to Pandas Datetime format
     2- Sorts the dataframe by Questionnaire_Session_ID and event_timestamp in ascending order
     3 - Introduces a lag of +1 in event_timestamp by grouping by Questionnaire_Session_ID
     4 - Computes the difference between Original and Lag event_timestamps
     5 - Extracts the seconds from the Interval
     6 - Returns the processed dataframe

  """

    df[timestamp] = pd.to_datetime(df[timestamp])

    sorted_df = df.sort_values(by=[session_id, timestamp], ascending=True)
    sorted_df['Lag_event_timestamp'] = sorted_df.groupby([session_id])[timestamp].shift(1)
    sorted_df['Interval'] = sorted_df[timestamp] - sorted_df['Lag_event_timestamp']
    sorted_df["difference"] = sorted_df['Interval'].dt.total_seconds()

    #to associate the difference with how long user spent on the 1st screen (not the screen they went to upon click) (null will exist for the event that takes user off the questionnaire)
    sorted_df[difference_column] = sorted_df.difference.shift(-1)

    return sorted_df


def aggregate_questions_revisited(df2, session_id, value_column, question_number_column, difference_column, min_question_id, max_question_id):
    """
       Combines the time taken on questions that were revisted multiple times by the user.

       inputs:
       - df = pandas dataframe of the data
       - session_id = Questionnaire_Session_ID in this case. Can also be session_uuid
       - value_column = The value for the each label in the analytics data. In this case, it is the Question_ID for each question_loaded action
       - question_number_column = the column with the question numbers
       - difference_column = To store the extracted seconds/minutes from the interval. Seconds in this case

       output:
        dataframe of the session_id, value_column, and summed difference_column

      1 - Groups by Session_ID and value in received order to get total seconds
      2 - Converts the grouped Series to a Pandas Dataframe
      3 - Resets the index for the dataframe
      4 - Filters out any values for Question_ID that is greater than 20
      5 - Returns the processed dataframe

    """
    time = df2.groupby([session_id, value_column, question_number_column], sort=False)[difference_column].sum()
    time_df = pd.DataFrame(time)
    time_df.reset_index(inplace=True)
    if question_number_column in time_df.columns.values: 
      time_df = time_df.loc[ (time_df[question_number_column] >= min_question_id) & (time_df[question_number_column] <= max_question_id), ]
    return time_df


def remove_abnormal_use_data(time_df, session_id, difference_column, filter_threshold_min, filter_threshold_max):
    """
        Removes all questionnaire data associated with any user that takes less than a specific number of seconds or more than a specific number of seconds.

      inputs:
      - time_df = pandas dataframe from previous function
      - session_id = Questionnaire_Session_ID in this case. Can also be session_uuid
      - difference_column = To store the extracted seconds/minutes from the interval. Seconds in this case
      - filter_threshold_min = Argument to accept only those responses that took greater than the specified number. 
      - filter_threshold_max = Argument to accept only those responses that took less than the specified number. 

      output:
      dataframe of users whose minimum time answering is greater than 2 or 3 seconds

      1 - Regroup by Questionnaire_Session_ID to get minimum seconds for each
      2 - Add a filter_pass column to take in Sessions with time greater than 2 seconds
      3 - Merges this df with time_df on Questionnaire_Session_ID as the common column
      4 - Allows only those sessions which have answering time greater than 2 seconds as True

    """

    #time_filter = time_df.groupby([session_id], sort=False).min(difference_column).reset_index()
    time_filter = time_df.groupby([session_id], sort=False).agg({difference_column:['min','max']}).reset_index()
    time_filter['filter_pass'] = (time_filter[difference_column]["min"] >= filter_threshold_min) & (time_filter[difference_column]["max"] <= filter_threshold_max)
    time_df_with_filter = time_df.merge(time_filter[[session_id,"filter_pass"]].droplevel(axis=1,level=1), on=session_id)
    time_df_filtered = time_df_with_filter[(time_df_with_filter["filter_pass"] == True)]
    #time_df_filtered = time_df_with_filter[ (time_df_with_filter[difference_column] >= filter_threshold_min) & (time_df_with_filter[difference_column] <= filter_threshold_max)]
    #time_df_with_filter[(time_df_with_filter.duration > 300).values]
    #time_df_filtered[(time_df_filtered.duration > 300).values]

    return time_df_filtered


# OPTION 2 for filtering
# minimums = time_df.groupby(['session_uuid'], sort = False)['difference_column'].min() > 2.0
# keep_IDs = minimums.index[minimums].values
# time_df_keep = time_df[time_df['session_uuid'].isin(keep_IDs)]


def drop_off(time_df_filtered, session_id, groupby_column):
    """
      Computes the drop_off % of each value in the df.

      inputs:
      - time_df_filtered = pandas dataframe with no abnormal data
      - session_id = Questionnaire_Session_ID in this case. Can also be session_uuid
      - groupby_column = column with the value to group by

      output:
      pandas data frame of value_column and % dropoff.

      1 - Creates an empty Pandas Dataframe time_df2
      2 - Groups the input dataframe by the input column and gets unique Sessions for each
      3 - Sorts this dataframe by the inout column in descending order
      4 - Computes the User Interval by diving Unique Users by maximum Unique Users
      5 - Resets the index for plotting purposes
      6 - Returns time_df2 for Drop-off graph


    """
    time_df2 = pd.DataFrame()

    if not time_df_filtered.empty:
        time_df2['Unique_Users'] = time_df_filtered.groupby([groupby_column])[session_id].nunique()
        time_df2.sort_values(by=[groupby_column], ascending=False, inplace=True)
        time_df2['User Interval'] = time_df2['Unique_Users'] / time_df2['Unique_Users'].max()
        time_df2.reset_index(inplace=True)
        time_df2['User Interval %'] = (time_df2['User Interval'] * 100)

        #print("The number of Unique Users are = ", time_df2['Unique_Users'].max())
    else:
        time_df2 = pd.DataFrame(columns=[groupby_column, 'Unique_Users', "User Interval", "User Interval %"])

    return time_df2


"""PLOTLY FUNCTIONS"""


def plotly_lineplot(time_df2, x_column, y_column, x_axis_label, y_axis_label, graph_title, image_name):
    """
    input:
    time_df2 = pandas dataframe containing the data to plot
    x_column = x axis data for the plot
    y_column = y axis data for the plot
    x_axis_label = label for the x-axis on the plot
    y_axis_label = label for the y-axis on the plot
    graph_title = title for the plot
    image_name = Name for image to be saved
    
    output:
	labeled Plotly Line Plot object 
    
    1 - Creates a Plot using assigned dataframe and X and Y axes
    2 - Updates the X-axis to show all questions
    3 - Reverses the range for questions from 10 to 1
    4 - Adds axes labels, title, and modifies font and dimensions
    5 - Displays the Line Plot
    6 , 7 - If 'images' folder does not exist in your default directory, it assigns "images" folder
    8 - Saves the plot to "images" folder with the assigned name 
    
    """

    fig = go.Figure(data=go.Scatter(x=time_df2[x_column], y=time_df2[y_column]))

    fig.update_xaxes(range=[1, max(time_df2[x_column])], dtick=1)

    #fig['layout']['xaxis']['autorange'] = "reversed"

    fig.update_yaxes(rangemode='tozero')

    fig.update_layout(title=graph_title,
                      xaxis_title=x_axis_label,
                      yaxis_title=y_axis_label,
                      yaxis_tickformat='%',
                      autosize=False,
                      width=1000,
                      height=1000,
                      font=dict(family="Courier New, monospace",
                                size=18,
                                color="RebeccaPurple"))

    fig.add_annotation(
        yref="y domain",
        xref="x domain",
        y=1.0,
        x=1.0,
        text=f"N: {time_df2['Unique_Users'].max()} users",
        showarrow=False
    )
    return fig


def plotly_violinplot(time_df_filtered, x_column, y_column, x_axis_label, y_axis_label, graph_title, image_name):
    """
    input:
    time_df2 = pandas dataframe containing the data to plot
    x_column = x axis data for the plot
    y_column = y axis data for the plot
    x_axis_label = label for the x-axis on the plot
    y_axis_label = label for the y-axis on the plot
    graph_title = title for the plot
    image_name = Name for image to be saved

	output:
	labeled Plotly Line Plot object 
    
    1 - Creates a Violin Plot with assigned dataframe and columns
    2 - Updates X axis range to show all questions
    3 - Reverses the question order to display 10 to 1
    4 - Adds the assigned title, labels, and changes dimensions
    5 - Shows the resultant image
    6 , 7 - If 'images' folder does not exist in your default directory, it assigns "images" folder
    8 - Saves the plot to "images" folder with the assigned name
    
    """

    fig = px.violin(time_df_filtered, x=x_column, y=y_column, box=True,
                    points='all', color=None if time_df_filtered.empty else x_column)

    fig.update_xaxes(range=[1, time_df_filtered[x_column]], dtick=1)

    #fig['layout']['xaxis']['autorange'] = "reversed"

    fig.update_layout(title=graph_title,
                      xaxis_title=x_axis_label,
                      yaxis_title=y_axis_label,
                      autosize=False,
                      font=dict(family="Courier New, monospace",
                                size=18,
                                color="RebeccaPurple"))

    fig.add_annotation(
        yref="y domain",
        xref="x domain",
        y=1.0,
        x=1.0,
        text=f"N: {time_df_filtered['session_uuid'].nunique()} users",
        showarrow=False
    )

    return fig


def KPI4_analysis(data, min_answer_time, data_sources):
    """
   Runs all the analytics functions.

   inputs: 
   data = Pandas dataframe of the data
   min_answer_time = number (user must spend at least this much time for every question in order to include their data in the analysis )
   data_sources = list of url(s) to include in the analysis as data sources

   output: png plots for the dashboard
   
   1 - Loads the dataset from source
   2 - Computes the time differences to data and stores in time_differences
   3 - Aggregates the revisits to get total time and assigns it to revisits_summed
   4 - Removes developer data from the revisits_summed and stores in cleaned_data
   5 - Uses cleaned_data to get User Drop-off % for each value (Question_ID) and stores in drop_off_data
   6 - Creates a Swarm plot using cleaned_data and other plotting parameters
   7 - Creates a Line plot using drop_off_data and other plotting parameters
   8 - Creates a Violin plot using cleaned_data and other plotting parameters
   7 - Creates a Line plot using drop_off_data and other plotting parameters
   
 """
    #otherwise select anything that matches? or just sub
    #make regular expression string
    pattern_string = "|".join(data_sources)
    #if "climatemind" then also include None values
    #subset the data based on the data_sources
    #keep
    pattern_string="climatemind|prod"
    keep = data['page_url'].str.contains(pat=pattern_string, na=False)
    if "climatemind" in pattern_string:
      keep2 = data['page_url'].isnull()
      keep = keep | keep2
    
    data = data[keep]


    time_differences = compute_time_differences(data, 'session_uuid', 'event_timestamp', 'duration')

    revisits_summed = aggregate_questions_revisited(time_differences, 'session_uuid', 'value', 'question_number', 'duration', 1, 20)

    cleaned_data = remove_abnormal_use_data(revisits_summed, 'session_uuid', 'duration', min_answer_time, 300)

    drop_off_data = drop_off(cleaned_data, 'session_uuid', 'question_number')

    # swarm_plot_graph = swarm_plot(cleaned_data, 'value', 'duration', 'Question_ID',
    #                               'Time taken to answer (Seconds)', 'Total time taken to answer each question',
    #                               'Swarm Plot.png')
    #
    # dropoff_plot_graph = dropoff_plot(drop_off_data, 'value', 'User Interval',
    #                                   'Question_ID', 'User Interval %', 'User Drop-off Graph',
    #                                   'Line Plot.png')

    violin_plot = plotly_violinplot(cleaned_data, 'question_number', 'duration', 'question_number',
                                    'Time taken to answer (Seconds)', 'Total time taken to answer each question',
                                    'Violin Plot.png')

    line_plot = plotly_lineplot(drop_off_data, 'question_number', 'User Interval',
                                'question_number', 'User Interval %', 'User Drop-off Graph',
                                'Plotly Line Plot.png')

    # violin_plot.show()
    # line_plot.show()
    return violin_plot, line_plot


def map_to_data_urls(data_sources):
  """
  Maps from data_sources to data_urls.

  inputs:
  data_sources = list of user selected data_sources options

  output:
  data_urls = list of urls associated with the user selected data_sources
  """
  #make dictionary
  # source_dict = {
  #   "localhost": "http://localhost/",
  #   "test_env": "https://app-frontend-test-001.azurewebsites.net/",
  #   "prod_env": "https://app-frontend-prod-001.azurewebsites.net/",
  #   "app_url": "https://app.climatemind.org/"
  # }

  source_dict = {
    "localhost": "localhost",
    "test_env": "test",
    "prod_env": "prod",
    "app_url": "climatemind"
  }

  data_urls = [source_dict[url] for url in data_sources]
  return data_urls




def kpi4(analytics_data_df, sd, ed, min_answer_time, data_sources):
    """
    Callback function that runs everytime a filter is changed on client-side. Re-renders the plots using
    the new filter parameters.

    :param sd: start_date selected by user (automatically filled out by Dash, in ISO format)
    :param ed: end_date selected by user (same format as start_date)
    :min_answer_time: filter number entered by user (in seconds)
    :data_sources: list of user options selected that map to urls for data sources

    :return: tuple of violin plot (plotly graph object), sample size text, and dropoff-graph
    """
    if not (sd and ed):
        return dash.no_update, dash.no_update, dash.no_update
    fromdate = datetime.fromisoformat(sd)
    todate = datetime.fromisoformat(ed)

    date_filtered_analytics = analytics_data_df[
        (analytics_data_df["event_timestamp"] >= fromdate) & (analytics_data_df["event_timestamp"] <= todate)]

    data_urls = map_to_data_urls(data_sources)

    violin, line = KPI4_analysis(date_filtered_analytics, min_answer_time, data_urls)
    return violin, "", line


def run_dash_app():
    """
    Start the dash app, initialize the Dash layout, and run the server in Debug mode.
    This function will never exit.
    """
    app = dash.Dash(__name__)
    #application = app.server

    #load in the data (this should only by done once!)
    analytics = load_data(['question_loaded','questionnaire_finish'])
    parse_columns_native_formats(analytics)

    # Defines how the website will look and the positioning of the elements.
    app.layout = html.Div(children=[
        html.H1(children='ClimateMind analytics'),
        html.Div(
            children=[
                html.H2(children="KPI4 - Average reading time per question"),
                dcc.Graph(
                    id='kpi4-graph',
                    style={
                        "height": "600px"
                    }
                ),
                html.H3(
                    children="Date range and data source(s) to include in analysis"
                ),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=date(2018, 1, 1),
                    end_date=datetime.now(),
                    initial_visible_month=datetime.now()
                ),

                dcc.Dropdown(
                    id='data-source-filter',
                    options=[
                        {'label': 'localhost', 'value': 'localhost'},
                        {'label': 'test_env', 'value': 'test_env'},
                        {'label': 'prod_env', 'value': 'prod_env'},
                        {'label': 'app_url', 'value': 'app_url'}
                    ],
                    value=['app_url'],
                    multi=True
                ),  
                html.H3(
                    children="Minimum question answer time threshold (seconds)"
                ),
                dcc.Input(
                    id='min-question-time-slider',
                    type= "number",
                    placeholder = "Time (Default 3 seconds)",
                    min=0,
                    step=1,
                    value=3,
                ),
                html.P(
                    children=["Sample size: ", 0],
                    id="sample-size-header"
                ),
                html.Hr(),
                html.Div(children=[
                    dcc.Graph(
                        id="dropoff-graph"
                    )
                ]),
                html.H3(
                    children=f"Latest event: {analytics.event_timestamp.max()}"
                )
            ], style={
                'max-width': '1000px'
            }, ),

    ])

    @app.callback([
        # Violin plot
        dash.dependencies.Output("kpi4-graph", "figure"),

        # Shows the sample size as a header text
        dash.dependencies.Output("sample-size-header", "children"),

        # Drop-off line chart
        dash.dependencies.Output("dropoff-graph", "figure")],
        [
            dash.dependencies.Input('date-picker-range', 'start_date'),
            dash.dependencies.Input('date-picker-range', 'end_date'),
            dash.dependencies.Input('min-question-time-slider', 'value'),
            dash.dependencies.Input('data-source-filter', 'value'),
        ])
    def kpi4_inner(*args):
        """
        Register a callback with the app. Since Dash callbacks are registered using function decorators,
        we make a closure function that calls an outer function
        """
        return kpi4(analytics, *args)

    app.run_server(host="0.0.0.0", port=8050, debug=True, dev_tools_hot_reload=False)


if __name__ == "__main__":
    run_dash_app()
