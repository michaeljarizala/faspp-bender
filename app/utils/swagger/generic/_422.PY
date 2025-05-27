from app.utils.schema.common_schema import APIErrorResponse

_422_validation_error = {
    "model": APIErrorResponse,
    "description": "Validation Error",
    "content": {
        "application/json": {
            "example": {
                "success": False,
                "error": {
                    "code": 422,
                    "message": "Request validation failed. Check input fields.",
                    "data": {
                        "errors": [
                            {
                                "field": "body.password",
                                "message": "Field required",
                                "type": "missing",
                            }
                        ]
                    },
                },
            }
        }
    },
}