import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
load_dotenv()

class SQLServer:
    """
    Create an engine and use pd.read_sql to read data
    Example: pd.read_sql(query, SQLServer(SERVER="EXAMPLE_SERVER").engine)
    """
    def __init__(self, SERVER):
        self.engine = create_engine(os.getenv(SERVER))