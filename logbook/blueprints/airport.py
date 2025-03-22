from flask import Blueprint, render_template, redirect, url_for, flash
from logbook.database import db, Airport, State, Country, Flight
from logbook.blueprints.auth import login_required
from logbook.forms import AirportForm



bp = Blueprint("airport", __name__)


@bp.route("/")
@login_required
def airport_index():
    countries = db.session.scalars(db.select(Country)).all()
    return render_template("airport/airport_index.html", countries=countries)


@bp.route("/<int:id>/get_airports")
@login_required
def get_airports(id):
    country = db.session.query(Country).get_or_404(id)

    if country.has_states:
        airports = db.session.scalars(db.select(Airport)
                .join(State)
                .where(Airport.country_id==id)
                .order_by(State.descr, Airport.identifier)).all()
        states = list(dict.fromkeys([a.state.descr for a in airports]))
        states_value = []
        for s in states:
            state = db.session.execute(db.select(State).filter_by(descr=s)).scalar_one_or_none()
            airports_value = [{"id": a.id, "identifier": a.identifier, "city": a.city,} for a in state.airports]
            states_value.append({
                "descr": state.descr,
                "airports": airports_value,}) 

        response_json = {
                "has_states": True,
                "states": states_value,
                }

    else:
        airports = db.session.scalars(db.select(Airport)
                .where(Airport.country_id==id)
                .order_by(Airport.identifier)).all()
        response_json = {
                "has_states": False,
                "airports": [{
                    "id": a.id,
                    "identifier": a.identifier,
                    "city": a.city,} for a in airports],}

    return response_json


@bp.route("/<int:id>/get_flights")
@login_required
def get_flights(id):
    airport = db.session.query(Airport).get_or_404(id)
    flights = db.session.scalars(db.select(Flight)
            .where(db.func.instr(Flight.route, airport.identifier))
            .order_by(Flight.date)).all()

    return {"flights": [{
        "date": f.date.strftime("%Y-%m-%d"),
        "tail_number": f.airplane.tail_number,
        "route": f.route,} for f in flights],}


@bp.route("/<int:id>/add", methods=["POST","GET"])
@login_required
def add_airport(id):
    form = AirportForm()
    airport = db.session.query(Airport).get_or_404(id)

    form.state_id.choices = [(0, "Choose a State")] + [(s.id, s.descr) for s in db.session.scalars(db.select(State).order_by(State.descr)).all()]
    form.country_id.choices = [(0, "Choose a Country")] + [(c.id, c.descr) for c in db.session.scalars(db.select(Country).order_by(Country.descr)).all()]

    if form.validate_on_submit():
        airport.city = form.city.data

        state_id = form.state_id.data
        new_state = form.new_state.data
        if state_id:
            airport.state_id = state_id
        else:
            airport.state = State(descr=new_state)

        country_id = form.country_id.data
        new_country = form.new_country.data
        if country_id:
            airport.country_id = country_id
        else:
            airport.country = Country(descr=new_country)

        db.session.commit()
        flash(f"{airport.identifier} added successfully.")
        return redirect(url_for("airport.airport_index"))

    return render_template("airport/add_airport.html", form=form, airport=airport)


@bp.route("/<int:id>/edit", methods=["POST","GET"])
@login_required
def edit_airport(id):
    form = AirportForm()
    airport = db.session.query(Airport).get_or_404(id)
    
    form.state_id.choices = [(0, "Choose a State")] + [(s.id, s.descr) for s in db.session.scalars(db.select(State).order_by(State.descr)).all()]
    form.country_id.choices = [(0, "Choose a Country")] + [(c.id, c.descr) for c in db.session.scalars(db.select(Country).order_by(Country.descr)).all()]

    if form.validate_on_submit():
        airport.identifier = form.identifier.data.upper()
        airport.city = form.city.data

        state_id = form.state_id.data
        new_state = form.new_state.data
        if state_id:
            airport.state_id = state_id
        else:
            airport.state = State(descr=new_state)

        country_id = form.country_id.data
        new_country = form.new_country.data
        if country_id:
            airport.country_id = country_id
        else:
            airport.country = Country(descr=new_country)

        db.session.commit()
        flash(f"{airport.identifier} has been updated.")
        return redirect(url_for("airport.airport_index"))

    form.state_id.data = airport.state_id
    form.country_id.data = airport.country_id
    return render_template("airport/edit_airport.html", form=form, airport=airport)

