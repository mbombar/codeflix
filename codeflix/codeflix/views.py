from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.shortcuts import resolve_url
from django.template import loader
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, TemplateView

from . import settings
from .forms import SignUpForm
from .tokens import account_activation_token

# create your views here.


class UserCreateView(CreateView):
    """
    A view used to register a new user.
    """
    email_template_name = 'registration/account_activation_email.html'
    form_class = SignUpForm
    success_url = reverse_lazy('account_activation_sent')
    template_name = 'registration/signup.html'
    title = _("Sign up")
    token_generator = account_activation_token

    def form_valid(self, form):
        """
        If the form is valid, then the user is created with is_active set to False
        so that the user cannot log in until the email has been validated.
        """
        use_https = self.request.is_secure()
        user = form.save(commit=False)
        user.is_active = False
        user.save()  # Sends a signal to create the corresponding profile object.
        site = get_current_site(self.request)
        subject = "Activate your {} account".format(site.name)
        message = loader.render_to_string('registration/account_activation_email.html',
                                          {
                                              'user': user,
                                              'domain': site.domain,
                                              'site_name': site.name,
                                              'protocol': 'https' if use_https else 'http',
                                              'token': self.token_generator.make_token(user),
                                              'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                          })
        user.email_user(subject, message)
        return super().form_valid(form)


class UserActivateView(TemplateView):
    succes_url = reverse_lazy('account_activation_done')
    title = _("Account Activation")

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        """
        The dispatch method looks at the request to determine whether it is a GET, POST, etc,
        and relays the request to a matching method if one is defined, or raises HttpResponseNotAllowed
        if not. We chose to check the token in the dispatch method to mimic PasswordReset from
        django.contrib.auth
        """
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        user = self.get_user(kwargs['uidb64'])
        token = kwargs['token']

        if user is not None and account_activation_token.check_token(user, token):
            self.validlink = True
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            return super().dispatch(*args, **kwargs)
        else:
            # Display the "Account Activation unsuccessful" page.
            return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'title': _('Account Activation unsuccessful'),
                'validlink': False,
            })
        return context


class UserActivateDoneView(TemplateView):
    template_name = 'registration/account_activation_complete.html'
    title = _('Account activation complte')

    def get_context_data(self, **kwargs):
        """
        Provides the template with the login_url.
        """
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


class UserActivationEmailSentView(TemplateView):
    template_name = 'registration/account_activation_email_sent.html'
    title = _('Account activation email sent')
