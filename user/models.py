from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
def gettext_noop(s): return s

LANGUAGES = (
    ('en', gettext_noop('English')),
    ('it', gettext_noop('Italian')),
    # ('de', gettext_noop('German')),
    # ('fr', gettext_noop('French')),
    # ('es', gettext_noop('Spanish')),
)

# Create your models here.
class User(AbstractUser):
  privacy = models.BooleanField(default=False, verbose_name=_("Consent Privacy"))
  newsletter = models.BooleanField(default=False, verbose_name=_("Consent Newsletter"))
  lang = models.CharField(default='en', max_length=10, choices=LANGUAGES, verbose_name=_("Preferred language"))

  class Meta:
    db_table = 'auth_user'

