from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from secret_db_credentials import DATABASE_PARAMS # Make sure to name your file and variable exactly as written here
import urllib.parse

"""
This is a standalone script that can be used to manually add google analytics data pulled via the reporting API
to the project's analytics table hosted in Azure. NOTE - the project currently has a modified version of this script 
running automatically as an Azure runbook. Speak to a member of the team for the api authentication and db login
credentials.
"""

# Authorisation info required to access Analytics Reporting API
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'secret.json'  # Make sure to name your file exactly as written here
VIEW_ID = '232128049'


def initialize_analytics_reporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
        An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = None
    try:
        analytics = build('analyticsreporting', 'v4', credentials=credentials)
    except Exception as e:
        print('Failed to create API service object', e)

    return analytics


def get_report(analytics):
    """Queries the Analytics Reporting API V4.

    Args:
        analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
        The Analytics Reporting API V4 response.
    """
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    # Adjust date range according to your needs
                    'dateRanges': [{'startDate': '8daysAgo', 'endDate': 'today'}],
                    'metrics': [
                        {'expression': 'ga:hits'}
                    ],
                    'dimensions': [
                        {"name": "ga:eventCategory"},
                        {"name": "ga:eventAction"},
                        {"name": "ga:eventLabel"},
                        {"name": "ga:dimension1"},  # session_id
                        {"name": "ga:dimension2"},  # event_ts
                        {"name": "ga:dimension3"}  # eventValue
                    ]
                    # "filtersExpression":"ga:pagePath=~products;ga:pagePath!@/translate",
                    # #Filter by condition "containing products"
                    # 'orderBys': [{"fieldName": "ga:sessions", "sortOrder": "DESCENDING"}],
                    # 'pageSize': 100
                }]
        }
    ).execute()


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
        response: An Analytics Reporting API V4 response.
    """
    for report in response.get('reports', []):
        column_header = report.get('columnHeader', {})
        dimension_headers = column_header.get('dimensions', [])
        metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            date_range_values = row.get('metrics', [])

            for header, dimension in zip(dimension_headers, dimensions):
                print(header + ': ', dimension)

            for i, values in enumerate(date_range_values):
                print('Date range:', str(i))
                for metricHeader, value in zip(metric_headers, values.get('values')):
                    print(metricHeader.get('name') + ':', value)


def ga_response_list(response):
    """Parses ga response and returns a list of results as dictionaries.
    https://janakiev.com/blog/python-google-analytics/
    Args:
        response: An Analytics Reporting API V4 response.
    Returns:
        row_list: A list of results as dictionaries.
    """
    row_list = []
    # Get each collected report
    for report in response.get('reports', []):
        # Set column headers
        column_header = report.get('columnHeader', {})
        dimension_headers = column_header.get('dimensions', [])
        metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])

        # Get each row in the report
        for row in report.get('data', {}).get('rows', []):
            # create dict for each row
            row_dict = {}
            dimensions = row.get('dimensions', [])
            date_range_values = row.get('metrics', [])

            # Fill dict with dimension header (key) and dimension value (value)
            for header, dimension in zip(dimension_headers, dimensions):
                row_dict[header] = dimension

            # Fill dict with metric header (key) and metric value (value)
            for i, values in enumerate(date_range_values):
                for metric, value in zip(metric_headers, values.get('values')):
                    # Set int as int, float as float, uuid as uuid
                    if ',' in value or '.' in value:
                        row_dict[metric.get('name')] = float(value)
                    else:
                        row_dict[metric.get('name')] = int(value)
            # Remove hits from the row dictionary
            row_dict.pop('ga:hits', None)
            # Change session_uuid back to a uuid
            row_dict['ga:dimension1'] = uuid.UUID(row_dict.get('ga:dimension1'))
            row_dict['ga:dimension2'] = datetime.strptime(row_dict.get('ga:dimension2'), '%Y-%m-%d %H:%M:%S')
            row_list.append(row_dict)

    return row_list


def connect_to_db():
    """
    Helper function to create connection to the Azure db.

    Returns:
      engine: A SQLAlchemy engine.
    """
    # Database params should never be published
    db_credentials = DATABASE_PARAMS
    database_uri = 'mssql+pyodbc:///?odbc_connect=%s' % urllib.parse.quote_plus(str(db_credentials))
    engine = None
    try:
        engine = create_engine(database_uri, echo=False)
    except Exception as e:
        print('Failed to create engine', e)

    return engine


def build_df_no_duplicates(row_list):
    """Checks the list of results from the Analytics Reporting API V4 response against the db, removes duplicates,
    and converts to a pandas dataframe.

   Args:
       row_list: A list of results as dictionaries from the Analytics Reporting API V4 response.
   Returns:
       df: A pandas dataframe with rows already in the db removed.
   """
    engine = connect_to_db()
    edited_row_list = []

    # Check if results list is empty

    if not row_list:
        print('No new analytics data for this time period.')
    else:
        # Check if data is already in the db
        for row in row_list:
            category = row['ga:eventCategory']
            action = row['ga:eventAction']
            label = row['ga:eventLabel']
            session_uuid = row['ga:dimension1']
            event_timestamp = row['ga:dimension2']
            value = row['ga:dimension3']

            row_exists = engine.execute('SELECT * FROM analytics_data WHERE category=? AND action=? AND label=? AND '
                                        'session_uuid=? AND event_timestamp=? and value=?',
                                        (category, action, label, session_uuid, event_timestamp, value)).first()

            # Add only unique rows to the list to be added to the db
            if not row_exists:
                edited_row_list.append(row)

    # Convert the list to a dataframe
    df = pd.DataFrame(edited_row_list)

    return df


def persist_df_to_db(df):
    """Connects to Azure db and adds pandas dataframe.

    Args:
      df: A pandas dataframe of non-duplicate results from the last call to the Analytics Reporting
      API V4.
    """
    engine = connect_to_db()
    # Provide column heading defaults to stop pandas using GA column headings
    db_columns = ['category', 'action', 'label', 'session_uuid', 'event_timestamp', 'value']

    if not df.empty:
        try:
            df.rename(columns=dict(zip(df.columns, db_columns)))\
                .to_sql('analytics_data', engine, if_exists='append', index=False)
        except Exception as e:
            print('Error - data not added to the db', e)
    else:
        print('No new data to add to the db')


def main():
    analytics = initialize_analytics_reporting()
    response = get_report(analytics)
    row_list = ga_response_list(response)
    df = build_df_no_duplicates(row_list)
    persist_df_to_db(df)
    print('Done')

    # df.to_csv("page_by_session.csv")
    # print_response(response)


if __name__ == '__main__':
    main()
