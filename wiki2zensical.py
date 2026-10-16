#!/usr/bin/env python3
"""Mirror the ACC/CSP extension-config GitHub wiki into this Zensical site.

Run it with no arguments::

    python wiki2zensical.py

It clones ``acc-extension-config.wiki.git`` into a temporary directory, cleans
every page up the same way the MkDocs mirror does, drops the result into
``docs/`` next to this file and rewrites the ``nav`` table in
``zensical.toml`` so the sidebar matches the wiki's own ``_Sidebar.md``.

What "cleaning up" means here (same rules as ``wiki2mkdocs.py``):

* wiki chrome (``_Sidebar.md``, ``_Footer.md``, ...) and the ``templates/``
  directory are skipped - they are not content;
* page files are renamed to lowercase, filesystem-safe slugs
  (``Cars-\u2013-Brakes`` -> ``cars-brakes.md``);
* internal wiki links, same-wiki URLs and asset links are rewritten to the
  local ``.md`` files so nothing points back at github.com;
* images and other media are copied to ``docs/assets/``;
* line endings are normalised and trailing whitespace is stripped.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

# --------------------------------------------------------------------------
# Fixed settings - the script intentionally takes no arguments.
# --------------------------------------------------------------------------

OWNER = "ac-custom-shaders-patch"
REPO = "acc-extension-config"
WIKI_URL = f"https://github.com/{OWNER}/{REPO}.wiki.git"

SITE_ROOT = Path(__file__).resolve().parent
DOCS_DIR = SITE_ROOT / "docs"
CONFIG = SITE_ROOT / "zensical.toml"

#: GitHub page files whose purpose is chrome, not content.
CHROME_PAGES = {
    "_sidebar",
    "_footer",
    "_header",
    "_navbar",
    "_editlinks",
    "_toc",
}

#: Directories that never contain publishable content.
SKIP_DIRS = {"templates", ".git", ".github", ".vscode", ".obsidian"}

#: Separators GitHub accepts between the words of a page slug. The ACC wiki
#: uses a literal hyphen + EN DASH + hyphen (``-``U+2013``-``).
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


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def normalize_key(name: str) -> str:
    """Fuzzy key used to match a link target to a wiki page."""
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


def derive_title(stem: str) -> str:
    """``Cars-\u2013-Brake-Disc-FX`` -> ``Cars: Brake Disc FX``."""
    parts = [p for p in SEP_RE.split(stem) if p.strip()]
    if not parts:
        return stem
    if len(parts) == 1:
        return parts[0].replace("-", " ").replace("_", " ").strip()
    head, tail = parts[0], " ".join(parts[1:])
    tail = re.sub(r"[-_]+", " ", tail).strip()
    return f"{head}: {tail}" if head.lower() not in ("wiki", "home") else tail


def run(cmd: list[str], optional: bool = False) -> str:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
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
    out_name: str
    keys: set[str] = field(default_factory=set)
    title: str = ""
    nav_title: str = ""


def discover(root: Path) -> tuple[list[Page], str]:
    """Map every markdown page to its output filename; find the sidebar."""
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

FENCE_RE = re.compile(r"^(?P<fence>`{3,}|~{3,})(?P<info>[^\n]*)$")
#: A thematic break / horizontal rule (``---``, ``----``, ...).
HRULE_RE = re.compile(r"^-{3,}$")
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


@dataclass
class Ctx:
    index: dict[str, Page]
    assets: list[Path]
    stats: "Stats"
    owner: str
    repo: str

    def is_self(self, owner: str, repo: str) -> bool:
        return owner.lower() == self.owner.lower() and repo.lower() == self.repo.lower()


@dataclass
class Stats:
    pages: int = 0
    internal: int = 0
    external: int = 0
    broken_pages: int = 0
    broken_assets: int = 0
    notes: list[str] = field(default_factory=list)

    def note(self, msg: str) -> None:
        if msg not in self.notes:
            self.notes.append(msg)


def iter_code_spans(line: str):
    for m in INLINE_CODE_RE.finditer(line):
        yield m.span()


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
            page = lookup(m.group("page"), ctx.index)
            if page is None:
                stats.note(f"{src_file}: wiki URL points at a missing page: {dest}")
                stats.broken_pages += 1
                return dest
            stats.internal += 1
            return page.out_name[:-3] if is_html_attr else page.out_name
        stats.external += 1
        return dest

    if dest.startswith("/"):
        stats.external += 1
        return "https://github.com" + dest

    path_part, sep, anchor = dest.partition("#")
    ext = Path(path_part).suffix.lower()

    if not path_part:
        if anchor:
            return f"#{anchor}"
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
        stats.broken_pages += 1
        stats.note(f"{src_file}: unresolved page link {dest!r}")
        return dest

    stats.internal += 1
    if sep:
        return f"{page.out_name}#{md_anchor(anchor) if anchor else anchor}"
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


def fenced_spans(lines: list[str]) -> set[int]:
    """Line numbers inside *closed* fences (a stray opener is left as text)."""
    inside: set[int] = set()
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
            if (other and other.group("fence")[0] == marker[0]
                    and len(other.group("fence")) >= len(marker)
                    and not other.group("info").strip()):
                close = j
                break
        if close is None:
            i += 1
            continue
        inside.update(range(i, close + 1))
        i = close + 1
    return inside


def convert_page(page: Page, out_dir: Path, ctx: Ctx) -> None:
    text = page.src.read_text(encoding="utf-8", errors="replace")
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    in_code = fenced_spans(lines)

    out: list[str] = []
    headings: list[tuple[int, str]] = []

    for lineno, line in enumerate(lines):
        line = line.rstrip()
        if lineno in in_code:
            out.append(line)
            continue
        if HRULE_RE.match(line):
            # A dashes-only rule must be its own block: without a blank line a
            # following heading is glued to it and a preceding line would be
            # turned into a setext heading by the dashes.
            if out and out[-1] != "":
                out.append("")
            out.append(line)
            nxt = lines[lineno + 1].rstrip() if lineno + 1 < len(lines) else ""
            if nxt != "":
                out.append("")
            continue
        hm = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if hm:
            headings.append((len(hm.group(1)), hm.group(2)))
        out.append(rewrite_line(line, page.src.name, ctx))

    body = "\n".join(out).rstrip() + "\n"

    page.title = page.nav_title or derive_title(page.stem)
    has_h1 = bool(headings) and headings[0][0] == 1
    if not has_h1:
        body = f"# {page.title}\n\n{body}"

    (out_dir / page.out_name).write_text(body, encoding="utf-8")
    ctx.stats.pages += 1


# --------------------------------------------------------------------------
# Navigation (from the wiki's own _Sidebar.md)
# --------------------------------------------------------------------------

@dataclass
class NavNode:
    title: str
    page: Page | None = None
    url: str = ""
    children: list["NavNode"] = field(default_factory=list)


def split_sidebar_entry(entry: str) -> tuple[str, str]:
    m = MD_LINK_RE.search(entry)
    if not m:
        return re.sub(r"[*_`]", "", entry).strip(), ""
    return m.group("text").strip(), unquote(m.group("dest").strip())


def parse_sidebar(path: Path, ctx: Ctx) -> list[NavNode]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.replace("\r\n", "\n").split("\n")

    roots: list[NavNode] = []
    stack: list[tuple[int, NavNode]] = []
    in_code = fenced_spans(lines)

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
    kept: list[NavNode] = []
    for node in nodes:
        node.children = prune_nav(node.children)
        if node.page is None and not node.url and not node.children:
            continue
        kept.append(node)
    return kept


def drop_page(nodes: list[NavNode], page: Page | None) -> list[NavNode]:
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


def used_pages(nodes: list[NavNode]) -> set[str]:
    """Output filenames already placed in the nav tree."""
    used: set[str] = set()
    for node in nodes:
        if node.page is not None:
            used.add(node.page.out_name)
        used |= used_pages(node.children)
    return used


def dedupe_nav(nodes: list[NavNode], seen: set[str] | None = None) -> list[NavNode]:
    """Drop repeated page references (the wiki sidebar lists some twice)."""
    if seen is None:
        seen = set()
    out: list[NavNode] = []
    for node in nodes:
        if node.page is not None:
            if node.page.out_name in seen:
                continue
            seen.add(node.page.out_name)
        node.children = dedupe_nav(node.children, seen)
        if node.page is None and not node.url and not node.children:
            continue
        out.append(node)
    return out


# --------------------------------------------------------------------------
# Config emission (Zensical uses TOML, not YAML)
# --------------------------------------------------------------------------

def toml_str(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def nav_to_toml(nodes: list[NavNode], indent: int) -> list[str]:
    lines: list[str] = []
    pad = "  " * indent
    for node in nodes:
        if node.url:
            lines.append(f"{pad}{{ {toml_str(node.title)} = {toml_str(node.url)} }},")
        elif node.page is not None:
            lines.append(f"{pad}{{ {toml_str(node.title)} = {toml_str(node.page.out_name)} }},")
        elif node.children:
            lines.append(f"{pad}{{ {toml_str(node.title or 'Section')} = [")
            lines.extend(nav_to_toml(node.children, indent + 1))
            lines.append(f"{pad}] }},")
    return lines


def find_nav_bounds(content: str) -> tuple[int, int] | None:
    """Locate ``nav = [...]`` in the config, skipping quoted strings."""
    start = content.find("nav = [")
    if start == -1:
        return None
    i = content.find("[", start)
    depth = 0
    in_string = False
    delim = None
    while i < len(content):
        c = content[i]
        if in_string:
            if c == "\\":
                i += 2
                continue
            if c == delim:
                in_string = False
        elif c in ('"', "'"):
            if content[i:i + 3] in ('"""', "'''"):
                close = content.find(content[i:i + 3], i + 3)
                if close == -1:
                    break
                i = close + 3
                continue
            in_string = True
            delim = c
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return start, i + 1
        i += 1
    return None


def update_config(nav: list[NavNode]) -> None:
    content = CONFIG.read_text(encoding="utf-8")
    bounds = find_nav_bounds(content)
    if bounds is None:
        raise SystemExit(f"could not find a 'nav = [...]' block in {CONFIG}")
    start, end = bounds

    block = ["nav = ["] + nav_to_toml(nav, 1) + ["]"]
    new_content = content[:start] + "\n".join(block) + content[end:]
    CONFIG.write_text(new_content, encoding="utf-8")


# --------------------------------------------------------------------------
# Assets
# --------------------------------------------------------------------------

def copy_assets(root: Path) -> list[Path]:
    assets: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts):
            continue
        if path.suffix.lower() not in IMAGE_EXT and path.suffix.lower() not in MEDIA_EXT:
            continue
        target = DOCS_DIR / "assets" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        assets.append(target)
    return assets


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main() -> int:
    work = Path(tempfile.mkdtemp(prefix="wiki2zensical-"))
    try:
        print(f"Cloning {WIKI_URL}")
        run(["git", "clone", "--quiet", "--depth", "1", WIKI_URL, str(work)])

        # Fresh docs tree: everything here is regenerated on every run.
        if DOCS_DIR.exists():
            shutil.rmtree(DOCS_DIR)
        DOCS_DIR.mkdir(parents=True)

        stats = Stats()
        pages, sidebar = discover(work)
        if not pages:
            raise SystemExit("no markdown pages found - is the wiki enabled?")
        index = build_index(pages)
        print(f"Found {len(pages)} pages")

        assets = copy_assets(work)
        if assets:
            print(f"Copied {len(assets)} asset(s) to docs/assets/")

        ctx = Ctx(index=index, assets=assets, stats=stats, owner=OWNER, repo=REPO)

        nav: list[NavNode] = []
        if sidebar:
            nav = parse_sidebar(Path(sidebar), ctx)
            if not nav:
                print("Warn: _Sidebar.md produced no nav; falling back to alphabetical")

        for page in pages:
            convert_page(page, DOCS_DIR, ctx)

        if not nav:
            ordered = sorted(pages, key=lambda p: (p.out_name != "index.md", p.title.lower()))
            nav = [NavNode(title=p.title, page=p) for p in ordered]

        # The wiki home page always leads the nav and is never repeated.
        home = next((p for p in pages if p.out_name == "index.md"), None)
        if home is not None:
            nav = drop_page(nav, home)

        nav = dedupe_nav(nav)

        # Pages the sidebar forgot still get published, under their own group.
        used = used_pages(nav)
        if home is not None:
            used.add(home.out_name)
        leftover = [p for p in pages if p.out_name not in used]
        if leftover:
            leftover.sort(key=lambda p: p.title.lower())
            nav.append(NavNode(title="Additional pages",
                               children=[NavNode(title=p.title, page=p) for p in leftover]))

        # Home first, then the wiki's groups as top-level nav sections.
        final: list[NavNode] = []
        if home is not None:
            final.append(NavNode(title="Home", page=home))
        final.extend(nav)

        update_config(final)

        print("\n--- summary ---")
        print(f"pages written   : {stats.pages}")
        print(f"links rewritten : {stats.internal} internal, {stats.external} external")
        if stats.broken_pages or stats.broken_assets:
            print(f"unresolved      : {stats.broken_pages} page link(s), "
                  f"{stats.broken_assets} asset link(s)")
        for note in stats.notes[:20]:
            print(f"  - {note}")
        if len(stats.notes) > 20:
            print(f"  ... and {len(stats.notes) - 20} more")
        print(f"\nWrote {DOCS_DIR} and updated {CONFIG}")
        print("Build with:  zensical build --clean")
        return 0
    finally:
        # Windows can keep git pack files locked briefly; cmd's rmdir survives it.
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(work)],
                       capture_output=True)


if __name__ == "__main__":
    raise SystemExit(main())
