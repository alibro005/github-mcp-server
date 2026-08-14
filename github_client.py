"""Thin wrapper around the GitHub REST API.

Keeping all HTTP logic here means the tool functions stay simple,
and error handling / retries only need to live in one place.
"""

import requests
from config import GITHUB_API_BASE, HEADERS


class GitHubClientError(Exception):
    """Raised when a GitHub API call fails."""


def _get(path: str, params: dict | None = None) -> list | dict:
    url = f"{GITHUB_API_BASE}{path}"
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        if status == 404:
            raise GitHubClientError(f"Not found: {path}") from e
        if status == 401:
            raise GitHubClientError("Authentication failed — check GITHUB_TOKEN") from e
        if status == 403:
            raise GitHubClientError("Forbidden or rate-limited by GitHub API") from e
        raise GitHubClientError(f"GitHub API error ({status}) on {path}") from e
    except requests.exceptions.RequestException as e:
        raise GitHubClientError(f"Network error calling GitHub API: {e}") from e


def get_user_repos(username: str) -> list:
    return _get(f"/users/{username}/repos", params={"per_page": 100, "sort": "updated"})


def get_repo_issues(repo: str, state: str = "open") -> list:
    return _get(f"/repos/{repo}/issues", params={"state": state, "per_page": 50})


def get_repo_pulls(repo: str, state: str = "open") -> list:
    return _get(f"/repos/{repo}/pulls", params={"state": state, "per_page": 50})


def get_repo_commits(repo: str, limit: int = 5) -> list:
    return _get(f"/repos/{repo}/commits", params={"per_page": limit})
