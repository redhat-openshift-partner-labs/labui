import time

import requests
import jq
import re
from decouple import config
from distutils.version import StrictVersion


def get_openshift_versions():
    payload = requests.get("https://quay.io/api/v1/repository/openshift-release-dev/ocp-release?includeTags=true").json()
    versions = jq.compile(".tags|with_entries(select(.key|match(\"x86_64\")))|keys").input(payload).first()
    pattern = ".*(hotfix|assembly|art|fc|rc).*"
    images = []
    selectable_versions = []
    filtered = [version for version in versions if not re.match(pattern, version)]
    for version in filtered:
        release = version.split("-")
        image = release[0]
        images.append(image)
    images.sort(key=StrictVersion, reverse=True)
    for image in images:
        selectable_versions.append((image, "ocp-" + image))
    return selectable_versions


def get_labs(is_superuser, email):
    url = 'http://localhost:3000/requests'
    labs = {}
    labs_list = []

    if is_superuser:
        for i in range(5):
            res = requests.get(url, headers={'Authorization': 'Bearer %s' % config('ACCESS_TOKEN')})
            if res.status_code != 200:
                time.sleep(2)
                continue
            else:
                labs = res.json()
                break

        if labs:
            for i in range(len(labs)):
                labs_list.append(labs[i])
            return labs_list
        else:
            return labs_list
    else:
        for i in range(5):
            res = requests.get(url, headers={'Sponsor': email})
            if res.status_code != 200:
                time.sleep(2)
                continue
            else:
                labs = res.json()
                break

        if labs:
            for i in range(len(labs)):
                labs_list.append(labs[i])
            return labs_list
        else:
            return labs_list


def get_lab(cluster_id):
    url = 'http://localhost:3000/requests/' + cluster_id
    lab = {}

    for i in range(5):
        res = requests.get(url, headers={'Authorization': 'Bearer %s' % config('ACCESS_TOKEN')})
        if res.status_code != 200:
            time.sleep(2)
            continue
        else:
            lab = res.json()
            break
    return lab
