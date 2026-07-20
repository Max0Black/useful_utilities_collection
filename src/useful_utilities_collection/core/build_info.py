import sys
from datetime import datetime, timezone
from pathlib import Path

from useful_utilities_collection.version import (
    __version__,
    __author__,
    __product_name__,
    __description__,
    __copyright__,
    __license__,
    __internal_name__,
    __repository_url__,
)


def _is_frozen() -> bool:
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def _read_version_resource() -> dict[str, str]:
    if sys.platform != "win32" or not _is_frozen():
        return {}

    try:
        import win32api  # pywin32
    except Exception:
        return {}

    try:
        exe_path = sys.executable
        info = win32api.GetFileVersionInfo(exe_path, "\\")
        ms = info["FileVersionMS"]
        ls = info["FileVersionLS"]
        file_version = f"{(ms >> 16) & 0xFFFF}.{(ms >> 0) & 0xFFFF}.{(ls >> 16) & 0xFFFF}.{(ls >> 0) & 0xFFFF}"

        lang_codepage = win32api.GetFileVersionInfo(
            exe_path, "\\VarFileInfo\\Translation"
        )[0]
        codepage = f"{lang_codepage[0]:04X}{lang_codepage[1]:04X}"

        def string_value(name: str) -> str:
            try:
                return win32api.GetFileVersionInfo(
                    exe_path, f"\\StringFileInfo\\{codepage}\\{name}"
                )
            except Exception:
                return ""

        return {
            "file_version": file_version,
            "company": string_value("CompanyName"),
            "product": string_value("ProductName"),
            "description": string_value("FileDescription"),
            "internal_name": string_value("InternalName"),
            "copyright": string_value("LegalCopyright"),
            "original_filename": string_value("OriginalFilename"),
        }
    except Exception:
        return {}


def get_build_info() -> dict[str, str]:
    res = _read_version_resource()
    frozen = _is_frozen()

    version = res.get("file_version") or __version__
    product = res.get("product") or __product_name__
    description = res.get("description") or __description__
    author = res.get("company") or __author__
    copyright_ = res.get("copyright") or __copyright__
    internal_name = res.get("internal_name") or __internal_name__
    original_filename = res.get("original_filename") or (
        f"{__internal_name__}.exe" if frozen else "source (not built)"
    )

    if frozen:
        build_source = "Compiled executable"
        build_time = _read_pe_timestamp()
    else:
        build_source = "Running from source"
        build_time = _read_source_build_time()

    return {
        "version": version,
        "author": author,
        "product": product,
        "description": description,
        "copyright": copyright_,
        "license": __license__ or "MIT",
        "internal_name": internal_name,
        "original_filename": original_filename,
        "repository_url": __repository_url__,
        "build_source": build_source,
        "build_time": build_time,
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
    }


def _read_pe_timestamp() -> str:
    try:
        import win32api
        ts = win32api.GetFileVersionInfo(sys.executable, "\\")["FileDateLS"]
        if ts:
            return datetime.fromtimestamp(ts / 1e7 - 11644473600, tz=timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
    except Exception:
        pass

    return "N/A"


def _read_source_build_time() -> str:
    try:
        version_file = Path(__file__).resolve().parent / "version.py"
        mtime = version_file.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "N/A"

