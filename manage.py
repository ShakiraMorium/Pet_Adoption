#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def _stabilize_runserver_autoreload():
    """
    Work around a Python 3.13 + Django autoreload KeyError that can occur on
    startup (e.g. KeyError: 'xml.etree.ElementTree').

    When running runserver locally, force --noreload unless explicitly
    overridden.
    """
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        if '--noreload' not in sys.argv:
            sys.argv.append('--noreload')
def main():
    """Run administrative tasks."""
    _stabilize_runserver_autoreload()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_adoption.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
