from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from variables import BakeOffEnvironmentVariables

db_host = BakeOffEnvironmentVariables.db_host
db_port = BakeOffEnvironmentVariables.db_port
db_name = BakeOffEnvironmentVariables.db_name
db_user = BakeOffEnvironmentVariables.db_user
db_pass = BakeOffEnvironmentVariables.db_pass

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()