# -*- coding: utf-8 -*-
# Locate the MSVC/SDK dirs that vs_toolchain.py downloaded (DEPOT_TOOLS_WIN_TOOLCHAIN=1)
# and write a cmd env file for the v8dasm compile step.
import os, sys, glob

v8_dir = os.path.abspath(sys.argv[1])
wt = os.path.join(os.path.dirname(v8_dir), "win_toolchain")

def latest(pattern):
    hits = sorted(glob.glob(pattern))
    return hits[-1] if hits else None

msvc_base = latest(os.path.join(wt, "vs_files", "*", "VC", "Tools", "MSVC", "*"))
sdk_base  = latest(os.path.join(wt, "vs_files", "*", "Windows Kits", "10"))
assert msvc_base and sdk_base, "pinned toolchain not found under " + wt

msvc_ver = os.path.basename(msvc_base)
sdk_ver_dirs = glob.glob(os.path.join(sdk_base, "Include", "*"))
sdk_ver = os.path.basename(sorted(sdk_ver_dirs)[-1])

lines = []
lines.append('set "MSVC_INC=%s"' % os.path.join(msvc_base, "include"))
lines.append('set "MSVC_LIB=%s"' % os.path.join(msvc_base, "lib", "x64"))
lines.append('set "MSVC_BIN=%s"' % os.path.join(msvc_base, "bin", "HostX64", "x64"))
lines.append('set "SDK_INC_UCRT=%s"' % os.path.join(sdk_base, "Include", sdk_ver, "ucrt"))
lines.append('set "SDK_INC_SHARED=%s"' % os.path.join(sdk_base, "Include", sdk_ver, "shared"))
lines.append('set "SDK_INC_UM=%s"' % os.path.join(sdk_base, "Include", sdk_ver, "um"))
lines.append('set "SDK_LIB_UM=%s"' % os.path.join(sdk_base, "Lib", sdk_ver, "um", "x64"))
lines.append('set "SDK_LIB_UCRT=%s"' % os.path.join(sdk_base, "Lib", sdk_ver, "ucrt", "x64"))
lines.append('set "SDK_BIN=%s"' % os.path.join(sdk_base, "bin", sdk_ver, "x64"))

out = os.path.join(os.environ.get("TEMP", "."), "v8_tc_env.cmd")
with open(out, "w", encoding="ascii") as f:
    f.write("\n".join(lines) + "\n")
print("env file:", out)
for l in lines: print("  ", l[:120])
