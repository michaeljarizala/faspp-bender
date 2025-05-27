from app.utils.schema.common_schema import APIErrorResponse

_401_invalid = {
    "model": APIErrorResponse,
    "description": "Unauthorized - Invalid Authorization credentials.",
    "content": {
        "application/json": {
            "example": {
                "success": False,
                "error": {
                    "code": 401,
                    "message": "Authorization credentials are missing."
                }
            }
        }
    },
}

_401_missing = {
    "model": APIErrorResponse,
    "description": "Unauthorized - No Authorization credentials provided.",
    "content": {
        "application/json": {
            "example": {
                "success": False,
                "error": {
                    "code": 401,
                    "message": "Authorization credentials are missing."
                }
            }
        }
    },
}

_401_missing_and_invalid = {
    "model": APIErrorResponse,
    "description": "Unauthorized",
    "content": {
        "application/json": {
            "examples": {
                "MissingCredentials": {
                    "summary": "Missing Credentials",
                    "value": {
                        "success": False,
                        "error": {
                            "code": 401,
                            "message": "Authorization credentials are missing."
                        }
                    }
                },
                "InvalidCredentials": {
                    "summary": "Invalid Credentials",
                    "value": {
                        "success": False,
                        "error": {
                            "code": 401,
                            "message": "Authorization credentials are invalid."
                        }
                    }
                }
            }
        }
    },
}