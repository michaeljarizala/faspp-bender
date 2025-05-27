from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.user.schemas.UserSchema import UserCreate, UserSchema
from app.modules.user.services.UserService import create_user, get_user_by_id
from app.utils.security.authentication import is_user_auth, is_user_or_api_client_auth
from app.utils.schema.common_schema import APISingleResponse, APIErrorResponse


router = APIRouter(prefix="/v1/user", tags=["User"])

@router.get("/", response_model=APISingleResponse|APIErrorResponse)
def get_user(request: dict = Depends(is_user_auth), db: Session = Depends(get_db)):
    if request.is_authenticated:
        user = get_user_by_id(db, request.actor.id)
        
        if not user:
            return APIErrorResponse(
                success=False,
                error={
                    "code": 400,
                    "message": "User not found."
                }
            )

        return APISingleResponse(
            success=True,
            message="User info fetched successfully!",
            data=UserSchema.model_validate(user, from_attributes=True)
        )

@router.get("/{id}/", response_model=APISingleResponse|APIErrorResponse)
def get_user(id: int, request: dict = Depends(is_user_or_api_client_auth), db: Session = Depends(get_db)):

    if request.is_authenticated:
        user = get_user_by_id(db, id)
        
        if not user:
            return APIErrorResponse(
                success=False,
                error={
                    "code": 400,
                    "message": "User not found."
                }
            )

        return APISingleResponse(
            success=True,
            message="User info fetched successfully!",
            data=UserSchema.model_validate(user, from_attributes=True)
        )

@router.post("/signup/", response_model=APISingleResponse|APIErrorResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user
