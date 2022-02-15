import json
import time
import requests

from datetime import datetime, timedelta
from allauth.socialaccount.models import SocialAccount
from decouple import config
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LabRequestsForm
from .services import get_openshift_versions, get_labs, get_lab


def create_request(req):
    formdata = req.POST.dict()

    # Set necessary fields
    if formdata["primary_phone_number"] == "":
        formdata["primary_phone_number"] = 0
    else:
        formdata["primary_phone_number"] = int(formdata["primary_phone_number"])

    if formdata["secondary_phone_number"] == "":
        formdata["secondary_phone_number"] = 0
    else:
        formdata["secondary_phone_number"] = int(formdata["secondary_phone_number"])

    formdata["partner"] = True
    if formdata["request_type"] == "":
        formdata["request_type"] = "general"

    date = datetime.now()
    timefmt = '%Y-%m-%dT%H:%M:%SZ'
    formdata["time"] = datetime.strftime(date, timefmt)
    formdata["epoch"] = int(date.strftime('%s'))

    # Remove unnecessary fields
    fields = ["csrfmiddlewaretoken"]
    for field in fields:
        del formdata[field]

    # Set start_date and desired_start_date
    if formdata["start_date"] != "":
        date = datetime.strptime(formdata["start_date"], "%d %b, %Y")
        timefmt = '%Y-%m-%dT%H:%M:%SZ'

        formdata["desired_start_date"] = datetime.strftime(date, timefmt)
        formdata["start_date"] = datetime.strftime(date, timefmt)
    else:
        date = datetime.now()
        timefmt = '%Y-%m-%dT%H:%M:%SZ'

        formdata["desired_start_date"] = datetime.strftime(date, timefmt)
        formdata["start_date"] = datetime.strftime(date, timefmt)

    # Set end_date based on desired_start_date
    match formdata["reservation_time"]:
        case "1d":
            formdata["end_date"] = datetime.strftime(date + timedelta(days=1), timefmt)
            formdata["adjusted_end_date"] = datetime.strftime(date + timedelta(days=1), timefmt)
        case "1w":
            formdata["end_date"] = datetime.strftime(date + timedelta(days=7), timefmt)
            formdata["adjusted_end_date"] = datetime.strftime(date + timedelta(days=7), timefmt)
        case "2w":
            formdata["end_date"] = datetime.strftime(date + timedelta(days=14), timefmt)
            formdata["adjusted_end_date"] = datetime.strftime(date + timedelta(days=14), timefmt)
        case "1m":
            formdata["end_date"] = datetime.strftime(date + timedelta(days=30), timefmt)
            formdata["adjusted_end_date"] = datetime.strftime(date + timedelta(days=30), timefmt)

    payload = json.dumps(formdata)
    url = "http://localhost:3000/requests"

    res = requests.post(url, payload, headers={'Authorization': 'Bearer %s' % config('ACCESS_TOKEN')})
    message = res.json()

    if res.status_code != 200:
        openshift_versions = get_openshift_versions()
        form = LabRequestsForm()
        return render(req, 'labrequests/create.html',
                      {
                          'form': form,
                          'versions': openshift_versions,
                          'message': message,
                          'heading': 'Create',
                          'pageview': 'Requests',
                      })

    openshift_versions = get_openshift_versions()
    form = LabRequestsForm()
    return render(req, 'labrequests/create.html',
                  {
                      'form': form,
                      'versions': openshift_versions,
                      'message': message,
                      'heading': 'Create',
                      'pageview': 'Requests',
                  })


# utility
class CreateRequestView(LoginRequiredMixin, View):
    def get(self, req):
        #if not req.user.is_authenticated:
        openshift_versions = get_openshift_versions()
        form = LabRequestsForm()
        return render(req, 'labrequests/create.html',
                      {
                          'form': form,
                          'versions': openshift_versions,
                          'heading': 'Create',
                          'pageview': 'Requests',
                      })


class ApprovedRequestView(LoginRequiredMixin, View):
    def get(self, req, cluster_id):
        if req.user.is_superuser:
            url = 'http://localhost:3000/requests/approved/' + cluster_id
            res = requests.post(url, headers={'Authorization': 'Bearer %s' % config('ACCESS_TOKEN')})
            msg = res.json()

            print(msg)
            lab = get_lab(cluster_id)

            # noinspection PyBroadException
            try:
                lab["picture"] = SocialAccount.objects.get(
                    extra_data__contains='"email": "{}"'.format(lab["sponsor"])).get_avatar_url()
            except SocialAccount.DoesNotExist:
                lab["picture"] = "https://via.placeholder.com/96?text="

            return render(req, 'labrequests/single.html', {'lab': lab, 'heading': 'View', 'pageview': 'Request', 'message': msg})

        return redirect('requests-view')


class DeniedRequestView(LoginRequiredMixin, View):
    def get(self, req, cluster_id):
        if req.user.is_superuser:
            url = 'http://localhost:3000/requests/denied/' + cluster_id
            res = requests.post(url, headers={'Authorization': 'Bearer %s' % config('ACCESS_TOKEN')})
            msg = res.json()

            print(msg)
            lab = get_lab(cluster_id)

            # noinspection PyBroadException
            try:
                lab["picture"] = SocialAccount.objects.get(
                    extra_data__contains='"email": "{}"'.format(lab["sponsor"])).get_avatar_url()
            except SocialAccount.DoesNotExist:
                lab["picture"] = "https://via.placeholder.com/96?text="

            return render(req, 'labrequests/single.html', {'lab': lab, 'heading': 'View', 'pageview': 'Request', 'message': msg})

        return redirect('requests-view')
    

class DeleteRequestView(LoginRequiredMixin, View):
    def get(self, req, cluster_id):
        if req.user.is_superuser:
            url = 'http://localhost:3000/requests/deleted/' + cluster_id
            res = requests.post(url, headers={'Authorization': 'Bearer %s' % config('ACCESS_TOKEN')})
            msg = res.json()

            labs = get_labs(req.user.is_superuser, req.user.email)
            return render(req, 'labrequests/view.html',
                          {'labs': labs, 'heading': 'View', 'pageview': 'Requests', 'message': msg})

        return redirect('requests-view')


class ViewRequestsView(LoginRequiredMixin, View):
    def get(self, req):
        if req.user.is_authenticated:
            labs = get_labs(req.user.is_superuser, req.user.email)
        return render(req, 'labrequests/view.html', {'labs': labs, 'heading': 'View', 'pageview': 'Requests'})
    

class ViewSingleRequestView(LoginRequiredMixin, View):
    def get(self, req, cluster_id):
        if req.user.is_authenticated:
            lab = get_lab(cluster_id)

        if (req.user.email != lab["sponsor"]) and (not req.user.is_superuser):
            labs = get_labs(req.user.is_superuser, req.user.email)
            return render(req, 'labrequests/view.html', {'labs': labs, 'heading': 'View', 'pageview': 'Requests', 'message': 'Unauthorized'})

        # noinspection PyBroadException
        try:
            lab["picture"] = SocialAccount.objects.get(
                extra_data__contains='"email": "{}"'.format(lab["sponsor"])).get_avatar_url()
        except SocialAccount.DoesNotExist:
            lab["picture"] = "https://via.placeholder.com/96?text="

        return render(req, 'labrequests/single.html', {'lab': lab, 'heading': 'View', 'pageview': 'Request'})


class ManageRequestsView(LoginRequiredMixin, View):
    def get(self, req):
        if req.user.is_authenticated:
            labs = get_labs(req.user.is_superuser, req.user.email)
        return render(req, 'labrequests/manage.html', {'labs': labs, 'heading': 'Manage', 'pageview': 'Requests'})


class ManageSingleRequestView(LoginRequiredMixin, View):
    def get(self, req, cluster_id):
        if req.user.is_authenticated:
            lab = get_lab(req.user.is_superuser, req.user.email, cluster_id)
            
        if req.user.email != lab["sponsor"] and not req.user.is_superuser:
            labs = get_labs(req.user.is_superuser, req.user.email)
            return render(req, 'labrequests/view.html', {'labs': labs, 'heading': 'View', 'pageview': 'Requests', 'message': 'Unauthorized'})

        return render(req, 'labrequests/single.html', {'lab': lab, 'heading': 'Manage', 'pageview': 'Request'})
