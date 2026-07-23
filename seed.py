"""One-time population of the database from the site's original starter
content (previously hardcoded in data.py). Run via:

    flask seed-db

Safe to re-run — each table is only seeded if it's currently empty, so it
won't overwrite content you've since edited through the admin dashboard.
"""
import data
from config import Config
from models import (
    ApproachStep,
    CoreValue,
    Project,
    Sector,
    Service,
    SiteSetting,
    SkillGroup,
    Stat,
    ValueProp,
)

FEATURED_SLUGS = {"e-comcen", "nafacial", "swagcitybymercy"}


def run_seed(db):
    settings = SiteSetting.get()
    if not settings.SITE_NAME:
        settings.SITE_NAME = Config.SITE_NAME
        settings.SITE_TAGLINE = Config.SITE_TAGLINE
        settings.SITE_DESCRIPTION = Config.SITE_DESCRIPTION
        settings.SITE_KEYWORDS = Config.SITE_KEYWORDS
        settings.SITE_URL = Config.SITE_URL
        settings.CONTACT_EMAIL = Config.CONTACT_EMAIL
        settings.GITHUB_URL = Config.GITHUB_URL
        settings.LOCATION = Config.LOCATION
        settings.LINKEDIN_URL = Config.LINKEDIN_URL
        settings.TWITTER_URL = Config.TWITTER_URL
        settings.WHATSAPP_URL = Config.WHATSAPP_URL
        print("Seeded site settings.")

    if Stat.query.count() == 0:
        for i, s in enumerate(data.STATS):
            db.session.add(Stat(value=s["value"], label=s["label"], order=i))
        print(f"Seeded {len(data.STATS)} stats.")

    if ValueProp.query.count() == 0:
        for i, v in enumerate(data.VALUE_PROPS):
            db.session.add(ValueProp(icon=v["icon"], title=v["title"], text=v["text"], order=i))
        print(f"Seeded {len(data.VALUE_PROPS)} value props.")

    if CoreValue.query.count() == 0:
        for i, c in enumerate(data.CORE_VALUES):
            db.session.add(CoreValue(title=c["title"], text=c["text"], order=i))
        print(f"Seeded {len(data.CORE_VALUES)} core values.")

    if ApproachStep.query.count() == 0:
        for i, a in enumerate(data.APPROACH_STEPS):
            db.session.add(ApproachStep(title=a["title"], text=a["text"], order=i))
        print(f"Seeded {len(data.APPROACH_STEPS)} approach steps.")

    if Service.query.count() == 0:
        for i, s in enumerate(data.SERVICES):
            db.session.add(Service(
                slug=s["slug"], icon=s["icon"], title=s["title"],
                summary=s["summary"], bullets=s["bullets"], order=i,
            ))
        print(f"Seeded {len(data.SERVICES)} services.")

    if SkillGroup.query.count() == 0:
        for i, g in enumerate(data.SKILL_GROUPS):
            db.session.add(SkillGroup(title=g["title"], icon=g["icon"], skills=g["skills"], order=i))
        print(f"Seeded {len(data.SKILL_GROUPS)} skill groups.")

    if Sector.query.count() == 0:
        for i, sec in enumerate(data.SECTORS):
            db.session.add(Sector(
                title=sec["title"], icon=sec["icon"], image=sec.get("image"),
                proven=sec["proven"], text=sec["text"], projects=sec["projects"], order=i,
            ))
        print(f"Seeded {len(data.SECTORS)} sectors.")

    if Project.query.count() == 0:
        for i, p in enumerate(data.PROJECTS):
            db.session.add(Project(
                slug=p["slug"], title=p["title"], category=p["category"],
                category_label=p["category_label"], confidential=p["confidential"],
                summary=p["summary"], description=p["description"], image=p.get("image"),
                repo=p.get("repo"), highlights=p["highlights"], tech=p["tech"],
                featured=p["slug"] in FEATURED_SLUGS, order=i,
            ))
        print(f"Seeded {len(data.PROJECTS)} projects.")

    db.session.commit()
    print("Seed complete.")
