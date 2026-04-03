from pathlib import Path

_SRC_PACKAGE_DIR = Path(__file__).resolve().parent.parent / "src" / "supply_chain_env"

if not _SRC_PACKAGE_DIR.exists():
    raise ModuleNotFoundError(f"Expected source package at {_SRC_PACKAGE_DIR}")

# Make the repo-local src package importable before any globally installed copy.
__file__ = str(_SRC_PACKAGE_DIR / "__init__.py")
__path__ = [str(_SRC_PACKAGE_DIR)]

with open(__file__, "r", encoding="utf-8") as _src_init:
    exec(compile(_src_init.read(), __file__, "exec"), globals(), globals())
