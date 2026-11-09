# KFlowLabs blog brand guide

Short art contract for the blog and its cross-channel covers. Prose, routes and
publication schedules are out of scope.

## Provenance

Source: K-FLOW LABS / Flow System V2, marked FINAL / USER APPROVED on 2026-11-06.
The V2 guide supersedes the earlier root design system. Assets are copied from
the supplied brand kit by `tools/build_brand_assets.py`; generated covers reuse
the original path-based wordmark, monogram and three-line flow motif. Do not
redraw, trace or AI-generate the logos.

## Palette

| Token | Value | Use |
| --- | --- | --- |
| Charcoal | `#101416` | dark brand field, sidebar |
| Off-white | `#F7F9FB` | light page field |
| White ink | `#F4F6F5` | text on charcoal |
| Ink | `#172B3A` | text on light surfaces |
| Mint | `#A9D7CD` | emphasis and flow on dark surfaces |
| Deep teal | `#006779` | links and emphasis on light surfaces |
| Muted light | `#526573` | secondary text on light |
| Muted dark | `#B5BEBD` | secondary text on dark |
| Divider light | `#CAD6DF` | rules and borders on light |
| Divider dark | `#394347` | rules and borders on dark |

Silver is an artwork material, not a text color. Do not override the semantic
prompt/status colors in the theme.

## Typography

- Display: Space Grotesk Bold. The supplied woff2 and OFL license live in
  `assets/brand/fonts/`. Use it for English headings and labels.
- Korean and body: Pretendard with installed/system fallbacks. No web font
  download is required.
- Technical labels may use IBM Plex Mono when it is available; fall back to a
  system monospace.
- Keep headings left aligned. Avoid repeating the company name throughout a
  card.

## Logo and flow rules

- Keep the original KF geometry. Keep at least the width of the F stem clear
  around the mark. A small avatar uses the mark, not the full ribbon.
- On charcoal surfaces the wordmark and mark are reversed to white ink. On
  off-white surfaces use the supplied dark original.
- The three flow lines mean the three service areas: AI/AX workflow automation,
  web and mobile test automation, and education technology. They are not
  sequential steps.
- Keep text in the left 60% of ribbon/cover artwork and let lines bleed to the
  right. Do not place important text in the right artwork zone.

## Channel map

| Channel | Asset | Notes |
| --- | --- | --- |
| GitHub Pages home | native theme + `_includes/kflowlabs-brand-header.html` | Avatar `kf-avatar-dark.svg`; social preview `blog-social.png` |
| Favicon and PWA | `kf-avatar-dark.svg`, `kf-avatar-dark.png` | 1024×1024 identity; SVG favicon with PNG fallback |
| GitHub social preview | `assets/brand/blog-social.png` | 1600×900, Korean title two lines, wordmark, low-key contact |
| Naver blog title | `assets/brand/naver-title.png` (master 1920×480) + `assets/brand/naver-title-773.png` (saved 773×194 derivative) | Top-header layout; the 773×194 derivative is the uploaded width |
| Naver blog avatar | `assets/brand/kf-avatar-dark.png` | Separate from the ID shared photo; ID photo stays unchanged |
| Naver mobile cover | `assets/brand/naver-mobile-cover.png` | 1024×1024, charcoal, KF monogram and two-line Korean title |
| Medium | `assets/brand/medium-mobile-automation.png` | 1600×900 cover; existing explanatory image and prose stay |
| Medium wordmark | `assets/brand/medium-wordmark.png` | 1280×320 transparent field, reversed white original wordmark |
| Prepared field series | `field-series-erp.png`, `field-series-ai-coaching.png`, `field-series-baguio-adaptation.png`, `field-series-a1-reports.png` | 1600×900 covers; prepared assets, not publication authorization |

Contact: `kimkitae@kflowlabs.com`. Public wordmark: `K-FLOW LABS`. Author
identity: 김기태의 AX 작업노트 · KFlowLabs / Kitae Kim | KFlowLabs.

## Channel language policy

- Medium: titles, body, covers, captions and CTAs are English for global
  readers.
- Naver: Korean.
- GitHub Pages: bilingual routes preserved as-is.

The four English Medium drafts and their assets are prepared privately; they are
not published or scheduled by this repository task.

## Mobile-safe thumbnails

- Keep the headline and one supporting line in the central 60% of the frame.
- No tiny email or URL text on Naver or Medium covers; use a short contact line
  only where it remains legible.
- Crop from the right, never through the wordmark or headline.
- Check a 390px-wide preview for text clipping and horizontal overflow.

## Verified channel controls

Native inspection confirmed these free controls; account edits remain outside
this repository task:

- Medium free custom profile header accepts a solid hex color, an image, a wide
  logo, responsive preview, and Publish.
- Naver free controls cover skin, title, profile, and mobile cover. The current
  left-title orange skin is 185px wide and obsolete; the replacement uses a
  top-header layout. The saved title derivative is 773×194, generated from the
  1920×480 master.
- On Naver, untick the ID photo option; the shared ID photo stays unchanged.
  The Naver blog avatar is a separate upload and does not replace the ID photo.
- Medium and Naver avatar upload accept the supplied 1024×1024 PNG.

Native profile design changes are still owned by the running root task; this
guide records the policy and saved upload dimensions, not applied profiles.

## Regenerate and check

```sh
python3 tools/build_brand_assets.py --source "/path/to/brand-kit-v2-2026-11"
python3 tools/build_brand_assets.py --source "/path/to/brand-kit-v2-2026-11" --check
```

`--check` verifies copied source hashes, SVG XML and dimensions, inline fixture
SVGs and relative font URLs, self-contained references, absent private paths,
and PNG dimensions when renders exist. Open `assets/brand/index.html` to
inspect all nine renders.

Native Naver and Medium account controls are not edited by this repository
task. The verified controls above are the only upload claims.
