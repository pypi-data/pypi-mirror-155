import re
import tarfile
import tempfile
import zipfile
from pathlib import Path

from .__about__ import __version__
from ._main import _encrypt, _get_random_string


def encrypt_path(path) -> None:
    path = Path(path)

    if path.isdir():
        for p in path.rglob("*.py"):
            encrypt_py(p)

    elif path.suffix == ".py":
        encrypt_py(path)

    elif path.suffix in [".whl", ".zip"]:
        encrypt_zip(path)

    elif path.suffixes[-2:] == [".tar", ".gz"]:
        encrypt_tar_gz(path)

    else:
        raise ValueError(f"x21: Don't know how to encrypt {path}")


def encrypt_py(path: Path) -> None:
    if path.suffix != ".py":
        raise ValueError("Must be .py file")

    with open(path) as f:
        content = f.read()

    iv = _get_random_string(16)
    scode = _encrypt("22b", content, iv)
    content = f"""from x21 import __dex_22b__

__dex_22b__(
    globals(),
    "{iv}",
    {scode}
)"""

    with open(path, "w") as f:
        f.write(content)


def encrypt_zip(zip_path: Path) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        with zipfile.ZipFile(zip_path) as w:
            w.extractall(tmpdir)

        for p in tmpdir.rglob("*.py"):
            encrypt_py(p)

        # inject x21 dependency in METADATA file
        for item in tmpdir.iterdir():
            if item.name.endswith(".dist-info"):
                with open(item / "METADATA") as f:
                    content = f.read()

                # inject x21 Requires-Dist before first Requires-Dist
                content = re.sub(
                    "Requires-Dist:",
                    f"Requires-Dist: x21 (>={__version__})\nRequires-Dist:",
                    content,
                    count=1,
                )

                with open(item / "METADATA", "w") as f:
                    f.write(content)
                break

        # shutil.make_archive(zip_path, "zip", tmpdir)
        with zipfile.ZipFile(zip_path, "w") as zf:
            for p in tmpdir.rglob("*"):
                zf.write(p, p.relative_to(tmpdir))


def encrypt_tar_gz(tar_path: Path) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        with tarfile.open(tar_path) as tar:
            tar.extractall(tmpdir)

        for p in tmpdir.rglob("*.py"):
            encrypt_py(p)

        with tarfile.open(tar_path, "w:gz") as tar:
            # Override the temp directory by `.` (the current dir)
            tar.add(tmpdir, arcname=".")
