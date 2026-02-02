#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge markdown docs in docs/api_docs/*.md into a single JSON file.

Default:
  - Input:  docs/api_docs/*.md (excluding README.md)
  - Output: docs/apis/apis.json

This script uses only Python stdlib.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


_RE_H = re.compile(r"^(#{1,6})\s+(.*)\s*$")
_RE_BASIC_INFO_ITEM = re.compile(r"^- \*\*(.+?)\*\*:\s*(.*)\s*$")
_RE_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_RE_CODE_FENCE = re.compile(r"^```(\w+)?\s*$")
_RE_ID_SCORE = re.compile(r"^(?P<id>\d+)(?:-(?P<score>\d+))?\.md$")


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def _strip_md(s: str) -> str:
    """Best-effort strip of simple markdown wrappers for values."""
    s = s.strip()
    if not s:
        return s
    # backticks
    if len(s) >= 2 and s[0] == "`" and s[-1] == "`":
        return s[1:-1].strip()
    # markdown link -> URL
    m = _RE_MD_LINK.search(s)
    if m:
        return m.group(2).strip()
    return s


def _extract_api_name(api_url: str) -> str:
    """Extract API name from URL path.
    
    Examples:
        https://qyapi.weixin.qq.com/cgi-bin/user/create?access_token=TOKEN -> user/create
        https://qyapi.weixin.qq.com/cgi-bin/chatdata/set_public_key?... -> chatdata/set_public_key
    """
    if not api_url:
        return ""
    
    # Remove query string
    url_path = api_url.split("?")[0]
    
    # Extract path after /cgi-bin/
    parts = url_path.split("/cgi-bin/")
    if len(parts) > 1:
        return parts[1].strip("/")
    
    # Fallback: just get the last two path segments
    segments = [s for s in url_path.split("/") if s]
    if len(segments) >= 2:
        return "/".join(segments[-2:])
    elif segments:
        return segments[-1]
    
    return ""


def _parse_bool_zh(s: str) -> Optional[bool]:
    s = s.strip()
    if s == "是":
        return True
    if s == "否":
        return False
    return None


def _parse_markdown_table(lines: List[str], start: int) -> Tuple[Optional[Dict[str, Any]], int]:
    """
    Parse a markdown table starting at `start` (line with leading '|').
    Returns (table, next_index).

    table = { "headers": [...], "rows": [[...], ...] }
    """
    if start >= len(lines):
        return None, start
    if not lines[start].lstrip().startswith("|"):
        return None, start
    if start + 1 >= len(lines):
        return None, start

    header_line = lines[start].strip()
    sep_line = lines[start + 1].strip()
    if not sep_line.startswith("|") or "-" not in sep_line:
        return None, start

    def split_row(row: str) -> List[str]:
        row = row.strip()
        if not row.startswith("|"):
            return []
        if row.endswith("|"):
            row = row[1:-1]
        else:
            row = row[1:]
        return [c.strip() for c in row.split("|")]

    headers = split_row(header_line)
    # Basic validity: separator should have same column count (best-effort)
    sep_cols = split_row(sep_line)
    if headers and sep_cols and len(sep_cols) != len(headers):
        # still allow, but keep parsing
        pass

    i = start + 2
    rows: List[List[str]] = []
    while i < len(lines):
        ln = lines[i].rstrip("\n")
        if not ln.strip():
            break
        if not ln.lstrip().startswith("|"):
            break
        rows.append(split_row(ln))
        i += 1

    return {"headers": headers, "rows": rows}, i


def _normalize_params_from_table(table: Dict[str, Any]) -> List[Dict[str, Any]]:
    headers = [h.strip() for h in table.get("headers", [])]
    rows = table.get("rows", []) or []

    # Map by header names (CN/EN)
    idx: Dict[str, int] = {}
    for i, h in enumerate(headers):
        idx[h] = i

    def get_col(row: List[str], *names: str) -> str:
        for n in names:
            j = idx.get(n)
            if j is not None and j < len(row):
                return row[j].strip()
        return ""

    out: List[Dict[str, Any]] = []
    for row in rows:
        name = get_col(row, "参数名", "name", "字段", "字段名")
        if not name and row:
            # fallback: first column
            name = row[0].strip()
        typ = get_col(row, "类型", "type")
        required_raw = get_col(row, "必填", "required", "是否必须")
        desc = get_col(row, "说明", "description", "含义")

        item: Dict[str, Any] = {
            "name": name,
            "type": typ,
            "required": _parse_bool_zh(required_raw),
            "required_raw": required_raw.strip() if required_raw else "",
            "description": desc,
        }
        out.append(item)
    return out


@dataclasses.dataclass
class ParsedDoc:
    id: str
    score: Optional[int]
    title: str
    doc_url: str
    method: str
    api_url: str
    api_name: str
    description: str
    request_params: List[Dict[str, Any]]
    response_params: List[Dict[str, Any]]
    request_examples: List[Dict[str, Any]]
    response_examples: List[Dict[str, Any]]
    sections: List[Dict[str, Any]]
    source_file: str


def _parse_md_file(path: Path) -> ParsedDoc:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    m = _RE_ID_SCORE.match(path.name)
    doc_id = m.group("id") if m else path.stem
    score = int(m.group("score")) if m and m.group("score") else None

    title = ""
    doc_url = ""
    method = ""
    api_url = ""
    description_lines: List[str] = []

    request_params: List[Dict[str, Any]] = []
    response_params: List[Dict[str, Any]] = []
    request_examples: List[Dict[str, Any]] = []
    response_examples: List[Dict[str, Any]] = []
    sections: List[Dict[str, Any]] = []

    cur_h2: str = ""
    cur_h3: str = ""
    cur_section_lines: List[str] = []
    cur_section_title: str = ""

    def flush_generic_section() -> None:
        nonlocal cur_section_lines, cur_section_title
        content = "\n".join(cur_section_lines).strip()
        if cur_section_title and content:
            sections.append({"title": cur_section_title, "content": content})
        cur_section_lines = []
        cur_section_title = ""

    i = 0
    while i < len(lines):
        ln = lines[i]

        # Code fence
        m_f = _RE_CODE_FENCE.match(ln.strip())
        if m_f:
            lang = (m_f.group(1) or "").strip() or "text"
            i += 1
            code_lines: List[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code = "\n".join(code_lines).strip("\n")
            # consume closing fence if present
            if i < len(lines) and lines[i].strip().startswith("```"):
                i += 1

            ex: Dict[str, Any] = {"language": lang, "code": code}
            # attach based on current heading context
            if cur_h2 == "请求信息" and ("示例" in cur_h3 or "请求" in cur_h3):
                request_examples.append(ex)
            elif cur_h2 == "响应信息" and ("示例" in cur_h3 or "响应" in cur_h3):
                response_examples.append(ex)
            else:
                # keep as part of generic section
                cur_section_lines.append(f"```{lang}\n{code}\n```")
            continue

        # Headings
        m_h = _RE_H.match(ln)
        if m_h:
            level = len(m_h.group(1))
            text_h = m_h.group(2).strip()

            if level == 1 and not title:
                title = text_h
            if level <= 3:
                flush_generic_section()

            if level == 2:
                cur_h2 = text_h
                cur_h3 = ""
                # We only start generic capture for non-structured sections
                cur_section_title = text_h if text_h not in ("基本信息", "请求信息", "响应信息") else ""
            elif level == 3:
                cur_h3 = text_h
                if cur_h2 not in ("基本信息", "请求信息", "响应信息"):
                    cur_section_title = f"{cur_h2} / {cur_h3}".strip(" /")
                else:
                    cur_section_title = ""
            else:
                # lower-level headings: treat as generic content boundaries
                cur_section_title = cur_section_title or text_h
            i += 1
            continue

        # Basic info bullets
        if cur_h2 == "基本信息":
            m_bi = _RE_BASIC_INFO_ITEM.match(ln.strip())
            if m_bi:
                k = m_bi.group(1).strip()
                v = _strip_md(m_bi.group(2))
                if k == "文档地址":
                    doc_url = v
                elif k in ("文档 ID", "文档ID", "文档 Id"):
                    # prefer value inside file name, but keep if present
                    doc_id = v.strip("`")
                elif k == "请求方法":
                    method = v
                elif k == "接口地址":
                    api_url = v
                else:
                    # preserve other basic info as generic section content
                    cur_section_lines.append(ln)
                i += 1
                continue

        # Interface description block
        if cur_h2 == "接口描述":
            if ln.strip():
                description_lines.append(ln)
            i += 1
            continue

        # Tables (request/response params)
        if ln.lstrip().startswith("|"):
            table, next_i = _parse_markdown_table(lines, i)
            if table:
                params = _normalize_params_from_table(table)
                if cur_h2 == "请求信息" and ("参数" in cur_h3 or "参数" in cur_h2):
                    request_params.extend(params)
                elif cur_h2 == "响应信息" and ("参数" in cur_h3 or "参数" in cur_h2):
                    response_params.extend(params)
                else:
                    # keep the raw table as generic content
                    cur_section_lines.extend(lines[i:next_i])
                i = next_i
                continue

        # Default: accumulate into generic section if we are in a non-structured section
        if cur_section_title:
            cur_section_lines.append(ln)

        i += 1

    flush_generic_section()

    description = "\n".join(description_lines).strip()

    # Best-effort: if basic info misses method/api_url, try to extract from text
    if not method:
        m2 = re.search(r"请求方式[:：]\s*([A-Z]+)", text)
        if m2:
            method = m2.group(1).strip()
    if not api_url:
        m3 = re.search(r"请求地址[:：]\s*(https?://\S+)", text)
        if m3:
            api_url = m3.group(1).strip()

    # Extract API name from URL
    api_name = _extract_api_name(api_url)

    return ParsedDoc(
        id=str(doc_id),
        score=score,
        title=title,
        doc_url=doc_url,
        method=method,
        api_url=api_url,
        api_name=api_name,
        description=description,
        request_params=request_params,
        response_params=response_params,
        request_examples=request_examples,
        response_examples=response_examples,
        sections=sections,
        source_file=str(path.as_posix()),
    )


def build(input_dir: Path, output_file: Path, pretty: bool, limit: Optional[int]) -> Dict[str, Any]:
    md_files = sorted(p for p in input_dir.glob("*.md") if p.name != "README.md")
    if limit is not None:
        md_files = md_files[:limit]

    apis: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    for p in md_files:
        try:
            doc = _parse_md_file(p)
            apis.append(dataclasses.asdict(doc))
        except Exception as e:
            errors.append({"file": str(p), "error": repr(e)})

    data: Dict[str, Any] = {
        "generated_at": _now_iso(),
        "source_dir": str(input_dir.as_posix()),
        "count": len(apis),
        "error_count": len(errors),
        "errors": errors[:50],  # cap in output to keep file reasonable
        "apis": apis,
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    if pretty:
        output_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        output_file.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge docs/api_docs/*.md into docs/apis/apis.json")
    parser.add_argument(
        "--input-dir",
        default=str(Path(__file__).resolve().parents[1] / "api_docs"),
        help="Directory containing api_docs markdown files",
    )
    parser.add_argument(
        "--output",
        default=str(Path(__file__).resolve().parent / "apis.json"),
        help="Output JSON path",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON (indent=2)")
    parser.add_argument("--limit", type=int, default=None, help="Only process first N markdown files")
    args = parser.parse_args()

    input_dir = Path(args.input_dir).resolve()
    output_file = Path(args.output).resolve()
    data = build(input_dir=input_dir, output_file=output_file, pretty=bool(args.pretty), limit=args.limit)

    print(f"OK: {data['count']} apis -> {output_file}")
    if data["error_count"]:
        print(f"WARN: {data['error_count']} errors (showing first {len(data['errors'])} in json)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


