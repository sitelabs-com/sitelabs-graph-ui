<!-- menu -->
[Features](features.md) · **Using the page** · [Serving it](serving.md) · [Development](development.md) · [Security](security.md) · [References](index.md)

**Using the page:** **Overview** · [Graph views](graph-views.md)
<!-- /menu -->

# Using the page

> **For:** anyone exploring a graph by hand: analysts, developers, whoever runs the server.
> **You'll find:** opening the page, what each part does, the keys, and where it keeps things.

## Opening it

The server serves the page at **`/console`**, for example `http://127.0.0.1:5050/console` for
sitelabs-partitioned-graph. The page needs no key to open. If the server needs one for queries, type
it into **API key** at the top: it goes with every request as `X-API-Key`, and is remembered in this
browser ([Security](security.md#the-api-key)).

The title is the server's, from its `config.json`. Buttons for features the server doesn't have
(**Profile**, **Cancel**, **as of a past load**) aren't shown.

## The side panel

On the left (above the query at phone width):

* **The totals**: nodes, relationships and the current load, when the server has `schema`.
* **Labels**, **Node types** (with `schema`) and **Relationship types**. With `schema`, each has its
  count, and each type its properties (`name: type`). Click one to run a query that shows some of them:

    ```cypher
    MATCH (n:`Person`) RETURN n LIMIT 25
    MATCH (a)-[r:`KNOWS`]->(b) RETURN a, r, b LIMIT 25
    ```

    Without `schema`, the lists come from `CALL db.labels()` and `CALL db.relationshipTypes()`, with no
    counts.
* **History** ([below](#history)).

Changing the API key loads the lists again.

## The query box

The page starts with a query that counts the nodes by label. The box:

* **Colours** keywords, strings, numbers, `$parameters`, `:Labels` and `// comments`.
* **Completes** as you type: keywords after two letters, and labels and relationship types after a
  `:` (from the side panel). Up to eight suggestions; ↑ and ↓ choose, **Tab** or **Enter** accepts,
  **Escape** closes them.
* **Marks a syntax error** with a wavy underline, when the server's message says `offset N`. Typing
  clears it.

| Key | What it does |
|---|---|
| Ctrl+Enter, ⌘+Enter | Run |
| Tab | Accept a suggestion; otherwise indent by two spaces |
| Escape, then Tab | Leave the box (for moving round the page by keyboard) |
| ↑, ↓ | Move between suggestions |

**Parameters** go in the box below, as JSON: `{"name": "Ann"}`. A query refers to them as `$name`.
JSON that doesn't parse stops the run with a message.

## Running

| Button | Sends |
|---|---|
| **Run** | The query, its parameters, and `"read_only": true` to `POST /opencypher` |
| **Profile** (with `profile`) | The same with `"profile": true`; the answer opens on the **Profile** tab |
| **Explain** | `EXPLAIN` and the query: the plan, without running it |
| **Cancel** (with `cancel`) | `DELETE /queries/{id}` for the running query |
| **as of a past load** (with `past`) | A load number, sent as `at_load`: the graph as it was then |

The status line, on the right, shows how long it took (in the browser, so network included), the rounds
and calls when the server reports them, and the number of rows, or "more rows" when there are more
pages to fetch. An error from the server shows in red, with its HTTP status.

## The answer

| Tab | What it shows |
|---|---|
| **Table** | The first 2,000 rows. A node is `(:Label) {properties}`, a relationship `[:TYPE] {properties}`, a path its number of hops |
| **3D**, **2D** | The nodes, relationships and paths in the answer, drawn ([Graph views](graph-views.md)) |
| **JSON** | The whole answer as the server sent it, made only when the tab is opened, and cut at 5 MB |
| **Profile** (with `profile`) | The total time, split between waiting for the partitions and the coordinator; the plan; every round of calls with the partitions, rows sent and received, and its time |

With `pages`, the page asks for 500 rows at a time, and **More rows** fetches the next page.

## History

The last **50** queries run in this browser, newest first, with no repeats. Click one to put it in the
box (it doesn't run). **Clear** forgets them all. It keeps their text only, not their parameters, which
may be private. A query is remembered when it is run, whether it worked or not.

## What it keeps in the browser

All in `localStorage`, for this server's address only:

| Key | What |
|---|---|
| `graph-ui.key` | The API key, as typed |
| `graph-ui.history` | The history: a JSON list of query texts |
| `graph-ui.theme` | `light` or `dark`, once the ◐ button has been used; otherwise the system's |

When the browser won't store (a private window, blocked site data), the page still works and forgets
them on leaving.
