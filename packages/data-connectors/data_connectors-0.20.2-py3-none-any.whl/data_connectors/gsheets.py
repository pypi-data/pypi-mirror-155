import os
import pygsheets
from dotenv import load_dotenv
load_dotenv()

class Gsheets:
    """
    Query by spreadsheet, then worksheet
    Example: Gsheets().query('stocks', 'data')
    """
    def __init__(self):
        self.client = pygsheets.authorize(service_file=(os.getenv("GSHEETS_SERVICE_ACCOUNT")))

    def query(self, spreadsheet, worksheet):
        """
        Returns results of spreadsheet, worksheet as a pandas DataFrame
        """        
        return self.client.open_by_key(os.getenv(spreadsheet)).worksheet_by_title(worksheet).get_as_df()