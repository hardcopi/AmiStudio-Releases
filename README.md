# AmiStudio-Releases

Release archives and the app list for **AmiStudio**, a suite of apps for classic 68k Amigas (AmigaOS 3.x).
This repo holds no source code. Each app's source lives in its own private repo; finished `.lha` archives are
published here as GitHub Release assets, and `manifest.txt` says which version of each app is current.

The **AmiStudio** launcher on the Amiga reads `manifest.txt`, shows every app as an icon (grey = not installed,
thin **Update** button = newer version available) and installs, updates and rolls back apps from the releases below.

## Apps

| App | id | Status |
|---|---|---|
| AmiStudio (launcher) | `launcher` | [0.1.17 beta](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/launcher-v0.1.17) ([AmiStudio-0.1.17.lha](https://github.com/hardcopi/AmiStudio-Releases/releases/download/launcher-v0.1.17/AmiStudio-0.1.17.lha)): one program for 68020-68060 with FPU (MUI required; small AmiStudio-020/-gadtools stubs only so 0.1.16 can update itself, removed by the next update); starts single-build apps such as AmiSurf 0.92 on 020/030 too, says when an FPU or MUI is missing, and removes an app's old -020/-gadtools programs and icons on update; 0.1.16: backdrop pictures checked on OS 3.1 datatypes with broken and bogus IFF/PNG files (no crash), clearer backdrop error messages (empty file, "Couldn't open" with the name; libamistudio 0.1.9); 0.1.15 was the AmiKit text fix: clean character counts for Text()/TextLength()/TextFit() (no freeze or Guru with AfA_OS antialiased text; libamistudio 0.1.6); 0.1.14 added AmiGrid to the grid with its own icon (beta apps on); 0.1.13 was the stack fix: always runs on at least 64 KB of stack, also from a Shell with the 4 KB default (no more MUI stack warning); 0.1.12 was the Host restart fix: when apps still use the old Host it offers "Restart it now anyway" (run-host.sh --restart) and checks that the installed Host answers; 0.1.11 was a clean-up release (ReadMe, unused icons, GPL v3 COPYING); since 0.1.10 it checks the AmiStudio Host and offers its update (Check for updates, and apps with `min_host` such as AmiDrive), then restarts the Host, also one from AmiSurf's AmiKit edition; Google Drive with AmiDrive since 0.1.9 (needs Host 0.1.8) |
| AmiPaint (formerly Paint) | `amipaint` (was `paint`) | [1.0.68 beta](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/amipaint-v1.0.68) ([AmiPaint-1.0.68.lha](https://github.com/hardcopi/AmiStudio-Releases/releases/download/amipaint-v1.0.68/AmiPaint-1.0.68.lha)): single 68020+FPU MUI binary (AmiPaint only; GadTools/020 variants dropped); Ken's revised splash; Stack 4096 CLEAN_EXIT |
| AmiSurf | `amisurf` | [0.98 beta](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/amisurf-v0.98) ([AmiSurf-0.98.lha](https://github.com/hardcopi/AmiStudio-Releases/releases/download/amisurf-v0.98/AmiSurf-0.98.lha), AmiKit edition [AmiSurf-0.98-AmiKit.lha](https://github.com/hardcopi/AmiStudio-Releases/releases/download/amisurf-v0.98/AmiSurf-0.98-AmiKit.lha) with Host 0.1.7 + the 0.97 engine, ~249 MB): pages show much faster on slow and emulated Amigas (AmiKit/Amiberry 68040, 1712x772 page, Host 0.1.12: about 0.5-0.75 s per whole page instead of 2.5-3.3 s; scrolling about 11 frames a second instead of 0-1), with no Host or engine change; the page no longer changes height (780/772/780) after loading; the window popup menu has Snapshot/Unsnapshot (window IDs); iconify pauses frames and catches up when shown. Gated at Stack 4096 with and without a Host on 68040 RTG and 68030 AGA under MuForce (no hits), against Host 0.1.12, on a real-speed 68020+68882, and on AmiKit under Amiberry against the launcher-installed Host 0.1.12 (already running, and started by AmiSurf). 0.97: fixes "Waiting for first frame" on AmiKit under Amiberry (the Host sent the page, but Amiberry's network emulation did not report it, so AmiSurf never read it; it now checks the connection directly); sends the bookmarks bar state only to a 0.97+ engine, so Host 0.1.12's 0.90 engine gets nothing it does not know. Gated at Stack 4096 with and without a Host on 68040 RTG and 68030 AGA under MuForce (no hits), against Host 0.1.12, on a real-speed 68020+68882, and on AmiKit under Amiberry against the launcher-installed Host 0.1.12 (already running, and started by AmiSurf). 0.96: starts the launcher-installed AmiStudio Host itself on AmiKit when none runs (it retried for good when the launcher was closed or the Host had stopped); the log names the Host address source and whether a token is there. 0.95: hidden bookmarks can be shown again (Bookmarks menu, and per bookmark plus the whole bar on the Bookmarks page), a space of padding on bar buttons, pastes can no longer move or resize the Settings window, About says Chromium and explains its terms, new splash art by Ken (also on 256-colour Workbenches). Gated at Stack 4096 with and without a Host on 68040 RTG and 68030 AGA under MuForce (no hits), against Host 0.1.12, and on a real-speed 68020+68882. 0.94: no endless "Waiting for first frame..." when connected without a page picture (asks the engine again after 8 s, reconnects after 20 s, logs why); gated at Stack 4096 with and without a Host on 68040 RTG and 68030 AGA under MuForce (no hits), against Host 0.1.12, and on a real-speed 68020+68882. 0.93: no Guru on AGA when the start splash closes. 0.92: one program for 68020-68060 with FPU (MUI; needs mui=1), waits up to 20 s for a Host that is still starting |
| AmiDiscord | `amidiscord` | [0.0.7 beta](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/amidiscord-v0.0.7) ([AmiDiscord-0.0.7.lha](https://github.com/hardcopi/AmiStudio-Releases/releases/download/amidiscord-v0.0.7/AmiDiscord-0.0.7.lha)): suite single-build — one AmiDiscord binary (MUI, 68020 + hard FPU; -020/-040/gadtools builds dropped; no-FPU requester kept); since 0.0.6 About picture only when Icons/about.png is a valid PNG; since 0.0.5 AmiKit text fix; since 0.0.4 always ≥64 KB stack; self-contained drawer + AmiStudio Prefs when launched (needs AmiStudio Host 0.1.4+, Host service `amidiscord`; tested with 0.1.12) |
| AmiDrive | `amidrive` | [0.1.3 beta](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/amidrive-v0.1.3) ([AmiDrive-0.1.3.lha](https://github.com/hardcopi/AmiStudio-Releases/releases/download/amidrive-v0.1.3/AmiDrive-0.1.3.lha)): Google Drive control panel; Open drawer works with Directory Opus Magellan (AmiKit), Workbench 3.5+, Scalos and C:WBRun/C:Open; sign-in in AmiSurf (with a Host that has AmiSurf sign-in; older Hosts use the PC's browser), says why when there is no Host and starts the Host on AmiKit (needs AmiStudio 0.1.9 and AmiStudio Host 0.1.8+, Host service `amidrive`) |
| AmiWrite | `amiwrite` | [0.1.5 beta](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/amiwrite-v0.1.5) ([AmiWrite-0.1.5.lha](https://github.com/hardcopi/AmiStudio-Releases/releases/download/amiwrite-v0.1.5/AmiWrite-0.1.5.lha), ~2.4 MB with the bundled fonts): word processor, based on WordCraft by the ArtCraft team; early beta: text editing, .txt and WordCraft's .wcraft.json, first formatting commands (Format/Insert/Paragraph/View menus, Font and Paragraph windows, bookmarks; View > Galley (fonts) shows the real fonts and sizes; no .docx, pages or printing yet); no icons yet (no .info files in the archive); OS 3.1+, 68020/030 or 68040/060 with FPU, MUI optional. 0.1.5: galley view with the bundled fonts (smoothed on RTG), View > Galley toggle, caret keys and scrolling by galley lines, colours and decorations; 0.1.4: fix for the freeze/crash when selecting text on AmiKit/AfA_OS antialiased text, fix for cursor trails on RTG with AAText, much faster typing, bundled fonts (Source Sans 3, Source Serif 4, Inter, JetBrains Mono, SIL OFL); 0.1.2: own 64 KB stack |
| AmiGrid | `amigrid` | [0.0.5 beta](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/amigrid-v0.0.5) ([AmiGrid-0.0.5.lha](https://github.com/hardcopi/AmiStudio-Releases/releases/download/amigrid-v0.0.5/AmiGrid-0.0.5.lha)): spreadsheet based on GridCraft; 0.0.5: saves .xlsx workbooks (every sheet, values, formulas with results, number formats and styles, column widths, row heights, merged ranges, hidden sheets, 1900/1904 dates; Save As .xlsx is the default for workbooks), .xlsx opens about 4x faster (1 MB/20,000 rows: about 40 s on a 68040, 80 s on a 68020), Amiga date-time and number fixes; not saved yet: charts, pictures, comments, hyperlinks, conditional formats, validation, protection, autofilters, tables, print areas. 0.0.4: opens .xlsx workbooks with a Sheet menu; 0.0.3: 254 functions, number formats and a Format menu; 0.0.2: formulas with recalculation; 0.0.1: first beta, grid and CSV open/save. Next: Excel-style ribbon |
| AmiStudio Host (PC component, not for the Amiga) | `host` | [0.1.14 beta](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/host-v0.1.14) ([amistudio-host-0.1.14-linux-x86_64.tar.gz](https://github.com/hardcopi/AmiStudio-Releases/releases/download/host-v0.1.14/amistudio-host-0.1.14-linux-x86_64.tar.gz)), Linux x86_64, includes the AmiSurf 1.03 Chromium browser engine (seeds default bookmarks when bookmarks.tsv is missing or empty on a prior config; engine says "connected (engine 1.03)" on connect; since 0.1.13 Manage Bookmarks/History keep Edit/Hide/Delete on screen with long addresses and Bookmarks page show/hide on the bar), AmiDiscord app mode and rclone 1.75.2 for Google Drive (service `amidrive`; needs fuse3); Google sign-in in AmiSurf for AmiDrive 0.1.2+; Sign-in crash fix on Fedora 44 / Nobara since 0.1.10 (~263 MB); stops on request when AmiStudio 0.1.7+ quits |
| AmiStudio Host for macOS (alpha, not in the manifest) | `host` | [0.1.11 alpha 1](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/host-macos-v0.1.11-alpha.1): Apple Silicon, Intel and universal tarballs for Amiberry / AmiKit on a Mac; AmiSurf engine and AmiDiscord, no Google Drive yet; manual install (`sh run-host.sh`), not yet tested on a real Mac |
| AmiStudio Host for Raspberry Pi / Linux ARM64 (alpha, not in the manifest) | `host` | [0.1.12 alpha 1](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/host-linux-arm64-v0.1.12-alpha.1) ([amistudio-host-0.1.12-linux-arm64.tar.gz](https://github.com/hardcopi/AmiStudio-Releases/releases/download/host-linux-arm64-v0.1.12-alpha.1/amistudio-host-0.1.12-linux-arm64.tar.gz)): Raspberry Pi 5 on 64-bit Raspberry Pi OS; AmiSurf 0.90 engine (headless, no display needed), AmiDiscord and rclone 1.75.2 for Google Drive (needs fuse3); service capped at MemoryMax 2G; manual install (`sh run-host.sh` or `install-user.sh`), built from AmiStudio-Host PR #2, not yet tested on a real Pi (~246 MB) |

The suite name stays **AmiStudio**. App display names are AmiPaint, AmiSurf, AmiDiscord, AmiDrive and AmiWrite (AmiPaint and AmiSurf were
formerly Paint / AmiStudio Paint and AmiStudio Browser). Matrix Chat (formerly AmiStudio Chat, release `matrixchat-v0.1`) is
superseded by AmiDiscord and no longer listed; its release stays for reference.

**No apps hidden (as of 25 Oct 2026):** every suite app is listed in `manifest.txt` again (AmiWrite on 24 Oct; AmiDrive and AmiGrid on 25 Oct, full production). `manifest-hidden.txt` is gone while empty. To hide an app later, move its block there and run `python3 tools/amsrel.py json`.

"Coming soon" entries are placeholders: the launcher lists them as grey icons and does not offer to install them
until a release is published.

## Downloads

Everything is under [Releases](https://github.com/hardcopi/AmiStudio-Releases/releases). GitHub's "Latest" badge
does not mean much here, because several apps share this repo: **`manifest.txt` decides what is current.**

To install by hand, unpack an archive anywhere with `lha x <App>-<ver>.lha` and open the drawer. Every archive
contains `<App>.info` and the `<App>/` drawer at its top level (AmiWrite 0.1.x has no icons yet, so only the drawer).

## Tags and asset names

- One GitHub Release per app version. Tag `<app>-v<ver>`, all lower case:
  `amipaint-v1.0.63`, `amisurf-v0.79`, `matrixchat-v0.2`, `launcher-v0.1.1`, `host-v0.1`.
- Release title is the display name plus version (`AmiPaint 1.0.63`, `AmiSurf 0.79`, `Matrix Chat 0.2`); the body is
  that version's CHANGES section.
- Assets:
  - Amiga archive `<Drawer>-<ver>.lha`, packed with `jlha c1q`:
    - AmiPaint: `AmiPaint-<ver>.lha` (id `amipaint`; 1.0.63 was first released as `Paint-1.0.63.lha` under id `paint`,
      tag `paint-v1.0.63`, kept on GitHub but no longer in the manifest)
    - AmiSurf: `AmiSurf-<ver>.lha`
    - AmiDiscord: `AmiDiscord-<ver>.lha`
    - AmiDrive: `AmiDrive-<ver>.lha`
    - AmiWrite: `AmiWrite-<ver>.lha`
    - Matrix Chat: `MatrixChat-<ver>.lha`
    - Launcher: `AmiStudio-<ver>.lha`
  - Optional variants `<Drawer>-<ver>-<Variant>.lha` (AmiSurf's `-AmiKit` build).
  - Host parts: `amistudio-host-<ver>-linux-x86_64.tar.gz`, `amistudio-host-<ver>-macos-{arm64,x86_64,universal}.tar.gz` (alpha, tag `host-macos-v<ver>-alpha.N`, not in the manifest yet), `amistudio-host-<ver>-linux-arm64.tar.gz` (Raspberry Pi alpha, tag `host-linux-arm64-v<ver>-alpha.N`, not in the manifest yet; later `-windows-x64.zip`).
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

app amipaint              # starts a block; a blank line ends it
name AmiPaint
desc Photoshop-class paint program (PhotoCraft based)
ver 1.0.63
date 2026-10-17
tag amipaint-v1.0.63
file AmiPaint-1.0.63.lha
size 1834212              # bytes; checked before unpacking
sha256 9f2c...e1          # 64 hex digits; checked before unpacking
drawer AmiPaint           # top-level drawer in the archive
exe AmiPaint              # the one 68020+FPU MUI build; launchers before 0.1.17 (and older apps) also use exe-020 / exe-gadtools
needs os=3.1 cpu=68020 fpu=1 mui=1 rtg=opt   # single build (22.10.2026): MUI required; publish.sh writes this, --needs overrides
host none                 # or the AmiStudio Host service the app needs (browser, pdf, ...)
icon Icons/about.png      # path inside the drawer, used for the icon grid
min_launcher 0.1.1
notes https://github.com/hardcopi/AmiStudio-Releases/releases/tag/amipaint-v1.0.63
```

Other keys:
- `channel beta` marks a beta. Launchers only show it with `BETA=ON` (pre-1.0; after 1.0 a separate AmiStudio Beta
  launcher reads betas).
- `min_host <ver>` (e.g. `min_host 0.1.8` for AmiDrive, whose `amidrive` service came with Host 0.1.8): the oldest
  AmiStudio Host the app works with. When such an app is installed, updated or started and the Host installed in
  AmiStudio/Host or the Host that answers is older, the launcher offers "Update the AmiStudio Host now" (download,
  then the old Host is restarted). Launchers before this key ignore it, like any unknown key.
- `variant <name> <file> <size> <sha256>` lists an extra archive on the same release (e.g. `amikit`).
- `status soon` marks a **placeholder**: an announced app with no release yet. A block with neither `ver` nor `file`
  is also a placeholder. Launchers from 0.1.1 show it as a grey "coming soon" icon and never try to download it.
  When the first release is published, `tools/publish.sh` removes `status soon` and fills in the release keys.

**PC components** (the AmiStudio Host) use a `component` block instead of `app`, always after the app blocks and
after a blank line. Launchers skip these blocks (0.1.1-0.1.3 read them as ignored global lines), so the Amiga never
shows or downloads them; the Host reads its own block for its update check.
```
component host
name AmiStudio Host
ver 0.1.1
tag host-v0.1.1
file amistudio-host-0.1.1-linux-x86_64.tar.gz   # amistudio-<id>-<ver>-<platform>.tar.gz (.zip for windows-*)
size ...
sha256 ...
channel beta
platform linux-x86_64     # required for components
```
A component has no `drawer`, `exe`, `needs`, `icon`, `min_launcher` or `min_host`. Publish one with
`tools/publish.sh host 0.1.2 amistudio-host-0.1.2-linux-x86_64.tar.gz --component --platform linux-x86_64 --beta`
(`--new-app` the first time).

`manifest.json` holds the same data for the Host and for desktop tools. It is generated from `manifest.txt` by
`tools/mkmanifest.sh`; never edit it by hand.

## Publishing (app bots, only when Rich asks)

Nothing is published without Rich's OK. Until then app bots keep building into their own `dist/`.

1. Build and pack as usual (`jlha c1q`), so you have `dist/<Drawer>-<ver>.lha` with a correct
   `$VER: <Exe> <ver> (dd.mm.yyyy)` in every binary.
2. Dry run in a checkout of this repo (prints the release, SHA256SUMS and the new manifest block; changes nothing):

       tools/publish.sh amipaint 1.0.64 /workspace/release/AmiPaint-1.0.64.lha --notes /tmp/changes-1.0.64.txt

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

The AmiStudio suite is licensed under the **GNU General Public License v3.0**
(decision 19 October 2026). Source repositories are being prepared for public release;
until then, source is available on request. Each archive still carries its own ReadMe
and ATTRIBUTIONS for third-party components.
