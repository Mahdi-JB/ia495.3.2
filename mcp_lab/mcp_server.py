"""A real MCP server exposing mock tools over stdio.

Nothing here performs a real action. Each tool records what it was asked to do
and returns a confirmation string. Run it directly to sanity-check:

    python mcp_lab/mcp_server.py        (it will wait for a client on stdio)

Normally you don't run it yourself - bridge.py launches it as a subprocess.
"""
# mcp 2.x renamed FastMCP -> MCPServer. Support both so the lab runs on
# whichever version is installed.
try:
    from mcp.server.mcpserver import MCPServer as _Server      # mcp >= 2
except ModuleNotFoundError:                                     # mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Server

mcp = _Server("ia495-mock-tools")


@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    return f"[SIMULATED] email -> {to} | subject={subject!r} | {len(body)} chars"


@mcp.tool()
def read_file(path: str) -> str:
    """Read a report file from /data/reports/."""
    return f"[SIMULATED] read {path}"


@mcp.tool()
def query_database(table: str, filter: str, limit: int = 10) -> str:
    """Query a database table with a filter expression."""
    return f"[SIMULATED] query {table} where {filter} limit {limit}"


@mcp.tool()
def create_event(title: str, date: str, attendees: list[str]) -> str:
    """Create a calendar event."""
    return f"[SIMULATED] event {title!r} on {date} with {len(attendees)} attendees"


@mcp.tool()
def post_message(channel: str, text: str) -> str:
    """Post a message to a chat channel."""
    return f"[SIMULATED] posted to {channel}: {len(text)} chars"


if __name__ == "__main__":
    mcp.run()
