<!-- menu -->
[Features](features.md) · [Using the page](using.md) · **Serving it** · [Development](development.md) · [Security](security.md) · [References](index.md)

**Serving it:** [Overview](serving.md) · **Server contract** · [Installing into a project](installing.md)
<!-- /menu -->

# Server contract

> **For:** developers of a server that serves the page. **You'll find:** every path the page calls,
> every field it sends and reads, and what each optional feature adds.

The page calls only its own server (`connect-src 'self'`), at these paths. Every call sends
`Content-Type: application/json`, and `X-API-Key` when a key has been typed. An answer that isn't
2xx is shown as `<status>: <error>`, from its `error` field, or its whole body when that isn't JSON.

## Always

| Path | What |
|---|---|
| `GET /console` | `console.html`, with the [content security policy](security.md#the-content-security-policy). Needs no key: the page asks for one |
| `GET /console/config.json` | What the server has ([below](#consoleconfigjson)) |
| `GET /console/vendor/<file>` | `3d-force-graph.min.js` and `force-graph.min.js`, and no other file. Called the first time a graph tab opens |
| `POST /opencypher` | Queries ([below](#post-opencypher)) |

### `/console/config.json`

```json
{"title": "Graph console", "schema": true, "pages": true, "profile": true, "past": true, "cancel": true,
 "login": {"sso": true, "keys": true}}
```

`title` names the page and its tab. Each other field turns on a [feature](#optional-features); a
missing one is off. When the file can't be fetched, every feature is off and the title is
"Graph console".

### `POST /opencypher`

The request:

| Field | When | What |
|---|---|---|
| `query` | Always | The query text; with **Explain**, `EXPLAIN ` and the query |
| `params` | Always | The parameters, as a JSON object (`{}` when there are none) |
| `read_only` | Always | `true`. The server must refuse a write, with a 400 |
| `page_size` | With `pages` | `500` |
| `profile` | With `profile`, on **Profile** | `true` |
| `at_load` | With `past`, when a load is given | The load number |

Headers: `X-API-Key` (when typed), and `X-Request-ID: console-<8 hex digits>` on each query from the
query box, for `cancel`.

The answer:

```json
{"columns": ["a", "r"],
 "rows": [{"a": {"id": "1", "labels": ["Person"], "properties": {"name": "Ann"}},
           "r": {"id": "7", "type": "KNOWS", "start": "1", "end": "2", "properties": {}}}],
 "stats": {"rounds": 2, "calls": 4}}
```

| Field | What |
|---|---|
| `columns` | The column names, in order |
| `rows` | One object a row, keyed by column |
| `stats` | Optional. With `rounds` and `calls`, the status line shows them |
| `cursor` | With `pages`: the next page's cursor, or absent/null on the last |
| `profile` | With `profile`, when asked for ([below](#profile)) |

The values the page draws and shows specially:

| Value | Shape |
|---|---|
| A node | `{"id", "labels", "properties"}` |
| A relationship | `{"id", "type", "start", "end", "properties"}`: `start` and `end` are node ids |
| A path | `{"nodes", "relationships"}`: lists of the above |

Ids may be strings or numbers, but must be the same for a node and the relationships that refer to it,
and must not be `0` or `""`: the graph views skip a value whose `id` is empty or zero.

An error: a non-2xx status and `{"error": "..."}`. When the message holds `offset N` (a character offset
into the query), the page marks the query there.

### What the page's own queries need

| Query | Needs |
|---|---|
| `CALL db.labels() YIELD label RETURN label` | Without `schema`: the labels, a row each |
| `CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType` | Without `schema`: the relationship types |
| ``MATCH (n:`L`) RETURN n LIMIT 25`` | Clicking a label or node type |
| ``MATCH (a)-[r:`T`]->(b) RETURN a, r, b LIMIT 25`` | Clicking a relationship type |
| `MATCH (a)-[r]-(b) WHERE id(a) = $id RETURN a, r, b LIMIT 100` | Expanding; `id()` must take the node's `id` as the answer gives it |

## Optional features

### `schema`

`GET /schema` answers:

```json
{"load": 12, "nodes": 1000, "relationships": 8000,
 "labels": [{"name": "Person", "count": 1000}],
 "node_types": [{"name": "Person", "count": 1000, "properties": [{"name": "name", "type": "str"}]}],
 "relationship_types": [{"name": "KNOWS", "count": 8000, "properties": []}]}
```

### `pages`

`page_size` in the request, `cursor` in the answer, and `GET /opencypher/cursors/{cursor}` answering
`{"rows", "cursor"}` for the next page. **Fetch more rows to draw** adds `?page_size=5000`.

### `profile`

`"profile": true` in the request; the answer's `profile`:

```json
{"seconds": {"total": 0.012, "partitions": 0.009, "coordinator": 0.003},
 "plan": ["NodeScan(p:Person)", "Expand(p)-[:KNOWS]->(q)"],
 "rounds": [{"round": 1, "call": ["scan"], "partitions": [0, 1], "sent": 0, "received": 120, "seconds": 0.004}]}
```

The shape is sitelabs-partitioned-graph's (the plan's lines above are only an illustration): a server
without partitions would turn this off.

### `past`

`at_load` in the request: read the graph as it was after that load.

### `cancel`

`DELETE /queries/{id}`, with the `X-Request-ID` the query was sent with. Whatever the query's own
request then answers (usually an error) is shown as usual; an error from the `DELETE` is shown too.

### `login`

An object, `{"sso": true, "keys": true}`: the page can sign in, and stay signed in in this browser,
with a session cookie the server sets. The page never sees the cookie or a token.

| Path | What |
|---|---|
| `GET /session` | Who is signed in: `{"signed_in": true, "name", "role"}`, or `{"signed_in": false}` (200 either way, so the browser logs no error) |
| `POST /session` | With `keys`, on **Sign in with the key**: a session for the key in `X-API-Key`, set as a cookie |
| `DELETE /session` | **Sign out**: the cookie dropped |
| `GET /console/sso/start?next=<path>` | With `sso`, on **Sign in**: the server sends the browser to the identity provider, and back to the console signed in (or to `next`, a path on the server). A failure comes back as `/console?signin_error=<why>` |

With a session, the page sends no key: queries go with the cookie. `/console?next=<path>` returns to
`next` once signed in: a server can send a browser there from a page that needs a session, such as
its dashboards.

sitelabs-graph-database turns every feature off; sitelabs-partitioned-graph turns every one on, and `login`
when it has keys or an identity provider.
