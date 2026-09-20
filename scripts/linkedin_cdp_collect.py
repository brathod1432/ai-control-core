"""Read-only LinkedIn collection through the local Chrome CDP endpoint.

This script intentionally avoids cookies, local storage, credentials, messages,
posting, liking, connecting, following, or profile edits. It only navigates to
LinkedIn pages and reads rendered page text from Chrome.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any


LINKEDIN_PAGES = [
    ("home_feed", "https://www.linkedin.com/feed/"),
    ("profile_root", "https://www.linkedin.com/in/"),
    ("my_network", "https://www.linkedin.com/mynetwork/"),
    ("my_network_connections", "https://www.linkedin.com/mynetwork/invite-connect/connections/"),
    ("recent_activity", "https://www.linkedin.com/in/me/recent-activity/all/"),
    ("profile_details_experience", "https://www.linkedin.com/in/me/details/experience/"),
    ("profile_details_skills", "https://www.linkedin.com/in/me/details/skills/"),
    ("profile_details_certifications", "https://www.linkedin.com/in/me/details/certifications/"),
]


READ_TEXT_JS = r"""
(() => {
  const clean = (s) => String(s || '').replace(/\u00a0/g, ' ').replace(/[ \t]+\n/g, '\n').trim();
  const title = document.title;
  const url = location.href;
  const canonical = document.querySelector('link[rel="canonical"]')?.href || '';
  const description = document.querySelector('meta[name="description"]')?.content || '';
  const bodyText = clean(document.body ? document.body.innerText : '');
  const headings = Array.from(document.querySelectorAll('h1,h2,h3')).map((el) => clean(el.innerText)).filter(Boolean);
  const anchors = Array.from(document.querySelectorAll('a[href]')).map((a) => ({
    text: clean(a.innerText || a.getAttribute('aria-label') || ''),
    href: a.href || ''
  })).filter((a) => a.text || a.href).slice(0, 200);
  return { title, url, canonical, description, bodyText, headings, anchors };
})()
"""


def load_chrome_module(plugin_script: Path) -> Any:
    spec = importlib.util.spec_from_file_location("chrome_cdp_mcp_local", plugin_script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {plugin_script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def page_targets(chrome: Any) -> list[dict[str, Any]]:
    return [target for target in chrome.list_targets() if target.get("type") == "page"]


def open_tab(chrome: Any, url: str) -> dict[str, Any]:
    result = chrome.tool_chrome_open_tab({"url": url, "foreground": False})
    target_id = result.get("target", {}).get("targetId")
    if target_id:
        return chrome.find_target({"targetId": target_id})
    return chrome.find_target({"urlContains": url})


def wait_ready(chrome: Any, target: dict[str, Any], seconds: int) -> None:
    deadline = time.time() + seconds
    while time.time() < deadline:
        try:
            state = chrome.evaluate(target, "document.readyState")
            if state in ("interactive", "complete"):
                return
        except Exception:
            pass
        time.sleep(0.5)


def scroll_read(chrome: Any, target: dict[str, Any], passes: int, pause: float) -> dict[str, Any]:
    snapshots: list[dict[str, Any]] = []
    for index in range(passes):
        wait_ready(chrome, target, 5)
        data = chrome.evaluate(target, READ_TEXT_JS)
        if isinstance(data, dict):
            data["scrollPass"] = index
            snapshots.append(data)
        chrome.evaluate(
            target,
            "window.scrollBy({ top: Math.floor(window.innerHeight * 0.85), left: 0, behavior: 'instant' }); true;",
        )
        time.sleep(pause)

    final_data = chrome.evaluate(target, READ_TEXT_JS)
    if isinstance(final_data, dict):
        final_data["scrollPass"] = passes
        snapshots.append(final_data)

    seen = set()
    merged_lines: list[str] = []
    for snapshot in snapshots:
        text = snapshot.get("bodyText", "")
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or line in seen:
                continue
            seen.add(line)
            merged_lines.append(line)

    latest = snapshots[-1] if snapshots else {}
    latest["mergedText"] = "\n".join(merged_lines)
    latest["snapshotCount"] = len(snapshots)
    return latest


def redact(text: str) -> str:
    # Keep professional page text, but avoid persisting obvious credential-like data.
    text = re.sub(r"(?i)(password|token|cookie|secret|authorization)\s*[:=]\s*\S+", r"\1: [REDACTED]", text)
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[email redacted]", text)
    return text


def compact_lines(text: str, limit: int = 260) -> list[str]:
    lines = []
    seen = set()
    for raw in text.splitlines():
        line = raw.strip()
        if len(line) < 2 or line in seen:
            continue
        seen.add(line)
        lines.append(line)
        if len(lines) >= limit:
            break
    return lines


def summarize_findings(records: list[dict[str, Any]]) -> str:
    all_text = "\n".join(record.get("mergedText", "") for record in records)
    profile_markers = [
        "Quality Assurance Team Lead",
        "Product Owner",
        "Scrum Master",
        "PowerStore",
        "Enterprise Storage",
        "Test Automation",
        "Release Quality",
        "Dell Technologies",
        "Warsaw",
    ]
    visible_markers = [marker for marker in profile_markers if marker.lower() in all_text.lower()]

    return "\n".join(
        [
            "## Working Summary",
            "",
            "The visible LinkedIn material positions Brijesh Rathod around enterprise storage quality, Dell/PowerStore, test automation, product ownership, Scrum delivery, and release quality.",
            "",
            "Visible recurring markers:",
            *(f"- {marker}" for marker in visible_markers),
            "",
            "Recommended focus:",
            "- Own the niche of AI-era enterprise infrastructure quality: storage reliability, validation depth, release confidence, and automation strategy.",
            "- Expand the network toward QA directors, SRE/release engineering leaders, storage/platform engineering leaders, and infrastructure product leaders.",
            "- Comment on posts from Dell, storage, AI infrastructure, platform engineering, and quality leadership communities before sending senior connection requests.",
            "- Make the headline and About section more outcome-led, not only role-led.",
            "- Publish or comment weekly on practical lessons about release readiness, enterprise storage validation, and automation strategy.",
        ]
    )


def write_markdown(output_path: Path, records: list[dict[str, Any]], raw_json_path: Path) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sections = [
        "# LinkedIn Background Reference",
        "",
        f"Generated: {now}",
        "",
        "Source: read-only local Chrome CDP navigation to LinkedIn pages in the existing Chrome user data directory.",
        "",
        "Safety notes:",
        "- No posts, comments, messages, likes, follows, connection requests, profile edits, labels, deletions, or mailbox actions were performed.",
        "- The collector did not request cookies, tokens, passwords, local storage, or credentials.",
        "- Email-like strings are redacted in the saved Markdown/JSON.",
        "- Third-party network information is kept as visible page text for local reference only; use summaries rather than copying personal details into outbound material.",
        "",
        summarize_findings(records),
        "",
        "## Captured Pages",
        "",
    ]

    for record in records:
        lines = compact_lines(redact(record.get("mergedText", "")))
        sections.extend(
            [
                f"### {record['label']}",
                "",
                f"- Final title: {record.get('title', '')}",
                f"- Final URL: {record.get('url', '')}",
                f"- Canonical URL: {record.get('canonical', '')}",
                f"- Description: {redact(record.get('description', ''))}",
                f"- Scroll snapshots: {record.get('snapshotCount', 0)}",
                "",
                "Visible text excerpt:",
                "",
                "```text",
                *lines,
                "```",
                "",
            ]
        )

    sections.extend(
        [
            "## Next Iteration Ideas",
            "",
            "- Capture screenshots for sections that CDP text cannot represent clearly, then review for layout/profile completeness.",
            "- If LinkedIn blocks details pages or redirects unexpectedly, open the needed page manually once and rerun the collector.",
            "- Add a focused 30-day networking plan after reviewing the captured connection categories.",
            "",
            f"Raw redacted collection JSON: `{raw_json_path.name}`",
            "",
        ]
    )

    output_path.write_text("\n".join(sections), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-script", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--wait-seconds", type=int, default=8)
    parser.add_argument("--scroll-passes", type=int, default=4)
    args = parser.parse_args()

    chrome = load_chrome_module(Path(args.plugin_script))
    before_ids = {target.get("id") for target in page_targets(chrome)}

    records: list[dict[str, Any]] = []
    created_ids: list[str] = []

    for label, url in LINKEDIN_PAGES:
        target = open_tab(chrome, url)
        target_id = target.get("id")
        if target_id:
            created_ids.append(str(target_id))
        wait_ready(chrome, target, args.wait_seconds)
        time.sleep(max(args.wait_seconds - 2, 1))
        data = scroll_read(chrome, target, args.scroll_passes, 1.0)
        data["label"] = label
        data["requestedUrl"] = url
        data["targetId"] = target_id
        data["openedByCollector"] = target_id not in before_ids
        records.append(data)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_json_path = output_dir / "linkedin_background_reference.raw.json"
    md_path = output_dir / "linkedin_background_reference.md"

    redacted_records = json.loads(redact(json.dumps(records, ensure_ascii=False)))
    raw_json_path.write_text(json.dumps(redacted_records, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(md_path, redacted_records, raw_json_path)

    print(json.dumps({"markdown": str(md_path), "rawJson": str(raw_json_path), "pages": len(records)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
