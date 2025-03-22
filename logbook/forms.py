from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField, IntegerField, DecimalField
from wtforms import SelectField, SelectMultipleField, BooleanField, TextAreaField, FormField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import InputRequired, ValidationError, StopValidation, NumberRange, Optional, Length

from werkzeug.security import check_password_hash
from logbook.database import db, User



class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class LoginForm(UserForm):
    def validate_username(form, field):
        user = db.session.execute(db.select(User).filter_by(username=field.data)).scalar_one_or_none()
        if not user:
            raise ValidationError("Incorrect username!")

    def validate_password(form, field):
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one_or_none()
        if user and not check_password_hash(user.password, field.data):
            raise ValidationError("Incorrect pasword!")


class RegistrationForm(UserForm):
    pass


class FlightForm(FlaskForm):
    date = DateField("Date", validators=[InputRequired()])
    reg = RadioField("Regulation", choices=[("91", "Part 91"), ("135", "Part 135")], validators=[InputRequired()])
    route = StringField("Route", validators=[InputRequired()])
    tail_id = SelectField("Tail Number", coerce=int)
    new_tail_number = StringField("New Tail Number")
    takeoff_day = IntegerField("Day Takeoffs", validators=[NumberRange(min=0), Optional()])
    takeoff_night = IntegerField("Night Takeoffs", validators=[NumberRange(min=0), Optional()])
    landing_day = IntegerField("Day Landings", validators=[NumberRange(min=0), Optional()])
    landing_night = IntegerField("Night Landings", validators=[NumberRange(min=0), Optional()])
    crew_position = RadioField("Crew Member Position",
            choices=[("PIC", "Pilot in Command"), ("SIC", "Second in Command"), ("NA", "Not Applicable")])
    flight_time = DecimalField("Flight Time", places=1, validators=[NumberRange(min=0, max=20, message="Valid range 0-20.0 hrs.")])
    night = DecimalField("Night Time", places=1, validators=[NumberRange(min=0, max=20, message="Valid range 0-20.0 hrs.")])
    solo = BooleanField("Solo")
    x_c = BooleanField("Cross-Country")
    actual = DecimalField("Actual Instrument", places=1, validators=[NumberRange(min=0, max=20, message="Valid range 0-20.0 hrs.")])
    simulated = DecimalField("Simulated Instrument", places=1, validators=[NumberRange(min=0, max=8, message="Valid range 0-8.0 hrs.")])
    simulator = DecimalField("Simulator Time", places=1, validators=[NumberRange(min=0, max=8, message="Valid range 0-8.0 hrs.")])
    instructor_id = SelectField("Flight Instructor", coerce=int)
    student_id = SelectField("Student", coerce=int)
    instructor = StringField("Instructor Name", validators=[Optional()])
    student = StringField("Student Name", validators=[Optional()])
    approach = MultiCheckboxField("Approach(s)", choices=["ILS","LOC","VOR","RNAV","VISUAL","BC","ADF","CIRCLE"])
    hold = BooleanField("Holding")
    remarks = TextAreaField("Remarks", validators=[Optional()])

    def validate_route(form, field):
        airports = field.data.split("-")
        airports = [airport.strip() for airport in airports]
        for airport in airports:
            if not airport.isalnum():
                raise ValidationError(f"{airport} is not alpha-numeric.")
            if len(airport) < 3 or len(airport) > 4:
                raise ValidationError(f"{airport} should be 3 or 4 characters long.")

    def validate_new_tail_number(form, field):
        if form.tail_id.data:
            if field.data:
                raise ValidationError("Choose a tail number from your logbook or enter a new one, not both.")
        else:
            if not field.data:
                raise ValidationError("Choose a tail number from your logbook or enter a new one.")


class AirportForm(FlaskForm):
    identifier = StringField("Identifier", validators=[Length(min=3, max=4), InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    state_id = SelectField("State", coerce=int)
    new_state = StringField("New State")
    country_id = SelectField("Country", validators=[InputRequired()], coerce=int)
    new_country = StringField("New Country")

    def validate_identifier(form, field):
        if not field.data.isalnum():
            raise ValidationError("Invalid Identifier.")

    def validate_new_state(form, field):
        if form.state_id.data:
            if field.data:
                raise ValidationError("Choose a Logbook State or enter a new State, not both.")

    def validate_new_country(form, field):
        if form.country_id.data:
            if field.data:
                raise ValidationError("Choose a Logbook Country or enter a new Country, not both.")


class MakeModelForm(FlaskForm):
    cat_class = RadioField("Category and Class", choices=["ASEL", "AMEL"], validators=[InputRequired()])
    type_rating_id = SelectField("Type Rating", coerce=int, validators=[Optional()])
    new_type_rating = StringField("New Type Rating", validators=[Optional()])
    engine_type = RadioField("Engine Type", choices=["Piston", "Jet"], validators=[InputRequired()])
    gear_design = RadioField("Gear Design", choices=["Tailwheel", "Tricycle"], validators=[InputRequired()])
    gear_system = RadioField("Gear System", choices=["Fixed", "Retractable"], validators=[InputRequired()])
    is_complex = BooleanField("Complex")


class AirplaneForm(MakeModelForm):
    tail_number = StringField("Tail Number", validators=[Length(min=2, max=6), InputRequired()])
    model_id = SelectField("Make and Model", coerce=int)
    make_id = SelectField("Make", coerce=int)
    new_make = StringField("New Make")
    new_model = StringField("New Model")

    def validate_new_tail_number(form, field):
        if not field.data.isalnum():
            raise ValidationError("Invalid tail number.")

