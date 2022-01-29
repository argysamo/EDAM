from sqlmodel import SQLModel, create_engine
from edam.reader.models.Station import Station
from edam.reader.models.Sensor import Sensor
from edam.reader.models.AbstractObservable import AbstractObservable
from edam.reader.models.UnitOfMeasurement import UnitOfMeasurement

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:////Users/argyris/Developer/EDAM/edam/reader/models/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
