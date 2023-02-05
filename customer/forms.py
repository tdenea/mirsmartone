from django import forms
from django.utils import translation
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from oscar.apps.customer.forms import EmailUserCreationForm as CoreEmailUserCreationForm
from oscar.core.compat import (existing_user_fields, get_user_model)
from oscar.apps.customer.forms import UserForm as CoreUserForm

User = get_user_model()

class UserProfileCustomForm(CoreUserForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'lang']

class EmailUserCreationForm(CoreEmailUserCreationForm):
    CHOICES=[(True, _('presta il consenso')),
         (False, _('nega il consenso'))]

    newsletter = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('email', 'newsletter', 'privacy')
    
    field_order = ['email', 'password', 'password1', 'password2','privacy', 'newsletter',]


    def __init__(self, host=None, token=None, *args, **kwargs):
        self.host = host
        super().__init__(*args, **kwargs)
        self.fields['privacy'].label = _('*Label Privacy Registration')
        self.fields['privacy'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            # Salvo la lingua dell'utente
            print('DENTRO SAVE')
            language = translation.get_language()
            print(language)
            for key, lang in settings.LANGUAGES:
                if key == language:
                    user.lang = language
            user.save()
        return user