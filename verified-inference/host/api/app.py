from fastapi import FastAPI
from pydantic import BaseModel

import dependencies
from routers import main_router

dependencies.init_globals()

app = FastAPI()

app.include_router(
    main_router.router,
)

API_TITLE = "teeHost"
API_DESCRIPTION = "Host API for TEE deployment and proxy service."


class ApiInfo(BaseModel):
    title: str
    description: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": API_TITLE,
                "description": API_DESCRIPTION,
            }
        }


def get_api_info() -> ApiInfo:
    return ApiInfo(title=API_TITLE, description=API_DESCRIPTION)


@app.get(
    "/",
    summary="Returns API information",
    description="Returns API information",
    response_description="API information with title and description.",
    response_model=ApiInfo,
)
def root():
    return get_api_info()
