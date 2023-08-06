import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
load_dotenv()

class SQLServer:
    def __init__(self, SERVER):
        self.engine = create_engine(os.getenv(SERVER))