import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class TypeAbonnement(str, enum.Enum):
    MENSUEL = "MENSUEL"
    TRIMESTRIEL = "TRIMESTRIEL"
    ANNUEL = "ANNUEL"

class StatutReservation(str, enum.Enum):
    RESERVEE = "RESERVEE"
    EFFECTUEE = "EFFECTUEE"
    ANNULEE = "ANNULEE"

class Role(str, enum.Enum):
    ADMIN = "ADMIN"
    COACH = "COACH"
    ABONNE = "ABONNE"

class Coach(Base):
    __tablename__ = "coachs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prenom = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telephone = Column(String, nullable=True)
    specialite = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reservations = relationship("Reservation", back_populates="coach")

class Abonne(Base):
    __tablename__ = "abonnes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prenom = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telephone = Column(String, nullable=True)
    date_inscription = Column(DateTime, nullable=False)
    type_abonnement = Column(Enum(TypeAbonnement), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reservations = relationship("Reservation", back_populates="abonne")

class Activite(Base):
    __tablename__ = "activites"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String, unique=True, index=True, nullable=False)
    nom = Column(String, nullable=False)
    duree = Column(Integer, nullable=False) # duree en minutes
    places_max = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reservations = relationship("Reservation", back_populates="activite")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    abonne_id = Column(Integer, ForeignKey("abonnes.id"), nullable=False)
    activite_id = Column(Integer, ForeignKey("activites.id"), nullable=False)
    coach_id = Column(Integer, ForeignKey("coachs.id"), nullable=False)
    date_heure = Column(DateTime, nullable=False)
    statut = Column(Enum(StatutReservation), default=StatutReservation.RESERVEE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('abonne_id', 'activite_id', 'date_heure', name='_abonne_activite_date_uc'),
    )

    abonne = relationship("Abonne", back_populates="reservations")
    activite = relationship("Activite", back_populates="reservations")
    coach = relationship("Coach", back_populates="reservations")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.ADMIN, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
