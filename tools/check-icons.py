#!/usr/bin/env python3
"""No emoji or pictograph glyph ships as an icon on any page.

⛔ RANEE, 21 SEPT 2026: "I don't like those icons. Make them simple, outline,
abstract ... make them all gold and just an outline. I don't want any of those
types of icons anywhere." Every icon is an inline <svg class="pi"> now, styled
by the `svg.pi` rule in css/interior.css and css/chrome.css.

Scans rendered HTML only: comments, <style> and <script> bodies are skipped,
because the repo's own ⛔ notes live there. A CSS `content:` glyph is checked
separately, since a ::before check mark renders like any other icon.
Numeric entities (&#127969;) count: that is how the rentals page hid three.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {".git", "node_modules", "tools", "data"}
GLYPH = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿⬀-⯿⌀-⏿]")
ENTITY = re.compile(r"&#(x[0-9a-fA-F]+|\d+);")
HIDDEN = re.compile(r"<!--.*?-->|<style\b.*?</style>|<script\b.*?</script>", re.S)
CONTENT = re.compile(r"content:\s*([\"'])(.*?)\1")


def bad_chars(text):
    out = GLYPH.findall(text)
    for e in ENTITY.findall(text):
        cp = int(e[1:], 16) if e[0] == "x" else int(e)
        if GLYPH.match(chr(cp)):
            out.append(chr(cp))
    return out


def main():
    bad = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT)
        if SKIP & set(rel.parts):
            continue
        t = p.read_text()
        for c in bad_chars(HIDDEN.sub("", t)):
            bad.append(f"{rel}: {c!r} U+{ord(c):04X} in page markup")
        for css in re.findall(r"<style\b[^>]*>(.*?)</style>", t, re.S):
            for _, v in CONTENT.findall(re.sub(r"/\*.*?\*/", "", css, flags=re.S)):
                for c in bad_chars(v):
                    bad.append(f"{rel}: {c!r} U+{ord(c):04X} in a CSS content: rule")
    for p in sorted((ROOT / "css").glob("*.css")):
        css = re.sub(r"/\*.*?\*/", "", p.read_text(), flags=re.S)
        for _, v in CONTENT.findall(css):
            for c in bad_chars(v):
                bad.append(f"css/{p.name}: {c!r} U+{ord(c):04X} in a CSS content: rule")
    if bad:
        print("check-icons: emoji/pictograph icons found. Use <svg class=\"pi\">.")
        print("\n".join("  " + b for b in bad))
        return 1
    print("check-icons: no emoji icons in shipped HTML or CSS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
