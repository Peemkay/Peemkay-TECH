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

    # Primary application database — site content, admin user, contact
    # messages. A plain SQLite file is plenty for a single-admin portfolio.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploaded cover images / avatar (admin-managed content). Lives under
    # static/images so it matches the "images/<path>" convention every
    # template already uses for the seeded placeholder covers.
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images", "uploads")
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024  # 6 MB per upload
    ALLOWED_UPLOAD_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # Admin session cookies. SECURE requires HTTPS — enable in production
    # (PythonAnywhere serves HTTPS by default) via SESSION_COOKIE_SECURE=true.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _bool(os.environ.get("SESSION_COOKIE_SECURE"), default=False)
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 8  # 8 hours

    # Bootstrap credentials for `flask create-admin` / first-run auto-seed.
    # Only used when no admin user exists yet — safe to leave unset after
    # the first admin account has been created.
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

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
