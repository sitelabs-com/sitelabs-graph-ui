<!-- menu -->
[Features](features.md) · [Using the page](using.md) · **Serving it** · [Development](development.md) · [Security](security.md) · [References](index.md)

**Serving it:** **Overview** · [Server contract](server-contract.md) · [Installing into a project](installing.md)
<!-- /menu -->

# Serving it

> **For:** developers of a server that serves the page. **You'll find:** the steps, an example in
> FastAPI, and how to check it works.

A server needs three small routes for the page, and an openCypher endpoint the page can call. In
sitelabs-partitioned-graph and sitelabs-graph-database these are about 30 lines, in
`app/routers/console.py`. Every request and answer is in the [Server contract](server-contract.md).

## Step by step

1. **Install a copy** of a release into the project, for example into `app/static/graph-ui`
   ([Installing into a project](installing.md)).
2. **Serve the page** at `GET /console`: `console.html`, with the
   [content security policy](security.md#the-content-security-policy). It needs no key.
3. **Say what the server has** at `GET /console/config.json`: its title, and which of `schema`,
   `pages`, `profile`, `past` and `cancel` it has.
4. **Serve the two libraries** at `GET /console/vendor/<file>`: `3d-force-graph.min.js` and
   `force-graph.min.js`, and no other file.
5. **Answer queries** at `POST /opencypher`, refusing a write when `read_only` is true.
6. **Test it** against the server ([below](#checking-it-works)).

## An example, in FastAPI

```python
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

router = APIRouter(include_in_schema=False)
UI = Path(__file__).resolve().parents[1] / "static" / "graph-ui"      # the installed copy
VENDOR = ("3d-force-graph.min.js", "force-graph.min.js")
CONFIG = {"title": "Graph console", "schema": True, "pages": True, "profile": False, "past": False, "cancel": True}
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'unsafe-inline'; "
       "img-src 'self' data: blob:; connect-src 'self'; frame-ancestors 'none'")


@router.get("/console", response_class=HTMLResponse)
def console() -> HTMLResponse:
    return HTMLResponse((UI / "console.html").read_text(encoding="utf-8"),
                        headers={"Content-Security-Policy": CSP, "X-Content-Type-Options": "nosniff"})


@router.get("/console/config.json")
def config() -> dict:
    return CONFIG


@router.get("/console/vendor/{name}")
def vendor(name: str) -> FileResponse:
    if name not in VENDOR:                                             # these two, and no other file
        raise HTTPException(404, f"no file {name!r}")
    return FileResponse(UI / "vendor" / name, media_type="text/javascript",
                        headers={"Cache-Control": "public, max-age=86400", "X-Content-Type-Options": "nosniff"})
```

sitelabs-partitioned-graph's
[app/routers/console.py](https://github.com/sitelabs-com/sitelabs-partitioned-graph/blob/main/app/routers/console.py)
is this, with every feature on.

## Choosing the features

Turn on only what the server really does: the page sends the extra fields and calls the extra paths of
each one it is told about.

| Feature | Turn it on when the server has |
|---|---|
| `schema` | `GET /schema` with counts and properties |
| `pages` | `page_size` on `POST /opencypher`, a `cursor` in the answer, and `GET /opencypher/cursors/{cursor}` |
| `profile` | `"profile": true`, answered with the partitioned-graph profile shape |
| `past` | `at_load`: reading the graph as it was after a past load |
| `cancel` | `DELETE /queries/{id}`, with the id from `X-Request-ID` |

A server with none of them still gets the whole page apart from those; the labels and types then come
from `CALL db.labels()` and `CALL db.relationshipTypes()`. Without a `config.json` at all (a 404, or no
answer) the page treats every feature as off.

## Checking it works

* Open `/console`, and check the title, the side panel's lists, and that the browser's console shows no
  errors and no content-security-policy refusals.
* Run `MATCH (a)-[r]->(b) RETURN a, r, b LIMIT 25`, and open **3D** and **2D**.
* Run `CREATE (:Test)`: it must be refused.
* In the project's own tests: check the installed copy is the release
  (`python install.py --check`), and that each route answers as above. sitelabs-partitioned-graph
  also runs this page in a browser against itself.
