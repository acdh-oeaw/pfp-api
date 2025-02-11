from pydantic import BaseModel, Field
from typing import Annotated
from rdfproxy import ConfigDict, SPARQLBinding
from pydantic.networks import HttpUrl


class Entity(BaseModel): ...

class RelatedEntity(Entity):
    model_config = ConfigDict(group_by="id")
    id: Annotated[HttpUrl | None, SPARQLBinding("related_entity")] = None
    label: Annotated[str | None, SPARQLBinding("relatedEntityLabel")] = None

class RelatedPlace(Entity):
    model_config = ConfigDict(group_by="id")
    id: Annotated[HttpUrl | None, SPARQLBinding("related_place")] = None
    label: Annotated[str | None, SPARQLBinding("relatedPlaceLabel")] = None
    long: Annotated[float | None, SPARQLBinding("longitude")] = None
    lat: Annotated[float | None, SPARQLBinding("latitude")] = None

class Event(Entity):
    model_config = ConfigDict(group_by="id")
    id: Annotated[str, SPARQLBinding("event_id")]
    label: Annotated[str, SPARQLBinding("eventLabel")]
    startDate: str | None = None
    endDate: str | None = None
    relatedEntity: list[RelatedEntity]
    relatedPlace: RelatedPlace


class EntityProxy(Entity):
    id: Annotated[HttpUrl, SPARQLBinding("proxy")]
    label: str = Field(..., example="Arthur Schnitzler")

class Person(Entity):
    model_config = ConfigDict(group_by="id")
    id: Annotated[HttpUrl, SPARQLBinding("pfp_uri")]
    proxies: list[EntityProxy]


class PersonDetail(Entity):
    model_config = ConfigDict(group_by="id")
    id: Annotated[str, SPARQLBinding("prov_entity")]
    #label: Annotated[str, SPARQLBinding()]
    events: list[Event]
