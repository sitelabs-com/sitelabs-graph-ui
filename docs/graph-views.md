<!-- menu -->
[Features](features.md) · **Using the page** · [Serving it](serving.md) · [Development](development.md) · [Security](security.md) · [References](index.md)

**Using the page:** [Overview](using.md) · **Graph views**
<!-- /menu -->

# Graph views

> **For:** anyone drawing an answer. **You'll find:** what the 3D and 2D views draw and how, moving
> round them, the size limit, and expanding a node to explore.

## What is drawn

The **3D** tab uses [3d-force-graph](https://github.com/vasturiano/3d-force-graph) (three.js, WebGL),
the **2D** tab [force-graph](https://github.com/vasturiano/force-graph) (a canvas). Each is loaded from
`/console/vendor/` the first time its tab opens, so a page that only shows tables never loads them.

The page looks through every value of every row, including lists and maps inside them, for:

| Value | Recognised by | Drawn as |
|---|---|---|
| A node | `id`, `labels` and `properties` | A dot, coloured by its first label |
| A relationship | `id`, `type`, `start` and `end` | A line with an arrow, start to end |
| A path | `nodes` and `relationships` | Its nodes and relationships |

So `RETURN n`, `RETURN a, r, b`, `RETURN p` and `RETURN collect(n)` all draw. A query that returns only
properties (`RETURN n.name`) has nothing to draw, and the view says so.

**A relationship whose ends the answer didn't return** is drawn with grey placeholders for them, and
the line above the graph counts them ("ends not in the answer"). Return the nodes too
(`RETURN a, r, b`) to see them properly.

Six colours go round the labels in the order they are met; the legend below the graph says which is
which.

## Moving round

| | 3D | 2D |
|---|---|---|
| Drag the background | Turn | Pan |
| Scroll | Zoom | Zoom |
| Drag a node | Move it | Move it |
| Hover | Its labels, and its `name` or `title` | The same |
| Click a node | Everything about it, in a panel | The same |

When the layout settles, the view zooms to fit. Switching tab or theme draws it again. Leaving a graph
tab stops the drawing, so it doesn't keep the GPU busy. 3D needs WebGL; without it the tab says to use
2D.

## The size limit

**Draw up to** sets the most nodes drawn: 100, 500, **1,000** (the default), 2,000, 5,000 or 10,000.
The line above the graph says how many of how many nodes and relationships are drawn, and gives advice
past the sizes that stop being readable:

* over **500** nodes: narrow the query (labels, properties, `LIMIT`);
* over **2,000** in 3D: 3D is slow at this size, try 2D.

Past 1,000 nodes the views draw less to keep up: no arrows, a shorter layout, and in 3D coarser dots
and fainter lines. The numbers behind these limits are in [How big a graph](graph-size.md).

With `pages`, an answer may have more rows than were fetched. **Fetch more rows to draw** fetches pages
of 5,000 until there are ten times the limit (enough for the nodes and most of their relationships), or
none are left.

## Expanding a node

To explore a graph too big to draw, start small and grow it:

1. Run a query for one node or a few, for example
   `MATCH (p:Person {name: $name}) RETURN p`.
2. Open **3D** or **2D**, and click a node.
3. Click **Expand neighbours**. The page sends:

    ```cypher
    MATCH (a)-[r]-(b) WHERE id(a) = $id RETURN a, r, b LIMIT 100
    ```

    with the node's id, read-only, and adds what comes back beside it. The node is drawn larger, and
    the button says **Expanded**.
4. Click a new node and expand it, and so on.

What was expanded:

* **is always drawn**, whatever the size limit: it was asked for by hand;
* **stays** when you switch between 3D and 2D;
* **goes** with the next query, or with **Back to the answer**.

A node with more than 100 relationships shows its first 100, and says so.
