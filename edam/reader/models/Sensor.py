from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from edam.reader.models.UnitOfMeasurement import UnitOfMeasurement


class Sensor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    manufacturer: Optional[str] = Field(default=None)

    abstract_observable_id: Optional[int] = Field(default=None, foreign_key="abstractobservable.id")
    unit_of_measurement_id: Optional[int] = Field(default=None, foreign_key="unitofmeasurement.id")
    unitofmeasurement: Optional["UnitOfMeasurement"] = Relationship(back_populates="sensors")

    def __repr__(self):
        return f'<id {self.id!r}>'
