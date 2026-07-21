"""Template for the PythonAnywhere WSGI configuration file.

On PythonAnywhere, go to the Web tab -> your web app -> "WSGI configuration
file" (something like /var/www/yourusername_pythonanywhere_com_wsgi.py) and
replace its contents with this, adjusting the two values marked below.
"""
import sys
import os

# 1) Set this to the path where you uploaded/cloned this project on
#    PythonAnywhere, e.g. "/home/yourusername/peemkay-tech-portfolio"
project_home = "/home/yourusername/peemkay-tech-portfolio"

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 2) If you created a .env file for secrets/config, load it here so the
#    values are available to the app under mod_wsgi.
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, ".env"))

from app import app as application  # noqa: E402
