from fastapi import FastAPI, Query, Response, status

from rdfproxy import Page, SPARQLModelAdapter, QueryParameters

from pfp_api.models import Person
from pfp_api.queries import QueryBuilder


app = FastAPI()


@app.get("/")
def root():
    return Response(status_code=status.HTTP_200_OK)


@app.get("/persons")
def persons(
    page: int = Query(default=1, gt=0), size: int = Query(default=100)
) -> Page[Person]:
    query_parameters = QueryParameters()
    query_parameters.page = page
    query_parameters.size = size
    adapter = SPARQLModelAdapter(
        target="https://pfp-ts-backend.acdh-ch-dev.oeaw.ac.at/",
        query=str(QueryBuilder("person.rq")),
        model=Person,
    )
    return adapter.query(query_parameters)
