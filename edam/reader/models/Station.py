import json
import logging
from typing import Optional, Any

from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, SQLModel

module_logger = logging.getLogger('edam.reader.models')


class Station(SQLModel, table=True):
    """
    :var id: A unique id among other Stations
    :var name: The name of the Station
    :var mobile: Boolean, i.e. True of False
    :var polygon: :If mobile=True, then a polygon is given
    :var latitude:
    :var longitude:
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    mobile: bool = Field(default=False)
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    region: Optional[str] = None
    license: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[str] = None
    qualifiers: Optional[str] = None

    def __init__(self, name="Test Station", mobile=False, location="", latitude=None, longitude=None, region=None,
                 license=None, url=None, qualifiers=json.dumps({}), tags=json.dumps({}), **data: Any):
        """
        :param name:
        :param mobile:
        :param latitude:
        :param longitude:
        :param tags:
        """
        super().__init__(**data)
        self.name = name
        self.mobile = mobile
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.region = region
        self.license = license
        self.url = url

        self.qualifiers = qualifiers
        self.tags = tags

    def update(self, new_values: dict):
        for key, value in new_values.items():
            try:
                if key in ['tags', 'qualifiers']:
                    temp = getattr(self, key)  # type: dict
                    try:
                        value.update(temp)
                    except ValueError as e:
                        module_logger.warning(f"{e}")
                setattr(self, key, value)
            except AttributeError:
                module_logger.warning(f"{key} does not exist")

    @hybrid_property
    def tags(self):
        return json.loads(self.tags)

    @tags.setter
    def tags(self, value):
        self.tags = json.dumps(value)

    @hybrid_property
    def qualifiers(self):
        return json.loads(self._qualifiers)

    @qualifiers.setter
    def qualifiers(self, value):
        self._qualifiers = json.dumps(value)

    @property
    def missing_data(self):
        try:
            return self.qualifiers['missing_data']
        except KeyError:
            return ''

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __repr__(self):
        return f'<Name {self.name!r}>'
