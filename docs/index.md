<!-- menu -->
[Features](features.md) · [Using the page](using.md) · [Serving it](serving.md) · [Development](development.md) · [Security](security.md) · **References**
<!-- /menu -->

# References

> **For:** anyone looking for the right document. **You'll find:** every document, by section: what it
> is for and what it covers.

sitelabs-graph-ui is a read-only web page for a graph server: run openCypher queries, and see the
answer as a table, in 3D, in 2D or as JSON. Start with [Features](features.md).

## Features

| Document | Purpose | What's in it |
|---|---|---|
| [Features](features.md) | What the page does, in short | Querying, answers, what a server adds, around the page, what it doesn't do |

## Using the page

| Document | Purpose | What's in it |
|---|---|---|
| [Using the page](using.md) | Exploring a graph by hand | Opening it, the side panel, the query box and its keys, running, the answer's tabs, history, what it keeps in the browser |
| [Graph views](graph-views.md) | Drawing an answer | What is drawn and how it is recognised, moving round, the size limit, expanding a node |

## Serving it

| Document | Purpose | What's in it |
|---|---|---|
| [Serving it](serving.md) | Serving the page from a server | The steps, an example in FastAPI, choosing the features, checking it works |
| [Server contract](server-contract.md) | Everything the page calls | Every path, request field, header and answer, the page's own queries, each optional feature |
| [Installing into a project](installing.md) | Keeping a copy in a project | Installing and checking, the manifest, changing the page and releasing it, where the copies are |

## Development

| Document | Purpose | What's in it |
|---|---|---|
| [Development](development.md) | Working on the page | The repository, how the page is put together, trying a change, the vendored libraries, these docs |
| [Tests](testing.md) | What the tests cover | Running them, the stand-in server, every test, CI, what isn't tested |
| [How big a graph](graph-size.md) | How much is worth drawing | The measurements, what they show, the page's limits, measuring your own |

## Security

| Document | Purpose | What's in it |
|---|---|---|
| [Security](security.md) | What protects what | Read-only, escaping, the content security policy, the API key, history, what the server must do |

## Elsewhere in the repository

* [README.md](../README.md): the project in one page.
* [ui/vendor/README.md](../ui/vendor/README.md): the two libraries, their versions, licences and
  hashes.
* [install.py](../install.py): installing into a project, and checking a copy.
* [tools/docs.py](../tools/docs.py) and [docs/sitedocs.py](sitedocs.py): the docs' menus, and the
  site's sidebar written from them.
