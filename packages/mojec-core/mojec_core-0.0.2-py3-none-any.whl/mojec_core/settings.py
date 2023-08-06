import os, sys

from dotenv import load_dotenv

load_dotenv()

AUTH_USER_MODEL = 'app.User'

SECRET_KEY = 'da)(@*#Uhubjindu*(!@#$#@nfoinond-ahp*nen2@=*u)!g8m9pthdg'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


def db(key):
    return os.getenv(key)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': "django.db.backends.sqlite3",
            'NAME': "test.db"
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': db("DB_ENGINE"),
            'NAME': db('POSTGRES_DB'),
            'USER': db('POSTGRES_USER'),
            'PASSWORD': db('POSTGRES_PASSWORD'),
            'HOST': db('DB_HOST'),
            'PORT': db('DB_PORT'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(asctime)s %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'root': {
        'handlers': ['console', ],
        'level': 'DEBUG'
    },
    'loggers': {
        'django.request': {
            'handlers': [
                'console',
            ],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
SAFE_DELETE_FIELD_NAME = "deletedAt"
SAFE_DELETE_CASCADED_FIELD_NAME = "deletedViaCascade"
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'PAGINATE_BY_PARAM': 'limit'
}
