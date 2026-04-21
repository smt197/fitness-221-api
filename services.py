from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models, schemas
from datetime import datetime, timedelta
import jwt
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")
ALGORITHM = "HS256"

class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def create_user(db: Session, user: schemas.UserCreate):
        hashed_password = AuthService.get_password_hash(user.password)
        db_user = models.User(email=user.email, password=hashed_password, role=user.role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

class CoachService:
    @staticmethod
    def get_coachs(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Coach).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_coach(db: Session, coach_id: int):
        return db.query(models.Coach).filter(models.Coach.id == coach_id).first()

    @staticmethod
    def get_coach_by_tel(db: Session, tel: str):
        return db.query(models.Coach).filter(models.Coach.telephone == tel).first()

    @staticmethod
    def create_coach(db: Session, coach: schemas.CoachCreate):
        db_coach = models.Coach(**coach.model_dump())
        db.add(db_coach)
        db.commit()
        db.refresh(db_coach)
        return db_coach

    @staticmethod
    def update_coach(db: Session, coach_id: int, coach: schemas.CoachCreate):
        db_coach = CoachService.get_coach(db, coach_id)
        if db_coach:
            for key, value in coach.model_dump().items():
                setattr(db_coach, key, value)
            db.commit()
            db.refresh(db_coach)
        return db_coach

    @staticmethod
    def delete_coach(db: Session, coach_id: int):
        db_coach = CoachService.get_coach(db, coach_id)
        if db_coach:
            has_reserved = any(r.statut == models.StatutReservation.RESERVEE for r in db_coach.reservations)
            if has_reserved:
                raise HTTPException(status_code=400, detail="Impossible de supprimer un coach ayant des réservations en statut RESERVEE.")
            db.delete(db_coach)
            db.commit()
        return db_coach

class AbonneService:
    @staticmethod
    def get_abonnes(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Abonne).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_abonne(db: Session, abonne_id: int):
        return db.query(models.Abonne).filter(models.Abonne.id == abonne_id).first()

    @staticmethod
    def get_abonne_by_tel(db: Session, tel: str):
        return db.query(models.Abonne).filter(models.Abonne.telephone == tel).first()

    @staticmethod
    def _validate_abonne(abonne: schemas.AbonneCreate):
        if abonne.date_inscription.replace(tzinfo=None) > datetime.utcnow():
            raise HTTPException(status_code=400, detail="La date d'inscription ne peut pas être dans le futur.")

    @staticmethod
    def create_abonne(db: Session, abonne: schemas.AbonneCreate):
        AbonneService._validate_abonne(abonne)
        db_abonne = models.Abonne(**abonne.model_dump())
        db.add(db_abonne)
        db.commit()
        db.refresh(db_abonne)
        return db_abonne

    @staticmethod
    def update_abonne(db: Session, abonne_id: int, abonne: schemas.AbonneCreate):
        AbonneService._validate_abonne(abonne)
        db_abonne = AbonneService.get_abonne(db, abonne_id)
        if db_abonne:
            for key, value in abonne.model_dump().items():
                setattr(db_abonne, key, value)
            db.commit()
            db.refresh(db_abonne)
        return db_abonne

    @staticmethod
    def delete_abonne(db: Session, abonne_id: int):
        db_abonne = AbonneService.get_abonne(db, abonne_id)
        if db_abonne:
            if len(db_abonne.reservations) > 0:
                raise HTTPException(status_code=400, detail="Impossible de supprimer un abonné ayant des réservations.")
            db.delete(db_abonne)
            db.commit()
        return db_abonne

class ActiviteService:
    @staticmethod
    def get_activites(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Activite).offset(skip).limit(limit).all()

    @staticmethod
    def get_activite(db: Session, activite_id: int):
        return db.query(models.Activite).filter(models.Activite.id == activite_id).first()

    @staticmethod
    def _validate_activite(db: Session, activite: schemas.ActiviteCreate, activite_id: int = None):
        existing = db.query(models.Activite).filter(models.Activite.code == activite.code).first()
        if existing and existing.id != activite_id:
            raise HTTPException(status_code=400, detail="Le code d'activité existe déjà.")

    @staticmethod
    def create_activite(db: Session, activite: schemas.ActiviteCreate):
        ActiviteService._validate_activite(db, activite)
        db_activite = models.Activite(**activite.model_dump())
        db.add(db_activite)
        db.commit()
        db.refresh(db_activite)
        return db_activite

    @staticmethod
    def update_activite(db: Session, activite_id: int, activite: schemas.ActiviteCreate):
        ActiviteService._validate_activite(db, activite, activite_id)
        db_activite = ActiviteService.get_activite(db, activite_id)
        if db_activite:
            for key, value in activite.model_dump().items():
                setattr(db_activite, key, value)
            db.commit()
            db.refresh(db_activite)
        return db_activite
        
    @staticmethod
    def delete_activite(db: Session, activite_id: int):
        db_activite = ActiviteService.get_activite(db, activite_id)
        if db_activite:
            if len(db_activite.reservations) > 0:
                raise HTTPException(status_code=400, detail="Impossible de supprimer une activité ayant des réservations.")
            db.delete(db_activite)
            db.commit()
        return db_activite

class ReservationService:
    @staticmethod
    def get_reservations(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Reservation).offset(skip).limit(limit).all()

    @staticmethod
    def get_reservation(db: Session, reservation_id: int):
        return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    @staticmethod
    def _validate_reservation(db: Session, reservation: schemas.ReservationCreate, reservation_id: int = None):
        if reservation.date_heure.replace(tzinfo=None) <= datetime.utcnow():
            raise HTTPException(status_code=400, detail="La date et heure de la réservation doivent être dans le futur.")
        
        conflict_coach = db.query(models.Reservation).filter(
            models.Reservation.coach_id == reservation.coach_id,
            models.Reservation.date_heure == reservation.date_heure,
            models.Reservation.statut != models.StatutReservation.ANNULEE
        )
        if reservation_id:
            conflict_coach = conflict_coach.filter(models.Reservation.id != reservation_id)
        if conflict_coach.first():
            raise HTTPException(status_code=400, detail="Le coach a déjà une réservation à cette date et heure.")

        conflict_abonne = db.query(models.Reservation).filter(
            models.Reservation.abonne_id == reservation.abonne_id,
            models.Reservation.activite_id == reservation.activite_id,
            models.Reservation.date_heure == reservation.date_heure,
            models.Reservation.statut != models.StatutReservation.ANNULEE
        )
        if reservation_id:
            conflict_abonne = conflict_abonne.filter(models.Reservation.id != reservation_id)
        if conflict_abonne.first():
            raise HTTPException(status_code=400, detail="L'abonné a déjà réservé cette activité à ce créneau.")

        activite = db.query(models.Activite).filter(models.Activite.id == reservation.activite_id).first()
        if not activite:
            raise HTTPException(status_code=404, detail="Activité non trouvée.")
        
        reserved_count = db.query(models.Reservation).filter(
            models.Reservation.activite_id == reservation.activite_id,
            models.Reservation.date_heure == reservation.date_heure,
            models.Reservation.statut == models.StatutReservation.RESERVEE
        )
        if reservation_id:
            reserved_count = reserved_count.filter(models.Reservation.id != reservation_id)
            
        if reserved_count.count() >= activite.places_max:
            raise HTTPException(status_code=400, detail="Le nombre maximum de places pour cette activité a été atteint.")

    @staticmethod
    def create_reservation(db: Session, reservation: schemas.ReservationCreate):
        ReservationService._validate_reservation(db, reservation)
        db_reservation = models.Reservation(**reservation.model_dump(), statut=models.StatutReservation.RESERVEE)
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        return db_reservation

    @staticmethod
    def update_reservation(db: Session, reservation_id: int, reservation: schemas.ReservationCreate):
        ReservationService._validate_reservation(db, reservation, reservation_id)
        db_reservation = ReservationService.get_reservation(db, reservation_id)
        if db_reservation:
            for key, value in reservation.model_dump().items():
                setattr(db_reservation, key, value)
            db.commit()
            db.refresh(db_reservation)
        return db_reservation
        
    @staticmethod
    def delete_reservation(db: Session, reservation_id: int):
        db_reservation = ReservationService.get_reservation(db, reservation_id)
        if db_reservation:
            db.delete(db_reservation)
            db.commit()
        return db_reservation
