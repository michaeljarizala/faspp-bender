from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.schemas.AuthSchema import TokenCreate, TokenRefresh
from app.modules.auth.services.AuthService import generate_token, renew_token
from app.utils.schema.common_schema import APIResponse
from app.utils.swagger.auth.responses import (auth__token__response,
                                              auth__token_reresh__response)

router = APIRouter(prefix="/v1/auth", tags=["Auth"])


@router.post("/token/", response_model=APIResponse, responses=auth__token__response, description="""Acquire token for the user which can be used in making authorized requests to protected endpoints. Client may choose either `jwt` or `knox` as the authentication mode. `knox` mode does not currently support token renewal (refresh).""")
def token(payload: TokenCreate, db: Session = Depends(get_db), auth_mode: str = 'jwt'):
    generated_token = generate_token(db, payload.username, payload.password, auth_mode)

    return APIResponse(
        success=True, message="You have successfully signed-in.", data=generated_token
    )


@router.post(
    "/token/refresh/",
    response_model=APIResponse,
    responses=auth__token_reresh__response,
)
def refresh_token(payload: TokenRefresh, db: Session = Depends(get_db)):
    generated_token = renew_token(payload.token)

    return APIResponse(
        success=True,
        message="Your token has been successfully renewed.",
        data=generated_token,
    )
