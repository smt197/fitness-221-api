from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from database import engine, Base, get_db
import models, schemas
from services import (
    AuthService, CoachService, AbonneService, 
    ActiviteService, ReservationService
)
import jwt
from jwt import PyJWTError as JWTError
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness-221 API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "your-secret-key-for-jwt"), algorithms=["HS256"])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = AuthService.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def require_role(roles: List[models.Role]):
    def role_checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Not authorized")
        return current_user
    return role_checker

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API de gestion du studio FITNESS 221 !"}

# Auth Routes
@app.post("/api/auth/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = AuthService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return AuthService.create_user(db=db, user=user)

@app.post("/api/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = AuthService.get_user_by_email(db, form_data.username)
    if not user or not AuthService.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = AuthService.create_access_token(data={"email": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# Coach Routes
@app.get("/api/coachs", response_model=List[schemas.CoachResponse])
def get_coachs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return CoachService.get_coachs(db, skip=skip, limit=limit)

@app.get("/api/coachs/{id}", response_model=schemas.CoachResponse)
def get_coach(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    coach = CoachService.get_coach(db, id)
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    return coach

@app.post("/api/coachs", response_model=schemas.CoachResponse, status_code=status.HTTP_201_CREATED)
def create_coach(coach: schemas.CoachCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role([models.Role.ADMIN]))):
    db_coach = CoachService.get_coach_by_tel(db, tel=coach.telephone)
    if db_coach:
        raise HTTPException(status_code=400, detail="Numéro de téléphone déjà existant")
    return CoachService.create_coach(db, coach)

@app.put("/api/coachs/{id}", response_model=schemas.CoachResponse)
def update_coach(id: int, coach: schemas.CoachCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role([models.Role.ADMIN]))):
    updated_coach = CoachService.update_coach(db, id, coach)
    if not updated_coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    return updated_coach

@app.delete("/api/coachs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coach(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role([models.Role.ADMIN]))):
    deleted = CoachService.delete_coach(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Coach not found")
    return None

# Activités Routes
@app.get("/api/activites", response_model=List[schemas.ActiviteResponse])
def get_activites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return ActiviteService.get_activites(db, skip=skip, limit=limit)

@app.get("/api/activites/{id}", response_model=schemas.ActiviteResponse)
def get_activite(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    activite = ActiviteService.get_activite(db, id)
    if not activite:
        raise HTTPException(status_code=404, detail="Activite not found")
    return activite

@app.post("/api/activites", response_model=schemas.ActiviteResponse, status_code=status.HTTP_201_CREATED)
def create_activite(activite: schemas.ActiviteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role([models.Role.ADMIN]))):
    return ActiviteService.create_activite(db, activite)

@app.put("/api/activites/{id}", response_model=schemas.ActiviteResponse)
def update_activite(id: int, activite: schemas.ActiviteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role([models.Role.ADMIN]))):
    updated_activite = ActiviteService.update_activite(db, id, activite)
    if not updated_activite:
        raise HTTPException(status_code=404, detail="Activite not found")
    return updated_activite

@app.delete("/api/activites/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activite(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role([models.Role.ADMIN]))):
    deleted = ActiviteService.delete_activite(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Activite not found")
    return None

# Abonnes Routes
@app.get("/api/abonnes", response_model=List[schemas.AbonneResponse])
def get_abonnes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return AbonneService.get_abonnes(db, skip=skip, limit=limit)

@app.get("/api/abonnes/{id}", response_model=schemas.AbonneResponse)
def get_abonne(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    abonne = AbonneService.get_abonne(db, id)
    if not abonne:
        raise HTTPException(status_code=404, detail="Abonne not found")
    return abonne

@app.post("/api/abonnes", response_model=schemas.AbonneResponse, status_code=status.HTTP_201_CREATED)
def create_abonne(abonne: schemas.AbonneCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role([models.Role.ADMIN]))):
    db_abonne = AbonneService.get_abonne_by_tel(db, tel=abonne.telephone)
    if db_abonne:
        raise HTTPException(status_code=400, detail="Numéro de téléphone déjà existant")
    return AbonneService.create_abonne(db, abonne)

@app.put("/api/abonnes/{id}", response_model=schemas.AbonneResponse)
def update_abonne(id: int, abonne: schemas.AbonneCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role([models.Role.ADMIN]))):
    updated_abonne = AbonneService.update_abonne(db, id, abonne)
    if not updated_abonne:
        raise HTTPException(status_code=404, detail="Abonne not found")
    return updated_abonne

@app.delete("/api/abonnes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_abonne(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role([models.Role.ADMIN]))):
    deleted = AbonneService.delete_abonne(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Abonne not found")
    return None

# Reservations Routes
@app.get("/api/reservations", response_model=List[schemas.ReservationResponse])
def get_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return ReservationService.get_reservations(db, skip=skip, limit=limit)

@app.get("/api/reservations/{id}", response_model=schemas.ReservationResponse)
def get_reservation(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    reservation = ReservationService.get_reservation(db, id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@app.post("/api/reservations", response_model=schemas.ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        return ReservationService.create_reservation(db, reservation)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/reservations/{id}", response_model=schemas.ReservationResponse)
def update_reservation(id: int, reservation: schemas.ReservationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        updated_reservation = ReservationService.update_reservation(db, id, reservation)
        if not updated_reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return updated_reservation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/reservations/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    deleted = ReservationService.delete_reservation(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return None
