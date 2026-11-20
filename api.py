"""Read-only local API over human-voice-ontology.md.

Serves the AI markers, human patterns, transformations and rewrite guards as
JSON so other projects (outreach-ontology) can read the current research
without copying it. The markdown file stays the source of truth: it is
re-parsed whenever it changes on disk, so edits show up on the next request.

    python3 api.py                 # http://127.0.0.1:8765
    python3 api.py --port 9000

Endpoints (GET only):
    /                         index of endpoints
    /version                  sha256 prefix and modified time of the ontology
    /markers                  all AI markers (M01...)
    /markers/<id>             one marker, e.g. /markers/M01
    /patterns                 all human patterns (H01...)
    /patterns/<id>            one pattern, e.g. /patterns/H01
    /transformations          marker -> pattern swaps; ?marker=M01 filters
    /guards                   rules any rewrite pipeline must follow
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ONTOLOGY = Path(__file__).resolve().parent / "human-voice-ontology.md"

ENTRY_HEAD = re.compile(r"^### ([MH]\d+)\. (.+)$")
FIELD = re.compile(r"^- \*\*(.+?):\*\* ?(.*)$")
TX_HEAD = re.compile(r"^(\d+)\. \*\*(.+?)\*\*(.*)$")
GUARD = re.compile(r"^- \*\*(.+?)\*\*(.*)$")


def field_key(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def parse_tags(text: str) -> dict:
    tags = {}
    for part in text.split("·"):
        part = part.strip().strip("`")
        if ":" in part:
            key, value = part.split(":", 1)
            tags[key.strip()] = value.strip().split()
    return tags


def split_sections(lines: list[str]) -> dict[str, list[str]]:
    sections, current = {}, None
    for line in lines:
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return sections


def section(sections: dict, prefix: str) -> list[str]:
    for name, body in sections.items():
        if name.startswith(prefix):
            return body
    return []


def parse_entries(body: list[str]) -> list[dict]:
    """### Mnn./Hnn. blocks with '- **Field:** text' bullets; sub-bullets fold into the field."""
    entries, entry, key = [], None, None
    for line in body:
        head = ENTRY_HEAD.match(line)
        if head:
            entry = {"id": head.group(1), "name": head.group(2).strip()}
            entries.append(entry)
            key = None
            continue
        if line.startswith("### "):
            entry = key = None
            continue
        if entry is None or not line.strip():
            continue
        m = FIELD.match(line)
        if m:
            key = field_key(m.group(1))
            entry[key] = parse_tags(m.group(2)) if key == "tags" else m.group(2).strip()
        elif key and key != "tags" and line.startswith("  "):
            entry[key] = (entry[key] + "\n" + line.strip()).strip()
    return entries


def parse_transformations(body: list[str]) -> tuple[list[dict], list[dict]]:
    guards, txs, tx, in_guards = [], [], None, False
    key, key_indent = None, 0
    for line in body:
        if line.startswith("**Guards"):
            in_guards = True
            continue
        if in_guards:
            m = GUARD.match(line)
            if m:
                guards.append({"rule": m.group(1).rstrip("."), "detail": m.group(2).strip()})
            elif line.startswith("  ") and guards:
                guards[-1]["detail"] = (guards[-1]["detail"] + "\n" + line.strip()).strip()
            elif line.strip() and not line.startswith("- "):
                in_guards = False
        head = TX_HEAD.match(line)
        if head:
            title = (head.group(2) + head.group(3)).strip()
            ids = re.findall(r"\b([MH]\d+)\b", title)
            tx = {
                "n": int(head.group(1)),
                "title": title,
                "marker": next((i for i in ids if i.startswith("M")), None),
                "patterns": [i for i in ids if i.startswith("H")],
                "notes": [],
            }
            txs.append(tx)
            key = None
        elif tx and line.startswith("   ") and line.strip().startswith("- "):
            indent = len(line) - len(line.lstrip())
            m = FIELD.match(line.strip())
            if m:
                key, key_indent = field_key(m.group(1)), indent
                tx[key] = m.group(2).strip()
            elif key and indent > key_indent:
                tx[key] = (tx[key] + "\n" + line.strip()).strip()
            else:
                key = None
                tx["notes"].append(line.strip()[2:])
    return txs, guards


class Ontology:
    """Parsed view of the markdown, rebuilt when the file's mtime changes."""

    def __init__(self, path: Path):
        self.path = path
        self._mtime = None
        self.data: dict = {}

    def get(self) -> dict:
        mtime = self.path.stat().st_mtime
        if mtime != self._mtime:
            raw = self.path.read_bytes()
            sections = split_sections(raw.decode("utf-8").splitlines())
            txs, guards = parse_transformations(section(sections, "4."))
            self.data = {
                "version": {
                    "file": self.path.name,
                    "sha256": hashlib.sha256(raw).hexdigest()[:16],
                    "modified": datetime.fromtimestamp(mtime, timezone.utc).isoformat(timespec="seconds"),
                },
                "markers": parse_entries(section(sections, "2.")),
                "patterns": parse_entries(section(sections, "3.")),
                "transformations": txs,
                "guards": guards,
            }
            self._mtime = mtime
        return self.data


ONTOLOGY_VIEW = Ontology(ONTOLOGY)

INDEX = {
    "endpoints": [
        "/version",
        "/markers",
        "/markers/<id>",
        "/patterns",
        "/patterns/<id>",
        "/transformations?marker=<id>",
        "/guards",
    ]
}


def route(path: str, query: dict) -> tuple[int, object]:
    data = ONTOLOGY_VIEW.get()
    parts = [p for p in path.split("/") if p]
    if not parts:
        return 200, INDEX
    name, rest = parts[0], parts[1:]
    if name == "version" and not rest:
        return 200, data["version"]
    if name in ("markers", "patterns"):
        items = data[name]
        if not rest:
            return 200, items
        wanted = rest[0].upper()
        for item in items:
            if item["id"] == wanted:
                return 200, item
        return 404, {"error": f"no {name[:-1]} {rest[0]}"}
    if name == "transformations" and not rest:
        marker = query.get("marker", [None])[0]
        items = data["transformations"]
        if marker:
            items = [t for t in items if t["marker"] == marker.upper()]
        return 200, items
    if name == "guards" and not rest:
        return 200, data["guards"]
    return 404, {"error": f"unknown path {path}", **INDEX}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        try:
            status, payload = route(url.path, parse_qs(url.query))
        except FileNotFoundError:
            status, payload = 500, {"error": f"{ONTOLOGY.name} not found"}
        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"voice-reference API on http://127.0.0.1:{args.port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
