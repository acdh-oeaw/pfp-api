from jinja2 import Environment, PackageLoader
from typing import Annotated
from fastapi import FastAPI, Query, Response, status

from rdfproxy import Page, SPARQLModelAdapter, QueryParameters

from pfp_api.models import Person


app = FastAPI()
env = Environment(loader=PackageLoader("pfp_api"))


class PersonParams(QueryParameters):
    size: str = "foo"
    label: str = None


@app.get("/")
def root():
    return Response(status_code=status.HTTP_200_OK)


@app.get("/persons")
def persons(query_parameters: Annotated[PersonParams, Query()]) -> Page[Person]:
    template = env.get_template("persons.j2")
    adapter = SPARQLModelAdapter(
        target="https://pfp-ts-backend.acdh-ch-dev.oeaw.ac.at/",
        query=template.render(dict(query_parameters)),
        model=Person,
    )
    return adapter.query(query_parameters)
