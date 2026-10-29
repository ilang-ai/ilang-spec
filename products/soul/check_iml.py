#!/usr/bin/env python3
"""Checks for the published SOUL, each one an acceptance item of ACCEPTANCE.ilang.md.

    python products/soul/check_iml.py --iml [--codec DIR]   SOUL.iml is what the reference codec of IML compiles from
                                                             SOUL.ilang.md, and it decompiles back to SOUL.ilang.md,
                                                             byte for byte (MODULE::PRODUCT, PRODUCT-2)
    python products/soul/check_iml.py --length               SOUL.ilang.md holds at most MAX_CHARS characters, so it
                                                             fits one instruction field
    python products/soul/check_iml.py --site URL             the file served at URL is byte-identical to SOUL.ilang.md

Exit code 0 when the check passes, 1 when it fails, 2 when it could not run. Standard library and git only.
Without --codec the codec is cloned at the pinned commit into a temporary directory and removed afterwards.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ILANG = os.path.join(HERE, "SOUL.ilang.md")
IML = os.path.join(HERE, "SOUL.iml")
CODEC_REPO = "https://github.com/ilang-ai/iml-protocol.git"
CODEC_PIN = "3a545f13d069095d3ac257fdec50e3293f4373ee"  # iml-protocol, 0.5 stable (2026-09-29)
MAX_CHARS = 2000


def read(path):
    with open(path, "rb") as f:
        return f.read().replace(b"\r\n", b"\n")


def codec_run(codec, args, path):
    r = subprocess.run([sys.executable, "-m", "iml"] + args + [path], cwd=codec, capture_output=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr.decode("utf-8", "replace"))
        sys.exit(2)
    return r.stdout.replace(b"\r\n", b"\n")


def check_iml(codec):
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
        compiled = codec_run(codec, ["compile", "--document"], ILANG)
        ok1 = compiled == read(IML)
        print("compile SOUL.ilang.md == SOUL.iml:", "yes" if ok1 else "NO")
        decompiled = codec_run(codec, ["decompile"], IML)
        ok2 = decompiled == read(ILANG)
        print("decompile SOUL.iml == SOUL.ilang.md:", "yes" if ok2 else "NO")
        return 0 if ok1 and ok2 else 1
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def check_length():
    n = len(read(ILANG).decode("utf-8"))
    print("SOUL.ilang.md: %d characters, limit %d" % (n, MAX_CHARS))
    return 0 if n <= MAX_CHARS else 1


def check_site(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ilang-spec products/soul check)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        served = r.read().replace(b"\r\n", b"\n")
    a, b = hashlib.sha256(served).hexdigest(), hashlib.sha256(read(ILANG)).hexdigest()
    print("served %s\nrepo   %s" % (a, b))
    return 0 if a == b else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--iml"]:
        codec = args[args.index("--codec") + 1] if "--codec" in args else None
        sys.exit(check_iml(codec))
    if args == ["--length"]:
        sys.exit(check_length())
    if args[:1] == ["--site"] and len(args) == 2:
        sys.exit(check_site(args[1]))
    print(__doc__)
    sys.exit(2)
