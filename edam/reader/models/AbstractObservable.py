from typing import Optional

from sqlmodel import Field, SQLModel


class AbstractObservable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ontology: Optional[str] = Field(default=None)
