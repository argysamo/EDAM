from typing import TYPE_CHECKING, Optional, List

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from edam.reader.models.Sensor import Sensor


class UnitOfMeasurement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ontology: Optional[str] = Field(default=None)
    symbol: Optional[str] = Field(default=None)

    sensors: List["Sensor"] = Relationship(back_populates="unitofmeasurement")
