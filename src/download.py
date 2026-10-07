"""Extract step: download the Transfermarkt dataset and unpack raw files."""
from pathlib import Path
import shutil
import urllib.request
import zipfile

URL = "https://pub-e682421888d945d684bcae8890b0ec20.r2.dev/data/transfermarkt-datasets.zip"
RAW_DIR = Path("data/raw")
ZIP_PATH = RAW_DIR / "transfermarkt-datasets.zip"

def download(url: str, dest: Path) -> None:
    if dest.exists():
        print(f"File {dest} already exists, skipping download")
        return
    
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url}")
    request = urllib.request.Request(
        url, headers={"User-Agent": "football-club-analyser/1.0"}
    )
    with urllib.request.urlopen(request) as response, open(dest, "wb") as f:
        shutil.copyfileobj(response, f)
    print(f"Saved {dest} ({dest.stat().st_size / 1e6:.1f} MB)")


def unzip(zip_path: Path, target: Path) -> None:
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(target)
        print(f"Extracted {len(z.namelist())} files to {target}")


if __name__ == "__main__":
    download(URL, ZIP_PATH)
    unzip(ZIP_PATH, RAW_DIR)