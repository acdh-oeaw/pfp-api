from pydantic import BaseModel, Field


class Entity(BaseModel): ...


class Person(Entity):
    person: str = None
    label: str = Field(..., example="Arthur Schnitzler")
    graph: str = None
