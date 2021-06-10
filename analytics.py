from datetime import datetime, date
import dash_table
import pandas as pd

pd.options.plotting.backend = "plotly"
import pickle
import plotly.express as px
import pyodbc
import os
# Makes plots look nicer.
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

# Where are the pickle files located relative to this file location?
pickle_files_root_dir = 'data'

# Load the three main tables we'll require to pandas Dataframes.
# scores = pd.read_csv(pickle_files_root_dir + '/scores.csv')  # Scores table
# cf = pd.read_csv(pickle_files_root_dir + '/climate_feed.csv')  # Climate feed table
# analytics = pd.read_csv(pickle_files_root_dir + '/analytics_data.csv')  # analytics table

sqlconn = pyodbc.connect(os.environ["DATABASE_PARAMS"])

analytics = pd.read_sql("SELECT * FROM analytics_data", sqlconn)
cf = pd.read_sql("SELECT * FROM climate_feed", sqlconn)
scores = pd.read_sql("SELECT * FROM scores", sqlconn)

# Dictionary mapping IRI (some random base 64 string) to descriptive names.
iri_node_map = pickle.load(open(pickle_files_root_dir + '/iri_node_name_map.pickle', 'rb'))

personal_value_names = ["security", "conformity", "benevolence", "tradition", "universalism", "self_direction",
                        "stimulation", "hedonism", "achievement", "power"]


# Caching function so we don't have to compute dataframes everytime we reload the script.
def cache(name, value=None):
    if value is None:
        if os.path.exists("/tmp/" + name):
            return pickle.load(open("/tmp/" + name, "rb"))
        else:
            return None
    else:
        pickle.dump(value, open("/tmp/" + name, "wb"))
        return value


analytics_click_only = analytics[analytics['action'] == 'card_click']


# KPI 4 -- average question completion time
# Calculated by taking the start time of the next question, subtracted the start time of previous question.
# Outputs the question response time bar chart, the sample size heading, and the raw data table.
# sd: start_date (ISO format)
# ed: end_date
@app.callback([
    dash.dependencies.Output("kpi4-graph", "figure"),
    dash.dependencies.Output("sample-size-header", "children"),

    # Show the raw data as a table.
    dash.dependencies.Output("pivot-questions-table", "data"),
    dash.dependencies.Output("dropoff-graph", "figure")],

    [
        dash.dependencies.Input('date-picker-range', 'start_date'),
        dash.dependencies.Input('date-picker-range', 'end_date')
    ])
def kpi4(sd, ed):
    if not (sd and ed):
        return dash.no_update, dash.no_update, dash.no_update
    fromdate = datetime.fromisoformat(sd)
    todate = datetime.fromisoformat(ed)

    analytics["event_timestamp"] = pd.to_datetime(analytics["event_timestamp"])

    date_filtered_analytics = analytics[
        (analytics["event_timestamp"] >= fromdate) & (analytics["event_timestamp"] <= todate)]
    questions_filter = date_filtered_analytics['action'] == 'question_start'
    questions_filter = questions_filter | (date_filtered_analytics['action'] == 'question_loaded')
    temp = date_filtered_analytics[questions_filter].sort_values(
        ["event_timestamp", "value"], ascending=[True, False])

    questions_no_dups = pd.DataFrame(columns=temp.columns)
    for user_id, question_data in temp.groupby('session_uuid'):
        questions_sorted = question_data.drop_duplicates(subset='value')

        prevtime = questions_sorted.iloc[0, :]["event_timestamp"]
        for index, row in questions_sorted.iterrows():
            curtime = row["event_timestamp"]
            questions_sorted.loc[index, "time"] = (curtime - prevtime).seconds
            prevtime = curtime
        questions_no_dups = questions_no_dups.append(questions_sorted)
    questions_no_dups["value"] = questions_no_dups["value"].astype('float64')

    # Reverse the order of questions (higher value = first in question order).
    questions_no_dups["value"] = questions_no_dups["value"].map(lambda k: 10 - k)

    # Delete all rows where question `value` is 0 and 10, since we can't get the time for the last question,
    # and `value` = 0 is just a byproduct of the processing script.
    questions_final = questions_no_dups[questions_no_dups["value"] >= 1]

    print("Total size: ", questions_final.__len__())

    if questions_final.index.size:
        # First question is 1. Last question is 10 (there's no value for 10 because analytics events haven't been implemented for last question yet).

        fig = px.bar(questions_final.groupby('value').mean(), y="time")
        fig.update_yaxes(title={'text': "Time to answer question in seconds"})
        fig.update_xaxes(title={'text': "Question order"})

        # Pivot the table to show data by question order as columns.
        # Since we have data like this,
        # value (question number)     |     response time    |   ...
        #   3                                1s                  ...
        #   2                                5s                  ...
        #   1                                3s                  ...
        # When we pivot the table with `value` as columns, we'll get the response time for each question order.
        datatable = questions_final.pivot(columns="value", values="time", index="session_uuid") \
            .reset_index()

        dropoff = datatable.count()
        dropoff_graph = px.bar(dropoff, title="# of question completions vs question order (dropoff graph)", y=0)
        dropoff_graph.update_yaxes(title={'text': "Number of people answering"})
        dropoff_graph.update_xaxes(title={'text': "Question order"})
        return fig, "Sample size: " + str(len(questions_final.index)), datatable.to_dict('records'), dropoff_graph
    else:
        return dash.no_update, "Error: No events for date range", dash.no_update, dash.no_update


def generate_slider_marks():
    mark_nums = [14, 30, 60, 120, 180, 240, 300, 480]
    mark_text = [str(x) + " days ago" for x in mark_nums]
    return {-x: y for (x, y) in zip(mark_nums, mark_text)}


cols = ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", ]
cols = [{"name": f"Q.{i[0]}", "id": i} for i in cols]
cols = [{"name": "Session ID", "id": "session_uuid"}] + cols

data_table_layout = html.Div(children=[
    html.H2(
        children="Question response time vs. question order for each session_uuid (in seconds)."
    ),
    dash_table.DataTable(
        id="pivot-questions-table",
        columns=cols,
        style_cell={
            'font-size': '1.2em'
        }
    ),
    html.H2(
        children="# of question completions vs question order"
    ),
    dcc.Graph(
        id="dropoff-graph"
    )
])

app.layout = html.Div(children=[
    html.H1(children='ClimateMind analytics'),

    html.Div(
        children=[
            html.H2(children="KPI4 - Average reading time per question"),
            dcc.Graph(
                id='kpi4-graph'
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
            data_table_layout,

            html.H3(
                children=f"Latest event: {analytics.iloc[-1].event_timestamp}"
            )
        ], style={
            'max-width': '1000px'
        }, ),

])

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)
    # kpi4([-30, 0])
