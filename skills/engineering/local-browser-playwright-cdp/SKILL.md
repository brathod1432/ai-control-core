---
name: local-browser-playwright-cdp
description: Use when the user asks to inspect, automate, screenshot, or safely modify local or already-open Chrome/Chromium pages using Python Playwright over Chrome DevTools Protocol (CDP), especially on Windows with remote debugging enabled.
category: engineering
---

## Internal Safety Override

- Status: local-only by default.
- Use only loopback targets such as `http://127.0.0.1:<port>` or local files unless the user explicitly approves a specific external site.
- Before contacting any non-loopback URL, state the destination, data scope, credential source, and reason, then wait for explicit approval.
- Do not exfiltrate page content, cookies, storage state, screenshots, HAR files, traces, credentials, private documents, or repository metadata.
- Do not read or print secrets from cookies, localStorage, sessionStorage, IndexedDB, headers, request bodies, or page text. Redact sensitive values if they appear.
- Prefer observation and reversible page-local mutations. Do not submit forms, click destructive controls, purchase items, send messages, or trigger production actions unless explicitly requested.
- Audit categories: browser automation, local network loopback, secrets, screenshots.

# Local Browser Playwright CDP

## Purpose

This skill helps Codex analyze and modify pages running in a local or already-open Chrome/Chromium session by using Python Playwright and Chrome DevTools Protocol (CDP). It is optimized for Windows developer machines where Chrome can be launched with `--remote-debugging-port`, then inspected through `http://127.0.0.1:9222` without external network access.

Use this skill for:
- Inspecting already-open Chrome tabs when remote debugging is enabled.
- Capturing screenshots of local web apps, local files, and user-approved pages.
- Reading rendered DOM, computed styles, accessibility snapshots, console logs, and network activity.
- Making safe temporary page modifications for debugging, visual QA, demos, and accessibility exploration.
- Comparing visible UI state to source code or expected behavior.

Do not use this skill for:
- General web scraping at scale.
- Circumventing authentication, bot detection, paywalls, or site protections.
- Mutating production data without explicit user approval.
- Remote browser services, cloud browsers, telemetry collectors, or SaaS inspection tools.

## Decision Flow

1. Clarify target scope only when needed: already-open Chrome tab, local dev server, local HTML file, or a user-approved URL.
2. Prefer connecting to an existing local Chrome via CDP if the user wants current tabs, logged-in state, or manual browser context.
3. Launch a fresh Playwright browser only when isolation matters or no CDP-enabled Chrome is available.
4. Start with read-only inspection: page list, URL/title, screenshot, DOM summary, accessibility snapshot, console errors, and network summary.
5. For page changes, apply reversible client-side mutations only, document what changed, and avoid persistent writes unless requested.
6. Store temporary artifacts under the active workspace or the skill task directory, not in user profile folders.

## Windows Setup

### Launch Chrome With Remote Debugging

Close Chrome first if you need a clean profile, then run one of these from PowerShell or `cmd`:

```powershell
& "$env:ProgramFiles\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="$env:TEMP\codex-chrome-cdp"
```

```cmd
"%ProgramFiles%\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%TEMP%\codex-chrome-cdp"
```

Use a throwaway `--user-data-dir` when possible. It keeps automation state separate from the user's everyday Chrome profile and reduces the chance of exposing personal cookies, extensions, or account data.

If the user specifically needs an already-open personal profile, ask them to relaunch that profile with remote debugging enabled. Be extra careful not to dump cookies, storage, or full page content from sensitive sites.

### Check CDP Availability Locally

Only query loopback:

```powershell
Invoke-RestMethod http://127.0.0.1:9222/json/version
Invoke-RestMethod http://127.0.0.1:9222/json/list
```

If those fail, Chrome is not running with remote debugging, the port differs, or another process owns the port.

## Python Environment

Prefer an existing project virtual environment. If Playwright is missing, do not install packages without user approval. When installation is approved, prefer exact versions and local project dependency files.

Minimal imports:

```python
from pathlib import Path
from playwright.sync_api import sync_playwright
```

Use sync Playwright for short inspection scripts unless the existing repo already uses async Playwright.

## Connect To Already-Open Chrome Tabs

Connect over CDP to inspect the current Chrome session:

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

CDP_URL = "http://127.0.0.1:9222"
OUT = Path("skills/engineering/local-browser-playwright-cdp/.artifacts")
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP_URL)
    context = browser.contexts[0] if browser.contexts else browser.new_context()

    pages = [page for page in context.pages if not page.url.startswith("chrome://")]
    for i, page in enumerate(pages):
        print(f"[{i}] {page.title()!r} {page.url}")

    page = pages[0]
    page.screenshot(path=str(OUT / "current-tab.png"), full_page=True)

    browser.close()
```

Notes:
- `connect_over_cdp()` attaches to the running browser; it does not create a clean isolated browser.
- Attached contexts may contain user session state. Treat all cookies, storage, headers, and screenshots as sensitive.
- Closing the Playwright `browser` connection should detach from CDP. It should not close the user's Chrome window, but still avoid unnecessary `context.close()` calls against user-owned contexts.

## Select The Right Tab

Prefer explicit target selection by URL substring, title substring, or index from a printed page list:

```python
def choose_page(context, url_contains=None, title_contains=None, index=None):
    pages = [p for p in context.pages if p.url and not p.url.startswith("chrome://")]
    if index is not None:
        return pages[index]
    for page in pages:
        title = page.title()
        if url_contains and url_contains in page.url:
            return page
        if title_contains and title_contains.lower() in title.lower():
            return page
    raise RuntimeError("No matching tab found")
```

When multiple tabs match, stop and report the choices rather than guessing.

## Read-Only Inspection Recipes

### Page Summary

```python
summary = page.evaluate("""() => ({
  url: location.href,
  title: document.title,
  readyState: document.readyState,
  lang: document.documentElement.lang || null,
  bodyTextLength: document.body?.innerText?.length || 0,
  headings: [...document.querySelectorAll('h1,h2,h3')].slice(0, 20).map(h => ({
    level: h.tagName,
    text: h.innerText.trim()
  })),
  forms: [...document.forms].map(f => ({
    id: f.id || null,
    name: f.name || null,
    action: f.action || null,
    method: f.method || null,
    controls: f.elements.length
  })),
  links: [...document.links].slice(0, 30).map(a => ({
    text: a.innerText.trim().slice(0, 120),
    href: a.href
  }))
})""")
print(summary)
```

### DOM And Selector Discovery

Use semantic selectors first:

```python
buttons = page.get_by_role("button").all()
links = page.get_by_role("link").all()
inputs = page.locator("input, textarea, select, [contenteditable='true']").all()
print(len(buttons), len(links), len(inputs))
```

For compact DOM summaries, avoid printing full HTML. Extract only relevant elements and redact sensitive attributes:

```python
elements = page.evaluate("""() => [...document.querySelectorAll('button,a,input,textarea,select,[role]')]
  .slice(0, 100)
  .map((el, i) => ({
    i,
    tag: el.tagName.toLowerCase(),
    role: el.getAttribute('role'),
    type: el.getAttribute('type'),
    text: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('placeholder') || '').trim().slice(0, 120),
    id: el.id || null,
    testid: el.getAttribute('data-testid')
  }))""")
```

### Accessibility Snapshot

```python
snapshot = page.accessibility.snapshot(interesting_only=True)
print(snapshot)
```

Check:
- Missing accessible names for buttons, links, inputs, and dialogs.
- Heading order and landmark structure.
- Focus traps in modals.
- Keyboard reachability for interactive controls.
- Color or contrast issues by combining screenshots with computed styles.

### Console Logs And Page Errors

Register listeners before navigation or before reproducing the issue:

```python
messages = []
errors = []

page.on("console", lambda msg: messages.append({
    "type": msg.type,
    "text": msg.text[:1000],
    "location": msg.location,
}))
page.on("pageerror", lambda exc: errors.append(str(exc)[:1000]))

page.reload(wait_until="networkidle")
print({"console": messages, "pageerrors": errors})
```

Do not paste large logs into final output. Summarize repeated errors and redact tokens, emails, cookies, and IDs.

### Network Inspection

Capture metadata, not bodies, by default:

```python
requests = []
responses = []

page.on("request", lambda req: requests.append({
    "method": req.method,
    "url": req.url,
    "resource_type": req.resource_type,
}))

page.on("response", lambda res: responses.append({
    "status": res.status,
    "url": res.url,
    "content_type": res.headers.get("content-type"),
}))

page.reload(wait_until="networkidle")
failed = [r for r in responses if r["status"] >= 400]
print({"request_count": len(requests), "failed": failed[:30]})
```

Only capture request/response bodies when the user asks and the data is not sensitive. Never dump authorization headers, cookies, bearer tokens, API keys, CSRF tokens, or session IDs.

## Screenshots And Visual Evidence

### Full Page And Viewport Screenshots

```python
page.screenshot(path=str(OUT / "viewport.png"))
page.screenshot(path=str(OUT / "full-page.png"), full_page=True)
```

### Element Screenshot

```python
target = page.get_by_role("main")
target.screenshot(path=str(OUT / "main.png"))
```

### Stabilize Before Capture

```python
page.wait_for_load_state("domcontentloaded")
page.wait_for_timeout(250)
page.evaluate("""() => {
  document.querySelectorAll('video, canvas').forEach(el => el.pause?.());
}""")
```

Avoid long hard-coded sleeps. Use selectors, load states, or targeted waits first.

## Safe Page Mutation

Page mutation should usually be temporary, client-side, and reversible. Use it for visual debugging, highlighting, layout experiments, and content checks. Do not persist changes to application data unless explicitly requested.

### Reversible Mutation Pattern

```python
mutation_id = "codex-debug-style"
page.evaluate("""(mutationId) => {
  if (document.getElementById(mutationId)) return;
  const style = document.createElement('style');
  style.id = mutationId;
  style.textContent = `
    [data-codex-highlight="true"] {
      outline: 3px solid #ff6b00 !important;
      outline-offset: 2px !important;
    }
  `;
  document.head.appendChild(style);
}""", mutation_id)

page.locator("button").evaluate_all("""els => {
  els.forEach(el => el.dataset.codexHighlight = "true");
}""")

# Revert:
page.evaluate("""(mutationId) => {
  document.querySelectorAll('[data-codex-highlight]').forEach(el => {
    delete el.dataset.codexHighlight;
  });
  document.getElementById(mutationId)?.remove();
}""", mutation_id)
```

### Text Or Style Experiments

```python
page.evaluate("""() => {
  const banner = document.querySelector('[data-testid="hero-title"]');
  if (!banner) return false;
  banner.dataset.codexOriginalText = banner.textContent;
  banner.textContent = "Temporary local preview only";
  return true;
}""")
```

Before mutating:
- Capture a screenshot or DOM summary of the original state.
- Store original values in `dataset` or a local variable.
- Make changes visibly temporary if presenting results.
- Provide a revert snippet when reporting the change.

Never:
- Click controls labeled delete, remove, publish, send, buy, confirm, transfer, approve, or deploy unless the user explicitly requests that exact action.
- Fill password, payment, token, or recovery fields unless the user provides scoped approval.
- Change localStorage, cookies, IndexedDB, or service worker caches unless needed and approved.

## Local Dev App Workflow

When inspecting a local app at `localhost` or `127.0.0.1`:

1. Confirm which port and route to inspect.
2. Attach to CDP Chrome if the user wants their current tab; otherwise launch an isolated Playwright browser.
3. Navigate only to the local URL.
4. Wait for app readiness using an app-specific selector or `networkidle`.
5. Capture screenshot, accessibility snapshot, console errors, and failed network requests.
6. If asked to fix code, correlate UI evidence with source files before editing.

Fresh isolated browser example:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    page = context.new_page()
    page.goto("http://127.0.0.1:5173", wait_until="networkidle")
    page.screenshot(path="skills/engineering/local-browser-playwright-cdp/.artifacts/local-app.png", full_page=True)
    browser.close()
```

## Advanced CDP Options

Use Playwright's CDP session for capabilities not exposed by the high-level API:

```python
client = context.new_cdp_session(page)
client.send("DOM.enable")
client.send("Runtime.enable")
client.send("Overlay.enable")
```

Examples:
- `Performance.getMetrics` for JS heap and timing metrics.
- `DOMSnapshot.captureSnapshot` for layout-tree inspection.
- `CSS.getComputedStyleForNode` for exact computed CSS values.
- `Network.setBlockedURLs` to locally block analytics or noisy assets during debugging.
- `Emulation.setCPUThrottlingRate` for local performance checks.
- `Overlay.highlightNode` for visual debugging without editing DOM.

Keep CDP calls targeted. Some domains expose sensitive data or can alter page behavior globally.

### Performance Metrics

```python
client = context.new_cdp_session(page)
metrics = client.send("Performance.getMetrics")
interesting = {
    item["name"]: item["value"]
    for item in metrics["metrics"]
    if item["name"] in {"JSHeapUsedSize", "Nodes", "LayoutCount", "RecalcStyleCount"}
}
print(interesting)
```

### Temporary Request Blocking

Block only when it helps isolate a local issue and does not change the tested behavior incorrectly:

```python
client = context.new_cdp_session(page)
client.send("Network.enable")
client.send("Network.setBlockedURLs", {"urls": ["*://*/analytics/*", "*://*/telemetry/*"]})
page.reload(wait_until="networkidle")
```

## Artifact Handling

- Write screenshots, JSON summaries, traces, and HAR files inside the workspace, preferably `skills/engineering/local-browser-playwright-cdp/.artifacts/` for skill validation tasks.
- Do not commit sensitive artifacts unless the user explicitly asks and confirms they contain no secrets.
- Use short filenames that describe the page and state: `home-before.png`, `checkout-error-console.json`, `a11y-snapshot.json`.
- Redact secrets before saving summaries.

## Troubleshooting

### Cannot Connect To CDP

- Confirm Chrome was launched with `--remote-debugging-port=9222`.
- Confirm the URL is `http://127.0.0.1:9222`, not an external host.
- Check whether another Chrome instance reused the existing profile without remote debugging.
- Try a throwaway profile with `--user-data-dir="%TEMP%\codex-chrome-cdp"`.

### No Pages Found

- Ignore `chrome://`, `devtools://`, and extension pages.
- Open the target tab manually in the CDP-enabled Chrome window.
- Re-query `context.pages` after a short wait.

### Screenshots Are Blank Or Incomplete

- Wait for a known visible selector.
- Disable reduced-size viewport assumptions by setting a realistic viewport.
- Capture viewport first, then full page.
- Check whether the page uses cross-origin iframes or protected surfaces.

### Actions Do Nothing

- Verify the element is visible, enabled, and not covered by an overlay.
- Prefer role-based locators and `locator.click()` over coordinate clicks.
- Use `trial=True` where available to test actionability before changing state.
- Inspect console errors and failed network requests.

## Reporting Back

When finishing a browser analysis task, include:
- Target inspected: tab title, local URL or approved URL, and CDP port if relevant.
- Actions taken: screenshot, DOM summary, accessibility snapshot, network metadata, safe mutations.
- Findings: concise issues with evidence and file references if code was inspected.
- Artifacts created: paths to screenshots or JSON summaries.
- Safety notes: any skipped external network, redacted data, or actions avoided.

Keep reports focused. Do not paste full DOM, cookies, storage, HAR bodies, or large logs into chat.
