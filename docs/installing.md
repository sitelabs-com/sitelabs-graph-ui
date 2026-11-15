<!-- menu -->
[Features](features.md) · [Using the page](using.md) · **Serving it** · [Development](development.md) · [Security](security.md) · [References](index.md)

**Serving it:** [Overview](serving.md) · [Server contract](server-contract.md) · **Installing into a project**
<!-- /menu -->

# Installing into a project

> **For:** developers of a project that serves the page, and whoever releases it. **You'll find:**
> installing a copy, checking it, its manifest, and changing the page and releasing it.

A project keeps **a pinned copy of a release** in its own repository, with a manifest of its version
and files' hashes, which the project's tests check. It needs no submodule or package, and builds
offline.

## Installing and checking

From a checkout of this repository, beside the project's:

```bash
python install.py ../sitelabs-partitioned-graph/app/static/graph-ui          # replaces the copy
python install.py --check ../sitelabs-partitioned-graph/app/static/graph-ui  # is it this release?
```

[install.py](../install.py) needs the standard library only.

* **Installing** replaces the target with a copy of [ui/](../ui), and writes `MANIFEST.json`. It
  refuses a folder that has files and no `MANIFEST.json`, so it never replaces what it didn't install.
* **Checking** changes nothing. It says what differs (the version, or a file changed, added or
  missing) and exits 1, or says the target is this release and exits 0.

## The manifest

```json
{
 "name": "sitelabs-graph-ui",
 "version": "0.3.0",
 "files": {
  "console.html": "<sha-256>",
  "vendor/3d-force-graph.min.js": "<sha-256>",
  ...
 }
}
```

The version is [VERSION](../VERSION)'s; the files are every file in the copy except the manifest. A
project's tests compare the copy against it, so an edit made there fails them: **don't edit the
copies.**

## Changing the page

1. Change [ui/console.html](../ui/console.html) here, and its tests ([Tests](testing.md)).
2. Raise [VERSION](../VERSION): the patch number for a fix, the minor for a feature, the major when a
   server must change ([Server contract](server-contract.md)).
3. Commit, and tag the release (`v0.3.1`).
4. Install it into each project, and run each project's tests:

    ```bash
    python install.py ../sitelabs-partitioned-graph/app/static/graph-ui
    python install.py ../sitelabs-graph-database/app/static/graph-ui
    ```

5. When the change needs something new of a server, add it to the [Server contract](server-contract.md)
   and to each server, and give it a `config.json` feature if not every server will have it.

## Where the copies are

| Project | Copy | Serves it in |
|---|---|---|
| [sitelabs-partitioned-graph](https://github.com/sitelabs-com/sitelabs-partitioned-graph) | `app/static/graph-ui` | `app/routers/console.py` |
| [sitelabs-graph-database](https://github.com/sitelabs-com/sitelabs-graph-database) | `app/static/graph-ui` | `app/routers/console.py` |
