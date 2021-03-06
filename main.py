import json
import requests

from config import token


def accept_merge(url, headers):
    url      += "/merge"
    content   = "Merge 완료!\n Merge Accepted!"
    response  = requests.put(url = url, headers = headers)

    if response.status_code == 409:
        content = "Conflict를 해결해주세요!\nSolve your conflict problem!"

    return content


def check_file(url, headers):
    url      += "/files"
    response  = requests.get(url = url, headers = headers).json()

    file = response[0]["filename"]
    if (len(response) == 1) and (file == "test_by_js.js" or file == "test_by_python.py"):
        return True

    return False


def create_comment(url, headers, content):
    url     += "/comments"
    body     = {"body": content}
    response = requests.post(
        url     = url,
        headers = headers,
        data    =  json.dumps(body)
    )

    return response.json()


def lambda_handler(event, context):
    headers    = {
        "Accept"       : "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
    }
    data = json.loads(event["body"])

    commit_count        = data["pull_request"]["commits"]
    issue_url           = data["pull_request"]["issue_url"]
    pull_request_url    = data["pull_request"]["url"]


    if not check_file:
        content  = "test_by_ 파일만 수정하실 수 있습니다! 다른 파일은 건들이지 말아주세요.\nYou can only edit test_by_ file! Do not edit others."
        response = create_comment(issue_url, headers, content)
        print(response)
        return False

    if commit_count > 1:
        content  = "git rebase를 통해 commit을 정리해주세요 :)\n Squash your commits by using git rebase command :)"
        response = create_comment(issue_url, headers, content)
        print(response)
        return False

    content  = accept_merge(pull_request_url, headers)
    response = create_comment(issue_url, headers, content)
    print(response)
