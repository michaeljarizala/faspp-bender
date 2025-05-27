from app.utils.schema.common_schema import APIErrorResponse, APIResponse

"""Token Response"""
auth__token__response = {
    200: {
        "model": APIResponse,
        "description": "Successul login",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "You have successfully signed-in.",
                    "data": {
                        "access": "<jwt token string>",
                        "refresh": "<jwt refresh token string>",
                    },
                }
            }
        },
    },
    401: {
        "model": APIErrorResponse,
        "description": "Unauthorized - Invalid Credentials",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "error": {"code": 401, "message": "Invalid credentials."},
                }
            }
        },
    },
    422: {
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
    },
}


"""Token Refresh Response"""
auth__token_reresh__response = {
    200: {
        "model": APIResponse,
        "description": "Successul login",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Your token has been successfully renewed.",
                    "data": {
                        "access": "<jwt token string>",
                    },
                }
            }
        },
    },
    401: {
        "model": APIErrorResponse,
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "examples": {
                    "InvalidToken": {
                        "summary": "Invalid Refresh Token",
                        "value": {
                            "success": False,
                            "error": {"code": 401, "message": "Invalid refresh token."},
                        },
                    },
                    "ExpiredToken": {
                        "summary": "Expired Refresh Token",
                        "value": {
                            "success": False,
                            "error": {"code": 401, "message": "Refresh token expired."},
                        },
                    },
                }
            }
        },
    },
    422: {
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
                                    "field": "body.token",
                                    "message": "Field required",
                                    "type": "missing",
                                }
                            ]
                        },
                    },
                }
            }
        },
    },
}
