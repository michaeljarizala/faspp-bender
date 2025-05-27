import importlib
import pkgutil

from fastapi import APIRouter, FastAPI

from app.settings import ROOT_PATH

app = FastAPI(root_path=ROOT_PATH)

router = APIRouter()

# Auto-import all route files in the "routes" directory
package_name = __name__

for _, module_name, _ in pkgutil.iter_modules([__path__[0]]):
    module = importlib.import_module(f"{package_name}.{module_name}")
    if hasattr(module, "router"):
        router.include_router(module.router)
