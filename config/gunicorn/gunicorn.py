"""Gunicorn *development* config file"""

from pathlib import Path

# project path
pythonpath = str(Path(__file__).resolve().parent.joinpath("service"))
print(f"GUNICORN PYTHON PATH: {pythonpath}")
# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "service.wsgi:application"
# The granularity of Error log outputs
loglevel = "INFO"
# The number of worker processes for handling requests
core_number = 2
workers = core_number * 2 + 1  # core*2 + 1
# The socket to bind
bind = "0.0.0.0:8000"
# Restart workers when code changes (development only!)
reload = True
# Write access and error info to /var/log
# accesslog = errorlog = "/var/log/gunicorn/dev.log"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
# pidfile = "/var/run/gunicorn/dev.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = False
