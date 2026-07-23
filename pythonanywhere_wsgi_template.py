"""Template for the PythonAnywhere WSGI configuration file.

On PythonAnywhere, go to the Web tab -> your web app -> "WSGI configuration
file" (something like /var/www/yourusername_pythonanywhere_com_wsgi.py) and
replace its contents with this, adjusting the path marked below.
"""
import sys

# Set this to the path where you uploaded/cloned this project on
# PythonAnywhere, e.g. "/home/yourusername/peemkay-tech-portfolio"
project_home = "/home/yourusername/peemkay-tech-portfolio"

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# app.py loads .env itself (via python-dotenv) as soon as it's imported,
# so nothing else needs to happen here.
from app import app as application  # noqa: E402
