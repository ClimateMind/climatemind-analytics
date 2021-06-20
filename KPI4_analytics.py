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

warnings.filterwarnings('ignore')

csv_file_path = 'Path to the CSV file/page_by_session90-2.csv'


def load_data(_, targeted_action='question_loaded'):
    """
    input:
    - targeted_action = 'question_loaded' This is the action we need to analyze

    output:
    Pandas dataframe containing analytics data from the SQL DB

    """

    if "DATABASE_PARAMS" not in os.environ:
        raise RuntimeError("Environment variable DATABASE_PARAMS not detected")

    sqlconn = pyodbc.connect(os.environ["DATABASE_PARAMS"])



    analytics = pd.read_sql("SELECT * FROM analytics_data", sqlconn)
    return analytics.loc[analytics['action'] == targeted_action]


def parse_columns_native_formats(df):
    """
    input:
    - df = Pandas dataframe containing analytics_data

    output:
    Same dataframe with columns converted to numeric and datetime

    1 - Converts value (Question_ID) to numeric value
    2 - Converts the event_timestamp to Pandas datetime format

    """

    df['value'] = pd.to_numeric(df['value'])
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])


analytics = load_data(csv_file_path, 'question_loaded')
parse_columns_native_formats(analytics)


def compute_time_differences(df, session_id, timestamp, difference_column):
    """
	Computes the difference in seconds of consecutive timepoints in the data, grouped by session_id.

	input: 
	- df = Pandas dataframe from previous function
	- session_id = Questionnaire_Session_ID in this case. Can also be session_uuid
	- timestamp = The original event timestamp in the analytics data
	- difference_column = To store the extracted seconds/minutes from the interval. Seconds in this case

	output:
	 pandas dataframe with additional column 'Secs' that is the time interval between consecutive timepoints
     
     1 - Converts event_timestamp to Pandas Datetime format
     2- Sorts the dataframe by Questionnaire_Session_ID and event_timestamp in ascending order
     3 - Introduces a lag of +1 in event_timestamp by grouping by Questionnaire_Session_ID
     4 - Computes the difference between Original and Lag event_timestamps
     5 - Extracts the seconds from the Interval
     6 - Returns the processed dataframe

  """

    df[timestamp] = pd.to_datetime(df[timestamp])

    sorted_df = df.sort_values(by=[session_id, timestamp], ascending=True)

    df['Lag_event_timestamp'] = sorted_df.groupby([session_id])[timestamp].shift(1)

    df['Interval'] = df[timestamp] - df['Lag_event_timestamp']

    df[difference_column] = df['Interval'].dt.components['seconds']

    return df


def aggregate_questions_revisited(df2, session_id, value_column, difference_column):
    """
       Combines the time taken on questions that were revisted multiple times by the user.

       inputs:
       - df = pandas dataframe of the data
       - session_id = Questionnaire_Session_ID in this case. Can also be session_uuid
       - value_column = The value for the each label in the analytics data. In this case, it is the Question_ID for each question_loaded action
       - difference_column = To store the extracted seconds/minutes from the interval. Seconds in this case

       output:
        dataframe of the session_id, value_column, and summed difference_column

      1 - Groups by Session_ID and value in received order to get total seconds
      2 - Converts the grouped Series to a Pandas Dataframe
      3 - Resets the index for the dataframe
      4 - Filters out any values for Question_ID that is greater than 20
      5 - Returns the processed dataframe

    """

    time = df2.groupby([session_id, value_column], sort=False)[difference_column].sum()
    time_df = pd.DataFrame(time)
    time_df.reset_index(inplace=True)
    time_df = time_df.loc[time_df[value_column] < 20]
    return time_df


def remove_abnormal_use_data(time_df, session_id, difference_column, filter_threshold):
    """
        Removes all questionnaire data associated with any user that takes less than 2 seconds.

      inputs:
      - time_df = pandas dataframe from previous function
      - session_id = Questionnaire_Session_ID in this case. Can also be session_uuid
      - difference_column = To store the extracted seconds/minutes from the interval. Seconds in this case
      - filter_threshold = Argument to accept only those responses that took greater than 2 or 3 seconds. 

      output:
      dataframe of users whose minimum time answering is greater than 2 or 3 seconds

      1 - Regroup by Questionnaire_Session_ID to get minimum seconds for each
      2 - Add a filter_pass column to take in Sessions with time greater than 2 seconds
      3 - Merges this df with time_df on Questionnaire_Session_ID as the common column
      4 - Allows only those sessions which have answering time greater than 2 seconds as True

    """

    time_filter = time_df.groupby([session_id], sort=False).min(difference_column).reset_index()
    time_filter['filter_pass'] = time_filter[difference_column] > filter_threshold
    time_df_with_filter = time_df.merge(time_filter[[session_id, 'filter_pass']], on=session_id)
    time_df_filtered = time_df_with_filter[time_df_with_filter.filter_pass == True]

    return time_df_filtered


# OPTION 2 for filtering
# minimums = time_df.groupby(['session_uuid'], sort = False)['Secs'].min() > 2.0
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
    time_df2['Unique_Users'] = time_df_filtered.groupby([groupby_column])[session_id].nunique()
    time_df2.sort_values(by=[groupby_column], ascending=False, inplace=True)
    time_df2['User Interval'] = time_df2['Unique_Users'] / time_df2['Unique_Users'].max()
    time_df2.reset_index(inplace=True)
    time_df2['User Interval %'] = (time_df2['User Interval'] * 100)

    print("The number of Unique Users are  = ", time_df2['Unique_Users'].max())

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

    fig.update_xaxes(range=[1, 11], dtick=1)

    fig['layout']['xaxis']['autorange'] = "reversed"

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

    fig = px.violin(time_df_filtered, x=time_df_filtered[x_column], y=time_df_filtered[y_column], box=True,
                    points='all', color=time_df_filtered[x_column])

    fig.update_xaxes(range=[1, 11], dtick=1)

    fig['layout']['xaxis']['autorange'] = "reversed"

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


def KPI4_analysis(data):
    """
   Runs all the analytics functions.

   input: Pandas dataframe of the data
   output: png plots for the dashboard
   
   1 - Loads the dataset from csv_file_path to data
   2 - Computes the time differences to data and stores in time_differences
   3 - Aggregates the revisits to get total time and assigns it to revisits_summed
   4 - Removes developer data from the revisits_summed and stores in cleaned_data
   5 - Uses cleaned_data to get User Drop-off % for each value (Question_ID) and stores in drop_off_data
   6 - Creates a Swarm plot using cleaned_data and other plotting parameters
   7 - Creates a Line plot using drop_off_data and other plotting parameters
   8 - Creates a Violin plot using cleaned_data and other plotting parameters
   7 - Creates a Line plot using drop_off_data and other plotting parameters
   
 """

    time_differences = compute_time_differences(data, 'session_uuid', 'event_timestamp', 'Secs')

    revisits_summed = aggregate_questions_revisited(time_differences, 'session_uuid', 'value', 'Secs')

    cleaned_data = remove_abnormal_use_data(revisits_summed, 'session_uuid', 'Secs', -1)

    drop_off_data = drop_off(cleaned_data, 'session_uuid', 'value')

    # swarm_plot_graph = swarm_plot(cleaned_data, 'value', 'Secs', 'Question_ID',
    #                               'Time taken to answer (Seconds)', 'Total time taken to answer each question',
    #                               'Swarm Plot.png')
    #
    # dropoff_plot_graph = dropoff_plot(drop_off_data, 'value', 'User Interval',
    #                                   'Question_ID', 'User Interval %', 'User Drop-off Graph',
    #                                   'Line Plot.png')

    violin_plot = plotly_violinplot(cleaned_data, 'value', 'Secs', 'Question_ID',
                                    'Time taken to answer (Seconds)', 'Total time taken to answer each question',
                                    'Violin Plot.png')

    line_plot = plotly_lineplot(drop_off_data, 'value', 'User Interval',
                                'Question_ID', 'User Interval %', 'User Drop-off Graph',
                                'Plotly Line Plot.png')

    # violin_plot.show()
    # line_plot.show()
    return violin_plot, line_plot


def kpi4(sd, ed):
    """
    Callback function that runs everytime a filter is changed on client-side. Re-renders the plots using
    the new filter parameters.

    Currently, only date (from date and to date) filters are supported
    :param sd: start_date (automatically filled out by Dash, in ISO format
    :param ed: end_date (same format as start_date)
    :return: tuple of violin plot (plotly graph object), sample size text, and dropoff-graph
    """
    if not (sd and ed):
        return dash.no_update, dash.no_update, dash.no_update
    fromdate = datetime.fromisoformat(sd)
    todate = datetime.fromisoformat(ed)

    date_filtered_analytics = analytics[
        (analytics["event_timestamp"] >= fromdate) & (analytics["event_timestamp"] <= todate)]

    violin, line = KPI4_analysis(date_filtered_analytics)
    return violin, "", line


def run_dash_app():
    """
    Start the dash app, initialize the Dash layout, and run the server in Debug mode.
    This function will never exit.
    """
    app = dash.Dash(__name__)

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
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=date(2018, 1, 1),
                    end_date=datetime.now(),
                    initial_visible_month=datetime.now()
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
                    children=f"Latest event: {analytics.iloc[-1].event_timestamp}"
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
            dash.dependencies.Input('date-picker-range', 'end_date')
        ])
    def kpi4_inner(*args):
        """
        Register a callback with the app. Since Dash callbacks are registered using function decorators,
        we make a closure function that calls an outer function
        """
        return kpi4(*args)

    app.run_server(host="0.0.0.0", port=8050, debug=True, dev_tools_hot_reload=False)


if __name__ == "__main__":
    run_dash_app()
