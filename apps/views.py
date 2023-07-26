from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, FormView

from apps.froms import RegisterForm, CustomLoginForm
from apps.models import User
from apps.utils.mail import send_to_gmail
from apps.utils.token import one_time_token


def index(request):
    return render(request, 'index.html')


class AccountSettingMixin(View):

    def check_one_time_link(self, data):
        uid64 = data.get('uid64')
        token = data.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(e)
            user = None
        if user and one_time_token.check_token(user, token):
            user.is_active = True
            user.save()
            return user
        return False


class RegisterView(CreateView):
    template_name = 'auth/register.html'
    queryset = User.objects.all()
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save()
        send_to_gmail(self.object, get_current_site(self.request).domain)
        return HttpResponseRedirect(self.get_success_url())


class ActivateUserView(AccountSettingMixin, TemplateView):
    template_name = 'temp.html'

    def get(self, request, *args, **kwargs):
        if user := self.check_one_time_link(kwargs):
            login(request, user)
            return redirect('index')
        return HttpResponse('Activation link is invalid!')


class CustomLoginView(FormView):
    form_class = CustomLoginForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if not user or not user.is_active:
            return HttpResponse('User is not activated yet')
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
