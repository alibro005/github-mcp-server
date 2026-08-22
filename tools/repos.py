"""MCP tools for listing repositories."""

from config import GITHUB_USERNAME
from github_client import get_user_repos, GitHubClientError


def register(mcp):
    @mcp.tool()
    def list_my_repos() -> str:
        """List all repositories owned by the configured GitHub user."""
        try:
            repos = get_user_repos(GITHUB_USERNAME)
        except GitHubClientError as e:
            return f"Error: {e}"

        if not repos:
            return "No repositories found."

        lines = []
        for r in repos:
            visibility = "private" if r.get("private") else "public"
            stars = r.get("stargazers_count", 0)
            lines.append(f"{r['full_name']} ({visibility}, ★{stars})")
        return "\n".join(lines)
