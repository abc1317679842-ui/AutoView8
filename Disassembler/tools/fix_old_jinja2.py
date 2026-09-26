# -*- coding: utf-8 -*-
# V8 9.1 bundles jinja2 2.x which does `from collections import Mapping` etc.
# Those names moved to collections.abc in Python 3.10+. Install a global
# sitecustomize shim so the old imports work with Python 3.10+ runners.
import os, site

NAMES = ("Mapping", "MutableMapping", "Sequence", "MutableSequence",
         "Iterable", "Callable", "Hashable", "Set", "MutableSet",
         "ByteString", "Container", "Reversible", "Generator",
         "MappingView", "KeysView", "ItemsView", "ValuesView")

body = "import collections, collections.abc\n"
for n in NAMES:
    body += "setattr(collections, %r, getattr(collections.abc, %r))\n" % (n, n)

sp = site.getsitepackages()
target = None
for d in sp:
    f = os.path.join(d, "sitecustomize.py")
    if os.path.isdir(d) and os.access(d, os.W_OK):
        target = f
        break
if not target:
    # fall back: write next to the python executable's Lib
    import sys
    target = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "sitecustomize.py")
    os.makedirs(os.path.dirname(target), exist_ok=True)

with open(target, "w", encoding="utf-8") as f:
    f.write(body)
print("sitecustomize written:", target)
