import binascii
from base64 import urlsafe_b64decode
from jinja2 import Environment, PackageLoader
from typing import Annotated
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse

from rdfproxy import Page, SPARQLModelAdapter, QueryParameters

from pfp_api.models import Person, PersonDetail


app = FastAPI()
env = Environment(loader=PackageLoader("pfp_api"))


class PersonParams(QueryParameters):
    label: str = None


@app.get("/", response_class=RedirectResponse, status_code=302)
def root():
    return "/docs"


@app.get("/persons")
def persons(query_parameters: Annotated[PersonParams, Query()]) -> Page[Person]:
    template = env.get_template("persons.j2")
    adapter = SPARQLModelAdapter(
        target="https://pfp-ts-backend.acdh-ch-dev.oeaw.ac.at/",
        query=template.render(dict(query_parameters)),
        model=Person,
    )
    return adapter.query(query_parameters)


@app.get("/person/{person_id}")
def person(person_id: str):
    template = env.get_template("person.j2")
    try:
        person_id = urlsafe_b64decode(person_id).decode()
    except binascii.Error:
        raise HTTPException(status_code=404, detail="Person not found")
    adapter = SPARQLModelAdapter(
        target="https://pfp-ts-backend.acdh-ch-dev.oeaw.ac.at/",
        query=template.render({"person_id": person_id}),
        model=PersonDetail
    )
    return adapter.query(QueryParameters())
