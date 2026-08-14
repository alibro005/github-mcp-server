"""GitHub MCP Server.

Exposes GitHub repo activity (repos, issues, PRs, commits) as MCP tools
that any tool can call on request.

Run directly for local stdio use:
    python server.py
"""

from mcp.server import MCPServer

from tools import repos, issues, pulls, commits

mcp = MCPServer("github-mcp-server")

# Each tools/<x>.py module defines its own @mcp.tool() functions and registers them here. 

repos.register(mcp)
issues.register(mcp)
pulls.register(mcp)
commits.register(mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")
