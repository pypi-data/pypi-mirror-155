"""Django app made to get together a set of utilities to use with Django projects."""
__version__ = "1.9.1"
import django

if django.VERSION < (3, 2):
    default_app_config = "belt.apps.BeltConfig"
