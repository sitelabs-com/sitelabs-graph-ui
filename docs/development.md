<!-- menu -->
[Features](features.md) · [Using the page](using.md) · [Serving it](serving.md) · **Development** · [Security](security.md) · [References](index.md)

**Development:** **Overview** · [Tests](testing.md) · [How big a graph](graph-size.md)
<!-- /menu -->

# Development

> **For:** developers of the page. **You'll find:** the repository's layout, how the page is put
> together, trying a change, the vendored libraries, and these docs.

## The repository

| Path | What |
|---|---|
| [ui/console.html](../ui/console.html) | The page: HTML, CSS and script in one file, no build |
| [ui/vendor/](../ui/vendor) | The two graph libraries, unchanged from npm, and their licences |
| [install.py](../install.py) | Copies a release into a project, and checks a copy ([Installing](installing.md)) |
| [VERSION](../VERSION) | The release's version, written into each copy's manifest |
| [tests/test_ui.py](../tests/test_ui.py) | The page in a real browser against a stand-in server, and the install ([Tests](testing.md)) |
| [.github/workflows/](../.github/workflows) | CI, and publishing these docs |
| [docs/](index.md), [mkdocs.yml](../mkdocs.yml), [mkdocs_hooks.py](../mkdocs_hooks.py), [tools/docs.py](../tools/docs.py) | These docs, and their site ([below](#the-docs)) |
| [LICENSE.txt](../LICENSE.txt), [NOTICES.txt](../NOTICES.txt) | Apache-2.0; the libraries are MIT |

## How the page is put together

One file, in plain JavaScript, with no framework and no build step, so a project serves it as it is.
The script, in order:

* **State:** the rows, columns and cursor of the latest answer, the tab shown, the features from
  `config.json`, and what expanding has added (`extra`).
* **Calls** (`call()`): `fetch` with the key, and an error from the answer's `error` field.
* **The side panel** (`loadSchema()`): from `GET /schema`, or `db.labels()` and
  `db.relationshipTypes()`.
* **Running** (`run()`): the request, the status line, a syntax error's offset.
* **The answer** (`render()`, `showJson()`, `showProfile()`).
* **The graph views**: `library()` loads a library on first use; `gather()` finds nodes, relationships
  and paths anywhere in a row; `collect()` applies the size limit and adds placeholders; `graphData()`
  keeps each node's object between updates so it keeps its place; `draw()` and `expand()`.
* **The query box**: a transparent `<textarea>` over a `<pre>` holding the coloured text, kept the same
  size and scrolled together; `TOKEN` splits the text; `completions()` finds the word before the
  caret.
* **History**, and **start()**: fetch `config.json`, hide what the server doesn't have
  (`data-needs="..."` on an element), load the side panel.

**Why its own query box**, of about 100 lines: the usual editor libraries' language modes use a bare
name for the language that both projects refuse, and the page would need a build to bundle one.

Colours are CSS variables on `:root`, set again for dark mode; the graph views read them
(`tokens()`) when they draw, which is why switching theme draws again.

## Trying a change

The quickest way is the tests' stand-in server, which serves the page with every feature:

```bash
python -m pytest                      # everything
python -m pytest -k completing        # one test
```

To look at it by hand, serve it from a project (install your working copy into it,
[Installing](installing.md)), or open a test with Playwright's inspector:
`PWDEBUG=1 python -m pytest -k expanding`.

## The vendored libraries

[ui/vendor/README.md](../ui/vendor/README.md) lists each file's package, version, licence and SHA-256.
To update one: download the package's tarball from registry.npmjs.org, copy `dist/<name>.min.js`
here, update that table and [NOTICES.txt](../NOTICES.txt) if the licence changed, run the tests, and
raise [VERSION](../VERSION).

The page uses: `ForceGraph3D` / `ForceGraph`, `graphData`, `nodeId`, `nodeColor`, `nodeVal`,
`nodeLabel`, `linkLabel`, `linkColor`, `linkDirectionalArrowLength`, `linkDirectionalArrowRelPos`,
`cooldownTicks`, `onNodeClick`, `onEngineStop`, `zoomToFit`, `width`, `height`, `backgroundColor`,
`_destructor`, and in 3D `showNavInfo`, `nodeResolution` and `linkOpacity`. Check those still work
after an update; the tests draw and click in both views.

## The docs

These pages are in [docs/](index.md), and published to GitHub Pages at
<https://sitelabs-com.github.io/sitelabs-graph-ui/> by
[.github/workflows/mkdocs.yml](../.github/workflows/mkdocs.yml) on every push to `main` that changes
them (`mkdocs gh-deploy` to the `gh-pages` branch). It is the same set-up as
sitelabs-partitioned-graph's.

* **Every page starts with a menu**, for reading them on GitHub, between ``. [tools/docs.py](../tools/docs.py) writes it, and `mkdocs.yml`'s `nav` (the site's
  sidebar), from its `GROUPS`; [docs/sitedocs.py](sitedocs.py) holds the sections.
* **On the site**, [mkdocs_hooks.py](../mkdocs_hooks.py) leaves the menu out (the sidebar is the menu),
  and points links into the code (`../install.py`) at the file on GitHub.

To add or move a page: write it, add it to `GROUPS` in `tools/docs.py`, and run:

```bash
python tools/docs.py                  # the menus and mkdocs.yml's nav
python tools/docs.py --check          # what CI runs: fails if they are out of date
```

To see the site:

```bash
pip install -r requirements-docs.txt
mkdocs serve                          # http://127.0.0.1:8000
```

Publishing needs, once, **Settings → Pages → Build and deployment → Deploy from a branch: `gh-pages`,
`/ (root)`** on GitHub.
