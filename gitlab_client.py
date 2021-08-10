import json
import logging
import requests
from config import GITLAB_BASE_URL_V4_DEFAULT
from exceptions import MergeError

logging.basicConfig(level=logging.DEBUG)


class GitlabClient:
    def __init__(self, project_id, access_token, gitlab_base_url=GITLAB_BASE_URL_V4_DEFAULT, **kwargs):
        self.project_id = project_id
        self.access_token = access_token
        self.gitlab_base_url = gitlab_base_url
    
    # Branches
    def list_branches(self):
        response = self.__get(url="repository/branches")

        if response.ok:
            return response.json()
        
        return []


    def get_branch(self, branch_name):
        response = self.__get(url=f"repository/branches/{branch_name}")
        
        if response.ok:
            return response.json()
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to get branch {branch_name}: {error_message}")


    def create_branch(self, branch_name, branch_from):
        data={"branch": branch_name, "ref": branch_from}
        response = self.__post(url="repository/branches", data=data)
        
        if response.ok:
            logging.info(f"Created branch: {response.json()['name']}")
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to create branch {branch_name}: {error_message}")


    def delete_branch(self, branch_name):
        response = self.__delete(url=f"repository/branches/{branch_name}")
        
        if response.ok:
            logging.info(f"Deleted branch: {branch_name}")
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to delete branch {branch_name}: {error_message}")
    
    # Tags
    def create_tag(self, tag_name, tag_on):
        data={"tag_name": tag_name, "ref": tag_on, "message": f"Automated release {tag_name}"}
        response = self.__post(url="repository/tags", data=data)
        
        if response.ok:
            logging.info(f"Created tag: {response.json()['name']}")
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to create tag {tag_name}: {error_message}")


    def delete_tag(self, tag_name):
        response = self.__delete(url=f"repository/tags/{tag_name}")
        
        if response.ok:
            logging.info(f"Deleted tag: {tag_name}")
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to delete tag {tag_name}: {error_message}")
    
    # Merge requests
    def create_merge_request(self, source_branch, target_branch, title, **kwargs):
        data={"source_branch": source_branch, "target_branch": target_branch, "title": title, **kwargs}
        response = self.__post(url="merge_requests", data=data)
        
        json_response = response.json()
        if response.ok:
            logging.info(f"Created merge request: {json_response['iid']} - {json_response['title']}")
            return {
                "iid": json_response["iid"],
                "web_url": json_response["web_url"]
            }
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to create merge request: {error_message}")


    def delete_merge_request(self, merge_request_iid):
        response = self.__delete(url=f"merge_request/{merge_request_iid}")
        
        if response.ok:
            logging.info(f"Deleted merge request: {merge_request_iid}")
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to delete merge request {merge_request_iid}: {error_message}")


    def merge(self, merge_request_iid):
        response = self.__put(url=f"merge_requests/{merge_request_iid}/merge")
        
        json_response = response.json()
        if response.ok:
            logging.info(f"Merged merge request: {json_response['iid']} - {json_response['title']}")
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to merge merge request {merge_request_iid}: {error_message}")
            raise MergeError
    
    # Pipelines
    def list_pipelines_by_merge_request(self, merge_request_iid):
        response = self.__get(url=f"merge_requests/{merge_request_iid}/pipelines")

        json_response = response.json()
        if response.ok:
            return json_response
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to get pipelines for merge request {merge_request_iid}: {error_message}")
    
    def __get(self, url):
        response = requests.get(
            f"{self.gitlab_base_url}/projects/{self.project_id}/{url}",
            headers={"PRIVATE-TOKEN": self.access_token}
        )

        return response
    
    def __put(self, url, data={}):
        response = requests.put(
            f"{self.gitlab_base_url}/projects/{self.project_id}/{url}",
            headers={"PRIVATE-TOKEN": self.access_token},
            data=data
        )

        return response
    
    def __post(self, url, data={}):
        response = requests.post(
            f"{self.gitlab_base_url}/projects/{self.project_id}/{url}",
            headers={"PRIVATE-TOKEN": self.access_token},
            data=data
        )

        return response
    
    def __delete(self, url):
        response = requests.delete(
            f"{self.gitlab_base_url}/projects/{self.project_id}/{url}",
            headers={"PRIVATE-TOKEN": self.access_token}
        )

        return response
