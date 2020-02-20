import os
import pickle
import random

from codeforces.models import Problem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import redirect, resolve_url
from django.template import loader
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, TemplateView, UpdateView, View
from recommendation import recommendation as rec

from . import settings
from .forms import CodeforcesUpdateForm, SignUpForm
from .models import Profile
from .tokens import account_activation_token


# create your views here.

try:
    with open(os.path.join(settings.BASE_DIR, "codeflix-graph"), "rb") as pgraph:
        graph = pickle.load(pgraph, fix_imports=False)
except (TypeError, FileNotFoundError, EOFError, pickle.PickleError, pickle.UnpicklingError):
    graph = None

baseurl = "https://codeforces.com/contest/{cid}/problem/{index}"


class IndexView(TemplateView):
    """
    Homepage
    """
    template_name = 'index.html'
    title = _('Homepage')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('account_summary', pk=self.request.user.pk)
        return super().dispatch(*args, **kwargs)


class UserSummaryView(LoginRequiredMixin, TemplateView):
    """
    Homepage when user is loggedIn
    """
    template_name = 'index.html'
    title = _('Homepage')

    def get_context_data(self, **kwargs):
        try:
            problems = self.request.user.profile.cfuser.recommended_problems.all()
        except (TypeError, AttributeError):
            problems = Problem.objects.none()
        problemlist = []
        for pb in problems:
            name = pb.name
            url = baseurl.format(cid=pb.contest_id, index=pb.index)
            tags = pb.tags.all()
            problemlist.append((name, url, tags))
        random.shuffle(problemlist)
        context = super().get_context_data(**kwargs)
        context.update({
            'avatar': self.request.user.profile.avatar.url,
            'cfuser': self.request.user.profile.cfuser,
            'problems': problemlist,
        })
        return context


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
        site_name = settings.SITE_NAME or site.name
        subject = "Activate your {} account".format(site_name)
        message = loader.render_to_string('registration/account_activation_email.html',
                                          {
                                              'user': user,
                                              'domain': site.domain,
                                              'site_name': site_name,
                                              'protocol': 'https' if use_https else 'http',
                                              'token': self.token_generator.make_token(user),
                                              'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                          })
        user.email_user(subject, message)
        return super().form_valid(form)


class UserActivateView(TemplateView):
    title = _("Account Activation")
    template_name = 'registration/account_activation_complete.html'

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
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'title': _('Account Activation unsuccessful'),
                'validlink': False,
            })
        return context


class UserActivationEmailSentView(TemplateView):
    template_name = 'registration/account_activation_email_sent.html'
    title = _('Account activation email sent')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    template_name = "account/profile_update.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["avatar"] = context['user'].profile.avatar.url
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('account_summary', kwargs={'pk': self.object.id})


class AvatarUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['avatar']
    template_name = "account/avatar_update.html"

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('account_summary', kwargs={'pk': self.object.user.id})


class AvatarEraseView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = User.objects.get(id=kwargs.get('pk'))

        handle = user.profile.cfuser
        useremailconfirmed = user.profile.email_confirmed

        user.profile.delete()

        Profile.objects.create(user=user, cfuser=handle, email_confirmed=useremailconfirmed)
        user.profile.save()
        return redirect('account_summary', pk=kwargs['pk'])

class RenewRecommendationView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = User.objects.get(id=kwargs.get('pk'))
        cfuser = user.profile.cfuser
        cfuser.recommended_problems.clear()
        return redirect('recommendation', pk=kwargs['pk'])

class CodeforcesUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = CodeforcesUpdateForm
    template_name = "account/codeforces_update.html"

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('account_summary', kwargs={'pk': self.object.user.id})


class RecommendationView(TemplateView):
    """
    kwargs = {pk: primary key of the user}
    """
    template_name = "recommendation/generic.html"

    def dispatch(self, *args, **kwargs):
        assert 'pk' in kwargs
        uid = kwargs.get('pk')
        handle = self.get_cfuser(uid)
        self.recommendation = False

        if handle is not None and graph is not None:
            self.recommendation = True
            return super().dispatch(*args, **kwargs)
        else:
            # Display the "Recommendation unsuccessful" page
            return self.render_to_response(self.get_context_data())

    def get_cfuser(self, uid):
        try:
            user = User.objects.get(pk=uid)
            handle = user.profile.cfuser
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            handle = None
        return handle

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if not self.recommendation:
            context.update({
                'title' : _('Recommendation failed'),
                'recommendation' : False,
                'user': self.request.user,
            })
        else:
            user = User.objects.get(id=kwargs.get('pk'))
            cfuser = user.profile.cfuser
            handle = user.profile.cfuser.handle
            try:
                problems = cfuser.recommended_problems.all()
                if problems.count() == 0:
                    problems = rec.recommendation(handle, graph[1], graph[0])[:5]

            except (TypeError, AttributeError):
                problems = []
            recpb = []
            for pb in problems:
                pbobj = Problem.objects.filter(name=pb).first()
                cfuser.recommended_problems.add(pbobj)
                pburl = baseurl.format(cid=pbobj.contest_id, index=pbobj.index)
                tags = sorted(pbobj.tags.all(), key=lambda x: x.name)
                recpb.append((pb, pburl, tags))
            context.update({
                'title': _('Recommendation {}'.format(user)),
                'recommendation': True,
                'handle': handle,
                'problems': recpb,
                'user': self.request.user,
            })
        return context


class DumpGraphView(LoginRequiredMixin, View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        try:
            with open(os.path.join(settings.BASE_DIR, "codeflix-graph"), "wb") as pgraph:
                pickle.dump(graph, pgraph, protocol=pickle.HIGHEST_PROTOCOL,
                            fix_imports=False,)
        except TypeError:
            # Display the "Graph dump unsuccessful" page.
            return redirect(reverse_lazy("dump_graph_failed"))

        return redirect(reverse_lazy("dump_graph_done"))


class DumpGraphDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'graph/dump_complete.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['graph_length'] = len(graph[0])
        context['graph_dumped'] = True
        context['title'] = _('Graph dump complete')
        return context


class DumpGraphFailedView(LoginRequiredMixin, TemplateView):
    template_name = 'graph/dump_complete.html'
    title = _('Graph dump complete')

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Graph dump failed')
        context['graph_dumped'] = False
        return context


class LoadGraphView(LoginRequiredMixin, View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        global graph
        try:
            with open(os.path.join(settings.BASE_DIR, "codeflix-graph"), "rb") as pgraph:
                graph = pickle.load(pgraph, fix_imports=False)
        except (TypeError, FileNotFoundError, EOFError, pickle.PickleError, pickle.UnpicklingError):
            graph = None
            return redirect(reverse_lazy('load_graph_failed'))
        return redirect(reverse_lazy('load_graph_done'))


class LoadGraphDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'graph/load_complete.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['graph_length'] = len(graph[0])
            context['title'] = _('Graph load complete')
            context['graph_loaded'] = True
        except TypeError:
            context['title'] = _('Graph load failed')
            context['graph_loaded'] = False
        return context


class LoadGraphFailedView(LoginRequiredMixin, TemplateView):
    template_name = 'graph/load_complete.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Graph load failed')
        context['graph_loaded'] = False
        return context
