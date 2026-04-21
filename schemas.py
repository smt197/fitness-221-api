from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from models import TypeAbonnement, StatutReservation, Role

# Schemas for User
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Role = Role.ADMIN

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: Role
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[Role] = None

# Schemas for Coach
class CoachBase(BaseModel):
    prenom: str
    nom: str
    email: EmailStr
    telephone: Optional[str] = None
    specialite: str

class CoachCreate(CoachBase):
    pass

class CoachResponse(CoachBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas for Activite
class ActiviteBase(BaseModel):
    code: str
    nom: str
    duree: int = Field(gt=0)
    places_max: int = Field(gt=0)

class ActiviteCreate(ActiviteBase):
    pass

class ActiviteResponse(ActiviteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas for Abonne
class AbonneBase(BaseModel):
    prenom: str
    nom: str
    email: EmailStr
    telephone: Optional[str] = None
    date_inscription: datetime
    type_abonnement: TypeAbonnement

class AbonneCreate(AbonneBase):
    pass

class AbonneResponse(AbonneBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas for Reservation
class ReservationBase(BaseModel):
    abonne_id: int
    activite_id: int
    coach_id: int
    date_heure: datetime

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    id: int
    statut: StatutReservation
    created_at: datetime
    
    class Config:
        from_attributes = True
