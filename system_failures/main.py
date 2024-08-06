import os
import logging
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect, Column, Integer, String, ForeignKey

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'test-password')
DB_NAME = os.getenv('DB_NAME', 'hackerads')

DATABASE_URL = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'

MAX_19 = 19
MAX_64 = 64
FAILURE = 'failure'
SUCCESS = 'success'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

try:
    engine = create_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
except Exception as e:
    logger.error(f'Error connecting to the database: {e}')
    raise

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(MAX_64))
    last_name = Column(String(MAX_64))

    campaigns = relationship('Campaign', back_populates='customer')

class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    name = Column(String(MAX_64))

    customer = relationship('Customer', back_populates='campaigns')
    events = relationship('Event', back_populates='campaign')

class Event(Base):
    __tablename__ = 'events'

    dt = Column(String(MAX_19), primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    status = Column(String(MAX_64))

    campaign = relationship('Campaign', back_populates='events')

def create_sample_data(session):
    customer1 = Customer(id=1, first_name='Whitney', last_name='Ferrero')
    customer2 = Customer(id=2, first_name='Dickie', last_name='Romera')

    campaign1 = Campaign(id=1, customer_id=customer1.id, name='Upton Group')
    campaign2 = Campaign(id=2, customer_id=customer1.id, name='Roob, Hudson and Rippin')
    campaign3 = Campaign(id=3, customer_id=customer1.id, name='McCullough, Rempel and Larson')
    campaign4 = Campaign(id=4, customer_id=customer1.id, name='Lang and Sons')
    campaign5 = Campaign(id=5, customer_id=customer2.id, name='Ruecker, Hand and Haley')

    events = [
        ('2021-12-02 13:52:00', campaign1.id, FAILURE),
        ('2021-12-02 08:17:48', campaign2.id, FAILURE),
        ('2021-12-02 08:18:17', campaign2.id, FAILURE),
        ('2021-12-01 11:55:32', campaign3.id, FAILURE),
        ('2021-12-01 06:53:16', campaign4.id, FAILURE),
        ('2021-12-02 04:51:09', campaign4.id, FAILURE),
        ('2021-12-01 06:34:04', campaign5.id, FAILURE),
        ('2021-12-02 03:21:18', campaign5.id, FAILURE),
        ('2021-12-01 03:18:24', campaign5.id, FAILURE),
        ('2021-12-02 15:32:37', campaign1.id, SUCCESS),
        ('2021-12-01 04:23:20', campaign1.id, SUCCESS),
        ('2021-12-02 06:53:24', campaign1.id, SUCCESS),
        ('2021-12-02 08:01:02', campaign2.id, SUCCESS),
        ('2021-12-01 15:57:19', campaign2.id, SUCCESS),
        ('2021-12-02 16:14:34', campaign3.id, SUCCESS),
        ('2021-12-02 21:56:38', campaign3.id, SUCCESS),
        ('2021-12-01 05:54:43', campaign4.id, SUCCESS),
        ('2021-12-02 17:56:45', campaign4.id, SUCCESS),
        ('2021-12-02 11:56:50', campaign4.id, SUCCESS),
        ('2021-12-02 06:08:20', campaign5.id, SUCCESS)
    ]

    for dt, campaign_id, status in events:
        session.add(Event(dt=dt, campaign_id=campaign_id, status=status))

    session.add_all([customer1, customer2, campaign1, campaign2, campaign3, campaign4, campaign5])
    session.commit()

def query_failed_events():
    with Session() as session:
        results = (
            session.query(Customer.first_name, Customer.last_name, func.count(Event.status).label('failures'))
                .join(Customer.campaigns)
                .join(Campaign.events)
                .filter(Event.status == FAILURE)
                .group_by(Customer.id, Customer.first_name, Customer.last_name)
                .having(func.count(Event.status) > 3)
                .all()
        )
        for first_name, last_name, failures in results:
            logger.info(f'{first_name} {last_name} {failures}')

if __name__ == "__main__":
    if not inspect(engine).has_table('customers'):
        with Session() as session:
            Base.metadata.create_all(engine)
            create_sample_data(session)
    
    query_failed_events()
