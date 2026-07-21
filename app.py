"""Peemkay TECH — portfolio website.

Entry point for local development and for PythonAnywhere's WSGI config,
which should do:

    from app import app as application

Run locally with:

    python app.py
"""
import logging
import smtplib
from datetime import datetime
from email.message import EmailMessage

from flask import Flask, flash, redirect, render_template, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from database import init_db, save_message
from forms import ContactForm
from icons import render_icon, render_logo_mark
import data

app = Flask(__name__)
app.config.from_object(Config)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
app.jinja_env.globals["icon"] = render_icon
app.jinja_env.globals["logo_mark"] = render_logo_mark
app.jinja_env.globals["current_year"] = lambda: datetime.now().year

logger = logging.getLogger(__name__)

with app.app_context():
    init_db(app.config["DATABASE_PATH"])


@app.context_processor
def inject_globals():
    return {
        "site": app.config,
        "nav_links": data.NAV_LINKS,
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
    try:
        msg = EmailMessage()
        msg["Subject"] = f"New {cfg['SITE_NAME']} enquiry — {form.project_type.data}"
        msg["From"] = cfg["MAIL_USERNAME"] or cfg["CONTACT_EMAIL"]
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
    featured = [p for p in data.PROJECTS if p["slug"] in ("e-comcen", "nafacial", "swagcitybymercy")]
    return render_template(
        "index.html",
        stats=data.STATS,
        value_props=data.VALUE_PROPS,
        services=data.SERVICES[:4],
        sectors=data.SECTORS,
        projects=featured,
        skill_groups=data.SKILL_GROUPS,
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        approach_steps=data.APPROACH_STEPS,
        core_values=data.CORE_VALUES,
    )


@app.route("/skills")
def skills():
    return render_template("skills.html", skill_groups=data.SKILL_GROUPS)


@app.route("/services")
def services():
    return render_template("services.html", services=data.SERVICES)


@app.route("/sectors")
def sectors():
    return render_template("sectors.html", sectors=data.SECTORS)


@app.route("/projects")
def projects():
    return render_template(
        "projects.html",
        projects=data.PROJECTS,
        categories=data.PROJECT_CATEGORIES,
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        if form.website.data:
            # Honeypot tripped — silently pretend success so bots move on.
            logger.info("Honeypot triggered on contact form; discarding submission")
            return redirect(url_for("contact", sent=1))

        save_message(
            app.config["DATABASE_PATH"],
            name=form.name.data.strip(),
            email=form.email.data.strip(),
            project_type=form.project_type.data,
            message=form.message.data.strip(),
        )
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
        f"Sitemap: {app.config['SITE_URL']}/sitemap.xml",
    ]
    return "\n".join(lines), 200, {"Content-Type": "text/plain"}


@app.route("/sitemap.xml")
def sitemap_xml():
    pages = ["home", "about", "skills", "services", "sectors", "projects", "contact"]
    urls = "".join(
        f"<url><loc>{app.config['SITE_URL']}{url_for(p)}</loc></url>" for p in pages
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?>' \
          f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return xml, 200, {"Content-Type": "application/xml"}


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(_error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
