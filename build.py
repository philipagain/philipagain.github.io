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
SECTIONS = ["Hero", "So far", "Now", "Things I build", "About", "Follow along"]
STEP_MARKS = ["circle", "square", "triangle"]
NOW_MARKS = [
    '<span class="mark square" aria-hidden="true" style="background: var(--accent); width: 12px; height: 12px;"></span>',
    '<span class="mark circle" aria-hidden="true" style="background: var(--sky); width: 12px; height: 12px;"></span>',
    '<span class="mark triangle" aria-hidden="true"></span>',
]
SETTINGS = {"place", "photo", "link", "image", "tags", "signup note", "link text"}
SETTING = re.compile(r"^([A-Za-z ]+):\s+(.*)$")


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
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
        elif not stripped:
            if current:
                paragraphs.append(" ".join(current))
                current = []
        elif not current and SETTING.match(stripped) and SETTING.match(stripped).group(1).lower() in SETTINGS:
            key, value = SETTING.match(stripped).groups()
            settings[key.lower()] = value.strip()
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


def paragraphs_html(paragraphs, indent):
    out = []
    for p in paragraphs:
        if p.startswith("[") and p.endswith("]") and "](" not in p:
            out.append(f'{indent}<p class="small placeholder">{inline(p)}</p>')
        else:
            out.append(f"{indent}<p>{inline(p)}</p>")
    return "\n".join(out)


def build_steps(entries):
    if not entries:
        fail('"# So far" needs at least one "##" entry')
    out = []
    for i, (title, lines) in enumerate(entries):
        settings, bullets, paragraphs = parse_block(lines)
        last = i == len(entries) - 1
        out.append('          <li class="step next">' if last else '          <li class="step">')
        mark = "open" if last else STEP_MARKS[i % len(STEP_MARKS)]
        out.append(f'            <span class="rail" aria-hidden="true"><span class="mark {mark}"></span></span>')
        photo = settings.get("photo", "")
        if last:
            out.append('            <div class="photo next-box"><span>???</span></div>')
        elif photo and not photo.startswith("["):
            out.append(f'            <img class="photo" src="{attr(photo)}" alt="{attr(title)}" loading="lazy">')
        else:
            out.append(f'            <div class="photo placeholder-box">{inline(photo or f"[Photo: {title}]")}</div>')
        if "place" in settings:
            out.append(f'            <span class="place">{inline(settings["place"])}</span>')
        out.append(f"            <h3>{inline(title)}</h3>")
        if bullets:
            out.append("            <ul>")
            out += [f"              <li>{inline(b)}</li>" for b in bullets]
            out.append("            </ul>")
        if paragraphs:
            out.append(paragraphs_html(paragraphs, "            "))
        out.append("          </li>")
    return "\n".join(out)


def build_now(lines):
    _, bullets, _ = parse_block(lines)
    return "\n".join(
        f"        <li>{NOW_MARKS[i % len(NOW_MARKS)]}<span>{inline(b)}</span></li>"
        for i, b in enumerate(bullets)
    )


def build_tools(entries):
    out = []
    for title, lines in entries:
        settings, _, paragraphs = parse_block(lines)
        for key in ("link", "image"):
            if key not in settings:
                fail(f'tool "{title}" needs a "{key.capitalize()}:" line')
        tags = [t.strip() for t in settings.get("tags", "").split(",") if t.strip()]
        out.append(f'        <a class="card" href="{attr(settings["link"])}">')
        out.append(f'          <img src="{attr(settings["image"])}" alt="" width="72" height="72">')
        out.append('          <span style="display: flex; flex-direction: column; gap: 10px;">')
        out.append(f'            <span class="title">{inline(title)}</span>')
        out.append(f'            <span class="desc">{inline(" ".join(paragraphs))}</span>')
        out.append("          </span>")
        if tags:
            out.append('          <span class="tags">')
            for i, tag in enumerate(tags):
                cls = "tag filled" if i == 0 else "tag"
                out.append(f'            <span class="{cls}">{inline(tag)}</span>')
            out.append("          </span>")
        out.append("        </a>")
    return "\n".join(out)


def main():
    front, sections = parse((ROOT / "content.md").read_text(encoding="utf-8"))
    hero, _, hero_text = parse_block(sections["Hero"][0])
    _, _, so_far_intro = parse_block(sections["So far"][0])
    _, _, about = parse_block(sections["About"][0])
    _, _, follow = parse_block(sections["Follow along"][0])

    values = {
        "title": attr(front.get("title", "Philip again...")),
        "description": attr(front.get("description", "")),
        "share_description": attr(front.get("share description", "")),
        "hero_lead": inline(" ".join(hero_text)),
        "signup_note": inline(hero.get("signup note", "")),
        "hero_link": inline(hero.get("link text", "See what I'm building ↓")),
        "so_far_intro": inline(" ".join(so_far_intro)),
        "steps": build_steps(sections["So far"][1]),
        "now": build_now(sections["Now"][0]),
        "tools": build_tools(sections["Things I build"][1]),
        "about": paragraphs_html(about, "        "),
        "follow": inline(" ".join(follow)),
    }

    template = (ROOT / "template.html").read_text(encoding="utf-8")
    template = template.split("\n", 1)[1]  # drop the "edit content.md" note
    page = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], template)
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print("Built index.html from content.md")


if __name__ == "__main__":
    main()
