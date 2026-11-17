<!-- menu -->
[Features](features.md) · [Using the page](using.md) · [Serving it](serving.md) · [Development](development.md) · **Security** · [References](index.md)
<!-- /menu -->

# Security

> **For:** developers of the page and of servers that serve it, and whoever reviews them. **You'll
> find:** what keeps the page read-only, how it handles what comes from the graph, the policy it runs
> under, what it keeps in the browser, and what it leaves to the server.

## Read-only

Every query the page sends, from the query box, the side panel or expanding, has `"read_only": true`.
The server must refuse a write with it, **whatever the API key may do**, so a key with write access
can't change the graph through the page. The page doesn't try to spot writes itself: the server
decides.

## What comes from the graph

Labels, types, property names and values, error messages and the server's title are all data that
someone else may have written. The page:

* escapes them (`&`, `<`, `>`, `"`) before putting them into HTML, or sets them as text;
* escapes the graph views' hover labels, which the libraries put into HTML;
* builds the query box's colouring from escaped text, so HTML typed or pasted into it is shown, not
  run (a test checks this).

Clicking a label or type puts its name into a query in backticks. A name holding a backtick makes a
query that fails; it is still sent read-only.

## The content security policy

A server serves the page with:

```text
default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'unsafe-inline';
img-src 'self' data: blob:; connect-src 'self'; frame-ancestors 'none'
```

| Part | Means |
|---|---|
| `default-src 'self'`, `connect-src 'self'` | Nothing is loaded from, or sent to, anywhere but the server |
| `script-src 'self' 'unsafe-inline'` | The page's own script and the two libraries from `/console/vendor/`. No `eval`: the libraries work without it |
| `style-src 'unsafe-inline'` | The page's own styles |
| `img-src 'self' data: blob:` | The libraries' canvases and textures |
| `frame-ancestors 'none'` | No other site can put the page in a frame |

The libraries are served from a fixed list of two names, so the vendor path can't serve any other
file. Add `X-Content-Type-Options: nosniff` to both.

## The API key

* The page itself needs no key. Queries do, when the server needs one.
* The key is typed into the page, sent as `X-API-Key` with each request, and **kept in this browser's
  `localStorage`** (`graph-ui.key`), so it is there on the next visit. Anyone who can use that browser
  profile, or run script on the server's origin, can read it. Clear it from the field (it is saved
  when changed) on a shared machine.
* Where the server has keys that can only read, use one in the page. The page can't write with any
  key, but a key kept in a browser may leak, and a read-only one limits what it can then do elsewhere.

## Signing in

With `login` ([Server contract](server-contract.md#login)), the server keeps the sign-in, not the page:

* **Sign in** goes to the identity provider and back, and the server exchanges the code for a token
  itself. The browser gets a session cookie the server makes (HttpOnly, so no script can read it), not
  the token.
* **Sign in with the key** sends the typed key once, for a session, then clears it from the field and
  from `localStorage`.
* The server should make the cookie `SameSite=Strict`, and `Secure` over HTTPS, and let a session only
  read: then another site can't use it, and a leaked one can't change the graph.

## History

The history keeps the **text** of the last 50 queries in `localStorage`, not their parameters, which
may be private: put private values in parameters, not in the query. **Clear** forgets them.

## What the server must do

The page is a client: what protects the graph is the server.

* Refuse writes when `read_only` is true.
* Check `X-API-Key` on `POST /opencypher`, `GET /schema` and the other API paths; `/console`,
  `/console/config.json` and `/console/vendor/*` need none and hold nothing private.
* Serve the page over HTTPS anywhere but a developer's own machine: the key goes with every request.
* Limit how long a query may run and how many rows it may answer; the page asks for at most 5,000
  rows a page, but doesn't enforce anything.
