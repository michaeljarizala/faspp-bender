from fastapi import APIRouter

"""
Routes for v1
"""
# Auth Routes
from app.modules.auth.routes.v1 import router as module__auth__routers__v1
# Common Routes
from app.modules.common.routes.v1 import router as module__common__routers__v1

from app.settings import ROOT_PATH

router = APIRouter()

# Version 1 Routes
router.include_router(module__auth__routers__v1)
router.include_router(module__common__routers__v1)

