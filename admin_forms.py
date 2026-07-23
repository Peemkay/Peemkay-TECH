"""WTForms used by the admin dashboard.

List-shaped content (bullets, tech tags, highlights, skills, related
project names) uses TagListField — a small custom field backed by a JS
repeater widget in the templates (multiple inputs sharing one `name`,
read back here as a plain list of strings).
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, Field, IntegerField, PasswordField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from icons import ICONS

ICON_CHOICES = [(name, name) for name in sorted(ICONS.keys())]


class TagListField(Field):
    """A list-of-strings field with no built-in HTML widget — the admin
    templates render its repeater UI manually and post back several values
    under the same field name, which WTForms collects into a list here."""

    def _value(self):
        return self.data or []

    def process_formdata(self, valuelist):
        self.data = [v.strip() for v in valuelist if v and v.strip()]


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current password", validators=[DataRequired()])
    new_password = PasswordField("New password", validators=[DataRequired(), Length(min=8, message="At least 8 characters.")])
    confirm_password = PasswordField("Confirm new password", validators=[DataRequired()])


class SiteSettingsForm(FlaskForm):
    SITE_NAME = StringField("Site name", validators=[DataRequired(), Length(max=120)])
    SITE_TAGLINE = StringField("Tagline", validators=[Optional(), Length(max=255)])
    SITE_DESCRIPTION = TextAreaField("Meta description", validators=[Optional()])
    SITE_KEYWORDS = TextAreaField("SEO keywords (comma-separated)", validators=[Optional()])
    SITE_URL = StringField("Site URL", validators=[Optional(), Length(max=255)])
    CONTACT_EMAIL = StringField("Contact email", validators=[DataRequired(), Length(max=255)])
    GITHUB_URL = StringField("GitHub URL", validators=[Optional(), Length(max=255)])
    LOCATION = StringField("Location line", validators=[Optional(), Length(max=255)])
    LINKEDIN_URL = StringField("LinkedIn URL", validators=[Optional(), Length(max=255)])
    TWITTER_URL = StringField("Twitter / X URL", validators=[Optional(), Length(max=255)])
    WHATSAPP_URL = StringField("WhatsApp URL", validators=[Optional(), Length(max=255)])


class StatForm(FlaskForm):
    value = StringField("Value (e.g. 10+)", validators=[DataRequired(), Length(max=40)])
    label = StringField("Label (e.g. Software Systems Shipped)", validators=[DataRequired(), Length(max=120)])
    order = IntegerField("Order", default=0, validators=[Optional()])


class ValuePropForm(FlaskForm):
    icon = SelectField("Icon", choices=ICON_CHOICES, validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired(), Length(max=120)])
    text = TextAreaField("Text", validators=[DataRequired()])
    order = IntegerField("Order", default=0, validators=[Optional()])


class CoreValueForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=120)])
    text = TextAreaField("Text", validators=[DataRequired()])
    order = IntegerField("Order", default=0, validators=[Optional()])


class ApproachStepForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=120)])
    text = TextAreaField("Text", validators=[DataRequired()])
    order = IntegerField("Order", default=0, validators=[Optional()])


class ServiceForm(FlaskForm):
    slug = StringField("Slug (URL-safe id, e.g. custom-software)", validators=[DataRequired(), Length(max=120)])
    icon = SelectField("Icon", choices=ICON_CHOICES, validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired(), Length(max=120)])
    summary = TextAreaField("Summary", validators=[DataRequired()])
    bullets = TagListField("What's included")
    order = IntegerField("Order", default=0, validators=[Optional()])


class SkillGroupForm(FlaskForm):
    title = StringField("Group title", validators=[DataRequired(), Length(max=120)])
    icon = SelectField("Icon", choices=ICON_CHOICES, validators=[DataRequired()])
    skills = TagListField("Skills in this group")
    order = IntegerField("Order", default=0, validators=[Optional()])


class SectorForm(FlaskForm):
    title = StringField("Sector title", validators=[DataRequired(), Length(max=120)])
    icon = SelectField("Icon", choices=ICON_CHOICES, validators=[DataRequired()])
    image = FileField("Cover image", validators=[Optional(), FileAllowed(["png", "jpg", "jpeg", "webp"], "Images only.")])
    proven = BooleanField("Proven experience (shipped real work here)", default=False)
    text = TextAreaField("Description", validators=[DataRequired()])
    projects = TagListField("Related project names")
    order = IntegerField("Order", default=0, validators=[Optional()])


class ProjectForm(FlaskForm):
    slug = StringField("Slug (URL-safe id, e.g. my-project)", validators=[DataRequired(), Length(max=120)])
    title = StringField("Title", validators=[DataRequired(), Length(max=160)])
    category = StringField("Category key (e.g. defense, ecommerce, web)", validators=[DataRequired(), Length(max=60)])
    category_label = StringField("Category label (e.g. Government & Defense)", validators=[DataRequired(), Length(max=120)])
    confidential = BooleanField("Mark details as limited / confidential", default=False)
    featured = BooleanField("Feature on homepage", default=False)
    summary = TextAreaField("Short summary (used on homepage card)", validators=[DataRequired()])
    description = TextAreaField("Full description (used on Projects page)", validators=[DataRequired()])
    image = FileField("Cover image", validators=[Optional(), FileAllowed(["png", "jpg", "jpeg", "webp"], "Images only.")])
    repo = StringField("Repository URL", validators=[Optional(), Length(max=255)])
    highlights = TagListField("Highlights")
    tech = TagListField("Tech tags")
    order = IntegerField("Order", default=0, validators=[Optional()])


class AvatarUploadForm(FlaskForm):
    image = FileField("About-page avatar", validators=[DataRequired(), FileAllowed(["png", "jpg", "jpeg", "webp"], "Images only.")])
