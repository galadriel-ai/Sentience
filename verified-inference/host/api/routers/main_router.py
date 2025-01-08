from typing import List

from fastapi import APIRouter

from routers.routes import tee_router


TAG_ROOT = "root"

router = APIRouter()

routers_to_include: List[APIRouter] = [
    tee_router.router,
]

for router_to_include in routers_to_include:
    router.include_router(router_to_include)
