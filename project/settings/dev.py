from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#d0e=f9qduy!kdyy=k_@$yn+dzbel6i&e_e&fwa0u$qqcc67gr'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*', 'localhost', '195.201.206.156', '116.202.192.137', 'dev.mirsmartone.doppiozero.to']

IS_PRODUCTION = True

EMAIL_RECIPIENTS = ["rr@doppiozero.to", "lc@doppiozero.to"]
EMAIL_RECIPIENTS_CUSTOMER_SERVICE = ["rr@doppiozero.to", "lc@doppiozero.to"]
EMAIL_ORDERS = ["rr@doppiozero.to", "lc@doppiozero.to"]
EMAIL_RECIPIENTS_HIDDEN = ["rr@doppiozero.to", "lc@doppiozero.to"]

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

# Paypal credentials
PAYPAL_CALLBACK_HTTPS = False
PAYPAL_API_USERNAME = "sb-ahdfp3291205_api1.business.example.com"
PAYPAL_API_PASSWORD = "P8XNPKLR4J5AHHYR"
PAYPAL_API_SIGNATURE = "APioMws2wuxbSdpVCGS5l5doAkp1Aei6CfbYn14J0U7kmBVHn-Xv0u2S"
PAYPAL_SANDBOX_MODE = True

try:
    from .local import *
except ImportError:
    pass
