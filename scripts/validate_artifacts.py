#!/usr/bin/env python3
"""Validate sdlc-fa artifacts against their required-field contracts.

This is the deterministic check behind the gates: a worker result, an
assignment packet, or the status ledger either has its required fields or it
does not. Use it in G2_SCOPE / G6_STATUS and before trusting any worker output.

The required-field lists for assignment packets and worker results are read
from the canonical registry `agents/subagents.yaml`, so this script never
hard-codes a second copy of the contract. Ledger checks mirror the Status
Ledger template in `references/templates.md`.

Usage:
    validate_artifacts.py --type result    .sdlcfa/assignments/STORY-001.result.yaml
    validate_artifacts.py --type assignment .sdlcfa/assignments/STORY-001.packet.yaml
    validate_artifacts.py --type ledger     .sdlcfa/status.yaml
    validate_artifacts.py --type result FILE1 FILE2 ...     # many files at once

Targets may be YAML or JSON. PyYAML is used when installed; otherwise a small
built-in parser handles the indent-based YAML subset these contracts use.
Exit code 0 = all files valid, 1 = at least one missing field, 2 = usage/IO error.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(REPO_ROOT, "agents", "subagents.yaml")

# Ledger required fields mirror the Status Ledger template. Per-story fields are
# checked for every entry under `stories`.
LEDGER_TOP = ["version", "updated_at", "owner", "stories"]
LEDGER_PER_STORY = ["title", "status", "write_scope", "gates"]


# --------------------------------------------------------------------------- #
# Loading                                                                      #
# --------------------------------------------------------------------------- #
def load_data(path):
    """Load a YAML or JSON file into Python objects."""
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    if path.endswith(".json"):
        return json.loads(text)
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ModuleNotFoundError:
        return _mini_yaml(text)


def _mini_yaml(text):
    """Parse the indent-based YAML subset used by sdlc-fa contracts.

    Supports nested mappings, sequences of scalars, sequences of mappings,
    quoted/plain scalars, comments, and empty values (-> None). It is not a
    general YAML parser; install PyYAML for full coverage.
    """
    lines = []
    for raw in text.splitlines():
        stripped = raw.split("#", 1)[0].rstrip() if not _in_quotes_hash(raw) else raw.rstrip()
        if stripped.strip() == "":
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        lines.append((indent, stripped.strip()))

    pos = [0]

    def parse_block(min_indent):
        if pos[0] >= len(lines):
            return None
        indent, content = lines[pos[0]]
        if content.startswith("- "):
            return parse_seq(indent)
        return parse_map(indent)

    def parse_map(indent):
        result = {}
        while pos[0] < len(lines):
            cur_indent, content = lines[pos[0]]
            if cur_indent < indent or content.startswith("- "):
                break
            if cur_indent > indent:
                break
            pos[0] += 1
            key, _, val = content.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                # Look ahead: nested block or empty value.
                if pos[0] < len(lines) and lines[pos[0]][0] > indent:
                    result[key] = parse_block(indent + 1)
                else:
                    result[key] = None
            else:
                result[key] = _scalar(val)
        return result

    def parse_seq(indent):
        items = []
        while pos[0] < len(lines):
            cur_indent, content = lines[pos[0]]
            if cur_indent != indent or not content.startswith("- "):
                break
            pos[0] += 1
            rest = content[2:].strip()
            if ":" in rest and not _looks_scalar(rest):
                # Inline first key of a mapping item; re-feed as a map line.
                lines.insert(pos[0], (indent + 2, rest))
                items.append(parse_map(indent + 2))
            else:
                items.append(_scalar(rest))
        return items

    return parse_block(0)


def _in_quotes_hash(raw):
    # Conservative: if a '#' sits inside quotes, don't treat it as a comment.
    h = raw.find("#")
    if h == -1:
        return False
    seg = raw[:h]
    return seg.count('"') % 2 == 1 or seg.count("'") % 2 == 1


def _looks_scalar(rest):
    # A sequence item like "command: x" is a mapping; a bare path is a scalar.
    key = rest.split(":", 1)[0]
    return " " in key or "/" in key or "." in key


def _scalar(val):
    if val in ("null", "~", ""):
        return None
    if val in ("[]",):
        return []
    if val in ("{}",):
        return {}
    if len(val) >= 2 and val[0] in "\"'" and val[-1] == val[0]:
        return val[1:-1]
    return val


# --------------------------------------------------------------------------- #
# Required-field extraction from the canonical registry                        #
# --------------------------------------------------------------------------- #
def required_fields_from_registry(section):
    """Read a `required_fields:` list under a top-level key in subagents.yaml.

    Done with a tiny line scan so this script has no dependency on the target
    file being loadable, and stays a single source of truth with the registry.
    """
    if not os.path.exists(REGISTRY):
        fail(f"registry not found: {REGISTRY}", code=2)
    fields = []
    in_section = False
    in_list = False
    with open(REGISTRY, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.startswith(section + ":"):
                in_section = True
                continue
            if in_section and not line.startswith(" ") and line.strip():
                break  # next top-level key
            if in_section and line.strip() == "required_fields:":
                in_list = True
                continue
            if in_list:
                s = line.strip()
                if s.startswith("- "):
                    fields.append(s[2:].strip())
                elif s and not s.startswith("- "):
                    in_list = False
    return fields


# --------------------------------------------------------------------------- #
# Checking                                                                     #
# --------------------------------------------------------------------------- #
def get_dotted(obj, dotted):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return (False, None)
        cur = cur[part]
    return (True, cur)


def check_fields(obj, fields):
    missing = []
    for f in fields:
        present, value = get_dotted(obj, f)
        # Present-but-None counts as missing; empty list/str is allowed (e.g.
        # write_scope_used: [] for a read-only worker).
        if not present or value is None:
            missing.append(f)
    return missing


def check_ledger(obj):
    missing = []
    if not isinstance(obj, dict):
        return ["<root must be a mapping>"]
    for f in LEDGER_TOP:
        if obj.get(f) is None:
            missing.append(f)
    stories = obj.get("stories")
    if isinstance(stories, dict):
        for sid, story in stories.items():
            if not isinstance(story, dict):
                missing.append(f"stories.{sid} (must be a mapping)")
                continue
            for f in LEDGER_PER_STORY:
                if story.get(f) is None:
                    missing.append(f"stories.{sid}.{f}")
    return missing


def validate_one(path, kind):
    try:
        data = load_data(path)
    except FileNotFoundError:
        return [f"file not found: {path}"]
    except Exception as exc:  # noqa: BLE001 - report parse errors per file
        return [f"could not parse {path}: {exc}"]
    if data is None:
        return ["file is empty or unparseable"]

    if kind == "assignment":
        fields = required_fields_from_registry("shared_assignment_packet")
        return check_fields(data, fields)
    if kind == "result":
        fields = required_fields_from_registry("shared_result_contract")
        return check_fields(data, fields)
    if kind == "ledger":
        return check_ledger(data)
    fail(f"unknown --type {kind}", code=2)


def fail(msg, code=2):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--type",
        required=True,
        choices=["assignment", "result", "ledger"],
        help="contract to validate each file against",
    )
    parser.add_argument("files", nargs="+", help="artifact files (YAML or JSON)")
    args = parser.parse_args(argv)

    had_error = False
    for path in args.files:
        missing = validate_one(path, args.type)
        if missing:
            had_error = True
            print(f"FAIL {path}")
            for m in missing:
                print(f"  missing: {m}")
        else:
            print(f"OK   {path}")
    return 1 if had_error else 0


if __name__ == "__main__":
    sys.exit(main())
