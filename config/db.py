import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqliteName = 'ferremax'
base_dir = os.path.dirname(os.path.realpath(__file__))
datebaseUrl = f'sqlite:///{os.path.join(base_dir, sqliteName)}.db'


engine = create_engine(datebaseUrl,echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
