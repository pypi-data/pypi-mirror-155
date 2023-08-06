import os
import pygsheets
from dotenv import load_dotenv
load_dotenv()

class Gsheets:
    """
    Query by spreadsheet, then worksheet
    Example: Gsheets(SERVICE_ACCOUNT="EXAMPLE_SERVICE_ACCOUNT").query('GSHEETS_STOCKS', 'data')
    """
    def __init__(self, SERVICE_ACCOUNT):
        self.client = pygsheets.authorize(service_file=(os.getenv(SERVICE_ACCOUNT)))

    def query(self, spreadsheet, worksheet):
        """
        Returns results of spreadsheet, worksheet as a pandas DataFrame
        """        
        return self.client.open_by_key(os.getenv(spreadsheet)).worksheet_by_title(worksheet).get_as_df()