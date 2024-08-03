from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.auth import schemas, service, models
from src.database import get_db
from src.utils.cloudinary import upload_avatar

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = service.create_access_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = service.create_user(db, user)
    return db_user

@router.get("/verify/{token}", response_model=schemas.User)
def verify_user(token: str, db: Session = Depends(get_db)):
    user = service.verify_user(db, token)
    return user

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return service.get_current_user(db, token)

@router.get("/me", response_model=schemas.User)
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = service.get_current_user(db, token)
    return user

@router.post("/upload-avatar", response_model=schemas.User)
async def upload_user_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    avatar_url = upload_avatar(file.file)
    current_user.avatar_url = avatar_url
    db.commit()
    db.refresh(current_user)
    return current_user