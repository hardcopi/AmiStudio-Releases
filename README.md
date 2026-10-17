# AmiStudio-Releases

Release archives and the app list for **AmiStudio**, a suite of apps for classic 68k Amigas (AmigaOS 3.x).
This repo holds no source code. Each app's source lives in its own private repo; finished `.lha` archives are
published here as GitHub Release assets, and `manifest.txt` says which version of each app is current.

The **AmiStudio** launcher on the Amiga reads `manifest.txt`, shows every app as an icon (grey = not installed,
thin **Update** button = newer version available) and installs, updates and rolls back apps from the releases below.

## Apps

| App | id | Status |
|---|---|---|
| AmiStudio (launcher) | `launcher` | coming soon |
| Paint | `paint` | coming soon |
| AmiSurf | `amisurf` | coming soon (needs the AmiStudio Host on a PC) |
| Matrix Chat | `matrixchat` | coming soon |

The suite name stays **AmiStudio**. App display names are Paint, AmiSurf and Matrix Chat (formerly AmiStudio Paint,
AmiStudio Browser and AmiStudio Chat).

"Coming soon" entries are placeholders: the launcher lists them as grey icons and does not offer to install them
until a release is published.

## Downloads

Everything is under [Releases](https://github.com/hardcopi/AmiStudio-Releases/releases). GitHub's "Latest" badge
does not mean much here, because several apps share this repo: **`manifest.txt` decides what is current.**

To install by hand, unpack an archive anywhere with `lha x <App>-<ver>.lha` and open the drawer. Every archive
contains `<App>.info` and the `<App>/` drawer at its top level.

## Tags and asset names

- One GitHub Release per app version. Tag `<app>-v<ver>`, all lower case:
  `paint-v1.0.63`, `amisurf-v0.79`, `matrixchat-v0.2`, `launcher-v0.1.1`, `host-v0.1`.
- Release title is the display name plus version (`Paint 1.0.63`, `AmiSurf 0.79`, `Matrix Chat 0.2`); the body is
  that version's CHANGES section.
- Assets:
  - Amiga archive `<Drawer>-<ver>.lha`, packed with `jlha c1q`:
    - Paint: `Paint-<ver>.lha` (final archive name pending the Paint bot; may still ship as `AmiStudioPaint-<ver>.lha`
      until that bot updates)
    - AmiSurf: `AmiSurf-<ver>.lha`
    - Matrix Chat: `MatrixChat-<ver>.lha`
    - Launcher: `AmiStudio-<ver>.lha`
  - Optional variants `<Drawer>-<ver>-<Variant>.lha` (AmiSurf's `-AmiKit` build).
  - Host parts: `amistudio-host-<ver>-linux-x86_64.tar.gz` (later `-windows-x64.zip`).
  - `SHA256SUMS` on every release: one `sha256  filename` line per asset (`sha256sum -c SHA256SUMS` checks them).
- Download URL: `https://github.com/hardcopi/AmiStudio-Releases/releases/download/<tag>/<file>`

## manifest.txt

Read by the Amiga, so it is plain ASCII key/value text with no JSON: LF line endings, at most 32 KB, `#` starts a
comment (at the start of a line or after a space), unknown keys are ignored so the format can grow. A change that
would break old launchers bumps `format`.

URL: `https://raw.githubusercontent.com/hardcopi/AmiStudio-Releases/main/manifest.txt`
(override on the Amiga with the launcher's `MANIFEST=` tooltype; `MIRROR=` changes where archives come from).

```
format 1                  # required, first
updated 2026-10-17
launcher_min 0.1.1        # older launchers say "please update AmiStudio first"

app paint                 # starts a block; a blank line ends it
name Paint
desc Photoshop-class paint program (PhotoCraft based)
ver 1.0.63
date 2026-10-17
tag paint-v1.0.63
file Paint-1.0.63.lha
size 1834212              # bytes; checked before unpacking
sha256 9f2c...e1          # 64 hex digits; checked before unpacking
drawer Paint              # top-level drawer in the archive
exe Paint                 # 040 MUI build; the launcher picks exe-020 / exe-gadtools for the machine
needs os=3.1 cpu=68020 fpu=1 mui=opt rtg=opt
host none                 # or the AmiStudio Host service the app needs (browser, pdf, ...)
icon Icons/about.png      # path inside the drawer, used for the icon grid
min_launcher 0.1.1
notes https://github.com/hardcopi/AmiStudio-Releases/releases/tag/paint-v1.0.63
```

Other keys:
- `channel beta` marks a beta. Launchers only show it with `BETA=ON` (pre-1.0; after 1.0 a separate AmiStudio Beta
  launcher reads betas).
- `variant <name> <file> <size> <sha256>` lists an extra archive on the same release (e.g. `amikit`).
- `status soon` marks a **placeholder**: an announced app with no release yet. A block with neither `ver` nor `file`
  is also a placeholder. Launchers from 0.1.1 show it as a grey "coming soon" icon and never try to download it.
  When the first release is published, `tools/publish.sh` removes `status soon` and fills in the release keys.

`manifest.json` holds the same data for the Host and for desktop tools. It is generated from `manifest.txt` by
`tools/mkmanifest.sh`; never edit it by hand.

## Publishing (app bots, only when Rich asks)

Nothing is published without Rich's OK. Until then app bots keep building into their own `dist/`.

1. Build and pack as usual (`jlha c1q`), so you have `dist/<Drawer>-<ver>.lha` with a correct
   `$VER: <Exe> <ver> (dd.mm.yyyy)` in every binary.
2. Dry run in a checkout of this repo (prints the release, SHA256SUMS and the new manifest block; changes nothing):

       tools/publish.sh paint 1.0.64 ../amiga-photocraft-c/dist/Paint-1.0.64.lha --notes /tmp/changes-1.0.64.txt

   Options: `--variant amikit FILE`, `--extra FILE` (e.g. a Host tarball), `--beta`.
3. With Rich's OK, add `--publish`. The script then checks the version is newer than the listed one, creates the
   GitHub Release `<app>-v<ver>` with the archive(s) and `SHA256SUMS`, updates `manifest.txt` and
   `manifest.json`, re-downloads the asset to confirm size and SHA-256, and pushes one commit named `<app> <ver>`.
   If anything fails before the push, the manifest is not changed.

Needs `python3` and the GitHub CLI (`gh`) logged in with push rights here.

`tools/mkmanifest.sh` checks `manifest.txt` and rewrites `manifest.json`; `tools/mkmanifest.sh --remote --sha` also
downloads every listed asset and compares size and SHA-256.

## Security notes

- SHA-256 proves an archive matches the manifest, not who wrote the manifest. A signed manifest (ed25519, key
  built into the launcher) is planned.
- The AmiStudio Host (for AmiSurf and later apps) runs on a PC on your LAN. Never forward its port (9220) to the
  internet.

## Licence

Not decided yet. Each archive carries its own ReadMe and ATTRIBUTIONS.
