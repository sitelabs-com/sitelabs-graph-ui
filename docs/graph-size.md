<!-- menu -->
[Features](features.md) · [Using the page](using.md) · [Serving it](serving.md) · **Development** · [Security](security.md) · [References](index.md)

**Development:** [Overview](development.md) · [Tests](testing.md) · **How big a graph**
<!-- /menu -->

# How big a graph

> **For:** developers choosing the page's limits, and anyone wondering why a big answer isn't drawn.
> **You'll find:** what was measured, on what, what it shows, and how the page's limits follow from it.

**What limits a graph is what you can read, long before what the browser can draw.**

## What was measured

On an Apple M2 laptop (Chrome, its GPU), on connected data of about 8 relationships per node, all of it
drawn:

| Nodes, relationships | View | Layout | While laid out | Turning or panning | Can you read it? |
|---|---|---:|---:|---:|---|
| 116, 794 | 3D | 5.1 s | 60 fps | 60 fps | Yes |
| | 2D | 5.0 s | 60 fps | 61 fps | Yes |
| 1,052, 8,032 | 3D | 4.0 s | 31 fps | 48 fps | The clusters only, as a hairball |
| | 2D | 2.0 s | 61 fps | 60 fps | The clusters only, as a hairball |
| 5,212, 40,198 | 3D | 15.4 s | 5 fps | 7 fps | No: a solid disc |
| | 2D | 3.5 s | 36 fps | 55 fps | No: a solid disc |

*Layout* is the time until the layout settles (the page records it in the stage's `data-laid-out`).
The two frame-rate columns are while it is settling and afterwards, moving round it.

## What it shows

* **Around a hundred nodes** read well in either view.
* **Around a thousand** still draw smoothly, in 2D especially, but show only the clusters.
* **Five thousand** draw (2D comfortably, 3D barely), and show nothing.
* **Focused answers read well at any size of graph.** It is the size of the answer that matters, not
  of the graph.

## The page's limits

| Limit | Value | Why |
|---|---|---|
| Nodes drawn, by default | 1,000 | Where a picture stops showing more than clusters |
| "Hard to read" advice | over 500 nodes | Before the hairball |
| "3D is slow" advice | over 2,000 nodes in 3D | Between 31 and 5 fps |
| Fewer details drawn | over 1,000 nodes | No arrows, shorter layout, coarser 3D |
| Expanding | 100 relationships a node | One step at a time stays readable |

They are constants in [ui/console.html](../ui/console.html) (`describe()`, `draw()` and `EXPAND`).

So **expanding** is the way into a big graph: start from one node and grow it
([Expanding a node](graph-views.md#expanding-a-node)). Libraries that draw hundreds of thousands of
points (cosmos.gl, for example) aren't worth adding for that reason.

## Measuring your own

Draw an answer of the size you care about, in each view, and read:

* the layout time, from the line above the graph ("Laid out in N s"), or
  `document.getElementById('stage').dataset.laidOut` in the browser's console;
* the frame rate, from the browser's performance tools (in Chrome, **Rendering → Frame rendering
  stats**), while it settles and while you turn or pan it.

Say the machine, browser and data when adding a row to the table above.
