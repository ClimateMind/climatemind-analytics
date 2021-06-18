import pandas as pd
import numpy as np
import seaborn as sns
sns.set_theme(style="whitegrid")
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

csv_file_path = 'Path to the directory where csv dataset is saved/page_by_session90-2.csv'


def load_data(csv_file_path, targeted_action = 'question_loaded'):
    """
  Processes data to be in proper format for analysis.

  input: csv_file
  output: pandas dataframe
  
  1 - Takes the CSV file from the path defined and passes it to the analytics dataframe
  2 - Extracts only the action 'question_loaded' from the entire dataset
  3 - Returns the extracted dataframe ql_analytics
  
  """
    analytics = pd.read_csv(csv_file_path)
    ql_analytics = analytics.loc[analytics['Action'] == targeted_action]
    return ql_analytics
  

#To just check whether the above function is working or not  	
#df = load_data(csv_file_path, targeted_action = 'question_loaded')




def compute_time_differences(df):
    """
	Computes the difference in seconds of consecutive timepoints in the data, grouped by session_id.

	input: 
	- df = Pandas dataframe from previous function

	output:
	 pandas dataframe with additional column 'Secs' that is the time interval between consecutive timepoints
     
     1 - Converts Timestamp to Pandas Datetime format
     2- Sorts the dataframe by Questionnaire_Session_ID and Timestamp in ascending order
     3 - Introduces a lag of +1 in Timestamp by grouping by Questionnaire_Session_ID
     4 - Computes the difference between Original and Lag Timestamps 
     5 - Extracts the seconds from the Interval
     6 - Returns the processed dataframe

  """

    
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    sorted_df = df.sort_values(by = ['Questionnaire_Session_ID', 'Timestamp'], ascending=True)
    
    df['Lag_Timestamp'] = sorted_df.groupby(['Questionnaire_Session_ID'])['Timestamp'].shift(1)
    
    df['Interval'] = df['Timestamp'] - df['Lag_Timestamp']
    
    df['Secs'] = df['Interval'].dt.components['seconds']
    
    return df

#To check whether function is working or not
#df2 = compute_time_differences(df)
  	
	
  	
def aggregate_questions_revisited(df2):
  """
 	Combines the time taken on questions that were revisted multiple times by the user.

 	inputs:
 	- df = pandas dataframe of the data
 	
 	output:
 	 dataframe of the session_id, value_column, and summed difference_column
      
    1 - Groups by Session_ID and Value in received order to get total seconds
    2 - Converts the grouped Series to a Pandas Dataframe
    3 - Resets the index for the dataframe
    4 - Filters out any values for Question_ID that is greater than 20
    5 - Returns the processed dataframe
    
  """
  
  time = df2.groupby(['Questionnaire_Session_ID', 'Value'], sort = False)['Secs'].sum()
  time_df = pd.DataFrame(time)
  time_df.reset_index(inplace = True)
  time_df = time_df.loc[time_df['Value'] < 20]
  return time_df

#time_df = aggregate_questions_revisited(df2)
#time_df['Value'].unique()
  

def remove_abnormal_use_data(time_df):
  """
  	Removes all questionnaire data associated with any user that takes less than 2 seconds.
      
	inputs:
	time_df = pandas dataframe from previous function
    
	output:
	dataframe of users whose minimum time answering is greater than 2 seconds
    
    1 - Regroup by Questionnaire_Session_ID to get minimum seconds for each
    2 - Add a filter_pass column to take in Sessions with time greater than 2 seconds
    3 - Merges this df with time_df on Questionnaire_Session_ID as the common column
    4 - Allows only those sessions which have answering time greater than 2 seconds as True

  """
  
  time_filter = time_df.groupby(['Questionnaire_Session_ID'], sort = False).min('Secs').reset_index()
  time_filter['filter_pass'] = time_filter['Secs'] > 2
  time_df_with_filter = time_df.merge(time_filter[['Questionnaire_Session_ID','filter_pass']], on = 'Questionnaire_Session_ID')
  time_df_filtered = time_df_with_filter[time_df_with_filter.filter_pass == True] 

  return time_df_filtered

#To check whether the above function is working or not
#time_df_filtered = remove_abnormal_use_data(time_df)
  
#OPTION 2 for filtering
  #minimums = time_df.groupby(['Questionnaire_Session_ID'], sort = False)['Secs'].min() > 2.0
  #keep_IDs = minimums.index[minimums].values
  #time_df_keep = time_df[time_df['Questionnaire_Session_ID'].isin(keep_IDs)]



def drop_off(time_df_filtered, groupby_column):
  """
	Computes the drop_off % of each value in the df. 

	inputs:
	time_df_filtered = pandas dataframe with no abnormal data
	groupby_column = column with the value to group by
	
	output:
	pandas data frame of value_column and % dropoff.
    
    1 - Creates an empty Pandas Dataframe time_df2
    2 - Groups the input dataframe by the input column and gets unique Sessions for each
    3 - Sorts this dataframe by the inout column in descending order
    4 - Computes the User Interval by diving Unique Users by maximum Unique Users
    5 - Resets the index for plotting purposes
    6 - Returns time_df2 for Drop-off graph
    

  """
  time_df2= pd.DataFrame()
  time_df2['Unique_Users'] = time_df_filtered.groupby([groupby_column])['Questionnaire_Session_ID'].nunique()
  time_df2.sort_values(by = [groupby_column], ascending = False, inplace = True)
  time_df2['User Interval'] = time_df2['Unique_Users']/ time_df2['Unique_Users'].max()
  time_df2.reset_index(inplace = True)

  return time_df2

#To check whether the above function is working or not
#time_df2 = drop_off(time_df_filtered, 'Value')



def swarm_plot(time_df_filtered, x_column, y_column, x_axis_label, y_axis_label, graph_title, image_name):
  """
	Creates swarm plot with overlayed box plot of the data.

	inputs:
	time_df_filtered = pandas dataframe containing the data to plot
	x_column = x axis data for the plot
	y_column = y axis data for the plot
	x_axis_label = label for the x-axis on the plot
	y_axis_label = label for the y-axis on the plot
	graph_title = title for the plot
    image_name = Name for the image to be saved

	output:
	labeled graph object
    
    1 , 2 - Sets the figure dimensions
    3 - Creates a Seaborn Boxplot with assigned function inputs as parameters
    4 - Creates a Seaborn Swarmplot with assigned function inputs as parameters
    5 - Inverts the X-axis as we want X axis to be from 10 to 1
    6 , 7 - Sets X and Y axis labels as per input provided
    8 - Saves the resultant plot to your system
    9 - Returns the plot for viewing
    
  """
  
  fig = plt.gcf()
  fig.set_size_inches(15, 10)
  
  ax = sns.boxplot(x = time_df_filtered[x_column], y = time_df_filtered[y_column],
                   data = time_df_filtered, whis = np.inf, fliersize = 20).set(title = graph_title)
  ax = sns.swarmplot(x = time_df_filtered[x_column], y = time_df_filtered[y_column],
                     data = time_df_filtered, color = ".2", size = 5)
  
  ax.invert_xaxis()
  
  ax.set_xlabel(x_axis_label)
  ax.set_ylabel(y_axis_label)
  
  ax.figure.savefig(image_name)
  
  return ax


#To check whether the above function is working or not
#sp = swarm_plot(time_df_filtered, 'Value', 'Secs', 'Question_ID','Total time taken (Seconds)', 'Total time taken to answer each question')



def dropoff_plot(time_df2, x_column, y_column, x_axis_label, y_axis_label, graph_title, image_name):
    """
  	Creates graph of data dropoff

  	inputs:
  	time_df2 = pandas dataframe containing the data to plot
	x_column = x axis data for the plot
	y_column = y axis data for the plot
	x_axis_label = label for the x-axis on the plot
	y_axis_label = label for the y-axis on the plot
	graph_title = title for the plot
    image_name = Name for image to be saved

	output:
	labeled graph object
    
    1- Sets the dimensions for the Line Plot
    2 - Creates a Seaborn Lineplot with assigned dataframe and columns
    3 - Sets X and Y axis labels and Title for the graph
    4 - Inverts the X-axis to have order from 10 to 1
    5 - Saves the resultant plot to your system
    6 - Returns the plot for viewing
    
    
  """
    
    plt.figure(figsize=(20,9))
    
    ax = sns.lineplot(data = time_df2, x = time_df2[x_column] ,y = time_df2[y_column], markers = True)
    
    ax.set(xlabel = x_axis_label, ylabel = y_axis_label, title = graph_title)
    
    ax.invert_xaxis()
    
    ax.figure.savefig(image_name)
    
    return ax


#To check whether the above function is working or not
#dop = dropoff_plot(time_df2, 'Value', 'User Interval')

      
  



def KPI4_analysis(csv_file_path):
    """
   Runs all the analytics functions.

   input: Pandas dataframe of the data
   output: png plots for the dashboard
   
   1 - Loads the dataset from csv_file_path to data
   2 - Computes the time differences to data and stores in time_differences
   3 - Aggregates the revisits to get total time and assigns it to revisits_summed
   4 - Removes developer data from the revisits_summed and stores in cleaned_data
   5 - Uses cleaned_data to get User Drop-off % for each Value (Question_ID) and stores in drop_off_data
   6 - Creates a Swarm plot using cleaned_data and other plotting parameters
   7 - Creates a Line plot using drop_off_data and other plotting parameters
   
 """
    
    data = load_data(csv_file_path, 'question_loaded')
    
    time_differences = compute_time_differences(data)
    
    revisits_summed = aggregate_questions_revisited(time_differences)
    
    cleaned_data = remove_abnormal_use_data(revisits_summed)
    
    drop_off_data = drop_off(cleaned_data, 'Value')
    
    swarm_plot_graph = swarm_plot(cleaned_data, 'Value', 'Secs', 'Question_ID',
                                  'Time taken to answer (Seconds)', 'Total time taken to answer each question',
                                  'Swarm Plot.png')
    
    dropoff_plot_graph = dropoff_plot(drop_off_data, 'Value', 'User Interval',
                                      'Question_ID','User Interval %', 'User Drop-off Graph',
                                      'Line Plot.png')


	

"""
Once everything above is executed, use the below function to get the plots saved to your system

"""

KPI4_analysis(csv_file_path)