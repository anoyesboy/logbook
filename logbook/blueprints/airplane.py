from flask import Blueprint, render_template, redirect, url_for, flash
from logbook.database import db, Airplane, Make, Model, Type_rating
from logbook.blueprints.auth import login_required
from logbook.forms import AirplaneForm, MakeModelForm



bp = Blueprint("airplane", __name__)


@bp.route("/")
@login_required
def airplane_index():
    airplanes = db.session.scalars(db.select(Airplane).join(Model).join(Make).order_by(Make.descr, Model.descr)).all()
    return render_template("airplane/airplane_index.html", airplanes=airplanes)


@bp.route("/<int:id>/get_airplane")
@login_required
def get_airplane(id):
    airplane = db.session.query(Airplane).get_or_404(id)
    if airplane.model.nickname:
        nickname = airplane.model.nickname
    else:
        nickname = ""
    if airplane.model.type_rating:
        type_rating = airplane.model.type_rating.descr
    else:
        type_rating = ""
    if airplane.model.is_complex:
        is_complex = "Yes"
    else:
        is_complex = "No"
    flights = db.session.execute(airplane.flights.select()).scalars()
    return {"id": airplane.id,
            "tail_number": airplane.tail_number,
            "make": airplane.model.make.descr,
            "model": airplane.model.descr,
            "nickname": airplane.model.nickname,
            "cat_class": airplane.model.cat_class,
            "type_rating": type_rating,
            "engine_type": airplane.model.engine_type,
            "gear_design": airplane.model.gear_design,
            "gear_system": airplane.model.gear_system,
            "is_complex": is_complex,
            "flights": [{
                "date": f.date.strftime("%Y-%m-%d"),
                "route": f.route,
                "flight_time": f.flight_time,} for f in flights],}


@bp.route("/<int:id>/add", methods=["POST","GET"])
def add_airplane(id):
    form = AirplaneForm()

    form.model_id.choices = [(0, "Choose a  Make and Model")]
    form.model_id.choices += [(m.id, f"{m.make.descr} {m.descr}") \
            for m in db.session.scalars(db.select(Model).join(Make).order_by(Make.descr)).all()]

    form.make_id.choices = [(0, "Choose a Manufacturer")]
    form.make_id.choices += [(m.id, m.descr) for m in db.session.scalars(db.select(Make).order_by(Make.descr)).all()]

    form.type_rating_id.choices = [(0, "Choose a Type Rating")]
    form.type_rating_id.choices += [(tr.id, tr.descr) \
            for tr in db.session.scalars(db.select(Type_rating).order_by(Type_rating.descr)).all()]

    airplane = db.session.query(Airplane).get_or_404(id)

    if form.validate_on_submit():
        model_id = form.model_id.data
        if model_id:
            airplane.model_id = model_id

        else:
            new_model = Model(
                    descr=form.new_model.data,
                    cat_class=form.cat_class.data,
                    engine_type=form.engine_type.data,
                    gear_design=form.gear_design.data,
                    gear_system=form.gear_system.data)

            if form.is_complex.data:
                new_model.is_complex = 1

            make_id = form.make_id.data
            new_make = form.new_make.data
            if make_id:
                new_model.make_id = make_id
            else:
                new_model.make = Make(descr=new_make)

            type_rating_id = form.type_rating_id.data
            new_type_rating = form.new_type_rating.data
            if type_rating_id:
                new_model.type_rating_id = type_rating_id
            elif new_type_rating:
                new_model.type_rating = Type_rating(descr=new_type_rating)

            airplane.model = new_model

        db.session.commit()
        flash("Airplane added succuessfully.")
        return redirect(url_for("airplane.airplane_index"))

    return render_template("airplane/add_airplane.html", form=form, airplane=airplane)


@bp.route("/<int:id>/edit", methods=["POST","GET"])
def edit_airplane(id):
    form = AirplaneForm()
    airplane = db.session.query(Airplane).get_or_404(id)

    form.model_id.choices = [(0, "Choose a Make and Model")]
    form.model_id.choices += [(m.id, f"{m.make.descr} {m.descr}") \
            for m in db.session.scalars(db.select(Model).join(Make).order_by(Make.descr)).all()]

    form.make_id.choices = [(0, "Choose a Manufacturer")]
    form.make_id.choices += [(m.id, m.descr) for m in db.session.scalars(db.select(Make).order_by(Make.descr)).all()]

    form.type_rating_id.choices = [(0, "Choose a Type Rating")]
    form.type_rating_id.choices += [(tr.id, tr.descr) \
            for tr in db.session.scalars(db.select(Type_rating).order_by(Type_rating.descr)).all()]

    if form.validate_on_submit():
        model_id = form.model_id.data
        if model_id:
            airplane.model_id = model_id

        else:
            new_model = form.new_model.data

            if new_model != airplane.model.descr:
                new_model = Model(
                        descr=new_model,
                        cat_class=form.cat_class.data,
                        engine_type=form.engine_type.data,
                        gear_design=form.gear_design.data,
                        gear_system=form.gear_system.data)

                if form.is_complex.data:
                    new_model.is_complex = 1

                make_id = form.make_id.data
                new_make = form.new_make.data
                if make_id:
                    new_model.make_id = make_id
                else:
                    new_model.make = Make(descr=new_make)

                type_rating_id = form.type_rating_id.data
                new_type_rating = form.new_type_rating.data
                if type_rating_id:
                    new_model.type_rating_id = type_rating_id
                elif new_type_rating:
                    new_model.type_rating = Type_rating(descr=new_type_rating)

                airplane.model = new_model

        db.session.commit()
        flash("Airplane updated succuessfully.")
        return redirect(url_for("airplane.airplane_index"))

    form.model_id.data = airplane.model_id
    form.make_id.data = airplane.model.make_id
    if airplane.model.type_rating_id:
        form.type_rating_id.data = airplane.model.type_rating_id

    return render_template("airplane/edit_airplane.html", form=form, airplane=airplane)

