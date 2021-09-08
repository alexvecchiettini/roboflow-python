import json
import os
import time

import requests

from roboflow.core.project import Project
from roboflow.config import *


def check_key(api_key):
    if type(api_key) is not str:
        raise RuntimeError(
            "API Key is of Incorrect Type \n Expected Type: " + str(type("")) + "\n Input Type: " + str(type(api_key)))

    response = requests.post(API_URL + "/?api_key=" + api_key)
    r = response.json()

    if "error" in r or response.status_code != 200:
        raise RuntimeError(response.text)
    else:
        return r


def auth(api_key):
    r = check_key(api_key)
    w = r['workspace']

    return Roboflow(api_key, w)


class Roboflow():
    def __init__(self, api_key):
        self.api_key = api_key
        self.auth()

    def auth(self):
        r = check_key(self.api_key)
        w = r['workspace']

        self.current_workspace=w

        return self

    def workspace(self, the_workspace=None):

        if the_workspace is None:
            the_workspace = self.current_workspace

        list_projects = requests.get(API_URL + "/" + the_workspace + '?api_key=' + self.api_key).json()

        return list_projects

    def project(self, project_name, the_workspace=None):

        if the_workspace is None:
            the_workspace = self.current_workspace

        dataset_info = requests.get(API_URL + "/" + the_workspace + "/" + project_name + "?api_key=" + self.api_key)

        # Throw error if dataset isn't valid/user doesn't have permissions to access the dataset
        if dataset_info.status_code != 200:
            raise RuntimeError(dataset_info.text)

        dataset_info = dataset_info.json()['project']

        return Project(self.api_key, dataset_info['id'], dataset_info['type'], dataset_info['versions'])

    def __str__(self):
        json_value = {'api_key': self.api_key,
                      'workspace': self.workspace}
        return json.dumps(json_value, indent=2)
