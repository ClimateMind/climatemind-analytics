# import plotly.graph_objects as go
# import plotly.express as px
# import pyodbc
# import pickle
# from sql_queries import *

# iri_node_name_map = pickle.load(open('iri_node_name_map.pickle', 'rb'))
# db_params = os.environ.get("DATABASE_PARAMS", "place holder param. none found")
#
# # # cursor = conn.cursor()
#
# CLICKS_BY_CARD_ORDER = execute_sql_with_caching(CLICKS_BY_CARD_ORDER_QUERY, db_params)
#
# CARDS_SHOWN_VS_CARDS_CLICKED = execute_sql_with_caching(CARDS_SHOWN_VS_CARDS_CLICKED_QUERY, db_params)
# CARDS_SHOWN_VS_CARDS_CLICKED.loc[:, "all_cards_iri"].replace(iri_node_name_map, inplace=True)
#
# fig = go.Figure()
# fig.add_trace(go.Bar(
#     x=CLICKS_BY_CARD_ORDER.loc[:, "effect_position"].to_list(),
#     y=CLICKS_BY_CARD_ORDER.loc[:, "num_clicks"].to_list()
# ))
#
# fig.update_layout(
#     title="Card clicks vs card order in feed"
# )
# fig1 = px.bar(
#     CARDS_SHOWN_VS_CARDS_CLICKED,
#     x="all_cards_iri",
#     y=["cards_clicked", "cards_shown"],
#     title="cards clicked/cards shown for different cards"
# )
# fig.update_xaxes(dtick=1)
# fig.write_html("images/fig.html")
# fig1.write_html("images/fig1.html")


from matplotlib import pyplot as plt

import pandas as pd
import pickle
import os

# Makes plots look nicer.
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})

pickle_files_root_dir = 'data'
scores = pd.read_csv(pickle_files_root_dir + '/scores.csv')  # Scores table
cf = pd.read_csv(pickle_files_root_dir + '/climate_feed.csv')  # Climate feed table
analytics = pd.read_csv(pickle_files_root_dir + '/analytics_data.csv')  # analytics table

# Dictionary mapping IRI to human-readable names.
iri_node_map = pickle.load(open(pickle_files_root_dir + '/iri_node_name_map.pickle', 'rb'))

# Sets up the needed auxiliary dataframes.
personal_value_names = ["security", "conformity", "benevolence", "tradition", "universalism", "self_direction",
                        "stimulation", "hedonism", "achievement", "power"]


def cache(name, value=None):
    if value is None:
        if os.path.exists("/tmp/" + name):
            return pickle.load(open("/tmp/" + name, "rb"))
        else:
            return None
    else:
        pickle.dump(value, open("/tmp/" + name, "wb"))
        return value


def setup_top_3(scores):
    cache_ = cache(setup_top_3.__name__)
    if cache_ is not None:
        return cache_

    scores_top3 = pd.DataFrame()
    prev_row = list(scores.iterrows())
    for row, _ in prev_row:
        top_3 = scores.loc[row, [*personal_value_names]].astype('float64').nlargest(3).index
        if (top_3.isnull().sum()):
            print(top_3)

        temp = pd.concat([scores[["session_uuid", "user_uuid"]].loc[row]] * 3, axis=1, ignore_index=True).T
        temp.loc[0, "pv"] = top_3[0]
        temp.loc[1, "pv"] = top_3[1]
        temp.loc[2, "pv"] = top_3[2]
        scores_top3 = scores_top3.append(temp, ignore_index=True)
    return cache(setup_top_3.__name__, scores_top3)


# scores_top3 is similar to scores, except it contains triple the amount of rows.
# each row represents a user, so I clone that row three times.
scores_top3 = setup_top_3(scores)
analytics_click_only = analytics[analytics['action'] == 'card_click']
cards_clicked = scores_top3.merge(analytics_click_only, on="session_uuid", how='right')
cards_shown = scores_top3.merge(analytics_click_only, on="session_uuid", how='right')

# Data for the cards that are clicked, grouped by the user's personal value category, and further by the card id being clicked ('value').
grouped = cards_clicked.groupby(['pv', 'value'])  # cards that are clicked

# same as grouped, but data includes all cards shown to the user., instead of cards clicked.
grouped_shown = cards_shown.groupby(['pv', 'value'])

cards_opened_not_closed = []


# KPI 5
# Average time reading a card by card (filter out cards that don’t have a corresponding close event)
# I don't see a card_close event, so reading time for card 1 = (timestamp open card2) - (timestamp open card1)
def kpi5():
    from collections import defaultdict
    from datetime import datetime
    def default_series():
        return pd.Series(index=[0])

    card_read_times = defaultdict(default_series)  # Key: card value, Value: read times
    for k, v in analytics[analytics['action'] == 'card_click'].groupby('session_uuid'):
        v['event_timestamp'] = v['event_timestamp'].map(lambda a: datetime.fromisoformat(a))
        v = v.sort_values(['value', 'event_timestamp'])

        # Stores when a particular card was opened.
        # Keyed by card value, stores information about a particular open event.
        # When we find a close event, match it with the open event, calculate the time in between,
        # and delete the open event.
        open_time = dict()

        for index, row in v.iterrows():
            if row["value"] not in open_time:
                open_time[row["value"]] = row
            else:
                card_read_times[row["value"]][index] = row["event_timestamp"] - open_time[row["value"]][
                    "event_timestamp"]

                # Have found a close event. Delete that value from open_time
                del open_time[row["value"]]

        # Search for what cards were opened and not closed for KPI 6
        # If all cards opened are closed, then open_time dict should be empty.
        cards_opened_not_closed.extend(open_time.values())
    for k, v in card_read_times.items():
        # Take the median, get seconds.
        card_read_times[k] = v.quantile(0.5).seconds

        if (v.size < 5):
            print(f"Warning: only {v.size} people read {iri_node_map[k]}")
    readtime = pd.Series(card_read_times).sort_values().reset_index()
    readtime['Card Name'] = readtime['index'].map(iri_node_map)
    readtime['Median read time in seconds'] = readtime[0]
    readtime.plot.barh(y='Median read time in seconds', x="Card Name", figsize=(10, 10))


def kpi6():
    cards_opened_not_closed.clear()
    kpi5()
    df = pd.DataFrame(cards_opened_not_closed)['value'].value_counts().reset_index()
    df['Card Names'] = df['index'].map(iri_node_map)
    df["Number of drop offs"] = df["value"]
    df.plot.barh(y="Number of drop offs", x="Card Names", figsize=(10, 10), title = "Number of drop offs for each card")


# KPI 4 -- average question completion time
def kpi4():
    from datetime import datetime

    temp = analytics[analytics['category'] == 'questionnaire'].sort_values("event_timestamp")

    questions_no_dups = pd.DataFrame(columns=temp.columns)
    for user_id, question_data in temp.groupby('session_uuid'):
        questions_sorted = question_data.drop_duplicates(subset='value')

        prevtime = datetime.fromisoformat(questions_sorted.iloc[0, :]["event_timestamp"])
        for index, row in questions_sorted.iterrows():
            curtime = datetime.fromisoformat(row["event_timestamp"])
            questions_sorted.loc[index, "time"] = (curtime - prevtime).seconds
            prevtime = curtime
        questions_no_dups = questions_no_dups.append(questions_sorted)
    questions_no_dups["value"] = questions_no_dups["value"].astype('float64')
    questions_no_dups["value"] = questions_no_dups["value"].map(lambda k: 10 - k)

    # First question is 1. Last question is 10 (there's no value for 10 because analytics events haven't been implemented for last question yet).
    questions_no_dups.groupby('value').mean().plot.bar(title="Question completion time (seconds) for question order")


# Number of clicks for each card for each personal value category.
# e.g. If a person whose top 3 personal values are security, benevolence, and hedonism, then their clicks
# for each card will be added to all three graphs
def kpi3_v2():
    pv_clicked = {}
    pv_shown = {}
    for a, b in grouped.size().groupby(level=0):
        pv_clicked[a] = b[a].reset_index()

        pv_clicked[a]["value"] = pv_clicked[a]["value"].map(iri_node_map)
        pv_clicked[a].sort_values(ascending=False, by=0).plot.bar(x="value", y=0,
                                                                  title='All clicks' if not a else a,
                                                                  ylabel="num clicks")


# KPI 3 -- Average number of cards clicked across all personal values.
# Displayed as simple boxplot.
def kpi3():
    clicks_by_uuid = analytics[analytics['action'] == 'card_click'][['session_uuid', 'value']].groupby(
        'session_uuid').count()

    # Clicks must be smaller than 21 for it to be included. More than 21 clicks doesn't make sense.
    clicks_by_uuid[clicks_by_uuid["value"] <= 21].boxplot(title="Cards clicked per user")


# KPI 3 -- same as KPI 3, but one graph for each personal value.
def kpi3_v3():
    group_clicked = cards_clicked[['pv', 'session_uuid', 'analytics_id']].groupby(
        ['pv', 'session_uuid']).count().groupby(level=0).mean()
    group_clicked = group_clicked.rename(columns={'analytics_id': 'average number of clicks'})
    group_clicked.plot.bar()


# Cards clicked vs card order.
def kpi1():
    analytics_renamed = analytics[analytics['category'] == 'card']
    analytics_renamed = analytics.rename(columns={'value': 'effect_iri'})

    # Remove duplicate clicks from same session_uuid
    analytics_renamed = analytics_renamed.drop_duplicates(['session_uuid', 'effect_iri'])
    clicks = cf.merge(analytics_renamed, how="left", on=["session_uuid", "effect_iri"])
    clicksarray = [0] * 21
    shownarray = [0] * 21

    for _, row in clicks[['effect_position', 'analytics_id']].iterrows():
        if not pd.isnull(row['analytics_id']):
            clicksarray[int(row['effect_position']) - 1] += 1
        shownarray[int(row['effect_position']) - 1] += 1
    print(clicksarray, shownarray)
    pd.Series(clicksarray).plot.bar(title="Cards clicked vs card order", ylabel="Number of clicks",
                                    xlabel="Card order (0-indexed)")


def kpi2():
    for pv, clicks in grouped.count().groupby(level=0):
        fig, ax = plt.subplots()
        clicks = clicks['analytics_id'].droplevel(0).rename(index=iri_node_map).sort_values()
        clicks.plot.bar(ax=ax, subplots=True, ylabel="Card", title=pv, xlabel="Clicks")


# Entrypoint here:
# Just run any function kpi* and it will start matplotlib plots.
kpi6()
plt.show()
