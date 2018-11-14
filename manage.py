#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE" , "pur_beurre.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # to launch coverage after manage.py test : source : https://github.com/django-nose/django-nose/issues/180

    is_testing = 'test' in sys.argv

    if is_testing:
        import coverage

        cov = coverage.coverage(source=['quality'] ,
                                omit=['*/tests/*' , '*/forms.py' , '*/migrations/*' , '*/__init__.py' , '*/admin.py' ,
                                      '*/urls.py' , '*/apps.py'])
        cov.set_option('report:show_missing' , True)
        cov.erase()
        cov.start()

    # Add this 5 line above

    execute_from_command_line(sys.argv)

    # and add this 4 line below

    if is_testing:
        cov.stop()
        cov.save()
        cov.report()
