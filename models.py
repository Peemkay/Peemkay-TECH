"""SQLAlchemy models — the database-backed source of truth for every piece
of content shown on the public site, plus the admin user and contact
messages.

All list-shaped fields (highlights, tech, bullets, skills, related project
names) are stored as JSON columns holding a plain list of strings — the
admin UI edits these with a small repeater widget, so no delimiter-parsing
is needed on either side.
"""
from datetime import datetime, timezone

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


def utcnow():
    return datetime.now(timezone.utc)


class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)
    failed_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)


class SiteSetting(db.Model):
    """Singleton row (id=1) holding editable site-wide content/settings."""
    __tablename__ = "site_settings"

    id = db.Column(db.Integer, primary_key=True)
    SITE_NAME = db.Column(db.String(120), default="")
    SITE_TAGLINE = db.Column(db.String(255), default="")
    SITE_DESCRIPTION = db.Column(db.Text, default="")
    SITE_KEYWORDS = db.Column(db.Text, default="")
    SITE_URL = db.Column(db.String(255), default="")
    CONTACT_EMAIL = db.Column(db.String(255), default="")
    GITHUB_URL = db.Column(db.String(255), default="")
    LOCATION = db.Column(db.String(255), default="")
    LINKEDIN_URL = db.Column(db.String(255), default="")
    TWITTER_URL = db.Column(db.String(255), default="")
    WHATSAPP_URL = db.Column(db.String(255), default="")
    AVATAR_IMAGE = db.Column(db.String(255), default="covers/avatar.png")
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)

    @classmethod
    def get(cls):
        row = db.session.get(cls, 1)
        if row is None:
            row = cls(id=1)
            db.session.add(row)
            db.session.commit()
        return row


class OrderedMixin:
    """Shared ordering + timestamps for content collections."""
    order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)


class Stat(OrderedMixin, db.Model):
    __tablename__ = "stats"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(40), nullable=False)
    label = db.Column(db.String(120), nullable=False)


class ValueProp(OrderedMixin, db.Model):
    __tablename__ = "value_props"
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(40), nullable=False, default="star")
    title = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False, default="")


class CoreValue(OrderedMixin, db.Model):
    __tablename__ = "core_values"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False, default="")


class ApproachStep(OrderedMixin, db.Model):
    __tablename__ = "approach_steps"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False, default="")


class Service(OrderedMixin, db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    icon = db.Column(db.String(40), nullable=False, default="star")
    title = db.Column(db.String(120), nullable=False)
    summary = db.Column(db.Text, nullable=False, default="")
    bullets = db.Column(db.JSON, nullable=False, default=list)


class SkillGroup(OrderedMixin, db.Model):
    __tablename__ = "skill_groups"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    icon = db.Column(db.String(40), nullable=False, default="star")
    skills = db.Column(db.JSON, nullable=False, default=list)


class Sector(OrderedMixin, db.Model):
    __tablename__ = "sectors"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    icon = db.Column(db.String(40), nullable=False, default="star")
    image = db.Column(db.String(255), nullable=True)
    proven = db.Column(db.Boolean, default=False, nullable=False)
    text = db.Column(db.Text, nullable=False, default="")
    projects = db.Column(db.JSON, nullable=False, default=list)


class Project(OrderedMixin, db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    category_label = db.Column(db.String(120), nullable=False)
    confidential = db.Column(db.Boolean, default=False, nullable=False)
    summary = db.Column(db.Text, nullable=False, default="")
    description = db.Column(db.Text, nullable=False, default="")
    image = db.Column(db.String(255), nullable=True)
    repo = db.Column(db.String(255), nullable=True)
    highlights = db.Column(db.JSON, nullable=False, default=list)
    tech = db.Column(db.JSON, nullable=False, default=list)
    featured = db.Column(db.Boolean, default=False, nullable=False)


class ContactMessage(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    project_type = db.Column(db.String(60), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
