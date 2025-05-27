from fastapi import FastAPI
from fastapi.exceptions import (HTTPException, RequestValidationError,
                                ResponseValidationError)
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes import router
from app.settings import HOST, PORT, ROOT_PATH
from app.utils.exception import (
    custom_db_integrity_error_handler, custom_http_exception_handler,
    custom_http_internal_server_error_handler,
    custom_http_request_validation_exception_handler,
    custom_http_response_validation_exception_handler,
    custom_http_starlette_exception_handler)
from app.utils.swagger.documentation import description

app = FastAPI(
    title="FaSPP Bender API Documentation", root_path=ROOT_PATH,
    description=description,
    docs_url="/v1/docs/", redoc_url="/v1/redoc/"
)

"""
Overrides to Exception Handlers
This is important in order to maintain uniform format
to both successful and error API responses as defined
in our documentation.
"""
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(
    ResponseValidationError, custom_http_response_validation_exception_handler
)
app.add_exception_handler(
    RequestValidationError, custom_http_request_validation_exception_handler
)
app.add_exception_handler(Exception, custom_http_internal_server_error_handler)
app.add_exception_handler(IntegrityError, custom_db_integrity_error_handler)
app.add_exception_handler(
    StarletteHTTPException, custom_http_starlette_exception_handler
)

# Include all routes dynamically
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT, reload=True)
