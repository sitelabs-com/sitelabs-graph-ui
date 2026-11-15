<!-- menu -->
**Features** · [Using the page](using.md) · [Serving it](serving.md) · [Development](development.md) · [Security](security.md) · [References](index.md)
<!-- /menu -->

# Features

> **For:** anyone deciding whether the page does what they need. **You'll find:** every feature in
> short, with a link to the details.

sitelabs-graph-ui is **a read-only web page for a graph server**: run openCypher queries, and see the
answer as a table, in 3D, in 2D or as JSON. It is what
[sitelabs-graph-database](https://github.com/sitelabs-com/sitelabs-graph-database) and
[sitelabs-partitioned-graph](https://github.com/sitelabs-com/sitelabs-partitioned-graph) serve at
`/console`.

It is **one HTML file and two libraries**, with nothing to build and nothing fetched from the internet,
so it works on a private network. A project keeps a pinned copy of a release
([Installing into a project](installing.md)).

## Querying

* **Queries with parameters**, in a box, parameters as JSON. **Run**, or Ctrl+Enter (⌘+Enter on a Mac).
* **Read-only, always.** Every query goes with `"read_only": true`, so the server refuses a write,
  whatever the API key may do ([Security](security.md#read-only)).
* **Explain** puts `EXPLAIN` before the query.
* **The query box** colours the language, completes keywords and, after a `:`, labels and types, and
  marks where a syntax error is ([The query box](using.md#the-query-box)).
* **History:** the last 50 queries in this browser, newest first; their text only, not their
  parameters ([History](using.md#history)).
* **Labels and types** beside the query: click one to see some of them
  ([The side panel](using.md#the-side-panel)).

## Answers

* **A table** of the first 2,000 rows, **JSON** of the whole answer, and **3D** and **2D** graph views
  ([The answer](using.md#the-answer)).
* **The graph views** draw the nodes, relationships and paths anywhere in the answer, coloured by first
  label. Hover for a label, click a node for all of it ([Graph views](graph-views.md)).
* **Expanding:** click a node, then **Expand neighbours**, to add what it connects to, and carry on
  from there: the way to explore a graph too big to draw
  ([Expanding](graph-views.md#expanding-a-node)).
* **A size limit** on what is drawn, and advice when a graph is too big to read
  ([How big a graph](graph-size.md)).

## What a server adds

A server says what it has in `GET /console/config.json`, and the page shows only that
([Server contract](server-contract.md#optional-features)):

| Feature | What the page gets |
|---|---|
| `schema` | Counts of every label and type, and each type's properties, from `GET /schema` |
| `pages` | Answers 500 rows at a time, **More rows**, and **Fetch more rows to draw** |
| `profile` | **Profile**: the plan, and each round of partition calls with its time and sizes |
| `past` | **As of a past load**: reading the graph as it was after an earlier load |
| `cancel` | **Cancel** stops the running query |

## Around the page

* **Light and dark**, following the system, with a button to switch.
* **Works at phone width**: the side panel goes above the query.
* **Everything from the graph is escaped** before it is shown, and the page works under a strict
  content security policy ([Security](security.md)).
* **Tested in a real browser** against a stand-in server, once with every feature and once with none
  ([Tests](testing.md)).

## What it doesn't do

* **Write.** It is for reading and exploring; writes go through the server's API.
* **Edit a server's data model, users or keys.** Those belong to the server.
* **Draw very large answers.** What you can read runs out long before what the browser can draw
  ([How big a graph](graph-size.md)).
