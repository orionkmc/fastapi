from fastapi import APIRouter, Query, Path
from enum import Enum
from typing import Annotated
from pydantic import BaseModel


basic_router = APIRouter()


# Basic
@basic_router.get("/basic/", tags=["Basic"])
async def root():
    return {"message": "Hello World"}


# Path Parameters
@basic_router.get("/path_parameters/items/{item_id}", tags=["Path Parameters"])
async def read_item_path_params(item_id: int):
    return {"item_id": item_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@basic_router.get("/path_parameters/models/{model_name}", tags=["Path Parameters"])
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@basic_router.get("/type_conversion/items/{item_id}", tags=["Type Conversion"])
async def read_item_type_conversion(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@basic_router.get("/multiples_param/users/{user_id}/items/{item_id}", tags=["Multiples Param"])
async def read_user_item_multiples_param(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@basic_router.get("/required_params/items/{item_id}", tags=["Required Params"])
async def read_user_item_required_params(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


# Body request
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@basic_router.post("/request_body/items/", tags=["Request Body"])
async def create_item_request_body(item: Item):
    return item


# Request body + path + query parameters
@basic_router.put("/request_body/items/{item_id}", tags=["Request Body"])
async def update_item_request_body(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


# Query Parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@basic_router.get("/query_parameters/items/", tags=["Query Parameter"])
async def read_item_query_params(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@basic_router.get("/query_parameters/items/{item_id}", tags=["Query Parameter"])
async def read_item_optional_params(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@basic_router.get("/query_parameters/validations/items/", tags=["Query Parameter"])
async def read_items_validations(q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = "fixedquery"):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@basic_router.get("/query_parameters/multiple_values/items/", tags=["Query Parameter"])
async def read_items_multiple_values(q: Annotated[list[str] | None, Query(
    alias="item-query",
    description="Query string for the items to search in the database that have a good match"
)] = None):
    query_items = {"q": q}
    return query_items


@basic_router.get("/query_parameters/multiple_values_defaults/items/", tags=["Query Parameter"])
async def read_items_multiple_values_defaults(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items


@basic_router.get("/query_parameters/deprecating_param/items/", tags=["Query Parameter"])
async def read_items_deprecating_param(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@basic_router.get("/number_validations/items/{item_id}", tags=["Number Validations"])
async def read_items_number_validations(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1, le=1000)],
    q: str,
    size: Annotated[float, Path(g=0, lt=10.5)],
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
