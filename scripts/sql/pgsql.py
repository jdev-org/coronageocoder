from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float
from geoalchemy2 import Geometry
from datetime import datetime

def connect(sgbd, user, password, hots, port, db):
    url = '{}://{}:{}@{}:{}/{}'.format(sgbd, user, password, hots, port, db)
    return create_engine(url, client_encoding='utf8', echo=False)


def prepareSession(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def sqlTable(engine, tableName, schemaName):
    Base = declarative_base()
    Base.metadata.create_all(engine)
    #  table shema - create new table if not exist
    class sqlTable(Base):
        __tablename__ = tableName
        __table_args__ = ({"schema": schemaName})
        id = Column(Integer, primary_key=True)
        state = Column(String, nullable=True)
        country = Column(String)
        lat = Column(Float)
        long = Column(Float)
        date = Column(Date)
        confirmed = Column(Integer)
        deaths = Column(Integer)
        recovered = Column(Integer)
        geom = Column(Geometry('POINT', srid=4326))
        def __repr__(self):
            return "<Corona(state='%s', country='%s', date='%s', confirmed='%s', deaths='%s', recovered='%s')>" % (self.state, self.country, self.date, self.confirmed, self.deaths, self.recovered)

    sqlTable.__table__
    return sqlTable


def addData(line, session, table, colNames, prop):
    i=0
    for cell in line:
        if i>=5 and cell != '':
            value = int(cell)
            date = datetime.strptime(colNames[i], '%m/%d/%y')
            # not already exist in database
            new_entry = table(
                state = line[0],
                country = line[1],
                long = float(line[2]),
                lat = float(line[3]),
                date = date,
                geom = 'SRID=4326;POINT({} {})'.format(float(line[2]), float(line[3]))
            )
            if prop == 'confirmed':
                new_entry.confirmed = value
            elif prop == 'deaths':
                new_entry.deaths = value
            else :
                new_entry.recovered = value

            # control if this element was not already send to database
            res = session.query(table).filter_by(country=new_entry.country, date=date, state=new_entry.state).first()
            if not res:
                session.add(new_entry)
                session.commit()
            else :
                update(new_entry, res, session)
        i+=1


def needUpdate(newVal, originVal):
    if originVal is None and newVal is not None:
        return True
    elif originVal is not None and newVal is not None:
        return True
    else:
        return False

def update(created_entry, db_entry, session):
    newDate = created_entry.date.strftime('%m/%d/%y')
    originalDate = db_entry.date.strftime('%m/%d/%y')
    if newDate == originalDate:
        # update deaths
        if needUpdate(created_entry.deaths, db_entry.deaths):
            db_entry.deaths = created_entry.deaths
            session.commit()
        # update confirmed
        if needUpdate(created_entry.confirmed, db_entry.confirmed):
            db_entry.confirmed = created_entry.confirmed
            session.commit()
        # update recovered
        if needUpdate(created_entry.recovered, db_entry.recovered):
            db_entry.recovered = created_entry.recovered
            session.commit()
