# Peemkay TECH — Portfolio Website

A production-ready, multi-page Flask portfolio site for **Peemkay TECH** —
software engineering across sectors, including government & defense
technology. Dark, modern UI with a sticky navbar, mobile slide-in menu,
scroll animations, a filterable projects grid, and a working contact form
with spam protection.

## Pages

| Route        | Page                                            |
|--------------|--------------------------------------------------|
| `/`          | Home — hero, sectors, value props, featured projects, services, CTA |
| `/about`     | About — bio, values, process                      |
| `/skills`    | Skills — full tech stack by category              |
| `/services`  | Services offered, including defense/government solutions |
| `/sectors`   | Industries served (proven + open engagements)      |
| `/projects`  | Filterable project grid linking to GitHub repos    |
| `/contact`   | Contact form (saved to SQLite) + direct info + FAQ |

Plus `/robots.txt`, `/sitemap.xml`, and custom `404`/`500` error pages.

## Tech stack

- **Backend**: Flask 3, Flask-WTF (CSRF-protected forms), stdlib `sqlite3`
  for storing contact messages — no heavy ORM needed.
- **Frontend**: hand-authored responsive CSS (no framework, no build step)
  + vanilla JS for the navbar, mobile menu, scroll-reveal animations and
  project filtering. Fonts load from Google Fonts (visitor's browser only —
  the server has zero external runtime dependencies).
- **Content**: page copy and project/skill/service data live in `data.py`
  as plain Python — edit it directly, no CMS or database migration needed.

## Project layout

```
peemkay-tech-portfolio/
├── app.py                      # Routes, Flask app instance
├── config.py                   # Config from environment variables
├── data.py                     # All page content (projects, skills, etc.)
├── forms.py                    # Contact form (Flask-WTF)
├── database.py                 # SQLite storage for contact messages
├── icons.py                    # Inline SVG icon set
├── requirements.txt
├── .env.example                # Copy to .env and fill in
├── pythonanywhere_wsgi_template.py
├── templates/                  # Jinja2 templates
└── static/
    ├── css/style.css
    ├── js/main.js
    └── images/                 # favicons + social share image
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

python app.py
```

Visit `http://127.0.0.1:5000`.

## Customizing content

Almost everything you'll want to change lives in **`data.py`** and
**`config.py`** — no template edits needed for routine updates:

- `config.py` — site name/tagline, contact email, GitHub URL, optional
  LinkedIn/Twitter/WhatsApp links (blank = hidden), optional outbound email
  notifications for contact-form submissions.
- `data.py` — projects, skills, services, sectors, value props, about-page
  copy. Add a new project by appending a dict to `PROJECTS`; it will
  automatically appear on the Projects page and can be filtered by
  `category`.

## Contact form behaviour

- Every valid submission is saved to a local SQLite database at
  `instance/contacts.db` (created automatically) — nothing is lost even if
  email sending isn't configured.
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
   `SITE_URL` (e.g. `https://yourusername.pythonanywhere.com`), and
   `CONTACT_EMAIL`.

4. **Create the web app** in the PythonAnywhere **Web** tab:
   - Choose **"Add a new web app"** → **Manual configuration** (not the
     Flask wizard, since we already have the full project) → pick a Python
     version matching your venv (e.g. 3.10).
   - Set **Virtualenv** to `/home/<yourusername>/peemkay-tech-portfolio/venv`.
   - Open the **WSGI configuration file** link and replace its contents
     with the contents of `pythonanywhere_wsgi_template.py` from this
     project, updating `project_home` to your actual path.

5. **Map the static folder** so CSS/JS/images are served directly (faster,
   and takes load off the Flask app): in the **Web** tab's *Static files*
   section, add:
   - URL: `/static/` → Directory: `/home/<yourusername>/peemkay-tech-portfolio/static/`

6. **Reload the web app** (green button at the top of the Web tab).

7. Visit `https://<yourusername>.pythonanywhere.com` and confirm every
   page loads, the mobile menu works, and a test contact-form submission
   succeeds.

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
- [ ] Static file mapping configured in the Web tab
- [ ] Contact form tested end-to-end (submission appears in
      `instance/contacts.db`)
- [ ] `LINKEDIN_URL` / `TWITTER_URL` / `WHATSAPP_URL` filled in if you want
      those icons to appear
