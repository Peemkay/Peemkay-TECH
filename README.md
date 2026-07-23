# Peemkay TECH — Portfolio Website

A production-ready, multi-page Flask portfolio site for **Peemkay TECH** —
software engineering across sectors, including government & defense
technology. Dark, modern UI with a sticky navbar, mobile slide-in menu,
scroll animations, a filterable projects grid, a working contact form with
spam protection, and a full **admin dashboard** for managing every piece of
content on the site without touching code.

## Pages

| Route        | Page                                            |
|--------------|--------------------------------------------------|
| `/`          | Home — hero, sectors, value props, featured projects, services, CTA |
| `/about`     | About — bio, values, process                      |
| `/skills`    | Skills — full tech stack by category              |
| `/services`  | Services offered, including defense/government solutions |
| `/sectors`   | Industries served (proven + open engagements)      |
| `/projects`  | Filterable project grid linking to GitHub repos    |
| `/contact`   | Contact form (saved to the database) + direct info + FAQ |
| `/admin`     | Login-protected dashboard — see below              |

Plus `/robots.txt`, `/sitemap.xml`, and custom `404`/`500` error pages.

## Admin dashboard

Everything shown on the public site — every project, sector, service, skill,
value prop, core value, process step, hero stat, and the site-wide
name/tagline/contact/social settings — is stored in the database and
editable from a login-protected admin panel at **`/admin`**, no code changes
or redeploys required. It also includes a contact-message inbox for
everything submitted through the public contact form.

**First-time setup** (run once, locally or on the server):

```bash
flask --app app create-admin
```

This prompts for a username and password and creates the one admin account
the dashboard supports (this is a single-operator tool, not multi-tenant).
Alternatively, set `ADMIN_USERNAME`/`ADMIN_PASSWORD` in `.env` before the
first run and an admin account is created automatically on startup — handy
for a fresh PythonAnywhere deploy where an interactive prompt is awkward.

Then log in at `/admin/login` and you'll find, in the sidebar:

- **Projects, Sectors, Services, Skills, Value Props, Core Values, Process
  Steps, Hero Stats** — each has a list view and a create/edit form. List
  fields (highlights, tech tags, bullets, skills) use a small add/remove
  "repeater" control rather than a delimiter-separated text box.
- **Cover images** (projects/sectors) and the **About-page avatar** can be
  replaced with a real upload straight from the edit form / Site Settings
  page — dropped into `static/images/uploads/` automatically.
- **Messages** — every contact-form submission, with read/unread state.
- **Site Settings** — name, tagline, meta description/keywords, contact
  email, GitHub/LinkedIn/Twitter/WhatsApp links, location line.
- **Change Password**.

Security notes: passwords are hashed (never stored in plain text), all
state-changing requests are CSRF-protected, and the login form locks out
after 5 failed attempts for 15 minutes.

## Tech stack

- **Backend**: Flask 3, Flask-SQLAlchemy (SQLite by default), Flask-Login
  for admin auth, Flask-WTF for CSRF-protected forms.
- **Frontend**: hand-authored responsive CSS (no framework, no build step)
  + vanilla JS for the navbar, mobile menu, scroll-reveal animations,
  project filtering, and the admin dashboard's sidebar/repeater-field/image
  preview behaviour. Fonts load from Google Fonts (visitor's browser only —
  the server itself has zero external runtime dependencies).
- **Content**: lives in the database (see `models.py`), managed through the
  admin dashboard. `data.py` is now only the one-time **seed source** used
  by `flask seed-db` to populate a fresh database with the site's original
  starter content — it's not read by the running app.

## Project layout

```
peemkay-tech-portfolio/
├── app.py                      # Routes, Flask app instance, CLI commands
├── admin.py                    # Admin blueprint — auth + CRUD routes
├── admin_forms.py               # WTForms for the admin dashboard
├── models.py                   # SQLAlchemy models (all content + admin user)
├── seed.py                     # One-time DB seed from data.py's starter content
├── config.py                   # Config from environment variables
├── data.py                     # Original starter content (seed source only)
├── forms.py                    # Public contact form (Flask-WTF)
├── icons.py                    # Inline SVG icon set
├── requirements.txt
├── .env.example                # Copy to .env and fill in
├── pythonanywhere_wsgi_template.py
├── templates/
│   └── admin/                  # Admin dashboard templates
└── static/
    ├── css/style.css
    ├── css/admin.css
    ├── js/main.js
    ├── js/admin.js
    └── images/                 # favicons, social share image, covers/, uploads/
```

## Local development

Requires Python 3.9+.

```bash
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS/Linux

pip install -r requirements.txt
copy .env.example .env           # Windows: copy, macOS/Linux: cp
# edit .env — at minimum set a real SECRET_KEY

flask --app app seed-db          # populate the database with starter content
flask --app app create-admin     # create your admin login

python app.py
```

Visit `http://127.0.0.1:5000` for the site, `http://127.0.0.1:5000/admin`
to manage it.

## Customizing content

Day-to-day content changes (new project, edited bio text, a different
contact email, swapping a cover image) all happen through **`/admin`** —
no code, no redeploy.

Two things still live in code, since they're structural rather than content:

- `config.py` — infrastructure-level settings: secret key, database URL,
  upload limits, session cookie security, optional outbound-email
  notifications for contact-form submissions.
- `data.py` / `seed.py` — only relevant if you want to reset a fresh
  database back to the site's original starter content (`flask seed-db`
  skips any table that already has rows, so it's safe to re-run).

## Contact form behaviour

- Every valid submission is saved to the database and shows up in
  `/admin/messages` immediately — nothing is lost even if email sending
  isn't configured.
- A hidden honeypot field silently discards bot submissions.
- To also receive an email for each submission, set `MAIL_ENABLED=true` and
  the `MAIL_*` variables in `.env` (works with Gmail SMTP, SendGrid, etc. —
  note that PythonAnywhere's **free tier only allows outbound SMTP to a
  small allow-list of providers**; check their current docs before relying
  on this in production).

## Deploying to PythonAnywhere

1. **Get the code onto PythonAnywhere.**
   Easiest path: push this project to a GitHub repo, then on PythonAnywhere
   open a **Bash console** and run:
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git peemkay-tech-portfolio
   ```
   (Or upload the files directly via the Files tab if you'd rather not use
   git.)

2. **Create a virtualenv and install dependencies** (in the same Bash
   console):
   ```bash
   cd peemkay-tech-portfolio
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create your `.env` file** on the server:
   ```bash
   cp .env.example .env
   nano .env
   ```
   Set a real, random `SECRET_KEY` (generate one locally with
   `python -c "import secrets; print(secrets.token_hex(32))"`), your
   `SITE_URL` (e.g. `https://yourusername.pythonanywhere.com`),
   `CONTACT_EMAIL`, `SESSION_COOKIE_SECURE=true` (PythonAnywhere serves
   HTTPS by default), and either `ADMIN_USERNAME`/`ADMIN_PASSWORD` for an
   automatic first-run admin account, or plan to run `create-admin` in step 5.

4. **Create the web app** in the PythonAnywhere **Web** tab:
   - Choose **"Add a new web app"** → **Manual configuration** (not the
     Flask wizard, since we already have the full project) → pick a Python
     version matching your venv (e.g. 3.10).
   - Set **Virtualenv** to `/home/<yourusername>/peemkay-tech-portfolio/venv`.
   - Open the **WSGI configuration file** link and replace its contents
     with the contents of `pythonanywhere_wsgi_template.py` from this
     project, updating `project_home` to your actual path.

5. **Set up the database and admin account** (still in the Bash console):
   ```bash
   flask --app app seed-db
   flask --app app create-admin   # skip if you set ADMIN_USERNAME/PASSWORD in .env
   ```

6. **Map the static folder** so CSS/JS/images are served directly (faster,
   and takes load off the Flask app): in the **Web** tab's *Static files*
   section, add:
   - URL: `/static/` → Directory: `/home/<yourusername>/peemkay-tech-portfolio/static/`

7. **Reload the web app** (green button at the top of the Web tab).

8. Visit `https://<yourusername>.pythonanywhere.com` and confirm every
   page loads and a test contact-form submission succeeds, then log in at
   `/admin` and confirm you can edit something and see it reflected live.

### Updating after code changes

```bash
cd ~/peemkay-tech-portfolio
git pull
source venv/bin/activate
pip install -r requirements.txt   # only if requirements changed
```
Then hit **Reload** on the Web tab.

## Production checklist

- [ ] `SECRET_KEY` is a real random value, not the default
- [ ] `FLASK_DEBUG` is unset or `false`
- [ ] `SITE_URL` matches your actual PythonAnywhere domain (or custom domain)
- [ ] `SESSION_COOKIE_SECURE=true` once served over HTTPS
- [ ] Static file mapping configured in the Web tab
- [ ] Database seeded (`flask seed-db`) and admin account created
- [ ] Admin login tested, including that a wrong password is rejected
- [ ] Contact form tested end-to-end (submission appears in `/admin/messages`)
- [ ] `LINKEDIN_URL` / `TWITTER_URL` / `WHATSAPP_URL` filled in (via Site
      Settings in the admin panel) if you want those icons to appear
