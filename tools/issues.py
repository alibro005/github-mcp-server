"""MCP tools for repository issues."""

from github_client import get_repo_issues, GitHubClientError


def register(mcp):
    @mcp.tool()
    def get_open_issues(repo: str) -> str:
        """Get open issues for a repo.

        Args:
            repo: Full repo name, e.g. 'alibro005/github-mcp-server'
        """
        try:
            issues = get_repo_issues(repo, state="open")
        except GitHubClientError as e:
            return f"Error: {e}"

        # The GitHub issues endpoint also returns PRs — filter them out
        real_issues = [i for i in issues if "pull_request" not in i]
        if not real_issues:
            return "No open issues."

        return "\n".join(f"#{i['number']}: {i['title']}" for i in real_issues)
