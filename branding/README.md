# cpp-linter — brand asset library

Built from the org's existing mark: hand-drawn **amber circle + green check**, green serif
wordmark, and the yellow **lint squiggle**. Colors: Gold `#F8C418` · Green `#48B888` ·
Ink `#26241F` · Paper `#FAF6EE`.

## Social preview images (1280×640 — GitHub: Settings → General → Social preview)

| Repo | File |
|------|------|
| cpp-linter-action | `social/social-cpp-linter-action.png` |
| cpp-linter-hooks | `social/social-cpp-linter-hooks.png` |
| cpp-linter | `social/social-cpp-linter.png` |
| cpp-linter-rs | `social/social-cpp-linter-rs.png` |
| clang-tools-pip | `social/social-clang-tools-pip.png` |
| clang-tools-docker | `social/social-clang-tools-docker.png` |
| clang-tools-static-binaries | `social/social-clang-tools-static-binaries.png` |
| clang-tools-wheel | `social/social-clang-tools-wheel.png` |
| asdf-clang-tools | `social/social-asdf-clang-tools.png` |
| cpp-linter.github.io | `social/social-cpp-linter.github.io.png` |

## Org-level assets

| Asset | File | Use |
|-------|------|-----|
| README hero banner | `social/org-readme-banner.png` | `.github/profile/README.md`, repo READMEs |
| Profile banner (animated) | `../assets/profile-banner-light.svg`, `../assets/profile-banner-dark.svg` | `profile/README.md`, light and dark themes; see [Profile banner](#profile-banner) |
| Avatar — light | `social/avatar-light.png` | Org/profile avatar (640×640) |
| Avatar — dark | `social/avatar-dark.png` | Dark backgrounds |
| Avatar — gold tint | `social/avatar-tint.png` | Accent / alt avatar |

## Status marks (120×120 PNG with SVG sources, transparent — shown at 20 px in front of bot comment headings)

Solid circles on a 20 px grid: brand green `#48B888` with a white check, brand gold `#F8C418`
with a dark `#1F2328` exclamation mark, and red `#E5534B` with a white cross.
The SVG files are the sources; GitHub comments use the PNG files.

| Status | File | Use |
|--------|------|-----|
| Passed | `status/passed.png` (`.svg`) | nothing to report |
| Warned | `status/warned.png` (`.svg`) | findings (clang-format or clang-tidy warnings) |
| Failed | `status/failed.png` (`.svg`) | a clang-tidy error, or clang-format failed to run |

cpp-linter v2 links them from `https://raw.githubusercontent.com/cpp-linter/.github/main/branding/status/`,
so keep their names and location.

## Source artwork
`icon.png` (transparent check mark) · `wordmark.png` (full lockup, transparent) ·
`wordmark-text.png` (text-only, transparent) · `logo.png` / `banner.png` (originals on white).

Browse everything live in **Brand Assets.dc.html**.

## Profile banner

`profile-banner/generate.py` draws both banners. It embeds `profile-banner/logo-72.png` and the fonts in
`profile-banner/fonts`, cut down to the characters the banner uses (SIL Open Font License, texts alongside).
After changing the copy or the colors, run:

```bash
uv run branding/profile-banner/generate.py
```

## Developer Notes

The *.xcf files in this folder are GIMP projects.

To edit the brand_logo.xcf project, the Abril Fatface font must be installed to your system fonts. A copy of that font also exists in this folder (which includes the OTF License).
