from oscar.apps.customer.views import ProfileView as CoreProfileView
from oscar.apps.customer.views import ProfileUpdateView as CoreProfileUpdateView
from oscar.apps.customer.views import AccountAuthView as CoreAccountAuthView
from django.utils import translation
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from oscar.core.compat import get_user_model
from oscar.core.loading import (
    get_class, get_classes, get_model, get_profile_class)
from .forms import UserProfileCustomForm

User = get_user_model()

class AccountAuthView(CoreAccountAuthView):
    def get_login_success_url(self, form):
        user = form.get_user()
        translation.activate(user.lang)
        self.request.session[translation.LANGUAGE_SESSION_KEY] = user.lang
        
        redirect_url = form.cleaned_data['redirect_url']
        if redirect_url:
            return redirect_url

        # Redirect staff members to dashboard as that's the most likely place
        # they'll want to visit if they're logging in.
        if self.request.user.is_staff:
            return reverse('dashboard:index')

        return '/' + user.lang + settings.LOGIN_REDIRECT_URL

class ProfileView(CoreProfileView):
    def get_profile_fields(self, user):
        field_data = []

        exclude_fields = ['privacy', 'newsletter']
        # Check for custom user model
        for field_name in User._meta.additional_fields:
            if not field_name in exclude_fields:
              field_data.append(
                  self.get_model_field_data(user, field_name))

        # Check for profile class
        profile_class = get_profile_class()
        if profile_class:
            try:
                profile = profile_class.objects.get(user=user)
            except ObjectDoesNotExist:
                profile = profile_class(user=user)

            field_names = [f.name for f in profile._meta.local_fields]
            for field_name in field_names:
                if field_name in ('user', 'id'):
                    continue
                field_data.append(
                    self.get_model_field_data(profile, field_name))

        return field_data


class ProfileUpdateView(CoreProfileUpdateView):
    def get_form_class(self):
        return UserProfileCustomForm
    
    def form_valid(self, form):
        # Grab current user instance before we save form.  We may need this to
        # send a warning email if the email address is changed.
        try:
            old_user = User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            old_user = None

        form.save()

        # We have to look up the email address from the form's
        # cleaned data because the object created by form.save() can
        # either be a user or profile instance depending whether a profile
        # class has been specified by the AUTH_PROFILE_MODULE setting.
        new_email = form.cleaned_data.get('email')
        if new_email and old_user and new_email != old_user.email:
            # Email address has changed - send a confirmation email to the old
            # address including a password reset link in case this is a
            # suspicious change.
            self.send_email_changed_email(old_user, new_email)
        
        # Attivo lingua utente
        language = form.cleaned_data.get('lang')
        translation.activate(language)
        self.request.session[translation.LANGUAGE_SESSION_KEY] = language

        messages.success(self.request, _("Profile updated"))
        return redirect(self.get_success_url())