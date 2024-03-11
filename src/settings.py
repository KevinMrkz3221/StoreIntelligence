from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session, sessionmaker

from src.logger import Logger


ENGINE  = create_engine('sqlite:///top.db', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=ENGINE)
session = Session()


logger = Logger('amazon.log')
