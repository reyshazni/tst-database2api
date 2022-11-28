
from sqlalchemy import create_engine
class DatabaseManager:
    def __init__(self, db_engine: str) -> None:
        self.conn = create_engine(db_engine).connect()

    
db_engine  = "mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
dbInstance = DatabaseManager(db_engine=db_engine)

# how to execute query
dbInstance.conn.execute("{query}", {values})