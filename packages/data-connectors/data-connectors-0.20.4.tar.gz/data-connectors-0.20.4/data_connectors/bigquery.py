import os
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv
load_dotenv()

class BigQuery:

    """
    Pass in a service account file path and query data stored in BigQuery
    Example: BigQuery().query("SELECT * FROM `jinlee.dbt.fct_receive` LIMIT 10")
    """
    
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("BIGQUERY_SERVICE_ACCOUNT"), scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        self.client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    def query(self, sql):
        """
        Returns results of SQL Query as a pandas DataFrame
        """
        return self.client.query(sql).to_dataframe()