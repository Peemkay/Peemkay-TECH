"""Application configuration, loaded from environment variables.

Copy .env.example to .env and adjust values before deploying.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _bool(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() in ("1", "true", "yes", "on")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-me-in-production")
    DEBUG = _bool(os.environ.get("FLASK_DEBUG"), default=False)

    # SQLite database that stores contact-form submissions.
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "instance", "contacts.db")
    )

    # Site identity / metadata
    SITE_NAME = "Peemkay TECH"
    SITE_TAGLINE = "Software Engineering Across Every Sector — Enterprise to Defense"
    SITE_DESCRIPTION = (
        "Peemkay TECH designs and builds secure, production-grade software for "
        "government & defense, enterprise, e-commerce, education and beyond — "
        "web, mobile, desktop and AI/computer-vision systems."
    )
    SITE_URL = os.environ.get("SITE_URL", "https://peemkay.pythonanywhere.com")
    SITE_KEYWORDS = (
        "Peemkay TECH, software developer, Flutter developer, Python developer, "
        "defense software, military technology software, government software "
        "solutions, facial recognition, computer vision, Django developer, "
        "Flask developer, Nigeria software engineer"
    )

    CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "mubarakabubakarbako@gmail.com")
    GITHUB_URL = "https://github.com/Peemkay"
    LOCATION = "Nigeria — Available for Remote & On-site Engagements Worldwide"

    # Optional social links. Leave blank to hide the icon in the navbar/footer.
    LINKEDIN_URL = os.environ.get("LINKEDIN_URL", "")
    TWITTER_URL = os.environ.get("TWITTER_URL", "")
    WHATSAPP_URL = os.environ.get("WHATSAPP_URL", "")

    # Optional outbound email notifications for new contact messages.
    # Leave MAIL_SERVER unset to disable email sending entirely (form
    # submissions are always saved to the database regardless).
    MAIL_ENABLED = _bool(os.environ.get("MAIL_ENABLED"), default=False)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = _bool(os.environ.get("MAIL_USE_TLS"), default=True)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_RECIPIENT = os.environ.get("MAIL_RECIPIENT", CONTACT_EMAIL)
