import mimetypes
from typing import List

import requests
import json

from ango.models.label_category import LabelCategory


class SDK:
    def __init__(self, api_key, host="https://api.ango.ai"):
        self.api_key = api_key
        self.host = host

    def list_projects(self):
        url = "%s/v2/listProjects" % self.host

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_project(self, project_id):
        url = "%s/v2/project/%s" % (self.host, project_id)

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_tasks(self, project_id, page=1, limit=10, status=None):
        url = "%s/v2/project/%s/tasks?page=%s&limit=%s" % (self.host, project_id, page, limit)
        if status :
            url += "&status[eq]=%s" % status
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_task(self, task_id):
        url = "%s/v2/task/%s" % (self.host, task_id)

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def upload_files(self, project_id, file_paths):
        url = "%s/v2/project/%s/upload" % (self.host, project_id)

        payload = {}
        files = []
        for path in file_paths:
            file = open(path, 'rb')
            files.append(
                ('files', (file.name, file, mimetypes.guess_type(path)))
            )

        headers = {
            'apikey': self.api_key
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        return response.json()

    def upload_files_cloud(self, project_id, assets):
        url = "%s/v2/project/%s/cloud" % (self.host, project_id)
        payload = json.dumps({"assets": assets})
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def create_issue(self, task_id, content, position):
        import requests

        url = "%s/v2/issues" % self.host

        payload = json.dumps({
            "content": content,
            "labelTask": str(task_id),
            "position": str(position)
        })
        headers = {
            'apikey': self.api_key
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def get_assets(self):
        url = "%s/v2/assets" % self.host

        payload = {}
        headers = {
            'apikey': self.api_key
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def set_asset_priority(self, asset_id, project_id, priority):
        url = "%s/v2/assets/%s" % (self.host, asset_id)

        payload = json.dumps({
            "priority": priority,
            "project": project_id
        })
        headers = {
            'apikey': self.api_key
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def create_attachment(self, project_id, external_id, attachments):

        url = "%s/v2/attachments" % self.host

        payload = json.dumps({
            "project": project_id,
            "externalId": external_id,
            "attachments": attachments
        })
        headers = {
            'apikey': self.api_key
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def export(self, project_id):

        url = "%s/v2/export?project=%s" % (self.host, project_id)
        headers = {
            'apikey': self.api_key
        }
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def create_label_set(self, project_id: str, tools: List[LabelCategory]):

        url = "%s/v2/project/%s" % (self.host, project_id)
        headers = {
            'apikey': self.api_key
        }
        payload = json.dumps({
            "categorySchema": {
                "tools": list(map(lambda t: t.toDict(), tools)),
                "classifications": [],
                "relations": []
            }}
        )

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
