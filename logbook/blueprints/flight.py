from flask import Blueprint, render_template, redirect, url_for, request, flash
from logbook.database import db, Airplane, Instructor, Student, Flight, Airport
from logbook.database import Model, Make, Type_rating
from logbook.blueprints.auth import login_required
from logbook.forms import FlightForm



bp = Blueprint("flight", __name__)


def process_airports(form_route):
    airports = [a.strip() for a in form_route.upper().split("-")]
    route = ""
    save_airports = []
    airport_list = []
    for airport in airports:
        route += airport + " - "
        airport_in_db = db.session.execute(db.select(Airport).filter_by(identifier=airport)).scalar_one_or_none()
        if not airport_in_db and airport not in airport_list:
            airport_list.append(airport)
            save_airports.append(Airport(identifier=airport))
    
    db.session.add_all(save_airports)
    return route.rstrip(" - ")


@bp.route("/add_flight", methods=["POST","GET"])
@login_required
def add_flight():
    form = FlightForm()
    tails = db.session.scalars(db.select(Airplane)).all() 
    form.tail_id.choices = [(0, "Choose a Tail Number")]
    form.tail_id.choices += [(t.id, f"{t.tail_number} ({t.model.make.descr} {t.model.descr})") for t in tails]
    form.instructor_id.choices = [(0, "Choose a Flight Instructor")] + [(i.id, i.name) for i in db.session.scalars(db.select(Instructor)).all()]
    form.student_id.choices = [(0, "Choose a Student")] + [(s.id, s.name) for s in db.session.scalars(db.select(Student)).all()]

    if form.validate_on_submit():
        new_flight = Flight(
                date=form.date.data,
                reg=form.reg.data,
                route=process_airports(form.route.data),
                takeoff_day=form.takeoff_day.data,
                takeoff_night=form.takeoff_night.data,
                landing_day=form.landing_day.data,
                landing_night=form.landing_night.data,
                flight_time=form.flight_time.data,
                night=form.night.data,
                actual=form.actual.data,
                simulated=form.simulated.data,
                simulator=form.simulator.data,
                approach=request.form.getlist("approach"),
                remarks=form.remarks.data)

        if form.crew_position.data != "NA":
            new_flight.crew_position = form.crew_position.data

        if form.solo.data:
            new_flight.solo = 1

        if form.x_c.data:
            new_flight.x_c = 1

        if form.instructor_id.data:
            new_flight.instructor_id = form.instructor_id.data
        elif form.instructor.data:
            new_flight.instructor = Instructor(name=form.instructor.data.replace("'",""))

        if form.student_id.data:
            new_flight.student_id = form.student_id.data
        elif form.student.data:
            new_flight.student = Student(name=form.student.data.replace("'",""))

        if form.hold.data:
            new_flight.hold = 1

        if form.tail_id.data:
            new_flight.tail_id = form.tail_id.data
        else:
            new_flight.airplane = Airplane(tail_number=form.new_tail_number.data.upper().strip())

        db.session.add(new_flight)
        db.session.commit()
        flash("New flight added.")
        return redirect(url_for("index"))

    return render_template("flight/add_flight.html", form=form)


@bp.route("/<int:id>/edit_flight", methods=["POST","GET"])
@login_required
def edit_flight(id):
    form = FlightForm()
    flight = db.session.query(Flight).get_or_404(id)

    tails = db.session.scalars(db.select(Airplane)).all() 
    form.tail_id.choices = [(0, "Choose a Tail Number")]
    form.tail_id.choices += [(t.id, f"{t.tail_number} ({t.model.make.descr} {t.model.descr})") for t in tails]

    form.instructor_id.choices = [(0, "Choose a Flight Instructor")] + [(i.id, i.name) for i in db.session.scalars(db.select(Instructor)).all()]
    form.student_id.choices = [(0, "Choose a Student")] + [(s.id, s.name) for s in db.session.scalars(db.select(Student)).all()]

    if form.validate_on_submit():
        flight.date = form.date.data
        flight.reg = form.reg.data
        flight.route = process_airports(form.route.data)
        flight.tail_id = form.tail_id.data
        flight.takeoff_day = form.takeoff_day.data
        flight.takeoff_night = form.takeoff_night.data
        flight.landing_day = form.landing_day.data
        flight.landing_night = form.landing_night.data
        flight.flight_time = form.flight_time.data
        flight.night = form.night.data
        flight.actual = form.actual.data
        flight.simulated = form.simulated.data
        flight.simulator = form.simulator.data
        flight.approach = request.form.getlist("approach")
        flight.remarks = form.remarks.data

        if form.crew_position.data != "NA":
            flight.crew_position = form.crew_position.data

        if form.solo.data:
            flight.solo = 1

        if form.x_c.data:
            flight.x_c = 1

        if form.instructor_id.data:
            flight.instructor_id = form.instructor_id.data
        elif form.instructor.data:
            flight.instructor = Instructor(name=form.instructor.data.replace("'",""))

        if form.student_id.data:
            flight.student_id = form.student_id.data
        elif form.student.data:
            flight.student = Student(name=form.student.data.replace("'",""))

        if form.hold.data:
            flight.hold = 1

        if form.tail_id.data:
            flight.tail_id = form.tail_id.data
        else:
            flight.airplane = Airplane(tail_number=form.new_tail_number.data.upper().strip())

        db.session.commit()
        flash("Flight has been updated.")
        return redirect(url_for("index"))
    
    form.tail_id.data = flight.tail_id
    form.approach.data = flight.approach

    if flight.instructor_id:
        form.instructor_id.data = flight.instructor_id
    if flight.student_id:
        form.student_id.data = flight.student_id

    form.remarks.data = flight.remarks
    return render_template("flight/edit_flight.html", form=form, flight=flight)

