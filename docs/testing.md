<!-- menu -->
[Features](features.md) · [Using the page](using.md) · [Serving it](serving.md) · **Development** · [Security](security.md) · [References](index.md)

**Development:** [Overview](development.md) · **Tests** · [How big a graph](graph-size.md)
<!-- /menu -->

# Tests

> **For:** developers of the page. **You'll find:** running the tests, the stand-in server, what each
> test checks, what CI runs, and what isn't tested.

## Running them

```bash
pip install playwright pytest && playwright install chromium
python -m pytest
```

Without Playwright, or without a browser, only the install is tested and the rest are skipped. With
`REQUIRE_BROWSER=1` (as in CI) a missing browser fails the run instead, so a broken setup can't pass
by skipping.

## The stand-in server

[tests/test_ui.py](../tests/test_ui.py) starts a small `http.server` on a free port for each test. It
serves the page with the [content security policy](security.md#the-content-security-policy), the
libraries, a `config.json` and `GET /schema`, and answers `POST /opencypher` by the query's start:

| Query | Answer |
|---|---|
| `CALL db.labels()`, `CALL db.relationshipTypes()` | `Person`, `KNOWS` |
| `CREATE ...` | 400, `read-only` |
| One with `$id` (expanding) | Ann, KNOWS, and a new node, Bob |
| `ONE ...` | One node, Ann |
| `BAD ...` | 400, a syntax error at `offset 4` |
| Anything else | Ann, and a KNOWS to a node not in the answer |

It records every request it gets, so a test can check what the page sent. Two configs: `FULL`, every
feature on, and `PLAIN`, none.

## What each test checks

| Test | What |
|---|---|
| `test_install_copies_and_checks` | Installing writes a manifest with the version and every file; checking finds a changed file and an added one; installing again replaces its own copy; it refuses a folder it didn't install |
| `test_the_page_shows_what_the_server_has` (full, plain) | The title from `config.json`; each feature's buttons shown or hidden; counts only with `schema`; a run sends `read_only` and `page_size` only with `pages`; both graph views lay out, with placeholders; a write is refused and shown; no script errors |
| `test_expanding_a_node_adds_its_neighbours` (2D, 3D) | Clicking a node shows it; expanding sends its id, read-only, and adds its neighbour; it carries over to the other view; **Back to the answer** removes it |
| `test_a_new_answer_forgets_what_was_expanded` | A new query clears what was expanded |
| `test_the_box_highlights_and_shows_where_a_syntax_error_is` | Keywords, labels, parameters, comments and numbers are coloured; the coloured text matches the query; HTML typed into the box isn't run; a syntax error is marked, and typing clears it |
| `test_completing_labels_and_keywords` | Labels after `:` and keywords complete with Tab and Enter; Escape closes; Tab indents; Escape, then Tab, leaves the box |
| `test_history_keeps_the_last_queries_not_their_parameters` | Newest first, no repeats; no parameters stored; a click loads one; it survives a reload; **Clear** empties it |

The first two browser tests also fail on any uncaught script error in the page.

## In CI

[.github/workflows/ci.yml](../.github/workflows/ci.yml), on every push and pull request, on Ubuntu
24.04 with Python 3.12:

* the docs' menus and `mkdocs.yml`'s nav are up to date (`python tools/docs.py --check`);
* pinned pytest and Playwright, and Chromium with its system packages;
* `python -m pytest -ra` with `REQUIRE_BROWSER=1`.

[.github/workflows/mkdocs.yml](../.github/workflows/mkdocs.yml) publishes the docs
([Development](development.md#the-docs)).

Each project that serves the page also tests it against itself, and checks its copy is a release
([Installing into a project](installing.md)).

## What isn't tested

* **Other browsers.** Only Chromium runs in the tests; Firefox and Safari aren't tested.
* **Large graphs.** The size limits come from measurements by hand ([How big a graph](graph-size.md)),
  not from a test.
* **Paging, profiles, past loads and cancelling** beyond what is sent: the stand-in server doesn't
  answer with cursors or profiles. The projects' own tests cover them against the real servers.
* **The light and dark themes**, and the layout at phone width, by eye only.
