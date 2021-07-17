# climatemind-analytics
Climate Mind Analytics

Analytics data for the Climate Mind app is currently set up to be automatically added to our database once a week on Tuesdays at 13:00 PT. The process is automated using an Azure Python Runbook.

A standalone version of the automated script is provided here to demonstrate the logic or to manually add analytics data to our db.

To use the standalone script:

1. Get authorization to access the Climate Mind analytics data by contacting Andrew Banister (awban22@gmail.com).
2. Create a folder for the repo on your computer.
3. Clone this repo.
4. Set up and activate a virtual environment.
5. Run ```pip install -r requirements.txt```
6. Add the secret.json and secret_db_credentials.py files to your project. **Note**: make sure that your files are named exactly as written here to ensure they are imported correctly and are ignored correctly by Git. 
7. Run the CM_analytics.py script.

# KPI4
![image](/kpi4%20usage.gif)