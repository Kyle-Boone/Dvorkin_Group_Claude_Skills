#!/usr/bin/env python3
"""Fetch and parse an arXiv listing page (e.g. astro-ph/new daily mailer)."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape

USER_AGENT = "arxiv-daily-relevance/1.0 (Helen Shao research digest)"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
API_CHUNK = 50
API_PAUSE_SEC = 3.0


def fetch_html(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def strip_tags(html: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_arxiv_id(arxiv_id: str) -> str:
    """Strip version suffix for API id_list (e.g. 2305.10597v2 -> 2305.10597)."""
    return re.sub(r"v\d+$", "", arxiv_id)


def parse_listing(html: str) -> list[dict]:
    """Parse arXiv list page dt/dd pairs."""
    papers: list[dict] = []
    blocks = re.split(r"<dt\b", html, flags=re.I)
    for block in blocks[1:]:
        dt_end = block.find("</dt>")
        if dt_end == -1:
            continue
        dt_html = block[:dt_end]
        dd_html = block[dt_end + 5 :]
        dd_end = dd_html.find("</dd>")
        if dd_end != -1:
            dd_html = dd_html[:dd_end]

        abs_match = re.search(
            r'href\s*=\s*["\'](?:https?://arxiv\.org)?/abs/(\d{4}\.\d{4,5}(?:v\d+)?)["\']',
            dt_html,
            flags=re.I,
        )
        if not abs_match:
            continue
        arxiv_id = abs_match.group(1)
        abs_url = f"https://arxiv.org/abs/{arxiv_id}"

        title_match = re.search(
            r"class=['\"]list-title[^'\"]*['\"][^>]*>.*?(?:Title:\s*</span>|Title:)\s*(.*?)(?:</div>|</p>)",
            dd_html,
            flags=re.I | re.S,
        )
        title = strip_tags(title_match.group(1)) if title_match else ""

        authors_match = re.search(
            r"class=['\"]list-authors[^'\"]*['\"][^>]*>(.*?)(?:</div>|</p>)",
            dd_html,
            flags=re.I | re.S,
        )
        authors = strip_tags(authors_match.group(1)) if authors_match else ""

        subjects_match = re.search(
            r"class=['\"]list-subjects[^'\"]*['\"][^>]*>(.*?)(?:</div>|</p>)",
            dd_html,
            flags=re.I | re.S,
        )
        subjects = strip_tags(subjects_match.group(1)) if subjects_match else ""

        comments_match = re.search(
            r"class=['\"]list-comments[^'\"]*['\"][^>]*>(.*?)(?:</div>|</p>)",
            dd_html,
            flags=re.I | re.S,
        )
        comments = strip_tags(comments_match.group(1)) if comments_match else ""

        abstract_match = re.search(
            r"<p\s+class=['\"]mathjax['\"][^>]*>(.*?)</p>",
            dd_html,
            flags=re.I | re.S,
        )
        abstract = strip_tags(abstract_match.group(1)) if abstract_match else ""

        papers.append(
            {
                "arxiv_id": arxiv_id,
                "abs_url": abs_url,
                "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                "title": title,
                "authors": authors,
                "subjects": subjects,
                "comments": comments,
                "abstract": abstract,
            }
        )

    return papers


def fetch_abstracts_via_api(arxiv_ids: list[str]) -> dict[str, str]:
    """Batch-fetch abstracts from export.arxiv.org Atom API."""
    results: dict[str, str] = {}
    clean_ids = [normalize_arxiv_id(aid) for aid in arxiv_ids]

    for start in range(0, len(clean_ids), API_CHUNK):
        chunk = clean_ids[start : start + API_CHUNK]
        if start > 0:
            time.sleep(API_PAUSE_SEC)
        id_list = ",".join(chunk)
        api_url = (
            "https://export.arxiv.org/api/query?"
            + urllib.parse.urlencode({"id_list": id_list, "max_results": len(chunk)})
        )
        req = urllib.request.Request(api_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as resp:
            xml_text = resp.read().decode("utf-8", errors="replace")
        root = ET.fromstring(xml_text)
        for entry in root.findall("atom:entry", ATOM_NS):
            raw_id = entry.findtext("atom:id", default="", namespaces=ATOM_NS)
            m = re.search(r"(\d{4}\.\d{4,5})", raw_id)
            if not m:
                continue
            paper_id = m.group(1)
            summary = entry.findtext("atom:summary", default="", namespaces=ATOM_NS)
            results[paper_id] = " ".join(summary.split())

    return results


def fetch_abstract_from_abs_page(arxiv_id: str) -> str:
    html = fetch_html(f"https://arxiv.org/abs/{arxiv_id}")
    block_match = re.search(
        r'class="abstract[^"]*"[^>]*>\s*<span[^>]*>Abstract:</span>\s*(.*?)</blockquote>',
        html,
        flags=re.I | re.S,
    )
    if not block_match:
        return ""
    return strip_tags(block_match.group(1))


def backfill_abstracts(papers: list[dict], use_api: bool = True) -> int:
    """Fill missing abstracts. Returns count backfilled."""
    missing = [p for p in papers if not p.get("abstract")]
    if not missing:
        return 0

    filled = 0
    if use_api:
        try:
            api_map = fetch_abstracts_via_api([p["arxiv_id"] for p in missing])
            for paper in missing:
                key = normalize_arxiv_id(paper["arxiv_id"])
                if key in api_map and api_map[key]:
                    paper["abstract"] = api_map[key]
                    paper["abstract_source"] = "api"
                    filled += 1
        except Exception as exc:  # noqa: BLE001
            print(f"API backfill failed ({exc}); falling back to abs pages", file=sys.stderr)

    still_missing = [p for p in papers if not p.get("abstract")]
    for i, paper in enumerate(still_missing):
        try:
            paper["abstract"] = fetch_abstract_from_abs_page(paper["arxiv_id"])
            if paper["abstract"]:
                paper["abstract_source"] = "abs_page"
                filled += 1
        except Exception as exc:  # noqa: BLE001
            paper["abstract_error"] = str(exc)
        if (i + 1) % 25 == 0:
            print(f"abs-page backfill {i + 1}/{len(still_missing)}...", file=sys.stderr)

    return filled


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch papers from an arXiv listing URL")
    parser.add_argument("url", help="arXiv listing URL (e.g. https://arxiv.org/list/astro-ph/new)")
    parser.add_argument(
        "--with-abstracts",
        action="store_true",
        help="Backfill missing abstracts via arXiv API (then abs pages if needed)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max papers to return (0 = all)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Write JSON to file instead of stdout",
    )
    args = parser.parse_args()

    print(f"Fetching listing: {args.url}", file=sys.stderr)
    html = fetch_html(args.url)
    papers = parse_listing(html)
    print(f"Parsed {len(papers)} papers from HTML", file=sys.stderr)

    if args.limit > 0:
        papers = papers[: args.limit]

    if args.with_abstracts:
        n = backfill_abstracts(papers)
        print(f"Backfilled {n} abstracts", file=sys.stderr)

    missing_abstracts = sum(1 for p in papers if not p.get("abstract"))
    payload = {
        "source_url": args.url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "fetch_method": "listing_html",
        "count": len(papers),
        "abstracts_missing": missing_abstracts,
        "papers": papers,
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Wrote {len(papers)} papers to {args.output}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
