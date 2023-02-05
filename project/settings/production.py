from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#d0e=f9qduy!kdyy=k_@$yn+dzbel6i&e_e&fwa0u$qqcc67gr'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['localhost', '195.201.206.156', '116.202.192.137', 'mirsmartone.com']

IS_PRODUCTION = True

EMAIL_RECIPIENTS = ['adriano.m@spirometry.com',]
EMAIL_RECIPIENTS_CUSTOMER_SERVICE = ['adriano.m@spirometry.com',]
EMAIL_ORDERS = ['adriano.m@spirometry.com',]
EMAIL_RECIPIENTS_HIDDEN = ["adriano.m@spirometry.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mirsmartone_prod',               # Or path to database file if using sqlite3.
        'USER': 'mirsmartone',               # Not used with sqlite3.
        'PASSWORD': 'F9n5JwCVtVaCfC57',            # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': ''                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Paypal credentials Spirometry
PAYPAL_SANDBOX_MODE = False
PAYPAL_API_USERNAME = "fabiana.z_api1.spirometry.com"
PAYPAL_API_PASSWORD = "44K7W28SUACQLP7Q"
PAYPAL_API_SIGNATURE = "AxYLpqp7SWrCU8GZmTaZSCaWf3HUAOubUjGO4jjHoZnsWd8GxFtJ5QKw"

try:
    from .local import *
except ImportError:
    pass
