"""Configuration for the GitHub MCP server."""

import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_API_BASE = "https://api.github.com"

if not GITHUB_TOKEN:
    raise RuntimeError(
        "GITHUB_TOKEN is not set. Create a .env file (see .env.example) "
        "with a valid GitHub personal access token."
    )

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
