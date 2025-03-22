from flask import Blueprint, render_template, url_for
from logbook.database import db, Flight, Airplane, Model, Airport
from logbook.blueprints.auth import login_required
from datetime import datetime



bp = Blueprint("logbook", __name__)



def get_name_or_none(person):
    if person:
        return person.name
    else:
        return "None"



@bp.route("/")
@login_required
def index():
    totals = {}
    totals["TT"] = float(db.session.scalars(db.select(db.func.sum(Flight.flight_time))).first() or 0)
    totals["SE"] = float(db.session.scalars(db.select(db.func.sum(Flight.flight_time)).join(Airplane).join(Model).where(Model.cat_class=="ASEL")).first() or 0)
    totals["ME"] = float(db.session.scalars(db.select(db.func.sum(Flight.flight_time)).join(Airplane).join(Model).where(Model.cat_class=="AMEL")).first() or 0)
    totals["PIC"] = float(db.session.scalars(db.select(db.func.sum(Flight.flight_time)).filter_by(crew_position="PIC")).first() or 0)
    totals["Turbine"] = float(db.session.scalars(db.select(db.func.sum(Flight.flight_time)).join(Airplane).join(Model).where(Model.engine_type=="Jet")).first() or 0)
    totals["TurbinePIC"] = float(db.session.scalars(db.select(db.func.sum(Flight.flight_time)).join(Airplane).join(Model)
            .where(Flight.crew_position=="PIC").where(Model.engine_type=="Jet")).first() or 0)
    totals["actual"] = float(db.session.scalars(db.select(db.func.sum(Flight.actual))).first() or 0)
    totals["instrument"] = totals.get("actual") + float(db.session.scalars(db.select(db.func.sum(Flight.simulated))).first() or 0)
    totals["x_c"] = float(db.session.scalars(db.select(db.func.sum(Flight.flight_time)).where(Flight.x_c==1)).first() or 0)
    totals["night"] = float(db.session.scalars(db.select(db.func.sum(Flight.night))).first() or 0)

    new_airports = db.session.scalars(db.select(Airport).where(
        db.func.isnull(Airport.city) & \
                db.func.isnull(Airport.state_id) & \
                db.func.isnull(Airport.country_id))).all()

    new_airplanes = db.session.scalars(db.select(Airplane).where(db.func.isnull(Airplane.model_id))).all()

    return render_template("index.html", totals=totals, new_airports=new_airports, new_airplanes=new_airplanes)


@bp.route("/display_logbook/")
@login_required
def display_logbook():
    years = db.session.scalars(db.select(db.func.year(Flight.date)).distinct().order_by(Flight.date.desc())).all()
    return render_template("logbook/display_logbook.html", years=years)


@bp.route("/get_months/<int:year>")
@login_required
def get_months(year):
    months_in_year = db.session.scalars(db.select(db.func.month(Flight.date)).distinct().where(db.func.year(Flight.date)==year)).all()
    months = []
    for m in range(1, 13):
        if m in months_in_year:
            in_year = 1
        else:
            in_year = 0
        months += [{"id": m, "name": datetime(2020, m, 1).strftime("%b").upper(), "in_year": in_year,}]
    return {"cur_year": year,
            "months": months,}


@bp.route("/get_flights/<int:year>/<int:month>")
@login_required
def get_flights(year, month):
    flights = db.session.scalars(db.select(Flight).where(db.func.year(Flight.date)==year).where(db.func.month(Flight.date)==month)).all()
    return {"cur_month": month,
            "cur_year": year,
            "flights": [{
                "id": f.id,
                "date": f.date.strftime("%Y-%m-%d"),
                "tail": f.airplane.tail_number,
                "flight_time": f.flight_time,
                "route": f.route,} for f in flights],}


@bp.route("/get_flight_detail/<int:id>")
@login_required
def get_flight_detail(id):
    flight = db.session.query(Flight).get_or_404(id)

    airports = []
    for a in flight.airports:
        if a.city:
            city = a.city
            country = a.country.descr
            if a.state:
                state = a.state.descr
            else:
                state = ""
        airports.append({
            "identifier": a.identifier,
            "city": city,
            "state": state,
            "country": country,
            })

    if flight.crew_position:
        crew_position = flight.crew_position
    else:
        crew_position = "NA"

    return {"id": flight.id,
            "date": flight.date.strftime("%Y-%m-%d"),
            "reg": flight.reg,
            "tail": flight.airplane.tail_number,
            "make": flight.airplane.model.make.descr,
            "model": flight.airplane.model.descr,
            "route": flight.route,
            "airports": airports,
            "takeoff_day": flight.takeoff_day,
            "takeoff_night": flight.takeoff_night,
            "landing_day": flight.landing_day,
            "landing_night": flight.landing_night,
            "flight_time": flight.flight_time,
            "crew_position": crew_position,
            "instructor": get_name_or_none(flight.instructor),
            "student": get_name_or_none(flight.student),
            "solo": flight.solo,
            "x_c": flight.x_c,
            "night": flight.night,
            "actual": flight.actual,
            "simulated": flight.simulated,
            "simulator": flight.simulator,
            "approach": [a for a in flight.approach],
            "hold": flight.hold,
            "remarks": flight.remarks,}

