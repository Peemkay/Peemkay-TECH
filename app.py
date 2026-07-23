"""Peemkay TECH — portfolio website.

Entry point for local development and for PythonAnywhere's WSGI config,
which should do:

    from app import app as application

Run locally with:

    python app.py

First-time setup (creates the database + an admin account):

    flask create-admin
"""
import logging
import smtplib
from datetime import datetime
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()  # picks up .env for local dev; harmless no-op if absent

from flask import Flask, flash, redirect, render_template, url_for  # noqa: E402
from flask_login import LoginManager  # noqa: E402
from flask_wtf import CSRFProtect  # noqa: E402
from werkzeug.middleware.proxy_fix import ProxyFix  # noqa: E402

from config import Config
from forms import ContactForm
from icons import render_icon, render_logo_mark
from models import (
    AdminUser,
    ApproachStep,
    ContactMessage,
    CoreValue,
    Project,
    Sector,
    Service,
    SiteSetting,
    SkillGroup,
    Stat,
    ValueProp,
    db,
)

app = Flask(__name__)
app.config.from_object(Config)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
app.jinja_env.globals["icon"] = render_icon
app.jinja_env.globals["logo_mark"] = render_logo_mark
app.jinja_env.globals["current_year"] = lambda: datetime.now().year

logger = logging.getLogger(__name__)

db.init_app(app)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin.login"
login_manager.login_message = "Please log in to access the admin dashboard."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(AdminUser, int(user_id))


with app.app_context():
    db.create_all()

    # Convenience bootstrap: if no admin account exists yet and
    # ADMIN_USERNAME/ADMIN_PASSWORD are set (e.g. in .env), create one
    # automatically. This covers first deploys where running `flask
    # create-admin` interactively isn't convenient. Once an admin exists
    # this block is a no-op — safe to leave the env vars set afterward.
    if not AdminUser.query.first():
        bootstrap_user = app.config.get("ADMIN_USERNAME")
        bootstrap_pass = app.config.get("ADMIN_PASSWORD")
        if bootstrap_user and bootstrap_pass and len(bootstrap_pass) >= 8:
            admin_user = AdminUser(username=bootstrap_user)
            admin_user.set_password(bootstrap_pass)
            db.session.add(admin_user)
            db.session.commit()
            logger.info("Bootstrapped initial admin account '%s' from environment.", bootstrap_user)

from admin import admin_bp  # noqa: E402  (needs db/app configured first)

app.register_blueprint(admin_bp)


class SiteProxy:
    """Merges the editable SiteSetting DB row with static Config fallbacks,
    so `{{ site.SITE_NAME }}` keeps working in templates unchanged while
    admin edits take effect immediately without a redeploy."""

    def __init__(self, row, cfg):
        self._row = row
        self._cfg = cfg

    def __getattr__(self, name):
        value = getattr(self._row, name, None)
        if value:
            return value
        return self._cfg.get(name)


def get_site():
    return SiteProxy(SiteSetting.get(), app.config)


@app.context_processor
def inject_globals():
    return {
        "site": get_site(),
        "nav_links": [
            {"label": "Home", "endpoint": "home"},
            {"label": "About", "endpoint": "about"},
            {"label": "Skills", "endpoint": "skills"},
            {"label": "Services", "endpoint": "services"},
            {"label": "Sectors", "endpoint": "sectors"},
            {"label": "Projects", "endpoint": "projects"},
            {"label": "Contact", "endpoint": "contact"},
        ],
    }


@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


def _send_notification_email(form):
    cfg = app.config
    if not cfg.get("MAIL_ENABLED") or not cfg.get("MAIL_SERVER"):
        return
    site = get_site()
    try:
        msg = EmailMessage()
        msg["Subject"] = f"New {site.SITE_NAME} enquiry — {form.project_type.data}"
        msg["From"] = cfg["MAIL_USERNAME"] or site.CONTACT_EMAIL
        msg["To"] = cfg["MAIL_RECIPIENT"]
        msg["Reply-To"] = form.email.data
        msg.set_content(
            f"Name: {form.name.data}\n"
            f"Email: {form.email.data}\n"
            f"Project type: {form.project_type.data}\n\n"
            f"Message:\n{form.message.data}\n"
        )
        with smtplib.SMTP(cfg["MAIL_SERVER"], cfg["MAIL_PORT"], timeout=10) as smtp:
            if cfg.get("MAIL_USE_TLS"):
                smtp.starttls()
            if cfg.get("MAIL_USERNAME"):
                smtp.login(cfg["MAIL_USERNAME"], cfg["MAIL_PASSWORD"])
            smtp.send_message(msg)
    except Exception:
        logger.exception("Failed to send contact-form notification email")


@app.route("/")
def home():
    return render_template(
        "index.html",
        stats=Stat.query.order_by(Stat.order).all(),
        value_props=ValueProp.query.order_by(ValueProp.order).all(),
        services=Service.query.order_by(Service.order).limit(4).all(),
        sectors=Sector.query.order_by(Sector.order).all(),
        projects=Project.query.filter_by(featured=True).order_by(Project.order).all(),
        skill_groups=SkillGroup.query.order_by(SkillGroup.order).all(),
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        approach_steps=ApproachStep.query.order_by(ApproachStep.order).all(),
        core_values=CoreValue.query.order_by(CoreValue.order).all(),
    )


@app.route("/skills")
def skills():
    return render_template("skills.html", skill_groups=SkillGroup.query.order_by(SkillGroup.order).all())


@app.route("/services")
def services():
    return render_template("services.html", services=Service.query.order_by(Service.order).all())


@app.route("/sectors")
def sectors():
    return render_template("sectors.html", sectors=Sector.query.order_by(Sector.order).all())


@app.route("/projects")
def projects():
    all_projects = Project.query.order_by(Project.order).all()
    seen = {}
    for p in all_projects:
        seen.setdefault(p.category, p.category_label)
    categories = [{"key": "all", "label": "All Projects"}] + [
        {"key": key, "label": label} for key, label in seen.items()
    ]
    return render_template("projects.html", projects=all_projects, categories=categories)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        if form.website.data:
            # Honeypot tripped — silently pretend success so bots move on.
            logger.info("Honeypot triggered on contact form; discarding submission")
            return redirect(url_for("contact", sent=1))

        db.session.add(
            ContactMessage(
                name=form.name.data.strip(),
                email=form.email.data.strip(),
                project_type=form.project_type.data,
                message=form.message.data.strip(),
            )
        )
        db.session.commit()
        _send_notification_email(form)
        flash(
            "Thanks — your message has been received. I'll get back to you soon.",
            "success",
        )
        return redirect(url_for("contact", sent=1))

    return render_template("contact.html", form=form)


@app.route("/robots.txt")
def robots_txt():
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {get_site().SITE_URL}/sitemap.xml",
    ]
    return "\n".join(lines), 200, {"Content-Type": "text/plain"}


@app.route("/sitemap.xml")
def sitemap_xml():
    pages = ["home", "about", "skills", "services", "sectors", "projects", "contact"]
    site_url = get_site().SITE_URL
    urls = "".join(f"<url><loc>{site_url}{url_for(p)}</loc></url>" for p in pages)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    )
    return xml, 200, {"Content-Type": "application/xml"}


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(_error):
    return render_template("500.html"), 500


@app.cli.command("create-admin")
def create_admin_command():
    """Interactively create (or reset) the single admin account."""
    import getpass

    with app.app_context():
        existing = AdminUser.query.first()
        if existing:
            print(f"An admin user already exists: {existing.username}")
            if input("Reset its password instead? [y/N] ").strip().lower() != "y":
                return
            password = getpass.getpass("New password: ")
            if len(password) < 8:
                print("Password must be at least 8 characters.")
                return
            existing.set_password(password)
            db.session.commit()
            print("Password updated.")
            return

        username = input("Admin username: ").strip()
        password = getpass.getpass("Admin password (min 8 chars): ")
        if not username or len(password) < 8:
            print("Username required and password must be at least 8 characters.")
            return
        user = AdminUser(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Admin user '{username}' created.")


@app.cli.command("seed-db")
def seed_db_command():
    """Populate the database with the site's original starter content.
    Safe to re-run — skips any table that already has rows."""
    from seed import run_seed

    with app.app_context():
        run_seed(db)


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
