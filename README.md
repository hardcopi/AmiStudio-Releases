# AmiStudio-Releases

Release archives and the app list for **AmiStudio**, a suite of apps for classic 68k Amigas (AmigaOS 3.x).
This repo holds no source code. Each app's source lives in its own private repo; finished `.lha` archives are
published here as GitHub Release assets, and `manifest.txt` says which version of each app is current.

The **AmiStudio** launcher on the Amiga reads `manifest.txt`, shows every app as an icon (grey = not installed,
thin **Update** button = newer version available) and installs, updates and rolls back apps from the releases below.

## Apps

| App | id | Status |
|---|---|---|
| AmiStudio (launcher) | `launcher` | [0.1.10 beta](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/launcher-v0.1.10) ([AmiStudio-0.1.10.lha](https://github.com/hardcopi/AmiStudio-Releases/releases/download/launcher-v0.1.10/AmiStudio-0.1.10.lha)): checks the AmiStudio Host and offers its update (Check for updates, and apps with `min_host` such as AmiDrive), then restarts the Host, also one from AmiSurf's AmiKit edition; Google Drive with AmiDrive since 0.1.9 (needs Host 0.1.8) |
| AmiPaint (formerly Paint) | `amipaint` (was `paint`) | 1.0.66 beta |
| AmiSurf | `amisurf` | 0.87 beta |
| AmiDiscord | `amidiscord` | 0.0.3 beta (needs AmiStudio Host 0.1.4+, Host service `amidiscord`) |
| AmiDrive | `amidrive` | [0.1.2 beta](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/amidrive-v0.1.2) ([AmiDrive-0.1.2.lha](https://github.com/hardcopi/AmiStudio-Releases/releases/download/amidrive-v0.1.2/AmiDrive-0.1.2.lha)): Google Drive control panel; sign-in in AmiSurf (needs a Host with AmiSurf sign-in, not yet released, and the OAuth redirect fix; older Hosts use the PC's browser), says why when there is no Host and starts the Host on AmiKit (needs AmiStudio 0.1.9 and AmiStudio Host 0.1.8+, Host service `amidrive`) |
| AmiStudio Host (PC component, not for the Amiga) | `host` | [0.1.8 beta](https://github.com/hardcopi/AmiStudio-Releases/releases/tag/host-v0.1.8) ([amistudio-host-0.1.8-linux-x86_64.tar.gz](https://github.com/hardcopi/AmiStudio-Releases/releases/download/host-v0.1.8/amistudio-host-0.1.8-linux-x86_64.tar.gz)), Linux x86_64, includes the AmiSurf 0.85 Chromium browser engine, AmiDiscord app mode and rclone 1.75.2 for Google Drive (service `amidrive`; needs fuse3) (~263 MB); stops on request when AmiStudio 0.1.7+ quits |

The suite name stays **AmiStudio**. App display names are AmiPaint, AmiSurf, AmiDiscord and AmiDrive (AmiPaint and AmiSurf were
formerly Paint / AmiStudio Paint and AmiStudio Browser). Matrix Chat (formerly AmiStudio Chat, release `matrixchat-v0.1`) is
superseded by AmiDiscord and no longer listed; its release stays for reference.

"Coming soon" entries are placeholders: the launcher lists them as grey icons and does not offer to install them
until a release is published.

## Downloads

Everything is under [Releases](https://github.com/hardcopi/AmiStudio-Releases/releases). GitHub's "Latest" badge
does not mean much here, because several apps share this repo: **`manifest.txt` decides what is current.**

To install by hand, unpack an archive anywhere with `lha x <App>-<ver>.lha` and open the drawer. Every archive
contains `<App>.info` and the `<App>/` drawer at its top level.

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
exe AmiPaint              # 040 MUI build; the launcher picks exe-020 / exe-gadtools for the machine
needs os=3.1 cpu=68020 fpu=1 mui=opt rtg=opt
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
