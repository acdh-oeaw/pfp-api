import logging
import math
from collections.abc import Iterator
from rdfproxy.constructor import QueryConstructor
from rdfproxy.utils.models import QueryParameters
from rdfproxy.sparql_strategies import HttpxStrategy
from rdfproxy.mapper import ModelBindingsMapper
from rdfproxy.utils.models import Page
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class RDFProxyWrapper:
    def __init__(self, target: str):
        self.strategy = HttpxStrategy(target)

    def query(self, query, model, query_parameters) -> BaseModel:
        query_constructor = QueryConstructor(query=query, query_parameters=query_parameters, model=model)
        items_query = query_constructor.get_items_query()
        logger.debug(items_query)
        print(items_query)

        items_query_bindings: Iterator[dict] = self.strategy.query(items_query)
        mapper = ModelBindingsMapper(model, *items_query_bindings)
        items: list[BaseModel] = mapper.get_models()

        return items

    def paginate(self, query, model, page=1, size=100) -> Page[BaseModel]:
        qp = QueryParameters().parse_obj({"page": page, "size": size})
        query_constructor = QueryConstructor(query=query, query_parameters=qp, model=model)
        count_query = query_constructor.get_count_query()
        logger.debug(count_query)
        print(count_query)

        count_query_bindings: Iterator[dict] = self.strategy.query(count_query)
        total: int = int(next(count_query_bindings)["cnt"])
        pages: int = math.ceil(total / size)

        items = self.query(query, model, qp)

        return Page(items=items, page=page, size=size, total=total, pages=pages)
