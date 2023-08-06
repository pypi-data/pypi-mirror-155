=====
django-api-base
=====

django-api-base is simple django package that can be used to build RESTFUL web api's with django

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "django_api_base" to your INSTALLED_APPS setting like this::

    ```
    #!python

    INSTALLED_APPS = [
        ...
        'django_api_base',
    ]


    #Django-api-base settings
    API_TESTING = True

    ACCESS_TOKEN_EXPIRE_DAYS = 15

    FROM_EMAIL = ""

    BUCKET_URL = ""

    MIDDLEWARE_CLASSES = [
    ...
    'django_api_base.middleware.api_exception.APIExceptionHandler'  # APIExceptionHandler middleware should be added here
    'django_api_base.middleware.logging_middleware.LogAllServerCalls'  # For logging all server request calls info
    'django_api_base.middleware.logging_middleware.LogAllExceptionErrors'  # For logging all exceptions occured
    ]

    # Logging settings
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
        },
        'handlers': {
            'access': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': 'access.log',
                'formatter': 'verbose'
            },
            'error': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': 'error.log',
                'formatter': 'verbose'
            },
            'debug': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'debug.log',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'info': {
                'handlers': ['access'],
                'level': 'INFO',
            },
            'error': {
                'handlers': ['error'],
                'level': 'ERROR',
            },
            'debug': {
                'handlers': ['debug'],
                'level': 'DEBUG',
            },
        }
    }
    ```

2. Run `python manage.py migrate` to create the UserProfile model which can be used as a user profile model in your django project.

