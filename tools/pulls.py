"""MCP tools for pull requests."""

from github_client import get_repo_pulls, GitHubClientError


def register(mcp):
    @mcp.tool()
    def get_open_prs(repo: str) -> str:
        """Get open pull requests for a repo.

        Args:
            repo: Full repo name, e.g. 'alibro005/github-mcp-server'
        """
        try:
            prs = get_repo_pulls(repo, state="open")
        except GitHubClientError as e:
            return f"Error: {e}"

        if not prs:
            return "No open pull requests."

        return "\n".join(
            f"#{pr['number']}: {pr['title']} (by {pr['user']['login']})" for pr in prs
        )
