from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import PasswordSetView, PasswordChangeView
from django.urls import reverse_lazy
from django.http import HttpResponse
from allauth.socialaccount.models import SocialAccount


def get_sponsor_picture(req, email):
    user = SocialAccount.objects.get(extra_data__contains='"email": "{}"'.format(email)).get_avatar_url()
    return HttpResponse(user)


# utility
class DashboardView(LoginRequiredMixin, View):
    def get(self, req):
        greeting = {'heading': "FAQs", 'pageview': "Home"}
        return render(req, 'dashboard/dashboard.html', greeting)


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('dashboard')


class MyPasswordSetView(LoginRequiredMixin, PasswordSetView):
    success_url = reverse_lazy('dashboard')
