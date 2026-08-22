"""MCP tools for commit history."""

from github_client import get_repo_commits, GitHubClientError


def register(mcp):
    @mcp.tool()
    def get_recent_commits(repo: str, limit: int = 5) -> str:
        """Get recent commits for a repo.

        Args:
            repo: Full repo name, e.g. 'alibro005/github-mcp-server'
            limit: Number of commits to return (default 5)
        """
        try:
            commits = get_repo_commits(repo, limit=limit)
        except GitHubClientError as e:
            return f"Error: {e}"

        if not commits:
            return "No commits found."

        lines = []
        for c in commits:
            sha = c["sha"][:7]
            message = c["commit"]["message"].splitlines()[0]
            author = c["commit"]["author"]["name"]
            lines.append(f"{sha}: {message} ({author})")
        return "\n".join(lines)
