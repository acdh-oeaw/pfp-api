from pydantic import BaseModel, Field


class Entity(BaseModel): ...


class Person(Entity):
    label: str = Field(..., example="Arthur Schnitzler")
