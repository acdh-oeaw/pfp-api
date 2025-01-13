import binascii
from base64 import urlsafe_b64decode
from jinja2 import Environment, PackageLoader
from typing import Annotated
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse

from rdfproxy import Page, QueryParameters
from pfp_api.rdfproxy import RDFProxyWrapper

from pfp_api.models import Person, PersonDetail


app = FastAPI()
env = Environment(loader=PackageLoader("pfp_api"))
rfp = RDFProxyWrapper("https://pfp-ts-backend.acdh-ch-dev.oeaw.ac.at/")


class PersonParams(QueryParameters):
    label: str = None


@app.get("/", response_class=RedirectResponse, status_code=302)
def root():
    return "/docs"


@app.get("/persons")
def persons(query_parameters: Annotated[PersonParams, Query()]) -> Page[Person]:
    template = env.get_template("persons.j2")
    query = template.render(dict(query_parameters))
    return rfp.paginate(query=query, model=Person, page=query_parameters.page, size=query_parameters.size)


@app.get("/person/{person_id}")
def person(person_id: str):
    template = env.get_template("person.j2")
    try:
        person_id = urlsafe_b64decode(person_id).decode()
    except binascii.Error:
        raise HTTPException(status_code=404, detail="Person not found")

    query = template.render({"person_id": person_id})
    return rfp.query(query=query, model=PersonDetail)
