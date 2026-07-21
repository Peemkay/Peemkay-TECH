from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional

PROJECT_TYPES = [
    ("", "Select a project type…"),
    ("web", "Web Application"),
    ("mobile", "Mobile App"),
    ("desktop", "Desktop Software"),
    ("defense", "Government / Defense Solution"),
    ("ai", "AI / Computer Vision"),
    ("ecommerce", "E-Commerce Platform"),
    ("other", "Other / Not Sure Yet"),
]


class ContactForm(FlaskForm):
    name = StringField(
        "Full Name",
        validators=[DataRequired(message="Please enter your name."), Length(max=120)],
    )
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(message="Please enter your email address."),
            Email(message="Please enter a valid email address."),
            Length(max=120),
        ],
    )
    project_type = SelectField("Project Type", choices=PROJECT_TYPES, validators=[DataRequired(message="Please select a project type.")])
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Please enter a message."),
            Length(min=10, max=5000, message="Message should be between 10 and 5000 characters."),
        ],
    )
    # Honeypot field — hidden from real users via CSS. Left un-validated
    # here on purpose; app.py checks it post-validation and silently drops
    # the submission if a bot filled it in.
    website = HiddenField(validators=[Optional()])
