import csv
import logging
import os
import re
from contextlib import contextmanager
from enum import Enum
import json
import logging

import jinja2schema
from sqlalchemy import Boolean, Float

import yaml
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from edam.reader.database import Base, recreate_database
from edam.reader.models.AbstractObservable import AbstractObservable
from edam.reader.models.Station import Station
from edam.reader.models.UnitOfMeasurement import UnitOfMeasurement
from edam.reader.regular_expressions import template_file_header, for_loop_variables, var_for_line
from edam.utilities.exceptions import ErrorWithTemplate

module_logger = logging.getLogger('edam.reader.models')


class Observations(Base):
    __tablename__ = "Observations"
    """

    """
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    value = Column(String(60))
    helper_observable_id = Column(Integer, ForeignKey('HelperTemplateIDs.id'))

    def __init__(self, timestamp=None, value=None, helper_observable_id=None):
        """
        :param timestamp:
        :param value:
        :param flag:
        :param tags:
        """
        self.timestamp = timestamp
        self.value = value
        self.helper_observable_id = helper_observable_id

    def __repr__(self):
        return '<id %r>' % self.id


class Sensors(Base):
    __tablename__ = "Sensors"
    """
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    manufacturer = Column(String(60))
    tags = Column(String(500))

    abstract_observable_id = Column(
        Integer, ForeignKey('AbstractObservables.id'))
    # We may need to omit the following. It does not make any sense to me.
    unit_id = Column(Integer, ForeignKey('UnitsOfMeasurement.id'))

    sens1 = relationship('HelperTemplateIDs', backref='sensor', lazy='dynamic')

    def update(self, new_data_in_dict):
        for key, value in new_data_in_dict.items():
            try:
                setattr(self, key, value)
            except:
                module_logger.warning("{key} does not exist".format(key=key))
                pass

    def __init__(self, name="Test sensor",
                 manufacturer="Test manufacturer",
                 abstract_observable_id=None, unit_id=None,
                 tags=json.dumps({})):
        self.name = name
        self.manufacturer = manufacturer
        self.abstract_observable_id = abstract_observable_id
        self.unit_id = unit_id
        self.tags = json.dumps(tags)

    def __repr__(self):
        return f'<id {self.id!r}>'


class HelperTemplateIDs(Base):
    __tablename__ = "HelperTemplateIDs"
    """
    """
    id = Column(Integer, primary_key=True)
    observable_id = Column(String(30))

    abstract_observable_id = Column(
        Integer, ForeignKey('AbstractObservables.id'))
    unit_id = Column(Integer, ForeignKey('UnitsOfMeasurement.id'))
    station_id = Column(Integer, ForeignKey('Station.id'))
    sensor_id = Column(Integer, ForeignKey('Sensors.id'))

    start_date = Column(DateTime)
    end_date = Column(DateTime)
    number_of_observations = Column(Integer)
    frequency = Column(String(10))
    observable = relationship('AbstractObservables')
    station = relationship('Station',
                           back_populates="helper", cascade="all", single_parent=True)
    helper_observable_id = relationship(
        'Observations', backref='helper', lazy='dynamic')

    def update(self, new_data_in_dict):
        for key, value in new_data_in_dict.items():
            try:
                setattr(self, key, value)
            except KeyError:
                module_logger.warning("{key} does not exist".format(key=key))

    def update_metadata(self, metadata_in_dict):
        # TODO: If we append values, we have to change number of observations
        allowed = (
            'start_date',
            'end_date',
            'frequency',
            'number_of_observations')
        start_date_value = getattr(self, 'start_date')
        observations = getattr(self, 'number_of_observations')
        for key, value in metadata_in_dict.items():
            if key in allowed:

                if key == 'start_date' and start_date_value:
                    pass
                elif key == 'number_of_observations' and observations:
                    setattr(self, key, int(value) + observations)
                else:
                    setattr(self, key, value)

    def __init__(self, observable_id=None, sensor_id=None,
                 abstract_observable_id=None, unit_id=None,
                 station_id=None):
        self.observable_id = observable_id
        self.sensor_id = sensor_id
        self.abstract_observable_id = abstract_observable_id
        self.unit_id = unit_id
        self.station_id = station_id

        self.start_date = None
        self.end_date = None
        self.number_of_observations = None
        self.frequency = None

    @staticmethod
    def add_metadata_file(observable_id: str, station: Station, observables: [AbstractObservable]
                          , sensors: [Sensors], units_of_measurement: [UnitOfMeasurement]):
        pass

    def __repr__(self):
        return '<id %r>' % (self.id)


class StorageType(Enum):
    FILE = 'file'
    MEMORY = 'memory'


if __name__ == "__main__":
    recreate_database()
