import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
load_dotenv()

class SQLServer:
    """
    Pass in a conn string to generate the engine for querying
    Example: pd.read_sql(query, SQLServer(SERVER="EXAMPLE_SERVER_CONN_STRING").engine)
    
    SQLAlchemy EXAMPLE_SERVER_CONN_STRING Format:
    mssql+pyodbc://user:password@server-ip/database?driver=ODBC+Driver
    """
    def __init__(self, SQLSERVER_CONN_STR):
        self.engine = create_engine(os.getenv(SQLSERVER_CONN_STR))