#!/usr/bin/env python3
"""Every class a page uses is defined by a stylesheet that page actually loads.

⛔ THE HOME PAGE HAS BEEN SHIPPING A RAW BLUE LINK WHERE A BUTTON SHOULD BE.
index.html carries its own inline <style> and does NOT load css/interior.css,
so `.btn` and `.btn-gold` -- used on it -- were defined nowhere it could see.
Nothing failed; the markup was valid and the class name was spelled right. It
took a screenshot to notice, which is exactly the class of defect Ranee meant
by "there's some CSS airs for sure."

⛔ A class defined in interior.css does NOT count for a page that never links
interior.css. Resolving per page, not globally, is the whole point.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {".git", "node_modules", "tools", "data"}

# Applied by script at runtime, never written in the markup.
RUNTIME = {"active", "js", "img-revealed", "loaded", "is-visible"}


def main():
    bad = []
    for p in sorted(ROOT.rglob("*.html")):
        if SKIP & set(p.relative_to(ROOT).parts):
            continue
        t = p.read_text()
        css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", t, re.S))
        for href in re.findall(r'<link rel="stylesheet" href="([^"]+)"', t):
            if href.startswith("http"):
                continue
            f = (p.parent / href).resolve()
            if f.exists():
                css += "\n" + f.read_text()
        defined = set(re.findall(r"\.([A-Za-z][\w-]*)", css)) | RUNTIME
        used = set()
        for m in re.findall(r'class="([^"]+)"', t):
            used.update(c for c in m.split() if not c.startswith("{"))
        for c in sorted(used - defined):
            bad.append(f"{p.relative_to(ROOT)}: .{c}")

    print(f"{len(bad)} classes used with no rule the page can reach")
    for b in bad:
        print("  ", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
