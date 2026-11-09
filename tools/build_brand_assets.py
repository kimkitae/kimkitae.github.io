#!/usr/bin/env python3
"""Build the bounded KFlowLabs blog brand assets from the approved V2 kit.

Only allowlisted originals are copied. Generated covers reuse the original
path-based wordmark/monogram and flow motif; nothing is redrawn.

Usage:
  python3 tools/build_brand_assets.py --source "/path/to/brand-kit-v2-2026-11"
  python3 tools/build_brand_assets.py --source "/path/to/brand-kit-v2-2026-11" --check
"""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "brand"

# source-relative -> output-relative. No contact cards, QR, portraits, or
# personal metadata leave the CI folder.
COPY: dict[str, str] = {
    "source/kf-monogram-original.svg": "kf-monogram-original.svg",
    "source/kflowlabs-wordmark-original.svg": "kflowlabs-wordmark-original.svg",
    "kf-avatar-dark.svg": "kf-avatar-dark.svg",
    "kf-avatar-dark.svg.png": "kf-avatar-dark.png",
    "flow-lines.svg": "flow-lines.svg",
    "flow-background.png": "flow-background.png",
    "source/space-grotesk-bold.woff2": "fonts/space-grotesk-bold.woff2",
    "source/SPACE-GROTESK-OFL.txt": "fonts/SPACE-GROTESK-OFL.txt",
}

SIZES: dict[str, tuple[int, int]] = {
    "blog-social": (1600, 900),
    "naver-title": (1920, 480),
    "medium-mobile-automation": (1600, 900),
    "field-series-erp": (1600, 900),
    "field-series-ai-coaching": (1600, 900),
    "field-series-baguio-adaptation": (1600, 900),
    "field-series-a1-reports": (1600, 900),
    "medium-wordmark": (1280, 320),
    "naver-mobile-cover": (1024, 1024),
}

TITLES = {
    "blog-social": "KFlowLabs AX 작업노트",
    "naver-title": "KFlowLabs AX 작업노트",
    "medium-mobile-automation": "Mobile automation",
    "field-series-erp": "자동 배정에 담기지 않은 판단",
    "field-series-ai-coaching": "녹음부터 전달까지, 완료를 나누기",
    "field-series-baguio-adaptation": "같은 기능, 다른 캠퍼스의 연결",
    "field-series-a1-reports": "짧은 발화에서 유용한 리포트로",
    "medium-wordmark": "K-FLOW LABS",
    "naver-mobile-cover": "KFlowLabs AX 작업노트",
}

STYLE = """
@font-face{font-family:KFLDisplay;src:url('fonts/space-grotesk-bold.woff2')}
text{font-family:'Apple SD Gothic Neo','Noto Sans KR',Arial,sans-serif}
.display{font-family:KFLDisplay,'Apple SD Gothic Neo','Noto Sans KR',Arial,sans-serif;font-weight:700}
.mono{font-family:'IBM Plex Mono','SFMono-Regular',Consolas,monospace}
"""


def fail(message: str) -> None:
    raise SystemExit(f"brand assets: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_paths(path: Path) -> list[str]:
    root = ET.parse(path).getroot()
    paths = [el.get("d") for el in root.iter() if el.tag.endswith("path")]
    if not paths or any(not item for item in paths):
        fail(f"no path data in {path}")
    return paths


def wordmark(original_paths: list[str], x: int, y: int, scale: float, dark: bool,
             mono: bool = False) -> str:
    if mono:
        fills = ("#F4F6F5", "#F4F6F5")
    else:
        fills = ("#F4F6F5", "#B5BEBD") if dark else ("#121212", "#2E4053")
    shapes = "".join(
        f'<path fill="{fills[i % 2]}" d="{d}"/>' for i, d in enumerate(original_paths)
    )
    return f'<g transform="translate({x} {y}) scale({scale})">{shapes}</g>'


def flow(flow_paths: list[str], clip: tuple[int, int, int, int], stroke: str, opacity: str,
         transform: str = "") -> str:
    x, y, w, h = clip
    clip_id = f"flow-{x}-{y}-{w}-{h}"
    paths = "".join(f'<path d="{d}"/>' for d in flow_paths)
    return f'''<defs><clipPath id="{clip_id}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs>
<g clip-path="url(#{clip_id})" fill="none" stroke="{stroke}" stroke-width="3" opacity="{opacity}" transform="{transform}">{paths}</g>'''


def svg_doc(w: int, h: int, title: str, body: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">
  <title id="title">{html.escape(title)}</title>
  <defs><style>{STYLE}</style></defs>
{body}
</svg>
'''


def light_cover(title: str, eyebrow: str, headline: tuple[str, ...], subtitle: str, author: str,
                role: str, wordmark_paths: list[str], flow_paths: list[str]) -> str:
    lines = "\n".join(
        f'  <text x="110" y="{360 + index * 92}" font-size="84" fill="#172B3A" '
        f'class="display" data-kf-role="title" data-kf-line="{index + 1}">{html.escape(line)}</text>'
        for index, line in enumerate(headline)
    )
    body = f'''  <rect width="1600" height="900" fill="#F7F9FB"/>
{flow(flow_paths, (760, 0, 840, 900), "#006779", "0.16")}
  {wordmark(wordmark_paths, 110, 86, 0.5, False)}
  <rect x="110" y="200" width="40" height="4" fill="#006779"/>
  <text x="110" y="244" font-size="18" letter-spacing="3" fill="#006779" class="mono">{html.escape(eyebrow)}</text>
{lines}
  <text x="110" y="530" font-size="30" fill="#526573" data-kf-role="subtitle">{html.escape(subtitle)}</text>
  <path d="M110 744H900" stroke="#CAD6DF"/>
  <text x="110" y="792" font-size="26" fill="#172B3A" class="display" data-kf-role="author">{html.escape(author)}</text>
  <text x="110" y="824" font-size="19" fill="#526573" data-kf-role="role">{html.escape(role)}</text>'''
    return svg_doc(1600, 900, title, body)


def blog_social(w: int, h: int, wordmark_paths: list[str], flow_paths: list[str]) -> str:
    body = f'''  <rect width="{w}" height="{h}" fill="#101416"/>
{flow(flow_paths, (720, 0, 880, 900), "#A9D7CD", "0.55")}
  {wordmark(wordmark_paths, 110, 86, 0.54, True)}
  <text x="110" y="430" font-size="110" fill="#F4F6F5" class="display">AX 작업노트</text>
  <text x="110" y="520" font-size="32" fill="#A9D7CD">복잡한 일을, 흐르는 시스템으로.</text>
  <text x="110" y="570" font-size="24" fill="#B5BEBD">AI automation · Web &amp; mobile testing · EdTech</text>
  <path d="M110 744H620" stroke="#394347"/>
  <text x="110" y="792" font-size="26" fill="#F4F6F5" class="display">Kitae Kim</text>
  <text x="110" y="824" font-size="19" fill="#B5BEBD">Co-founder · K-FLOW LABS</text>
  <text x="110" y="862" font-size="18" fill="#F4F6F5">kimkitae@kflowlabs.com</text>'''
    return svg_doc(w, h, TITLES["blog-social"], body)


def naver_title(w: int, h: int, wordmark_paths: list[str], flow_paths: list[str]) -> str:
    body = f'''  <rect width="{w}" height="{h}" fill="#101416"/>
{flow(flow_paths, (1180, 0, 740, 480), "#A9D7CD", "0.55", transform="translate(0 -360)")}
  {wordmark(wordmark_paths, 160, 58, 0.42, True)}
  <text x="160" y="174" font-size="18" letter-spacing="3" fill="#A9D7CD" class="mono">FIELD NOTES / AX · AUTOMATION · AI SYSTEMS</text>
  <text x="160" y="274" font-size="84" fill="#F4F6F5" class="display">AX 작업노트</text>
  <text x="160" y="336" font-size="26" fill="#A9D7CD">복잡한 일을, 흐르는 시스템으로.</text>'''
    return svg_doc(w, h, TITLES["naver-title"], body)


def medium_mobile(w: int, h: int, wordmark_paths: list[str], flow_paths: list[str]) -> str:
    body = f'''  <rect width="{w}" height="{h}" fill="#101416"/>
{flow(flow_paths, (820, 0, 780, 900), "#A9D7CD", "0.45")}
  {wordmark(wordmark_paths, 110, 86, 0.5, True)}
  <text x="110" y="232" font-size="18" letter-spacing="3" fill="#A9D7CD" class="mono">FIELD NOTES / MOBILE TESTING</text>
  <text x="110" y="388" font-size="96" fill="#F4F6F5" class="display">Mobile automation</text>
  <text x="110" y="456" font-size="32" fill="#A9D7CD">Where setup, UI actions and evidence belong</text>
  <path d="M110 744H700" stroke="#394347"/>
  <text x="110" y="792" font-size="26" fill="#F4F6F5" class="display">Kitae Kim</text>
  <text x="110" y="824" font-size="19" fill="#B5BEBD">Co-founder · K-FLOW LABS</text>
  <text x="110" y="862" font-size="18" fill="#F4F6F5">kimkitae@kflowlabs.com</text>'''
    return svg_doc(w, h, TITLES["medium-mobile-automation"], body)


def medium_wordmark(w: int, h: int, wordmark_paths: list[str]) -> str:
    scale = 1.55
    x = (w - 709.5 * scale) / 2
    y = (h - 118 * scale) / 2
    body = wordmark(wordmark_paths, x, y, scale, True, mono=True)
    return svg_doc(w, h, "K-FLOW LABS wordmark", body)


def naver_mobile_cover(w: int, h: int, monogram_paths: list[str]) -> str:
    scale = 1.4
    mark_w, mark_h = 223 * scale, 163 * scale
    x, y = (w - mark_w) / 2, 250
    shapes = "".join(f'<path fill="#F4F6F5" d="{d}"/>' for d in monogram_paths)
    body = f'''  <rect width="{w}" height="{h}" fill="#101416"/>
  <g transform="translate({x} {y}) scale({scale})">{shapes}</g>
  <text x="{w / 2}" y="650" text-anchor="middle" font-size="58" fill="#F4F6F5" class="display" data-kf-role="title" data-kf-line="1">KFlowLabs</text>
  <text x="{w / 2}" y="730" text-anchor="middle" font-size="64" fill="#F4F6F5" class="display" data-kf-role="title" data-kf-line="2">AX 작업노트</text>'''
    return svg_doc(w, h, TITLES["naver-mobile-cover"], body)


def fixture_html(name: str, w: int, h: int, svg_text: str) -> str:
    inline = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", svg_text)
    inline = inline.replace("url('fonts/", "url('../fonts/")
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(name)} render fixture</title>
  <style>html,body{{margin:0;padding:0;background:transparent}}svg{{display:block;width:{w}px;height:{h}px}}</style>
</head>
<body data-kf-render="{name}">
{inline}</body>
</html>
'''


def contact_sheet() -> str:
    rows = []
    for name, (w, h) in SIZES.items():
        rows.append(
            f'''    <figure>
      <img src="{name}.png" alt="{html.escape(TITLES[name])}" width="{w}" height="{h}">
      <figcaption><a href="renders/{name}.html">{name}.svg</a> · {w}×{h}</figcaption>
    </figure>'''
        )
    cells = "\n".join(rows)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>KFlowLabs blog brand renders</title>
  <style>
    body{{margin:0;padding:2rem;background:#F7F9FB;color:#172B3A;font-family:Arial,'Apple SD Gothic Neo',sans-serif}}
    h1{{font-size:1.4rem;margin:0 0 .4rem}}
    p{{max-width:60rem;color:#526573;margin:0 0 2rem}}
    main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem}}
    figure{{margin:0}} img{{display:block;width:100%;height:auto;box-shadow:0 1px 6px rgba(16,20,22,.12)}}
    figcaption{{font-size:.8rem;margin-top:.5rem;color:#526573}}
    a{{color:#006779}}
  </style>
</head>
<body>
  <h1>KFlowLabs blog brand renders</h1>
  <p>Open this page after the PNGs are rendered from the paired SVGs. All {len(SIZES)} fixtures are listed below.</p>
  <main>
{cells}
  </main>
</body>
</html>
'''


def build(source: Path) -> None:
    for rel in COPY:
        if not (source / rel).is_file():
            fail(f"missing source file: {rel}")
    if not (source / "BRAND-GUIDE.txt").is_file():
        fail("source does not look like the V2 brand kit (BRAND-GUIDE.txt missing)")

    wordmark_paths = parse_paths(source / "source/kflowlabs-wordmark-original.svg")
    monogram_paths = parse_paths(source / "source/kf-monogram-original.svg")
    flow_paths = parse_paths(source / "flow-lines.svg")

    OUT.mkdir(parents=True, exist_ok=True)
    for rel, dest_rel in COPY.items():
        dest = OUT / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / rel, dest)

    outputs = {
        "blog-social.svg": blog_social(1600, 900, wordmark_paths, flow_paths),
        "naver-title.svg": naver_title(1920, 480, wordmark_paths, flow_paths),
        "medium-mobile-automation.svg": medium_mobile(1600, 900, wordmark_paths, flow_paths),
        "field-series-erp.svg": light_cover(
            TITLES["field-series-erp"], "FIELD SERIES / ERP", ("자동 배정에", "담기지 않은 판단"),
            "자동 배정과 사람의 판단 사이", "Kitae Kim",
            "Co-founder · K-FLOW LABS", wordmark_paths, flow_paths),
        "field-series-ai-coaching.svg": light_cover(
            TITLES["field-series-ai-coaching"], "FIELD SERIES / AI COACHING",
            ("녹음부터 전달까지,", "완료를 나누기"),
            "녹음에서 전달까지의 완료 기준", "Kitae Kim",
            "Co-founder · K-FLOW LABS", wordmark_paths, flow_paths),
        "field-series-baguio-adaptation.svg": light_cover(
            TITLES["field-series-baguio-adaptation"], "FIELD SERIES / BAGUIO",
            ("같은 기능, 다른", "캠퍼스의 연결"),
            "같은 기능을 다른 캠퍼스에 맞추기", "Kitae Kim",
            "Co-founder · K-FLOW LABS", wordmark_paths, flow_paths),
        "field-series-a1-reports.svg": light_cover(
            TITLES["field-series-a1-reports"], "FIELD SERIES / A1",
            ("짧은 발화에서", "유용한 리포트로"),
            "짧은 발화에서 리포트까지의 과정", "Kitae Kim",
            "Co-founder · K-FLOW LABS", wordmark_paths, flow_paths),
        "medium-wordmark.svg": medium_wordmark(1280, 320, wordmark_paths),
        "naver-mobile-cover.svg": naver_mobile_cover(1024, 1024, monogram_paths),
    }
    for name, content in outputs.items():
        (OUT / name).write_text(content, encoding="utf-8")

    renders = OUT / "renders"
    renders.mkdir(parents=True, exist_ok=True)
    for name, (w, h) in SIZES.items():
        svg_text = (OUT / f"{name}.svg").read_text(encoding="utf-8")
        (renders / f"{name}.html").write_text(fixture_html(name, w, h, svg_text), encoding="utf-8")
    (OUT / "index.html").write_text(contact_sheet(), encoding="utf-8")

    print(f"wrote {len(COPY)} source files, {len(outputs)} SVGs, {len(SIZES)} fixtures to {OUT}")


def private_marker(text: str) -> str | None:
    for marker in ("/Users/", "SynologyDrive", "Library/CloudStorage", "회사 CI"):
        if marker in text:
            return marker
    return None


def check(source: Path) -> None:
    errors: list[str] = []
    if not (source / "BRAND-GUIDE.txt").is_file():
        errors.append("source does not look like the V2 brand kit (BRAND-GUIDE.txt missing)")

    for rel, dest_rel in COPY.items():
        src = source / rel
        dst = OUT / dest_rel
        if not src.is_file():
            errors.append(f"missing source: {rel}")
        elif not dst.is_file():
            errors.append(f"missing copy: {dest_rel}")
        elif sha256(src) != sha256(dst):
            errors.append(f"copy hash differs: {dest_rel}")

    refs: list[tuple[Path, str]] = []
    for name, (w, h) in SIZES.items():
        svg = OUT / f"{name}.svg"
        if not svg.is_file():
            errors.append(f"missing svg: {name}.svg")
        else:
            text = svg.read_text(encoding="utf-8")
            try:
                root = ET.fromstring(text)
            except ET.ParseError as exc:
                errors.append(f"invalid XML: {name}.svg ({exc})")
            else:
                if (root.get("width"), root.get("height")) != (str(w), str(h)):
                    errors.append(f"svg size mismatch: {name}.svg")
                if root.get("viewBox") != f"0 0 {w} {h}":
                    errors.append(f"svg viewBox mismatch: {name}.svg")
            marker = private_marker(text)
            if marker:
                errors.append(f"private path marker {marker!r} in {name}.svg")
            refs.extend((svg, ref) for ref in re.findall(r"""(?:href|src)=["']([^"'#]+)["']""", text))
            refs.extend((svg, ref) for ref in re.findall(r"""url\(['"]([^'"]+)['"]\)""", text))

        fixture = OUT / "renders" / f"{name}.html"
        if not fixture.is_file():
            errors.append(f"missing fixture: renders/{name}.html")
        else:
            text = fixture.read_text(encoding="utf-8")
            if f'width="{w}"' not in text or f'height="{h}"' not in text:
                errors.append(f"fixture size mismatch: renders/{name}.html")
            if "<svg" not in text:
                errors.append(f"fixture does not inline its SVG: renders/{name}.html")
            if name != "medium-wordmark" and "url('../fonts/space-grotesk-bold.woff2')" not in text:
                errors.append(f"fixture font URL is not relative: renders/{name}.html")
            if private_marker(text):
                errors.append(f"private path marker in renders/{name}.html")
            refs.extend((fixture, ref) for ref in re.findall(r"""(?:href|src)=["']([^"'#]+)["']""", text))
            refs.extend((fixture, ref) for ref in re.findall(r"""url\(['"]([^'"]+)['"]\)""", text))

        png = OUT / f"{name}.png"
        if png.is_file():
            data = png.read_bytes()
            if data[:8] != b"\x89PNG\r\n\x1a\n":
                errors.append(f"invalid PNG: {name}.png")
            else:
                actual = (int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big"))
                if actual != (w, h):
                    errors.append(f"png size mismatch: {name}.png is {actual[0]}x{actual[1]}")

    index = OUT / "index.html"
    if not index.is_file():
        errors.append("missing index.html contact sheet")
    else:
        text = index.read_text(encoding="utf-8")
        for name in SIZES:
            if f'{name}.png' not in text:
                errors.append(f"contact sheet missing {name}.png")
        marker = private_marker(text)
        if marker:
            errors.append(f"private path marker {marker!r} in index.html")

    for owner, ref in refs:
        if ref.startswith("#"):
            continue
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", ref) or ref.startswith("/"):
            errors.append(f"non-relative reference {ref!r} in {owner.name}")
            continue
        target = (owner.parent / ref).resolve()
        if not target.is_file() and not (target.suffix == ".png" and target.parent == OUT.resolve()):
            errors.append(f"missing relative reference {ref!r} in {owner.name}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"check ok: {len(COPY)} copies, {len(SIZES)} SVGs, {len(SIZES)} fixtures")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="approved V2 brand kit directory")
    parser.add_argument("--check", action="store_true", help="validate copies and generated outputs")
    args = parser.parse_args()
    source = args.source.expanduser().resolve()
    if not source.is_dir():
        fail(f"source directory not found: {source}")
    if args.check:
        check(source)
    else:
        build(source)


if __name__ == "__main__":
    main()
