#!/usr/bin/env python3
"""Download a GitHub wiki and build a ready-to-serve MkDocs (Material) site.

Usage
-----
    python wiki2mkdocs.py            # no arguments needed: ACC/CSP extension config wiki
    python wiki2mkdocs.py <repo-or-wiki-url> [-o OUTPUT] [--workdir DIR] ...

One command does everything: clone or ``git pull`` the ``<repo>.wiki.git``
source, rewrite the wiki conventions (page separators, links, images, sidebar
navigation) into plain Markdown, write ``mkdocs.yml`` with the Material for
MkDocs theme, run ``mkdocs build`` and verify the result. It is safe to re-run
whenever the wiki changes.

Exit status is 0 on success, 1 when the build fails, the generated config is
invalid, or ``--strict`` was given and a broken internal link remains.

Publishing
----------
For a GitHub Pages mirror, pass ``--site-url`` so MkDocs emits absolute canonical
links, a sitemap and social cards, and ``--ignore-link`` for links that are
already broken upstream so they are reported without failing the run::

    python wiki2mkdocs.py ac-custom-shaders-patch/acc-extension-config \\
        --output acc-extension-config \\
        --site-url https://<owner>.github.io/<repo> \\
        --repo-url https://github.com/<owner>/<repo> \\
        --ignore-link 'Cars-\u2013-Extra-turbo-options'

Examples
--------
    python wiki2mkdocs.py
    python wiki2mkdocs.py ac-custom-shaders-patch/acc-extension-config
    python wiki2mkdocs.py https://github.com/ac-custom-shaders-patch/acc-extension-config.wiki.git -o site
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Sequence
from urllib.parse import unquote, urlsplit

# --------------------------------------------------------------------------
# Wiki conventions
# --------------------------------------------------------------------------

#: GitHub page files whose purpose is chrome, not content.
CHROME_PAGES = {
    "_sidebar",
    "_footer",
    "_header",
    "_navbar",
    "_editlinks",
    "_toc",
    "_footer.md",
}

#: Directories that never contain publishable content.
SKIP_DIRS = {"templates", ".git", ".github", ".vscode", ".obsidian"}

#: Separators GitHub accepts between the words of a page slug. The ACC wiki
#: uses a literal hyphen + EN DASH + hyphen (``-`U+2013`-``); others use a
#: plain triple hyphen or underscores.
SEP_RE = re.compile(r"(?:-{2,}|[-_\s]*\u2013[-_\s]*|[-_]{2,})")

IMAGE_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico", ".avif",
}
MEDIA_EXT = {".mp4", ".webm", ".ogg", ".mp3", ".wav", ".m4a", ".mov", ".pdf", ".zip"}

#: Characters that are legal in a URL path but hostile to filesystems.
FILENAME_UNSAFE = re.compile(r'[<>:"|?*\\]')

EXTERNAL_SCHEMES = (
    "http://", "https://", "//", "mailto:", "ftp://", "ftps://",
    "tel:", "data:", "irc:", "steam:", "javascript:", "#",
)


def normalize_key(name: str) -> str:
    """Fuzzy key used to match a link target to a wiki page.

    GitHub resolves wiki links case-insensitively and ignores punctuation and
    whitespace, so ``Cars---Wheels``, ``cars -–- wheels`` and ``CarsWheels``
    all point at the same page. Reproducing that here means links written by
    hand in the source keep working.
    """
    return re.sub(r"[^a-z0-9]+", "", unquote(name).lower())


def slugify(name: str) -> str:
    """Filesystem-friendly slug for a wiki page or link text."""
    slug = SEP_RE.sub("-", name)
    slug = FILENAME_UNSAFE.sub("", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-{2,}", "-", slug)
    slug = re.sub(r"[^\w\-()]+", "", slug, flags=re.UNICODE)
    slug = slug.strip("-.").lower()
    return slug or "page"


def md_anchor(text: str) -> str:
    """Approximate Python-Markdown's ``toc`` slugify for a heading."""
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
    slug = re.sub(r"[^\w\- ]+", "", text, flags=re.UNICODE).lower()
    slug = re.sub(r"[\s_]+", "-", slug.strip())
    return re.sub(r"-{2,}", "-", slug).strip("-")


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------

@dataclass
class Source:
    slug: str          # "owner-repo"
    url: str           # git remote, empty for a local directory
    root: Path         # local clone


def parse_source(raw: str) -> tuple[str, str, str]:
    """Return ``(owner, repo, clone_url)`` for a repo path, URL or wiki URL."""
    raw = raw.strip().rstrip("/")
    raw = re.sub(r"\.git$", "", raw)
    raw = re.sub(r"/wiki$", "", raw)

    if "://" in raw:
        parts = urlsplit(raw)
        if parts.hostname and parts.hostname.lower() not in ("github.com", "www.github.com"):
            raise SystemExit(f"only github.com is supported, got: {parts.hostname}")
        segs = [s for s in parts.path.split("/") if s]
    else:
        segs = [s for s in raw.split("/") if s]

    if len(segs) < 2:
        raise SystemExit(f"cannot read owner/repo from: {raw}")

    owner, repo = segs[0], segs[1]
    if repo.endswith(".wiki"):
        repo = repo[: -len(".wiki")]
    if not re.fullmatch(r"[A-Za-z0-9._-]+", owner) or not re.fullmatch(r"[A-Za-z0-9._-]+", repo):
        raise SystemExit(f"cannot read owner/repo from: {raw}")

    return owner, repo, f"https://github.com/{owner}/{repo}.wiki.git"


def fetch(src: Source, update: bool = True) -> None:
    """Clone the wiki if needed, otherwise fast-forward the existing clone."""
    if not src.url:
        if not src.root.is_dir():
            raise SystemExit(f"not a directory: {src.root}")
        print(f"  using local wiki at {src.root}")
        return
    if (src.root / ".git").is_dir():
        if not update:
            print(f"  reusing clone {src.root}")
            return
        print(f"  updating {src.root}")
        run(["git", "-C", str(src.root), "pull", "--ff-only", "--quiet"])
    else:
        if src.root.exists():
            shutil.rmtree(src.root)
        src.root.parent.mkdir(parents=True, exist_ok=True)
        print(f"  cloning {src.url}")
        run(["git", "clone", "--quiet", "--depth", "1", src.url, str(src.root)])
        run(["git", "-C", str(src.root), "submodule", "update", "--init", "--recursive",
             "--depth", "1"], optional=True)


def run(cmd: list[str], optional: bool = False) -> str:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    except FileNotFoundError:
        raise SystemExit(f"command not found: {cmd[0]}")
    if proc.returncode != 0:
        if optional:
            return ""
        sys.stderr.write(proc.stderr.strip() + "\n")
        raise SystemExit(f"command failed ({proc.returncode}): {' '.join(cmd)}")
    return proc.stdout


# --------------------------------------------------------------------------
# Page inventory
# --------------------------------------------------------------------------

@dataclass
class Page:
    stem: str
    src: Path
    out_name: str            # e.g. "cars-wheels.md"
    keys: set[str] = field(default_factory=set)
    title: str = ""
    nav_title: str = ""


def discover(root: Path) -> tuple[list[Page], dict[str, str]]:
    """Map every markdown page to its output filename.

    Returns the pages plus the sidebar path (if the wiki has one).
    """
    pages: list[Page] = []
    used: set[str] = set()

    for path in sorted(root.rglob("*.md"), key=lambda p: p.as_posix().lower()):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts[:-1]):
            continue
        if path.stem.lower() in CHROME_PAGES:
            continue

        base = slugify(path.stem)
        out_name = f"{base}.md"
        n = 2
        while out_name in used:
            out_name = f"{base}-{n}.md"
            n += 1
        used.add(out_name)

        keys = {normalize_key(path.stem), normalize_key(out_name)}
        if path.stem.lower() in ("home", "index", "readme"):
            keys |= {"index", "home", "readme"}
        pages.append(Page(stem=path.stem, src=path, out_name=out_name, keys=keys))

    sidebar = root / "_Sidebar.md"
    return pages, (str(sidebar) if sidebar.is_file() else "")


def build_index(pages: list[Page]) -> dict[str, Page]:
    index: dict[str, Page] = {}
    for page in pages:
        for key in page.keys:
            index.setdefault(key, page)
    home = next((p for p in pages if p.out_name == "index.md"), None)
    if home is None:
        for page in pages:
            if page.stem.lower() in ("home", "readme", "index"):
                home = page
                break
    if home is not None:
        home.out_name = "index.md"
        index.setdefault("index", home)
    return index


# --------------------------------------------------------------------------
# Markdown rewriting
# --------------------------------------------------------------------------

# Python-Markdown (and therefore MkDocs) only recognises a fence at column 0,
# so an indented ``` is rendered as literal text. Matching that rule keeps link
# rewriting in agreement with what the built site will actually show.
FENCE_RE = re.compile(r"^(?P<fence>`{3,}|~{3,})(?P<info>[^\n]*)$")
# Link text may contain balanced brackets (CommonMark allows one nesting level),
# which matters for wiki links such as [`WHEEL_LF`](Page) where the label is code.
LINK_TEXT = r"(?:[^\[\]\\]|\\.|\[[^\[\]]*\])*"
MD_LINK_RE = re.compile(
    r"(?P<bang>!?)\[(?P<text>" + LINK_TEXT + r")\]"
    r"\((?P<dest>[^()\s]*(?:\([^()]*\)[^()\s]*)*)(?P<title>\s+\"[^\"]*\")?\)"
)
HTML_LINK_RE = re.compile(r"(?P<attr>\b(?:href|src)\s*=\s*)(?P<q>[\"'])(?P<dest>[^\"']*)(?P=q)", re.I)
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.S)
SELF_WIKI_URL_RE = re.compile(
    r"^https?://(?:www\.)?github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.wiki)?/wiki/(?P<page>.+)$",
    re.I,
)


def iter_code_spans(line: str):
    """Yield ``(start, end)`` of inline code spans so links inside are skipped."""
    for m in INLINE_CODE_RE.finditer(line):
        yield m.span()


def outside_code(line: str, pos: int) -> bool:
    return not any(s < pos < e for s, e in iter_code_spans(line))


@dataclass
class Ctx:
    """State shared by every rewrite in one run."""

    index: dict[str, "Page"]
    assets: list[Path]
    stats: "Stats"
    owner: str
    repo: str
    fix_anchors: bool = False

    def is_self(self, owner: str, repo: str) -> bool:
        return owner.lower() == self.owner.lower() and repo.lower() == self.repo.lower()


def rewrite_line(line: str, src_file: str, ctx: Ctx) -> str:
    spans = list(iter_code_spans(line))

    def in_code(pos: int) -> bool:
        return any(s < pos < e for s, e in spans)

    def do_link(m: re.Match) -> str:
        if in_code(m.start()):
            return m.group(0)
        new = resolve_dest(m.group("dest"), src_file, ctx)
        return f"{m.group('bang')}[{m.group('text')}]({new}{m.group('title') or ''})"

    line = MD_LINK_RE.sub(do_link, line)

    def do_html(m: re.Match) -> str:
        if in_code(m.start()):
            return m.group(0)
        new = resolve_dest(m.group("dest"), src_file, ctx, is_html_attr=True)
        return f"{m.group('attr')}{m.group('q')}{new}{m.group('q')}"

    return HTML_LINK_RE.sub(do_html, line)


def resolve_dest(dest: str, src_file: str, ctx: Ctx, is_html_attr: bool = False) -> str:
    """Rewrite one link destination; unrecognised targets are returned as-is."""
    stats = ctx.stats
    dest = dest.strip()
    if not dest:
        return dest

    if dest.startswith(EXTERNAL_SCHEMES) or dest.startswith("\\"):
        m = SELF_WIKI_URL_RE.match(dest)
        if m and ctx.is_self(m.group("owner"), m.group("repo")):
            # A link back into this same wiki becomes a local page link.
            page = lookup(m.group("page"), ctx.index)
            if page is None:
                stats.note(f"{src_file}: wiki URL points at a missing page: {dest}")
                ctx.stats.broken_pages += 1
                return dest
            stats.internal += 1
            # Markdown links keep the extension; raw HTML hrefs get the served URL.
            return page.out_name[:-3] if is_html_attr else page.out_name
        stats.external += 1
        return dest

    if dest.startswith("/"):
        # GitHub resolves "/owner/repo/path" against github.com; MkDocs would
        # resolve it against the site root, so make it absolute.
        stats.external += 1
        return "https://github.com" + dest

    path_part, sep, anchor = dest.partition("#")
    ext = Path(path_part).suffix.lower()

    if not path_part:
        if anchor:
            stats.anchor += 1
            return f"#{md_anchor(anchor) if ctx.fix_anchors else anchor}"
        return dest

    if ext in IMAGE_EXT or ext in MEDIA_EXT or path_part.endswith("/"):
        asset = next((a for a in ctx.assets if a.name.lower() == Path(path_part).name.lower()), None)
        if asset is None:
            stats.note(f"{src_file}: missing asset {path_part!r}")
            stats.broken_assets += 1
            return dest
        stats.internal += 1
        return asset_rel(asset) + (f"#{anchor}" if sep else "")

    page = lookup(path_part, ctx.index)
    if page is None:
        ctx.stats.broken_pages += 1
        stats.note(f"{src_file}: unresolved page link {dest!r}")
        return dest

    stats.internal += 1
    if sep:
        new_anchor = md_anchor(anchor) if ctx.fix_anchors and anchor else anchor
        return f"{page.out_name}#{new_anchor}"
    return page.out_name


def lookup(target: str, index: dict[str, Page]) -> Page | None:
    target = unquote(target.strip())
    if target.lower().endswith(".md"):
        target = target[:-3]
    return index.get(normalize_key(target))


def asset_rel(asset: Path) -> str:
    """Path of a copied asset as seen from a page sitting in ``docs/``."""
    parts = asset.parts
    return "/".join(parts[parts.index("assets"):])


def fenced_spans(lines: list[str]) -> tuple[set[int], list[int]]:
    """Return the line numbers inside *closed* fences, plus unclosed openers.

    An unclosed fence is deliberately not treated as opening a code block:
    Python-Markdown (and therefore MkDocs) renders the stray ``` as literal text
    and keeps parsing the remainder as markdown, so link rewriting has to do
    the same or the two would disagree.
    """
    inside: set[int] = set()
    unclosed: list[int] = []
    i = 0
    while i < len(lines):
        m = FENCE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        marker = m.group("fence")
        close = None
        for j in range(i + 1, len(lines)):
            other = FENCE_RE.match(lines[j])
            # A closing fence has no info string and is at least as long.
            if (other and other.group("fence")[0] == marker[0]
                    and len(other.group("fence")) >= len(marker)
                    and not other.group("info").strip()):
                close = j
                break
        if close is None:
            unclosed.append(i + 1)
            i += 1
            continue
        inside.update(range(i, close + 1))
        i = close + 1
    return inside, unclosed


def convert_page(page: Page, out_dir: Path, src_file: str, ctx: Ctx, inject_title: bool) -> None:
    text = page.src.read_text(encoding="utf-8", errors="replace")
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    in_code, unclosed = fenced_spans(lines)
    for lineno in unclosed:
        ctx.stats.note(f"{src_file}:{lineno}: unclosed code fence, rest of the page may render oddly")

    out: list[str] = []
    headings: list[tuple[int, str]] = []

    for lineno, line in enumerate(lines):
        if lineno in in_code:
            out.append(line)
            continue

        hm = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if hm:
            headings.append((len(hm.group(1)), hm.group(2)))

        out.append(rewrite_line(line, src_file, ctx))

    body = "\n".join(out).rstrip() + "\n"

    # GitHub uses the file name as the page title, so the sidebar link text (or
    # the file name) is a better title than whatever heading opens the body -
    # wiki pages routinely start with a section heading instead.
    page.title = page.nav_title or derive_title(page.stem)
    has_h1 = bool(headings) and headings[0][0] == 1
    if inject_title and not has_h1:
        body = f"# {page.title}\n\n{body}"

    (out_dir / page.out_name).write_text(body, encoding="utf-8")
    ctx.stats.pages += 1


def derive_title(stem: str) -> str:
    """``Cars-–-Brake-Disc-FX`` -> ``Cars: Brake Disc FX``."""
    parts = [p for p in SEP_RE.split(stem) if p.strip()]
    if not parts:
        return stem
    if len(parts) == 1:
        return parts[0].replace("-", " ").replace("_", " ").strip()
    head, tail = parts[0], " ".join(parts[1:])
    tail = re.sub(r"[-_]+", " ", tail).strip()
    return f"{head}: {tail}" if head.lower() not in ("wiki", "home") else tail


# --------------------------------------------------------------------------
# Navigation
# --------------------------------------------------------------------------

@dataclass
class NavNode:
    title: str
    page: Page | None = None
    url: str = ""            # set when the sidebar entry points off-site
    children: list["NavNode"] = field(default_factory=list)


def parse_sidebar(path: Path, ctx: Ctx) -> list[NavNode]:
    """Turn ``_Sidebar.md`` headings + bullet lists into a nested nav tree.

    GitHub sidebars express nesting through heading levels (``##`` for a
    section, ``#####`` for a sub-section); the levels used are irrelevant here
    because only their relative order matters.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.replace("\r\n", "\n").split("\n")

    roots: list[NavNode] = []
    stack: list[tuple[int, NavNode]] = []
    in_code, _ = fenced_spans(lines)

    for lineno, raw in enumerate(lines):
        if lineno in in_code:
            continue
        line = raw.rstrip()

        hm = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if hm:
            depth = len(hm.group(1))
            title = hm.group(2).strip()
            while stack and stack[-1][0] >= depth:
                stack.pop()
            node = NavNode(title=title)
            (stack[-1][1].children if stack else roots).append(node)
            stack.append((depth, node))
            continue

        bm = re.match(r"^\s*[-*+]\s+(.*)$", line)
        if bm and stack:
            node = NavNode(title="")
            entry = bm.group(1).strip()
            if entry:
                title, target = split_sidebar_entry(entry)
                node.title = title
                if target.startswith(EXTERNAL_SCHEMES):
                    # An off-site link, e.g. to a sibling repository's wiki.
                    node.url = target
                    ctx.stats.external += 1
                else:
                    page = lookup(target, ctx.index) if target else None
                    if page is not None:
                        node.page = page
                        page.nav_title = title
                    elif target:
                        ctx.stats.note(f"_Sidebar.md: unresolved link {target!r}")
                        ctx.stats.broken_pages += 1
            stack[-1][1].children.append(node)

    return prune_nav(roots)


def prune_nav(nodes: list[NavNode]) -> list[NavNode]:
    """Drop empty sections so a stray ``## Table of Contents`` cannot leak in."""
    kept: list[NavNode] = []
    for node in nodes:
        node.children = prune_nav(node.children)
        if node.page is None and not node.url and not node.children:
            continue
        kept.append(node)
    return kept


def drop_page(nodes: list[NavNode], page: "Page | None") -> list[NavNode]:
    """Remove every reference to ``page``, hoisting its children if it had any."""
    if page is None:
        return nodes
    out: list[NavNode] = []
    for node in nodes:
        node.children = drop_page(node.children, page)
        if node.page is page:
            out.extend(node.children)
        else:
            out.append(node)
    return prune_nav(out)


def split_sidebar_entry(entry: str) -> tuple[str, str]:
    """``- [Brakes](Cars-–-Brakes)`` -> ``("Brakes", "Cars-–-Brakes")``."""
    m = MD_LINK_RE.search(entry)
    if not m:
        return re.sub(r"[*_`]", "", entry).strip(), ""
    return m.group("text").strip(), unquote(m.group("dest").strip())


def nav_to_yaml(nodes: list[NavNode], indent: int) -> tuple[list[str], set[str]]:
    """Emit nav in MkDocs' ``- Title: path`` form (path-first is not accepted)."""
    lines: list[str] = []
    used: set[str] = set()
    pad = " " * indent
    for node in nodes:
        if node.url:
            lines.append(f"{pad}- {yaml_scalar(node.title)}: {yaml_scalar(node.url)}")
        elif node.page is not None:
            used.add(node.page.out_name)
            lines.append(f"{pad}- {yaml_scalar(node.title)}: {yaml_scalar(node.page.out_name)}")
        elif node.children:
            lines.append(f"{pad}- {yaml_scalar(node.title or 'Section')}:")
            sub, sub_used = nav_to_yaml(node.children, indent + 4)
            lines.extend(sub)
            used |= sub_used
        else:
            lines.append(f"{pad}- {yaml_scalar(node.title)}")
    return lines, used


def yaml_scalar(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return "''"
    if re.search(r"[:#\[\]{}&*!|>'\"%@`,]|^\s|\s$|^\d+[.)]\s", text) or text.lower() in {
        "true", "false", "null", "yes", "no", "on", "off", "~"
    }:
        return "'" + text.replace("'", "''") + "'"
    return text


# --------------------------------------------------------------------------
# Config emission
# --------------------------------------------------------------------------

MATERIAL_FEATURES = [
    "navigation.instant",
    "navigation.tracking",
    "navigation.sections",
    "navigation.path",
    "navigation.footer",
    "navigation.top",
    "content.code.copy",
    "content.code.annotate",
    "search.highlight",
    "search.suggest",
    "toc.follow",
]

MATERIAL_EXTENSIONS = [
    "abbr",
    "admonition",
    "attr_list",
    "def_list",
    "footnotes",
    "md_in_html",
    "tables",
    "toc",
    {"toc": {"permalink": True, "permalink_title": "Link to this section"}},
    "pymdownx.details",
    "pymdownx.highlight",
    # anchor_linenums is what powers Material's code annotations and line links.
    {"pymdownx.highlight": {"anchor_linenums": True, "line_spans": "__span"}},
    "pymdownx.inlinehilite",
    "pymdownx.superfences",
    "pymdownx.tabbed",
    {"pymdownx.tabbed": {"alternate_style": True}},
    "pymdownx.tasklist",
]

CORE_EXTENSIONS = [
    "admonition",
    "attr_list",
    "def_list",
    "footnotes",
    "md_in_html",
    "tables",
    "toc",
    {"toc": {"permalink": True}},
]


def write_mkdocs_yml(
    out_root: Path,
    title: str,
    repo_url: str,
    nav: list[NavNode],
    leftover: list[Page],
    theme: str,
    use_material: bool,
    edit_uri: str,
    strict: bool,
    nest: bool = True,
    nav_root: str = "Documentation",
    site_url: str = "",
    source_url: str = "",
) -> None:
    docs_dir = out_root / "docs"
    lines: list[str] = [
        f"# Generated by wiki2mkdocs.py from {source_url or repo_url.replace('.wiki.git', '')}",
        "site_name: " + yaml_scalar(title),
        "site_description: " + yaml_scalar(f"Docs for {title}"),
        "docs_dir: docs",
        "site_url: " + (yaml_scalar(site_url) if site_url else "''"),
        "",
        "theme:",
        f"  name: {theme}",
    ]

    if use_material:
        lines.append("  features:")
        lines += [f"    - {f}" for f in MATERIAL_FEATURES]
        lines += [
            "  palette:",
            "    # Auto light/dark, with a manual toggle that remembers the choice.",
            "    - media: '(prefers-color-scheme: light)'",
            "      scheme: default",
            "      primary: indigo",
            "      accent: indigo",
            "      toggle:",
            "        icon: material/brightness-7",
            "        name: Switch to dark mode",
            "    - media: '(prefers-color-scheme: dark)'",
            "      scheme: slate",
            "      primary: indigo",
            "      accent: indigo",
            "      toggle:",
            "        icon: material/brightness-4",
            "        name: Switch to light mode",
            "  icon:",
            "    repo: fontawesome/brands/github",
            "  font:",
            "    text: Roboto",
            "    code: Roboto Mono",
        ]

    lines += [
        "",
        "markdown_extensions:",
    ]
    exts = MATERIAL_EXTENSIONS if use_material else CORE_EXTENSIONS
    for ext in exts:
        lines.append(f"  - {ext}" if isinstance(ext, str) else f"  - {yaml_mapping(ext)}")

    lines += ["", "nav:"]

    # The wiki front page always leads the nav, the way GitHub renders it, and
    # is never repeated further down the tree.
    home = next((p for p in leftover if p.out_name == "index.md"), None)
    nav = drop_page(nav, home) if home is not None else nav
    if home is not None:
        leftover = [p for p in leftover if p is not home]

    _, used = nav_to_yaml(nav, 2)
    extra = [p for p in leftover if p.out_name not in used]
    if extra:
        nav = nav + [NavNode(title="Additional pages",
                             children=[NavNode(title=p.title, page=p) for p in extra])]

    if home is not None:
        lines.append(f"  - Home: {yaml_scalar('index.md')}")

    # Material renders *top-level* nav sections as permanently open groups: it
    # hides their toggle and forces the child nav visible. Only items nested one
    # level deeper get a real collapse toggle. So the wiki's groups are wrapped
    # in a single root entry, which turns each of them into a collapsible
    # subsection - driven purely by the nav, with no custom CSS.
    if nest and len(nav) > 1:
        nav = [NavNode(title=nav_root, children=nav)]

    nav_lines, _ = nav_to_yaml(nav, 2)
    lines += nav_lines

    if repo_url:
        lines += [
            "",
            "repo_url: " + yaml_scalar(repo_url.replace(".wiki.git", "")),
            "repo_name: " + yaml_scalar(title),
        ]
    # The header repo button follows --repo-url (the mirror); the credit in the
    # footer and the social icon point back at the upstream wiki being mirrored.
    upstream_url = (source_url or repo_url).replace(".wiki.git", "")
    wiki_url = upstream_url + ("/wiki" if upstream_url else "")
    if use_material:
        credit = f"Content from the community wiki of {upstream_url}" if upstream_url else f"Content from {title}"
        if upstream_url and upstream_url != repo_url.replace(".wiki.git", ""):
            credit += " (mirrored automatically; not the canonical home)"
        lines += ["", "copyright: >-", "  " + credit]
    extra: dict[str, object] = {}
    if edit_uri:
        extra["edit_uri"] = edit_uri
    if use_material and wiki_url:
        extra["social"] = [{"icon": "fontawesome/brands/github", "link": wiki_url,
                            "name": f"{upstream_url.rsplit('/', 1)[-1]} wiki"}]
    if extra:
        lines += ["", "extra:"]
        for key, value in extra.items():
            lines.append(f"  {key}: {yaml_mapping(value)}")
    if strict:
        lines += ["", "strict: true"]

    (out_root / "mkdocs.yml").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def yaml_mapping(obj: dict | list) -> str:
    """Flow-style YAML for a dict or list, e.g. ``{toc: {permalink: true}}``."""
    if isinstance(obj, list):
        return "[" + ", ".join(yaml_mapping(item) if isinstance(item, dict)
                               else yaml_scalar(str(item)) for item in obj) + "]"
    parts = []
    for key, value in obj.items():
        if isinstance(value, (dict, list)):
            parts.append(f"{key}: {yaml_mapping(value)}")
        elif isinstance(value, bool):
            parts.append(f"{key}: {'true' if value else 'false'}")
        else:
            parts.append(f"{key}: {yaml_scalar(str(value))}")
    return "{" + ", ".join(parts) + "}"


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

@dataclass
class Stats:
    pages: int = 0
    internal: int = 0
    external: int = 0
    anchor: int = 0
    broken_pages: int = 0
    broken_assets: int = 0
    notes: list[str] = field(default_factory=list)

    def note(self, msg: str) -> None:
        if msg not in self.notes:
            self.notes.append(msg)


def copy_assets(root: Path, docs_dir: Path) -> list[Path]:
    assets: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts):
            continue
        if path.suffix.lower() not in IMAGE_EXT and path.suffix.lower() not in MEDIA_EXT:
            continue
        target = docs_dir / "assets" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        assets.append(target)
    return assets


# --------------------------------------------------------------------------
# Verification
# --------------------------------------------------------------------------

def verify_config(path: Path) -> list[str]:
    """Sanity-check the generated mkdocs.yml.

    Duplicate YAML keys are the failure mode that hurts most here: PyYAML keeps
    the last one and MkDocs never complains, so a repeated ``features:`` key
    silently turns an 11-item list into a single value.
    """
    try:
        import yaml
    except ImportError:
        return ["PyYAML is unavailable, cannot validate mkdocs.yml"]

    class StrictLoader(yaml.SafeLoader):
        pass

    def no_duplicates(loader, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise ValueError(
                    f"duplicate key {key!r} at line {key_node.start_mark.line + 1}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    StrictLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, no_duplicates)

    problems: list[str] = []
    try:
        cfg = yaml.load(path.read_text(encoding="utf-8"), Loader=StrictLoader)
    except ValueError as exc:
        return [f"mkdocs.yml: {exc}"]

    theme = cfg.get("theme") or {}
    name = theme.get("name") if isinstance(theme, dict) else None
    if name == "material":
        features = theme.get("features")
        if not isinstance(features, list) or not features:
            problems.append("theme.features must be a non-empty list")
        if len(theme.get("palette") or []) < 2:
            problems.append("theme.palette should offer both a light and a dark scheme")
        if "navigation.sections" not in (features or []):
            problems.append("navigation.sections is off, so sidebar groups lose their section styling")
        if "navigation.expand" in (features or []):
            problems.append("navigation.expand opens every subsection by default; it is the opposite of collapsible")
        if cfg.get("extra_css"):
            problems.append("extra_css is set; this generator is meant to run on theme settings alone")
        exts = cfg.get("markdown_extensions") or []
        have = {e if isinstance(e, str) else next(iter(e)) for e in exts}
        for needed in ("pymdownx.highlight", "pymdownx.superfences", "toc"):
            if needed not in have:
                problems.append(f"markdown_extensions is missing {needed}")

    docs = path.parent / (cfg.get("docs_dir") or "docs")
    targets: list[str] = []

    def collect(nodes: list) -> None:
        for node in nodes or []:
            if isinstance(node, dict):
                for value in node.values():
                    collect([value] if isinstance(value, str) else value)
            elif isinstance(node, str):
                targets.append(node)

    collect(cfg.get("nav"))
    for target in targets:
        if target.endswith(".md") and not (docs / target).exists():
            problems.append(f"nav points at a missing file: {target}")

    # Material hides the toggle for *top-level* nav groups and forces them open;
    # only items nested one level deeper collapse. So anything with children must
    # sit below a single root entry rather than directly at the top level.
    def is_group(node) -> bool:
        return isinstance(node, dict) and any(isinstance(v, (dict, list)) for v in node.values())

    top_groups = [n for n in (cfg.get("nav") or []) if is_group(n)]
    if len(top_groups) > 1:
        problems.append(
            f"{len(top_groups)} top-level nav sections are always open in Material; "
            "nest them under one root entry to make them collapsible")
    return problems


def verify_links(
    site_dir: Path,
    ignore: Sequence[str] = (),
    base_path: str = "",
) -> tuple[int, dict[str, list[str]]]:
    """Every internal href/src in the built site must resolve to a file on disk.

    ``ignore`` holds link targets known to be broken upstream (a wiki page that
    never existed). They are reported separately instead of failing the run, so
    an automated mirror stays green while new breakage still shows up.

    ``base_path`` is the path component of ``site_url``. MkDocs emits
    root-relative URLs such as ``/my-project/page/`` in the pages it generates
    itself, so that prefix has to be stripped before the target can be looked up
    inside ``site_dir``.
    """
    ignored: dict[str, list[str]] = {}
    for pattern in ignore:
        ignored.setdefault(pattern, [])
    broken: dict[str, list[str]] = {}
    prefix = ("/" + base_path.strip("/")) if base_path.strip("/") else ""
    pages = 0
    for html in sorted(site_dir.rglob("*.html")):
        pages += 1
        text = html.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'(?:href|src)="([^"]+)"', text):
            raw = m.group(1)
            if raw.startswith(("http://", "https://", "//", "mailto:", "data:", "javascript:", "#")):
                continue
            target = unquote(urlsplit(raw).path)
            if not target:
                continue
            if prefix and target.startswith(prefix + "/"):
                target = target[len(prefix):]
            resolved = site_dir / target.lstrip("/") if target.startswith("/") \
                else html.parent / target
            if resolved.is_dir():
                resolved = resolved / "index.html"
            if resolved.exists():
                continue
            where = html.relative_to(site_dir).as_posix()
            for pattern in ignore:
                if fnmatch(raw, pattern) or fnmatch(target.lstrip("/"), pattern):
                    ignored[pattern].append(f"{raw}  <- {where}")
                    break
            else:
                broken.setdefault(raw, []).append(where)
    return pages, broken, ignored


def build_site(out_root: Path) -> tuple[bool, str]:
    """Run ``mkdocs build`` against the generated config; return (ok, output)."""
    config = out_root / "mkdocs.yml"
    proc = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "-f", str(config)],
        cwd=out_root, capture_output=True, text=True, errors="replace",
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

DEFAULT_SOURCE = "ac-custom-shaders-patch/acc-extension-config"
DEFAULT_TITLE = "AC Extension Config Mirror"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "acc-extension-config"


def _have_material() -> bool:
    """True when both MkDocs and the Material theme are importable."""
    import importlib.util

    return (importlib.util.find_spec("mkdocs") is not None
            and importlib.util.find_spec("material") is not None)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Convert a GitHub wiki repository into an MkDocs (Material) site.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("source", nargs="?", default=None,
                    help="owner/repo, https://github.com/owner/repo, or the .wiki.git URL "
                         f"(default: {DEFAULT_SOURCE})")
    ap.add_argument("--from", dest="from_dir", default=None,
                    help="convert an already-cloned wiki directory instead of fetching")
    ap.add_argument("-o", "--output", default=str(DEFAULT_OUTPUT),
                    help=f"output directory (default: {DEFAULT_OUTPUT})")
    ap.add_argument("--workdir", default=None, help="where to keep the clone (default: <output>/.wiki-clone)")
    ap.add_argument("--title", default=None,
                    help=f"site title (default: {DEFAULT_TITLE!r} for the default wiki, else the repo name)")
    ap.add_argument("--theme", default="material",
                    help="mkdocs theme: material (default) or any other mkdocs theme name")
    ap.add_argument("--repo-url", default=None, help="link shown in the header (default: the GitHub repo)")
    ap.add_argument("--edit-uri", default="", help="edit_uri template for the 'edit' buttons")
    ap.add_argument("--no-inject-title", action="store_true",
                    help="do not add an H1 when a page has no top-level heading")
    ap.add_argument("--no-sidebar", action="store_true", help="ignore _Sidebar.md and auto-build the nav")
    ap.add_argument("--fix-anchors", action="store_true",
                    help="rewrite #fragment links to Python-Markdown heading slugs")
    ap.add_argument("--keep-output", action="store_true", help="do not wipe the output directory first")
    ap.add_argument("--no-update", action="store_true", help="do not git pull an existing clone")
    ap.add_argument("--no-build", action="store_true",
                    help="write the project but do not run 'mkdocs build' or check the result")
    ap.add_argument("--no-verify", action="store_true",
                    help="build the site but skip the mkdocs.yml and link checks")
    ap.add_argument("--strict", action="store_true", help="emit strict: true in mkdocs.yml")
    ap.add_argument("--site-url", default="",
                    help="public base URL of the built site, e.g. "
                         "https://<owner>.github.io/<repo> (needed for GitHub Pages)")
    ap.add_argument("--ignore-link", action="append", default=[], metavar="PATTERN",
                    help="internal link known to be broken upstream; may be given more than once. "
                         "Accepts shell-style wildcards, e.g. 'cars-extra-*'. Reported but not failed.")
    ap.add_argument("--flat-nav", action="store_true",
                    help="keep sidebar groups at the top level, where Material renders them always open")
    ap.add_argument("--nav-root", default="Documentation",
                    help="title of the single root nav entry the groups are nested under")
    args = ap.parse_args(argv)

    out_root = Path(args.output).resolve()

    if args.from_dir:
        if args.source:
            raise SystemExit("pass either a repository or --from, not both")
        workdir = Path(args.from_dir).resolve()
        if not workdir.is_dir():
            raise SystemExit(f"--from is not a directory: {workdir}")
        repo = workdir.name.removesuffix(".wiki") or "wiki"
        owner, url = repo, ""
        print(f"Source : {workdir} (local)")
    else:
        owner, repo, url = parse_source(args.source or DEFAULT_SOURCE)
        workdir = Path(args.workdir).resolve() if args.workdir else out_root / ".wiki-clone"
        print(f"Source : {url}")

    print(f"Output : {out_root}")
    src = Source(slug=f"{owner}-{repo}", url=url, root=workdir)
    fetch(src, update=not args.no_update)

    root = src.root
    if not any(root.glob("*.md")):
        raise SystemExit(f"no markdown pages found in {root} - is the wiki enabled?")

    docs_dir = out_root / "docs"
    if out_root.exists() and not args.keep_output:
        for child in docs_dir.iterdir() if docs_dir.exists() else []:
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    docs_dir.mkdir(parents=True, exist_ok=True)

    stats = Stats()
    pages, sidebar = discover(root)
    if not pages:
        raise SystemExit(f"no markdown pages found in {root}")
    index = build_index(pages)

    print(f"Found  : {len(pages)} pages")
    assets = copy_assets(root, docs_dir)
    if assets:
        print(f"Assets : {len(assets)} files copied to docs/assets/")

    ctx = Ctx(index=index, assets=assets, stats=stats, owner=owner, repo=repo,
              fix_anchors=args.fix_anchors)

    # Parse the sidebar first: it supplies the human titles used on the pages.
    nav: list[NavNode] = []
    if sidebar and not args.no_sidebar:
        nav = parse_sidebar(Path(sidebar), ctx)
        if not nav:
            print("Warn   : _Sidebar.md produced no nav; falling back to alphabetical")

    for page in pages:
        convert_page(page, docs_dir, page.src.name, ctx, not args.no_inject_title)

    if not nav:
        ordered = sorted(pages, key=lambda p: (p.out_name != "index.md", p.title.lower()))
        nav = [NavNode(title=p.title, page=p) for p in ordered]

    title = args.title or (DEFAULT_TITLE if args.source is None else repo)
    theme = args.theme
    if theme == "material" and not _have_material():
        raise SystemExit(
            "theme 'material' needs the Material for MkDocs package:\n"
            "    pip install mkdocs-material\n"
            "(or pass --theme mkdocs for the built-in theme)")
    config = out_root / "mkdocs.yml"
    write_mkdocs_yml(
        out_root,
        title=title,
        repo_url=args.repo_url or (f"https://github.com/{owner}/{repo}" if url else ""),
        nav=nav,
        leftover=pages,
        theme=theme,
        use_material=theme == "material",
        edit_uri=args.edit_uri,
        strict=args.strict,
        nest=not args.flat_nav,
        nav_root=args.nav_root,
        site_url=args.site_url,
        source_url=url.replace(".wiki.git", "") if url else "",
    )

    print("\n--- summary ---")
    print(f"pages written   : {stats.pages}")
    print(f"links rewritten : {stats.internal} internal, {stats.external} left external")
    if stats.broken_pages or stats.broken_assets:
        print(f"unresolved      : {stats.broken_pages} page link(s), {stats.broken_assets} asset link(s)")
    for note in stats.notes[:40]:
        print(f"  - {note}")
    if len(stats.notes) > 40:
        print(f"  ... and {len(stats.notes) - 40} more")

    failures: list[str] = []
    warnings: list[str] = []
    if not args.no_verify:
        problems = verify_config(config)
        print(f"config check    : {'ok' if not problems else str(len(problems)) + ' problem(s)'}")
        for problem in problems:
            print(f"  - {problem}")
        failures += problems
        # Empty site_url is fine for local preview but wrong for a hosted deploy,
        # so flag it without failing the run.
        if theme == "material" and not args.site_url:
            warnings.append("site_url is empty; pass --site-url before publishing")

    if args.no_build:
        print(f"\nProject ready (build skipped). Serve with:\n  mkdocs serve -f {config}")
        return _report(failures, warnings, args.strict)

    ok, output = build_site(out_root)
    print(f"build           : {'ok' if ok else 'FAILED'}")
    if not ok:
        failures.append("mkdocs build failed")
        print(output)
    elif not args.no_verify:
        scanned, broken, ignored = verify_links(
            out_root / "site", args.ignore_link,
            base_path=urlsplit(args.site_url).path if args.site_url else "")
        print(f"link check      : {scanned} page(s) scanned, {len(broken)} broken, "
              f"{sum(len(v) for v in ignored.values())} ignored")
        for target, where in sorted(broken.items()):
            print(f"  - {target}  <- {len(where)} page(s), e.g. {where[0]}")
        for pattern, hits in sorted(ignored.items()):
            if hits:
                print(f"  ~ ignored '{pattern}': {len(hits)} reference(s), e.g. {hits[0]}")
        if broken:
            # Almost always a page that never existed upstream, so warn rather
            # than fail - --strict turns these into a failure.
            warnings.append(f"{len(broken)} broken internal link(s)")

    print(f"\nServe with:  mkdocs serve -f {config}")
    return _report(failures, warnings, args.strict)


def _report(failures: list[str], warnings: list[str], strict: bool) -> int:
    if failures or (strict and warnings):
        parts = list(failures) + (warnings if strict else [])
        print(f"RESULT: FAILED ({'; '.join(parts)})")
        return 1
    if warnings:
        print(f"RESULT: OK, {len(warnings)} warning(s) - {warnings[0]}")
    else:
        print("RESULT: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
