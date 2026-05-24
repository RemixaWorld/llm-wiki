---
domain: docs.devin.ai
fetch_date: '2026-05-18T12:37:59.494897'
status: ok
url: https://docs.devin.ai/work-with-devin/deepwiki-mcp#setup-instructions
---

The DeepWiki MCP server provides programmatic access to DeepWiki’s public repository documentation and search capabilities (Ask Devin).## Documentation Index

Fetch the complete documentation index at: https://docs.devin.ai/llms.txt

Use this file to discover all available pages before exploring further.


## What is MCP?

The Model Context Protocol (MCP) is an open standard that enables AI apps to securely connect to MCP-compatible data sources and tools. You can think of MCP like a USB-C port for AI applications - a standardized way to connect AI apps to different services.## DeepWiki MCP Server

The DeepWiki MCP server is a free, remote, no-authentication-required service that provides access to public repositories.**Base Server URL:**

`https://mcp.deepwiki.com/`

### Available Tools

The DeepWiki MCP server offers three main tools:- Get a list of documentation topics for a GitHub repository`read_wiki_structure`

- View documentation about a GitHub repository`read_wiki_contents`

- Ask any question about a GitHub repository and get an AI-powered, context-grounded response`ask_question`


### Wire Protocols

The DeepWiki MCP server supports two wire protocols:#### Streamable HTTP - `/mcp`


**URL:**`https://mcp.deepwiki.com/mcp`

- Works with Cloudflare, OpenAI, and Claude
**Recommended for most integrations**

#### SSE (Server-Sent Events) - `/sse`


**URL:**`https://mcp.deepwiki.com/sse`

- Legacy protocol, being deprecated

The

`/mcp`

endpoint is recommended as SSE is being deprecated.## Setup Instructions

### For most clients (e.g. Windsurf, Cursor):

### For Claude Code:

## Related Resources

**Devin’s MCP Marketplace****Connecting remote MCP servers to Claude****OpenAI’s docs for using the DeepWiki MCP server****DeepWiki****Ask Devin**

Want DeepWiki capabilities for private repositories? Sign up for a Devin account at Devin.ai and use the Devin MCP server with your Devin API key.
