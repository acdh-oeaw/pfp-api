from pydantic import BaseModel, Field
from typing import List, Optional


class Entity(BaseModel): ...


class Event(Entity):
    label: str = None


class Person(Entity):
    person: str = None
    label: str = Field(..., example="Arthur Schnitzler")
    graph: str = None


class PersonDetail(Entity):
    person: str = None
    label: str = Field(..., example="Arthur Schnitzler")
    events: Optional[List[Event]] = None
