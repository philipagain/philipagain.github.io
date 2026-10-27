#!/usr/bin/env python3
"""Build index.html from content.md and template.html.

Run it with: python3 build.py
The GitHub Action in .github/workflows/build.yml runs it on every push.
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SECTIONS = ["Hero", "So far", "Now", "Things I build", "Photos", "About", "Get in touch"]
SETTINGS = {
    "place", "photo", "link", "image", "tags", "button text", "contact note", "link text",
    "heading", "note", "updated", "kind", "who", "last restart",
}
SETTING = re.compile(r"^([A-Za-z ]+):\s+(.*)$")
# The three logo colours, used in turn for the small leaf markers.
LEAVES = ["leaf-1", "leaf-2", "leaf-3"]
LEAF_SVG = '<svg class="leaf-mark {cls}" viewBox="-60 -110 120 220" aria-hidden="true"><path d="M 0 -100 A 110 110 0 0 1 0 100 A 110 110 0 0 1 0 -100 Z"/></svg>'


def fail(message):
    sys.exit(f"content.md: {message}")


def inline(text):
    """Escape HTML, then turn **bold**, *italic* and [text](url) into tags."""
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a class="ulink" href="\2">\1</a>', text)
    return text


def attr(text):
    return html.escape(text, quote=True)


def parse_block(lines):
    """Split an entry's lines into settings, bullets and paragraphs."""
    settings, bullets, paragraphs, current = {}, [], [], []
    for line in lines + [""]:
        stripped = line.strip()
        match = SETTING.match(stripped)
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
        elif not stripped:
            if current:
                paragraphs.append(" ".join(current))
                current = []
        elif not current and match and match.group(1).lower() in SETTINGS:
            settings[match.group(1).lower()] = match.group(2).strip()
        else:
            current.append(stripped)
    return settings, bullets, paragraphs


def parse(text):
    """Return (front matter, {section: (intro lines, [(entry title, lines)])})."""
    front = {}
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if match:
        for line in match.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                front[key.strip().lower()] = value.strip()
        text = text[match.end():]
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)

    sections, section, entry = {}, None, None
    for line in text.splitlines():
        if line.startswith("# "):
            section = line[2:].strip()
            sections[section] = ([], [])
            entry = None
        elif line.startswith("## "):
            if section is None:
                fail(f'"{line}" comes before any "# Section" heading')
            entry = (line[3:].strip(), [])
            sections[section][1].append(entry)
        elif section is not None:
            (entry[1] if entry else sections[section][0]).append(line)

    missing = [name for name in SECTIONS if name not in sections]
    if missing:
        fail("missing section(s): " + ", ".join(f'"# {name}"' for name in missing))
    return front, sections


def is_placeholder(p):
    return p.startswith("[") and p.endswith("]") and "](" not in p


def paragraphs_html(paragraphs, indent, cls=""):
    out = []
    for p in paragraphs:
        if is_placeholder(p):
            out.append(f'{indent}<p class="placeholder">{inline(p)}</p>')
        elif p.startswith("> "):
            out.append(f'{indent}<blockquote class="pull">{inline(p[2:])}</blockquote>')
        else:
            out.append(f'{indent}<p{cls}>{inline(p)}</p>')
    return "\n".join(out)


def note_html(note, indent):
    return f'{indent}<span class="margin-note" aria-hidden="false">{inline(note)}</span>' if note else ""


def build_steps(entries):
    """So far: one row per start. The last entry is the open one ("What's next")."""
    if not entries:
        fail('"# So far" needs at least one "##" entry')
    out = []
    for i, (title, lines) in enumerate(entries):
        settings, bullets, paragraphs = parse_block(lines)
        last = i == len(entries) - 1
        leaf = LEAF_SVG.format(cls="leaf-open" if last else LEAVES[i % 3])
        place = f'<span class="row-place">{inline(settings["place"])}</span>' if "place" in settings else ""
        body = []
        if bullets:
            body.append("              <ul>")
            body += [f"                <li>{inline(b)}</li>" for b in bullets]
            body.append("              </ul>")
        if paragraphs:
            body.append(paragraphs_html(paragraphs, "              "))
        note = note_html(settings.get("note"), "            ")
        if last:
            out.append(f'          <li class="row row-next" data-start>\n'
                       f'            <div class="row-line">{leaf}<span class="row-title">{inline(title)}</span>{place}</div>\n'
                       + ("\n".join(body) + "\n" if body else "") +
                       "          </li>")
        else:
            out.append(f'          <li class="row" data-start>\n'
                       f'            <details>\n'
                       f'              <summary class="row-line">{leaf}<span class="row-title">{inline(title)}</span>{place}<span class="row-toggle" aria-hidden="true"></span></summary>\n'
                       + "\n".join(body) + "\n"
                       f'            </details>\n'
                       + (note + "\n" if note else "") +
                       "          </li>")
    return "\n".join(out)


def build_now(lines):
    _, bullets, _ = parse_block(lines)
    return "\n".join(
        f'          <li>{LEAF_SVG.format(cls=LEAVES[i % 3])}<span>{inline(b)}</span></li>'
        for i, b in enumerate(bullets)
    )


def chat_html(title, bullets):
    """A small piece of the exported chat page: the tool's real output, drawn in HTML."""
    rows = []
    for i, b in enumerate(bullets):
        who, _, said = b.partition(": ")
        side = "me" if who.strip().lower() == "me" else "them"
        rows.append(f'              <div class="bubble {side}"><span class="who">{inline(who)}</span>{inline(said)}</div>')
    return (
        f'          <div class="chat" data-ui aria-hidden="true">\n'
        f'            <div class="chat-head"><span class="chat-title">{inline(title)}</span><span class="chat-meta">exported chat</span></div>\n'
        f'            <div class="chat-body">\n' + "\n".join(rows) + "\n"
        f'            </div>\n'
        f'          </div>'
    )


def build_tools(entries):
    out = []
    for title, lines in entries:
        settings, bullets, paragraphs = parse_block(lines)
        for key in ("link", "image"):
            if key not in settings:
                fail(f'tool "{title}" needs a "{key.capitalize()}:" line')
        tags = [t.strip() for t in settings.get("tags", "").split(",") if t.strip()]
        tag_html = "".join(f'<span class="tag">{inline(t)}</span>' for t in tags)
        out.append(
            f'      <article class="tool">\n'
            f'        <div class="tool-visual">\n{chat_html(title, bullets)}\n        </div>\n'
            f'        <div class="tool-text">\n'
            f'          <img src="{attr(settings["image"])}" alt="" width="72" height="72" loading="lazy">\n'
            f'          <h3><a href="{attr(settings["link"])}">{inline(title)}</a></h3>\n'
            f'          <p>{inline(" ".join(paragraphs))}</p>\n'
            f'          <div class="tags">{tag_html}</div>\n'
            f'        </div>\n'
            f'      </article>'
        )
    return "\n".join(out)


def webp_size(path):
    """Width and height of a WebP file, read from its header."""
    data = path.read_bytes()[:40]
    kind = data[12:16]
    if kind == b"VP8 ":
        return int.from_bytes(data[26:28], "little") & 0x3FFF, int.from_bytes(data[28:30], "little") & 0x3FFF
    if kind == b"VP8L":
        bits = int.from_bytes(data[21:25], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if kind == b"VP8X":
        return int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1
    fail(f"{path.name} is not a WebP file this script can read")


def build_rolls(entries):
    """One strip per roll of film, newest first. Each bullet is a file name."""
    folder = ROOT / "assets" / "img" / "photos"
    out = []
    for r, (title, lines) in enumerate(entries):
        _, bullets, _ = parse_block(lines)
        shots = []
        for n, b in enumerate(bullets, 1):
            name = b.partition(":")[0].strip()
            alt = f"Photo {n} of {len(bullets)}, {title}"
            small = folder / f"{name}-900.webp"
            if not small.exists():
                fail(f'photo "{name}" not found: add assets/img/photos/{name}-900.webp')
            big = next((folder / f"{name}-{w}.webp" for w in (1800, 1300) if (folder / f"{name}-{w}.webp").exists()), small)
            w, h = webp_size(small)
            shots.append(
                f'            <a class="photo" href="assets/img/photos/{big.name}">'
                f'<img src="assets/img/photos/{small.name}" alt="{attr(alt)}" width="{w}" height="{h}" loading="lazy"></a>'
            )
        older = " is-older" if r >= 2 else ""
        out.append(
            f'      <div class="roll{older}">\n'
            f'        <div class="roll-strip" role="region" aria-label="Roll of film: {attr(title)}" tabindex="0">\n'
            + "\n".join(shots) + "\n"
            f'        </div>\n'
            f'        <button type="button" class="roll-arrow roll-back" aria-label="Earlier photos" hidden><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>\n'
            f'        <button type="button" class="roll-arrow roll-on" aria-label="More photos" hidden><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>\n'
            f'      </div>'
        )
    return "\n".join(out)


def main():
    front, sections = parse((ROOT / "content.md").read_text(encoding="utf-8"))
    hero, _, hero_text = parse_block(sections["Hero"][0])
    so_far, _, so_far_intro = parse_block(sections["So far"][0])
    now, _, now_text = parse_block(sections["Now"][0])
    photos, _, photos_text = parse_block(sections["Photos"][0])
    about_settings, _, about = parse_block(sections["About"][0])
    contact, _, contact_text = parse_block(sections["Get in touch"][0])
    steps = sections["So far"][1]
    restarts = max(len(steps) - 1, 0)

    values = {
        "title": attr(front.get("title", "Philip again...")),
        "description": attr(front.get("description", "")),
        "share_description": attr(front.get("share description", "")),
        "email": attr(front.get("email", "hello@philipagain.com")),
        "updated": inline(now.get("updated", "")),
        "hero_lead": inline(" ".join(hero_text)),
        "hero_who": inline(hero.get("who", "")),
        "button_text": inline(hero.get("button text", "Get in touch")),
        "contact_note": inline(hero.get("contact note", "")),
        "hero_link": inline(hero.get("link text", "See what I'm building")),
        "so_far_intro": inline(" ".join(so_far_intro)),
        "restarts": str(restarts),
        "last_restart": inline(so_far.get("last restart", "")),
        "version": str(restarts + 1),
        "steps": build_steps(steps),
        "now_intro": paragraphs_html(now_text, "        "),
        "now": build_now(sections["Now"][0]),
        "tools": build_tools(sections["Things I build"][1]),
        "photos_title": inline(photos.get("heading", "Photos")),
        "photos_intro": inline(" ".join(photos_text)),
        "rolls": build_rolls(sections["Photos"][1]),
        "older_rolls": "" if len(sections["Photos"][1]) > 2 else " hidden",
        "about_title": inline(about_settings.get("heading", "About")),
        "about_lead": inline(about[0]) if about else "",
        "about": paragraphs_html(about[1:], "        "),
        "contact_title": inline(contact.get("heading", "Get in touch")),
        "contact_text": inline(" ".join(contact_text)),
    }

    template = (ROOT / "template.html").read_text(encoding="utf-8")
    template = template.split("\n", 1)[1]  # drop the "edit content.md" note
    page = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], template)
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print("Built index.html from content.md")


if __name__ == "__main__":
    main()
