import pandas as pd
import hashlib
import os
import pyodbc


CACHE_DIR = os.path.expanduser("~/.cache/")

def execute_sql_with_caching(sql_stmt, conn):
    if isinstance(conn, str):
        conn = pyodbc.connect(conn)


    hash_string = hashlib.md5(sql_stmt.encode()).hexdigest() + '.analytics-visualization.pickle'
    if os.path.isfile(CACHE_DIR + hash_string):
        print("Using cache for statement")
        return pd.read_pickle(CACHE_DIR + hash_string)
    else:
        df = pd.read_sql(sql_stmt, conn)
        df.to_pickle(CACHE_DIR + hash_string)
        return pd.read_sql(sql_stmt, conn)


CARDS_SHOWN_VS_CARDS_CLICKED_QUERY = """
--- card shown vs card clicked
select cf.all_cards_iri , count(ad.analytics_id)as cards_clicked, count(cf.climate_feed_id) as cards_shown
from analytics_data ad 
right join (
	select cf.solution_1_iri as all_cards_iri, * from climate_feed cf 
	union all
	select cf.solution_2_iri as all_cards_iri, * from climate_feed cf
	union all
	select cf.solution_3_iri as all_cards_iri, * from climate_feed cf
	union all
	select cf.solution_4_iri as all_cards_iri, * from climate_feed cf
	union all
	select cf.effect_iri as all_cards_iri, * from climate_feed cf
) as cf
on cf.session_uuid =ad.session_uuid AND ad.value =cf.all_cards_iri
where DATEDIFF(second,  '2021-01-21', cf.event_timestamp) > 0 and datediff(second,  cf.event_timestamp, ISNULL(ad.event_timestamp, cf.event_timestamp ) )<3600
GROUP BY cf.all_cards_iri
"""


CLICKS_BY_PV_QUERY = """
SELECT ad.value as card_iri,
		COUNT(CASE WHEN s.[conformity]>=3.5 THEN s.[conformity] ELSE NULL END) AS conformity,
		COUNT(CASE WHEN s.[benevolence]>=3.5 THEN s.[benevolence] ELSE NULL END) AS benevolence,
		COUNT(CASE WHEN s.[tradition]>=3.5 THEN s.[tradition] ELSE NULL END) AS tradition,
		COUNT(CASE WHEN s.[universalism]>=3.5 THEN s.[universalism] ELSE NULL END) AS universalism,
		COUNT(CASE WHEN s.[self_direction3.5 THEN s.[self_direction ELSE NULL END) AS self_direction
		COUNT(CASE WHEN s.[stimulation]>=3.5 THEN s.[stimulation] ELSE NULL END) AS stimulation,
		COUNT(CASE WHEN s.[hedonism]>=3.5 THEN s.[hedonism] ELSE NULL END) AS hedonism,
		COUNT(CASE WHEN s.[achievement]>=3.5 THEN s.[achievement] ELSE NULL END) AS achievement,
		COUNT(CASE WHEN s.[power]>=3.5 THEN s.[power] ELSE NULL END) AS power
    FROM analytics_data ad 
    INNER JOIN scores s 	
    on ad.session_uuid =s.session_uuid where ad.[action] = 'card_click' group by ad.value
"""


CLICKS_BY_CARD_ORDER_QUERY = """
SELECT cf.effect_position , count(cf.effect_position) as num_clicks
FROM analytics_data ad
INNER JOIN climate_feed as cf ON (
	ad.value =cf.effect_iri OR 
	ad.value =cf.solution_1_iri OR
	ad.value =cf.solution_2_iri OR
	ad.value =cf.solution_3_iri OR
	ad.value = cf.solution_4_iri 
	)  AND ad.session_uuid = cf.session_uuid AND datediff(second, cf.event_timestamp, ad.event_timestamp )<3600
	GROUP BY cf.effect_position ORDER BY cf.effect_position 
"""
