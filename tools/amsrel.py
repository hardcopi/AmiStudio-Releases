#!/usr/bin/env python3
"""AmiStudio-Releases helper: parse/check manifest.txt, write manifest.json, publish a release.

  amsrel.py json      [--repo-dir DIR]                 regenerate manifest.json from manifest.txt
  amsrel.py check     [--remote] [--sha] [--app ID]    validate manifest.txt (and the release assets on GitHub)
  amsrel.py publish   APP VER FILE.lha [options]       app bots: dry run unless --publish (needs Rich's OK)
  amsrel.py unhide    ID... | --all                    move hidden app blocks from manifest-hidden.txt back into manifest.txt
  amsrel.py publish   host VER amistudio-host-VER-linux-x86_64.tar.gz --component --platform linux-x86_64 ...

The format is documented in README.md ("manifest.txt"). Python 3.8+, no third-party modules.
Publishing uses the GitHub CLI (`gh`), logged in as an account that may push to hardcopi/AmiStudio-Releases.
"""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile, urllib.request, urllib.error

REPO = "hardcopi/AmiStudio-Releases"
DL = "https://github.com/%s/releases/download" % REPO
NOTES = "https://github.com/%s/releases/tag" % REPO
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYORDER = ["name", "desc", "ver", "date", "tag", "file", "size", "sha256", "channel", "status", "drawer", "exe",
            "needs", "host", "platform", "icon", "min_launcher", "min_host", "notes", "variant"]
MAXBYTES = 32 * 1024

class Bad(Exception): pass

def die(msg): print("amsrel: " + msg, file=sys.stderr); sys.exit(1)

def cap(app): return app[:1].upper() + app[1:]

# Suite stays AmiStudio; apps: AmiPaint, AmiSurf, Matrix Chat, AmiDiscord, AmiDrive, AmiWrite.
# ids: amipaint, amisurf, matrixchat (legacy ids paint/browser/chat still recognised).
# Archives: AmiPaint-<ver>.lha, AmiSurf-<ver>.lha,
# MatrixChat-<ver>.lha; launcher AmiStudio-<ver>.lha.
DISPLAY = {
    "launcher": "AmiStudio",
    "amipaint": "AmiPaint",
    "paint": "Paint",           # legacy id (renamed to amipaint)
    "amisurf": "AmiSurf",
    "matrixchat": "Matrix Chat",
    "amidiscord": "AmiDiscord",
    "amidrive": "AmiDrive",
    "amiwrite": "AmiWrite",
    "amigrid": "AmiGrid",
    "browser": "AmiSurf",       # legacy id
    "chat": "Matrix Chat",      # legacy id
    "host": "AmiStudio Host",   # PC component (component block)
}
DRAWER = {
    "launcher": "AmiStudio",
    "amipaint": "AmiPaint",
    "paint": "Paint",           # legacy id / old drawer
    "amisurf": "AmiSurf",
    "matrixchat": "MatrixChat",
    "amidiscord": "AmiDiscord",
    "amidrive": "AmiDrive",
    "amiwrite": "AmiWrite",
    "amigrid": "AmiGrid",
    "browser": "AmiStudioBrowser",  # legacy id / old drawer
    "chat": "AmiStudioChat",
}

def display_name(app):
    return DISPLAY.get(app, "AmiStudio " + cap(app))

def drawer_for(app):
    return DRAWER.get(app, "AmiStudio" + cap(app))

def asset_name(app, ver):
    return "%s-%s.lha" % (drawer_for(app), ver)

# PC-side parts (the AmiStudio Host) are "component" blocks: same keys as an app plus "platform", no Amiga keys.
# Launchers up to 0.1.3 treat a block that does not start with "app" as ignored global lines, so they never show
# or download a component (this needs the blank line before "component", which render() always writes).
def is_component(a): return a.get("_kind") == "component"
def component_asset(cid, ver, platform):
    return "amistudio-%s-%s-%s.%s" % (cid, ver, platform, "zip" if platform.startswith("windows") else "tar.gz")

def ver_key(v):
    """same order as the launcher's ver_cmp: numeric parts, a text suffix (b2, beta) sorts before the release"""
    out = []
    for part in v.split("."):
        m = re.match(r"(\d*)(.*)", part)
        out.append((int(m.group(1) or 0), (0, m.group(2)) if m.group(2) else (1, "")))
    while out and out[-1] == (0, (1, "")): out.pop()
    return out

# ---------- parse / write ----------
def parse(text):
    """returns (globals: list of (k, v, comment-lines)), header comment lines, apps: list of dict with '_order')"""
    head, glob, apps, cur = [], {}, [], None
    for raw in text.split("\n"):
        line = raw.rstrip("\r")
        s = line
        for i, ch in enumerate(s):   # '#' starts a comment at line start or after whitespace (URLs may carry '#')
            if ch == "#" and (i == 0 or s[i-1] in " \t"): s = s[:i]; break
        s = s.strip()
        if not s:
            if cur is None and not glob and line.startswith("#"): head.append(line)
            continue
        k, _, v = s.partition(" ")
        k, v = k.strip(), v.strip()
        if k in ("app", "component"):
            cur = {"id": v, "_kind": k, "_order": [], "variant": []}; apps.append(cur); continue
        if cur is None: glob[k] = v; continue
        if k == "variant": cur["variant"].append(v)
        else: cur[k] = v
        cur["_order"].append(k)
    return head, glob, apps

def is_placeholder(a): return a.get("status") == "soon" or (not a.get("ver") and not a.get("file"))

def render(head, glob, apps):
    out = list(head) or ["# AmiStudio manifest (format 1). See README.md."]
    for k in ("format", "updated", "launcher_min"):
        if k in glob: out.append("%s %s" % (k, glob[k]))
    for k, v in glob.items():
        if k not in ("format", "updated", "launcher_min"): out.append("%s %s" % (k, v))
    for a in [x for x in apps if not is_component(x)] + [x for x in apps if is_component(x)]:   # components last
        out.append(""); out.append("%s %s" % ("component" if is_component(a) else "app", a["id"]))
        keys = [k for k in KEYORDER if k in a] + [k for k in a if k not in KEYORDER and not k.startswith("_") and k != "id"]
        for k in keys:
            if k == "variant":
                for v in a["variant"]: out.append("variant " + v)
            elif a[k] != "": out.append("%s %s" % (k, a[k]))
    return "\n".join(out) + "\n"

def to_json(glob, apps):
    j = {"format": int(glob.get("format", 0)), "updated": glob.get("updated", ""), "launcher_min": glob.get("launcher_min", ""),
         "generated_from": "manifest.txt", "apps": []}
    for a in apps:
        e = {"id": a["id"], "kind": "component" if is_component(a) else "app", "placeholder": is_placeholder(a)}
        for k in KEYORDER:
            if k in ("variant",) or k not in a: continue
            e[k] = int(a[k]) if k == "size" else a[k]
        if "needs" in a:
            e["needs"] = dict(p.split("=", 1) for p in a["needs"].split() if "=" in p)
        if not e["placeholder"]:
            e["url"] = "%s/%s/%s" % (DL, a["tag"], a["file"])
        e["variants"] = []
        for v in a["variant"]:
            f = v.split()
            if len(f) >= 4: e["variants"].append({"name": f[0], "file": f[1], "size": int(f[2]), "sha256": f[3].lower(),
                                                  "url": "%s/%s/%s" % (DL, a.get("tag", ""), f[1])})
        j["apps"].append(e)
    return json.dumps(j, indent=2) + "\n"

# ---------- checks ----------
SAFE = re.compile(r"^[A-Za-z0-9._+-]+$")
def check(text, glob, apps, remote=False, sha=False, only=None):
    errs, warns = [], []
    if len(text.encode()) > MAXBYTES: errs.append("manifest.txt is over 32 KB (the launcher reads at most 32 KB)")
    try: text.encode("ascii")
    except UnicodeEncodeError: errs.append("manifest.txt must be plain ASCII")
    if "\r" in text: errs.append("manifest.txt must use LF line endings")
    if glob.get("format") != "1": errs.append("first global line must be 'format 1'")
    if not re.match(r"^\d{4}-\d\d-\d\d$", glob.get("updated", "")): errs.append("'updated YYYY-MM-DD' missing")
    seen = set()
    for a in apps:
        i = a["id"]; where = "app %s: " % i
        if not re.match(r"^[a-z][a-z0-9-]{0,22}$", i): errs.append(where + "id must be lower case a-z0-9-, max 23 chars")
        if i in seen: errs.append(where + "listed twice"); seen.add(i)
        seen.add(i)
        for k, n in (("name", 63), ("desc", 159), ("drawer", 47), ("exe", 47), ("needs", 95), ("icon", 95), ("notes", 199), ("file", 95), ("tag", 47), ("min_host", 15)):
            if len(a.get(k, "")) > n: errs.append(where + "%s longer than %d chars (launcher field size)" % (k, n))
        for k in ("drawer", "exe", "file"):
            v = a.get(k, "")
            if v and (not SAFE.match(v) or v == ".."): errs.append(where + "%s '%s' has unsafe characters" % (k, v))
        if is_component(a):
            if a.get("platform") is None or not re.match(r"^[a-z0-9_]+-[a-z0-9_]+$", a.get("platform", "")): errs.append(where + "component needs 'platform OS-ARCH' (linux-x86_64)")
            for k in ("drawer", "exe", "icon", "needs", "min_launcher", "min_host", "format", "updated", "launcher_min"):
                if k in a: errs.append(where + "component must not have '%s'" % k)
        elif a.get("drawer", drawer_for(i)) != drawer_for(i): warns.append(where + "drawer is not the suite name %s" % drawer_for(i))
        if is_placeholder(a):
            for k in ("file", "size", "sha256", "tag"):
                if a.get(k): warns.append(where + "placeholder has '%s' (ignored by the launcher)" % k)
            continue
        for k in ("ver", "file", "size", "sha256", "tag"):
            if not a.get(k): errs.append(where + "missing '%s'" % k)
        if a.get("tag") and a.get("ver") and a["tag"] != "%s-v%s" % (i, a["ver"]): errs.append(where + "tag must be %s-v%s" % (i, a["ver"]))
        want = component_asset(i, a["ver"], a.get("platform", "")) if is_component(a) and a.get("ver") else asset_name(i, a.get("ver", ""))
        if a.get("file") and a.get("ver") and a["file"] != want: (errs if is_component(a) else warns).append(where + "file %s %s" % ("must be" if is_component(a) else "is usually", want))
        if a.get("sha256") and not re.match(r"^[0-9a-fA-F]{64}$", a["sha256"]): errs.append(where + "sha256 must be 64 hex digits")
        if a.get("size") and not a["size"].isdigit(): errs.append(where + "size must be a byte count")
        if remote and (only is None or only == i) and a.get("tag") and a.get("file"):
            assets = [(a["file"], a.get("size"), a.get("sha256"))] + [tuple(v.split()[1:4]) for v in a["variant"] if len(v.split()) >= 4]
            for f, size, h in assets:
                url = "%s/%s/%s" % (DL, a["tag"], f)
                try:
                    got_size, got_sha = fetch_info(url, sha)
                    if size and got_size is not None and str(got_size) != str(size): errs.append(where + "%s is %s bytes on GitHub, manifest says %s" % (f, got_size, size))
                    if sha and h and got_sha != h.lower(): errs.append(where + "%s sha256 on GitHub is %s, manifest says %s" % (f, got_sha, h))
                    print("ok   %s (%s bytes%s)" % (url, got_size, ", sha256 matches" if sha else ""))
                except Exception as e: errs.append(where + "cannot fetch %s: %s" % (url, e))
    return errs, warns

def fetch_info(url, want_sha):
    req = urllib.request.Request(url, method="GET" if want_sha else "HEAD", headers={"User-Agent": "amsrel/1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        size = r.headers.get("Content-Length")
        if not want_sha: return (int(size) if size else None), None
        h, n = hashlib.sha256(), 0
        while True:
            b = r.read(65536)
            if not b: break
            h.update(b); n += len(b)
        return n, h.hexdigest()

def load(d):
    p = os.path.join(d, "manifest.txt")
    with open(p, newline="") as f: text = f.read()
    return text, parse(text)

def write_all(d, head, glob, apps):
    txt = render(head, glob, apps)
    errs, _ = check(txt, glob, apps)
    if errs: raise Bad("; ".join(errs))
    with open(os.path.join(d, "manifest.txt"), "w", newline="\n") as f: f.write(txt)
    with open(os.path.join(d, "manifest.json"), "w", newline="\n") as f: f.write(to_json(glob, apps))
    return txt

# ---------- hidden apps (manifest-hidden.txt) ----------
# Rich, 23 Oct 2026: "Hide AmiWord, AmiGrid and AmiDrive from the menu for now." Hidden app blocks live, unchanged, in
# manifest-hidden.txt (same format, never read by the launcher). publish refuses them; "unhide" moves them back.
HIDDEN = "manifest-hidden.txt"
def load_hidden(d):
    p = os.path.join(d, HIDDEN)
    if not os.path.exists(p): return None, [], []
    with open(p, newline="") as f: text = f.read()
    head, _, apps = parse(text)
    return text, head, apps

def cmd_unhide(o):
    d = o.repo_dir
    htext, hhead, happs = load_hidden(d)
    if htext is None: die("no %s" % HIDDEN)
    ids = [a["id"] for a in happs] if o.all else o.ids
    if not ids: die("name the apps to unhide (or --all)")
    text, (head, glob, apps) = load(d)
    for i in ids:
        a = next((x for x in happs if x["id"] == i), None)
        if a is None: die("%s is not in %s" % (i, HIDDEN))
        if any(x["id"] == i for x in apps): die("%s is already in manifest.txt" % i)
        at = next((k for k, x in enumerate(apps) if is_component(x)), len(apps))   # apps before components, as render() writes
        apps.insert(at, a); happs.remove(a)
    if not happs: head = [l for l in head if not l.startswith(("# Hidden for now (Rich", "# restore with: python3 tools/amsrel.py unhide"))]
    write_all(d, head, glob, apps)
    # keep the hidden file's own header; drop the moved blocks (or the whole file when it is empty)
    blocks = [b for b in htext.split("\n\n") if not any(b.startswith("app %s\n" % i) for i in ids)]
    rest = "\n\n".join(blocks).rstrip("\n") + "\n"
    if happs: open(os.path.join(d, HIDDEN), "w", newline="\n").write(rest)
    else: os.remove(os.path.join(d, HIDDEN))
    print("unhidden: %s. Commit manifest.txt, manifest.json and %s, then push; the launcher lists them on its next check." % (", ".join(ids), HIDDEN))

# ---------- commands ----------
def cmd_json(o):
    text, (head, glob, apps) = load(o.repo_dir)
    errs, warns = check(text, glob, apps)
    for w in warns: print("warn " + w)
    if errs: die("manifest.txt has errors:\n  " + "\n  ".join(errs))
    with open(os.path.join(o.repo_dir, "manifest.json"), "w", newline="\n") as f: f.write(to_json(glob, apps))
    n = sum(1 for a in apps if not is_placeholder(a))
    print("manifest.json: %d apps (%d released, %d placeholders)" % (len(apps), n, len(apps) - n))

def cmd_check(o):
    text, (head, glob, apps) = load(o.repo_dir)
    errs, warns = check(text, glob, apps, remote=o.remote, sha=o.sha, only=o.app)
    jp = os.path.join(o.repo_dir, "manifest.json")
    if os.path.exists(jp) and open(jp).read() != to_json(glob, apps): errs.append("manifest.json is out of date: run tools/mkmanifest.sh")
    for h in load_hidden(o.repo_dir)[2]:
        if any(a["id"] == h["id"] for a in apps): errs.append("app %s is in both manifest.txt and %s" % (h["id"], HIDDEN))
        else: print("hidden %s %s (%s)" % (h["id"], h.get("ver", ""), HIDDEN))
    for w in warns: print("warn " + w)
    for e in errs: print("FAIL " + e)
    print("%s: %d apps, %d error(s), %d warning(s)" % ("ok" if not errs else "FAILED", len(apps), len(errs), len(warns)))
    sys.exit(1 if errs else 0)

def sh(args, **kw):
    print("  $ " + " ".join(args)); return subprocess.run(args, check=True, **kw)

# One build per app since 22.10.2026 (Rich: "Drop 040 and Gadtools versions. You can drop the 020 name. Require an
# FPU though."): <exe> is a 68020 + hard FPU MUI program. Every app release writes that needs line; other keys an app
# had (rtg=opt for AmiPaint, a newer os=) are kept. --needs "..." overrides it.
SINGLE_BUILD = (("os", "3.1"), ("cpu", "68020"), ("fpu", "1"), ("mui", "1"))
def single_build_needs(old):
    have = [p.split("=", 1) for p in (old or "").split() if "=" in p]
    d = dict(have); out = []
    for k, v in SINGLE_BUILD:
        if k == "os" and d.get("os"): v = d["os"]
        out.append("%s=%s" % (k, v))
    out += ["%s=%s" % (k, v) for k, v in have if k not in dict(SINGLE_BUILD)]
    return " ".join(out)

def cmd_publish(o):
    d = o.repo_dir; app, ver = o.app, o.ver
    if not re.match(r"^[a-z][a-z0-9-]*$", app): die("app id must be lower case")
    if not re.match(r"^\d+(\.\d+)*[a-z0-9]*$", ver): die("version looks wrong: %s" % ver)
    files = [o.file] + [v[1] for v in o.variant] + o.extra
    for f in files:
        if not os.path.isfile(f): die("no such file: %s" % f)
    text, (head, glob, apps) = load(d)
    if any(x["id"] == app for x in load_hidden(d)[2]):
        die("%s is hidden from the launcher (Rich, 23 Oct 2026; see %s). Ask Rich before publishing it; to list it\n"
            "again run: python3 tools/amsrel.py unhide %s (then commit and push), and publish after that." % (app, HIDDEN, app))
    a = next((x for x in apps if x["id"] == app), None)
    comp = o.component or (a is not None and is_component(a))
    if a is not None and o.component and not is_component(a): die("%s is an app block, not a component" % app)
    if comp:
        platform = o.platform or (a or {}).get("platform")
        if not platform: die("a component needs --platform (e.g. linux-x86_64)")
        want = component_asset(app, ver, platform)
    else: want = asset_name(app, ver)
    if os.path.basename(o.file) != want: die("main %s must be named %s (got %s)" % ("file" if comp else "archive", want, os.path.basename(o.file)))
    if a is None and comp:
        if not o.new_app: die("component '%s' is not in manifest.txt; pass --new-app to add it" % app)
        a = {"id": app, "_kind": "component", "_order": [], "variant": [], "name": display_name(app), "desc": o.desc or display_name(app), "platform": platform}
        apps.append(a)
    if a is None:
        if not o.new_app: die("app '%s' is not in manifest.txt; add a placeholder block first (or pass --new-app)" % app)
        a = {"id": app, "_order": [], "variant": [], "name": display_name(app), "drawer": drawer_for(app), "exe": drawer_for(app),
             "needs": single_build_needs(""), "host": "none", "icon": "Icons/about.png", "min_launcher": glob.get("launcher_min", "0.1.1")}
        apps.append(a)
    if not is_placeholder(a) and ver_key(ver) <= ver_key(a["ver"]) and not o.allow_same:
        die("%s %s is not newer than the listed %s" % (app, ver, a["ver"]))
    def sha(f):
        h = hashlib.sha256()
        with open(f, "rb") as fh:
            for b in iter(lambda: fh.read(65536), b""): h.update(b)
        return h.hexdigest()
    import datetime
    tag = "%s-v%s" % (app, ver)
    a.pop("status", None)
    if comp: a["platform"] = platform
    else: a["needs"] = o.needs if o.needs else single_build_needs(a.get("needs", ""))   # MUI required, no GadTools build
    if o.desc: a["desc"] = o.desc
    a.update({"ver": ver, "date": o.date or datetime.date.today().isoformat(), "tag": tag, "file": want,
              "size": str(os.path.getsize(o.file)), "sha256": sha(o.file), "notes": "%s/%s" % (NOTES, tag)})
    if o.beta: a["channel"] = "beta"
    else: a.pop("channel", None)
    a["variant"] = ["%s %s %d %s" % (n, os.path.basename(f), os.path.getsize(f), sha(f)) for n, f in o.variant]
    glob["updated"] = a["date"] if a["date"] > glob.get("updated", "") else glob.get("updated", "")
    new_txt = render(head, glob, apps)
    errs, warns = check(new_txt, glob, apps)
    for w in warns: print("warn " + w)
    if errs: die("the new manifest would be invalid:\n  " + "\n  ".join(errs))
    sums = "".join("%s  %s\n" % (sha(f), os.path.basename(f)) for f in files)
    title = display_name(app) + " " + ver
    print("== %s %s -> %s" % (app, ver, tag))
    print("release title: %s%s" % (title, " (pre-release / beta)" if o.beta else ""))
    print("assets:\n" + "".join("  %s\n" % os.path.basename(f) for f in files) + "  SHA256SUMS")
    print("SHA256SUMS:\n" + sums)
    print("manifest block:\n" + "\n".join(l for l in new_txt.split("\n\n") if l.startswith("%s %s\n" % ("component" if comp else "app", app))) + "\n")
    if not o.publish:
        print("DRY RUN: nothing was created or pushed. Re-run with --publish once Rich has OK'd this release.")
        return
    # real publish
    st = subprocess.run(["git", "-C", d, "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    if st: die("the release repo checkout has local changes; commit or stash them first:\n" + st)
    sh(["git", "-C", d, "pull", "--ff-only", "-q"])
    if subprocess.run(["gh", "release", "view", tag, "--repo", REPO], capture_output=True).returncode == 0:
        die("release %s already exists on GitHub" % tag)
    with tempfile.TemporaryDirectory() as td:
        sp = os.path.join(td, "SHA256SUMS"); open(sp, "w").write(sums)
        np = os.path.join(td, "notes.md")
        notes = open(o.notes).read() if o.notes else "%s %s.\n" % (display_name(app), ver)
        how = ("This runs on the PC, not on the Amiga: unpack it and see README-HOST.md inside.\n" if comp else
               "Install with the AmiStudio launcher, or unpack the .lha anywhere and open the drawer.\n")
        open(np, "w").write(notes + "\n" + how + "SHA-256 sums are in SHA256SUMS.\n")
        args = ["gh", "release", "create", tag, "--repo", REPO, "--title", title, "--notes-file", np, "--target", "main"]
        if o.beta: args.append("--prerelease")
        args += ["--latest=false"]
        sh(args + files + [sp])
    # reload (pull may have changed it) and apply the same block
    text2, (head2, glob2, apps2) = load(d)
    for i, x in enumerate(apps2):
        if x["id"] == app: apps2[i] = a; break
    else: apps2.append(a)
    glob2["updated"] = max(glob2.get("updated", ""), a["date"])
    write_all(d, head2, glob2, apps2)
    errs, _ = check(render(head2, glob2, apps2), glob2, apps2, remote=True, sha=True, only=app)
    if errs: die("release created but the remote check failed, manifest NOT committed:\n  " + "\n  ".join(errs))
    sh(["git", "-C", d, "add", "manifest.txt", "manifest.json"])
    sh(["git", "-C", d, "commit", "-q", "-m", "%s %s%s" % (app, ver, " (beta)" if o.beta else "")])
    sh(["git", "-C", d, "push", "-q", "origin", "HEAD:main"])
    print("published %s; the launcher sees it on its next check." % tag)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo-dir", default=ROOT)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("json")
    c = sp.add_parser("check"); c.add_argument("--remote", action="store_true", help="check assets exist on GitHub with the listed size")
    c.add_argument("--sha", action="store_true", help="with --remote: download and compare sha256"); c.add_argument("--app")
    u = sp.add_parser("unhide"); u.add_argument("ids", nargs="*"); u.add_argument("--all", action="store_true")
    p = sp.add_parser("publish")
    p.add_argument("app"); p.add_argument("ver"); p.add_argument("file")
    p.add_argument("--variant", nargs=2, action="append", default=[], metavar=("NAME", "FILE"), help="e.g. --variant amikit AmiSurf-0.79-AmiKit.lha")
    p.add_argument("--extra", action="append", default=[], metavar="FILE", help="extra asset (Host tarball...), listed in SHA256SUMS only")
    p.add_argument("--beta", action="store_true", help="channel beta + GitHub pre-release")
    p.add_argument("--notes", metavar="FILE", help="release body (this version's CHANGES section)")
    p.add_argument("--component", action="store_true", help="a PC part (Host): 'component' block, file amistudio-ID-VER-PLATFORM.tar.gz")
    p.add_argument("--platform", help="component platform, e.g. linux-x86_64"); p.add_argument("--desc")
    p.add_argument("--needs", help='app needs line (default: the single-build "os=3.1 cpu=68020 fpu=1 mui=1", other keys kept)')
    p.add_argument("--date"); p.add_argument("--new-app", action="store_true"); p.add_argument("--allow-same", action="store_true")
    p.add_argument("--publish", action="store_true", help="really create the GitHub release and push the manifest (Rich's OK needed)")
    o = ap.parse_args()
    o.repo_dir = os.path.abspath(o.repo_dir)
    try: {"json": cmd_json, "check": cmd_check, "publish": cmd_publish, "unhide": cmd_unhide}[o.cmd](o)
    except Bad as e: die(str(e))
    except subprocess.CalledProcessError as e: die("command failed: %s" % e)

if __name__ == "__main__": main()
