#!/usr/bin/env python3
"""Checks for a published product, each one an acceptance item of its ACCEPTANCE.ilang.md.

    python products/check_product.py --dir products/<name> --iml [--codec DIR]
        <NAME>.iml is what the reference codec of IML compiles from <NAME>.ilang.md, and it decompiles back to
        <NAME>.ilang.md (MODULE::PRODUCT, PRODUCT-2). A document whose layout IML does not carry (blank lines)
        decompiles to the same lines without them; the check compares both files with blank lines removed and
        the compiled form byte for byte.
    python products/check_product.py --dir products/<name> --length MAX
        <NAME>.ilang.md holds at most MAX characters
    python products/check_product.py --dir products/<name> --site URL
        the file served at URL is byte-identical to <NAME>.ilang.md

The product directory holds exactly one *.ilang.md that is not ACCEPTANCE.ilang.md, and one *.iml beside it.
Exit code 0 when the check passes, 1 when it fails, 2 when it could not run. Standard library and git only.
Without --codec the codec is cloned at the pinned commit into a temporary directory and removed afterwards.
"""
import glob
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request

CODEC_REPO = "https://github.com/ilang-ai/iml-protocol.git"
CODEC_PIN = "3a545f13d069095d3ac257fdec50e3293f4373ee"  # iml-protocol, 0.5 stable (2026-09-29)


def files(d):
    ilang = [p for p in glob.glob(os.path.join(d, "*.ilang.md")) if os.path.basename(p) != "ACCEPTANCE.ilang.md"]
    iml = glob.glob(os.path.join(d, "*.iml"))
    if len(ilang) != 1 or len(iml) != 1:
        print("expected one product document and one IML file in %s, found %s and %s" % (d, ilang, iml))
        sys.exit(2)
    return os.path.abspath(ilang[0]), os.path.abspath(iml[0])


def read(path):
    with open(path, "rb") as f:
        return f.read().replace(b"\r\n", b"\n")


def no_blank(b):
    return b"\n".join(l for l in b.split(b"\n") if l.strip()) + b"\n"


def codec_run(codec, args, path):
    r = subprocess.run([sys.executable, "-m", "iml"] + args + [path], cwd=codec, capture_output=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr.decode("utf-8", "replace"))
        sys.exit(2)
    return r.stdout.replace(b"\r\n", b"\n")


def check_iml(d, codec):
    ilang, iml = files(d)
    tmp = None
    if codec is None:
        tmp = tempfile.mkdtemp(prefix="iml-codec-")
        codec = os.path.join(tmp, "iml-protocol")
        subprocess.run(["git", "clone", "-q", CODEC_REPO, codec], check=True)
        subprocess.run(["git", "-C", codec, "checkout", "-q", CODEC_PIN], check=True)
    try:
        head = subprocess.run(["git", "-C", codec, "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        if head != CODEC_PIN:
            print("codec is at %s, the pin is %s" % (head[:12], CODEC_PIN[:12]))
            return 2
        ok1 = codec_run(codec, ["compile", "--document"], ilang) == read(iml)
        print("compile %s == %s: %s" % (os.path.basename(ilang), os.path.basename(iml), "yes" if ok1 else "NO"))
        ok2 = no_blank(codec_run(codec, ["decompile"], iml)) == no_blank(read(ilang))
        print("decompile %s == %s (blank lines aside): %s" % (os.path.basename(iml), os.path.basename(ilang), "yes" if ok2 else "NO"))
        return 0 if ok1 and ok2 else 1
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def check_length(d, limit):
    ilang, _ = files(d)
    n = len(read(ilang).decode("utf-8"))
    print("%s: %d characters, limit %d" % (os.path.basename(ilang), n, limit))
    return 0 if n <= limit else 1


def check_site(d, url):
    ilang, _ = files(d)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ilang-spec products check)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        served = r.read().replace(b"\r\n", b"\n")
    a, b = hashlib.sha256(served).hexdigest(), hashlib.sha256(read(ilang)).hexdigest()
    print("served %s\nrepo   %s" % (a, b))
    return 0 if a == b else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--dir" not in args:
        print(__doc__)
        sys.exit(2)
    d = args[args.index("--dir") + 1]
    if "--iml" in args:
        codec = args[args.index("--codec") + 1] if "--codec" in args else None
        sys.exit(check_iml(d, codec))
    if "--length" in args:
        sys.exit(check_length(d, int(args[args.index("--length") + 1])))
    if "--site" in args:
        sys.exit(check_site(d, args[args.index("--site") + 1]))
    print(__doc__)
    sys.exit(2)
