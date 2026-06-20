from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Developer@0509",
    host="localhost",
    port=5432,
    database="Practice_DB"
)

engine = create_engine(url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)