from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, WriteOnlyMapped
from sqlalchemy.dialects.mysql import DATE, INTEGER, VARCHAR, DECIMAL, SET, ENUM, TINYINT, TEXT
from typing import List
import pymysql



class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

DEC_VALUE = DECIMAL(precision=3, scale=1)
APPROACH_SET = SET("ILS", "LOC", "VOR", "RNAV", "VISUAL", "BC", "ADF", "CIRCLE")


class User(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    username = db.Column(VARCHAR(length=30), nullable=False)
    password = db.Column(TEXT, nullable=False)

    def __repr__(self):
        return f"User: {self.username}"


class Flight(db.Model):
    id = db.Column(INTEGER, primary_key=True)

    date = db.Column(DATE, nullable=False)
    reg = db.Column(ENUM("91", "135"))
    tail_id = db.Column(db.ForeignKey("airplane.id"))
    route = db.Column(VARCHAR(length=100), nullable=False)

    takeoff_day = db.Column(INTEGER, default=0)
    takeoff_night = db.Column(INTEGER, default=0)
    landing_day = db.Column(INTEGER, default=0)
    landing_night = db.Column(INTEGER, default=0)

    flight_time = db.Column(DEC_VALUE, nullable=False)
    crew_position = db.Column(ENUM("PIC", "SIC"))
    student_id = db.Column(db.ForeignKey("student.id"))
    instructor_id = db.Column(db.ForeignKey("instructor.id"))

    solo = db.Column(TINYINT, default=0)
    x_c = db.Column(TINYINT, default=0)
    night = db.Column(DEC_VALUE, default=0.0)
    actual = db.Column(DEC_VALUE, default=0.0)
    simulated = db.Column(DEC_VALUE, default=0.0)
    simulator = db.Column(DEC_VALUE, default=0.0)

    approach = db.Column(APPROACH_SET)
    hold = db.Column(TINYINT, default=0)
    remarks = db.Column(TEXT)

    # equivalent to having an airport object list relationship
    @property
    def airports(self):
        airports = self.route.split("-")
        return [db.session.execute(db.select(Airport).filter_by(identifier=a.strip())).scalar_one_or_none() for a in airports]

    airplane: Mapped["Airplane"] = relationship(back_populates="flights")
    instructor: Mapped["Instructor"] = relationship(back_populates="flights")
    student: Mapped["Student"] = relationship(back_populates="flights")


class Airplane(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    tail_number = db.Column(VARCHAR(length=10), nullable=False)
    model_id = db.Column(db.ForeignKey("model.id"))

    @property
    def num_flights(self):
        return db.session.scalars(db.select(db.func.count(Flight.id)).filter_by(tail_id=self.id)).first()
    
    @property
    def hours(self):
        return float(db.session.scalars(db.select(db.func.sum(Flight.flight_time)).where(Flight.tail_id==self.id)).first())
    
    model: Mapped["Model"] = relationship(back_populates="tails")
    flights: WriteOnlyMapped[List["Flight"]] = relationship(back_populates="airplane", order_by="Flight.date")


class Type_rating(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    descr = db.Column(VARCHAR(length=10), nullable=False)

    model: Mapped["Model"] = relationship(back_populates="type_rating")


class Model(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    descr = db.Column(VARCHAR(length=25), nullable=False)
    nickname = db.Column(VARCHAR(length=25))
    make_id = db.Column(db.ForeignKey("make.id"), nullable=False)
    cat_class = db.Column(ENUM("ASEL", "AMEL"), nullable=False)
    type_rating_id = db.Column(db.ForeignKey("type_rating.id"))
    engine_type = db.Column(ENUM("Piston", "Jet"), nullable=False)
    gear_design = db.Column(ENUM("Tailwheel", "Tricycle"), nullable=False)
    gear_system = db.Column(ENUM("Fixed", "Retractable"), nullable=False)
    is_complex = db.Column(TINYINT, default=0)

    tails: Mapped[List["Airplane"]] = relationship(back_populates="model")
    make: Mapped["Make"] = relationship(back_populates="models")
    type_rating: Mapped["Type_rating"] = relationship(back_populates="model")


class Make(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    descr = db.Column(VARCHAR(length=25), nullable=False)

    models: Mapped[List["Model"]] = relationship(back_populates="make")


class Instructor(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR(length=100), nullable=False)
    flights: WriteOnlyMapped[List["Flight"]] = relationship(back_populates="instructor")


class Student(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR(length=100), nullable=False)
    flights: WriteOnlyMapped[List["Flight"]] = relationship(back_populates="student")


class Airport(db.Model):
    id = db.Column(INTEGER, primary_key=True)

    identifier = db.Column(VARCHAR(length=25), unique=True, nullable=False)
    city = db.Column(VARCHAR(length=100))
    state_id = db.Column(db.ForeignKey("state.id"))
    country_id = db.Column(db.ForeignKey("country.id"))

    state: Mapped["State"] = relationship(back_populates="airports")
    country: Mapped["Country"] = relationship(back_populates="airports")


class Country(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    descr = db.Column(VARCHAR(length=50), nullable=False)
    has_states = db.Column(TINYINT, default=0)

    airports: Mapped[List["Airport"]] = relationship(back_populates="country")


class State(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    descr = db.Column(VARCHAR(length=10), nullable=False)

    airports: Mapped[List["Airport"]] = relationship(
            back_populates="state",
            order_by="Airport.identifier")
