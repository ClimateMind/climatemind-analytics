import plotly.graph_objects as go
import plotly.express as px
import pyodbc
import pickle
from sql_queries import *

iri_node_name_map = pickle.load(open('iri_node_name_map.pickle', 'rb'))
db_params = os.environ.get("DATABASE_PARAMS", "place holder param. none found")

# cursor = conn.cursor()

CLICKS_BY_CARD_ORDER = execute_sql_with_caching(CLICKS_BY_CARD_ORDER_QUERY, db_params)

CARDS_SHOWN_VS_CARDS_CLICKED = execute_sql_with_caching(CARDS_SHOWN_VS_CARDS_CLICKED_QUERY, db_params)
CARDS_SHOWN_VS_CARDS_CLICKED.loc[:, "all_cards_iri"].replace(iri_node_name_map, inplace=True)

fig = go.Figure()
fig.add_trace(go.Bar(
    x=CLICKS_BY_CARD_ORDER.loc[:, "effect_position"].to_list(),
    y=CLICKS_BY_CARD_ORDER.loc[:, "num_clicks"].to_list()
))

fig.update_layout(
    title="Card clicks vs card order in feed"
)
fig1 = px.bar(
    CARDS_SHOWN_VS_CARDS_CLICKED,
    x="all_cards_iri",
    y=["cards_clicked", "cards_shown"],
    title="cards clicked/cards shown for different cards"
)
fig.update_xaxes(dtick=1)
fig.write_html("images/fig.html")
fig1.write_html("images/fig1.html")
