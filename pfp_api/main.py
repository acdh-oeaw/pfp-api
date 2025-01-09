from typing import Annotated
from fastapi import FastAPI, Query, Response, status

from rdfproxy import Page, SPARQLModelAdapter, QueryParameters

from pfp_api.models import Person
from pfp_api.queries import QueryBuilder


app = FastAPI()


class PersonParams(QueryParameters):
    label: str = None


@app.get("/")
def root():
    return Response(status_code=status.HTTP_200_OK)


@app.get("/persons")
def persons(query_parameters: Annotated[PersonParams, Query()]) -> Page[Person]:
    adapter = SPARQLModelAdapter(
        target="https://pfp-ts-backend.acdh-ch-dev.oeaw.ac.at/",
        query=str(QueryBuilder("person.rq")),
        model=Person,
    )
    return adapter.query(query_parameters)
