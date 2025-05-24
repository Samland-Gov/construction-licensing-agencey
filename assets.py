import os
import shutil
import zipfile
import urllib.request
from pathlib import Path

# Define paths
static_dir = Path("app/static")
assets_dir = static_dir / "assets"
zip_path = Path("govuk_frontend.zip")

# Remove existing GOV.UK Frontend assets
for path in ["fonts", "images"]:
    shutil.rmtree(static_dir / path, ignore_errors=True)

# Remove any existing govuk-frontend* folders/files
for item in static_dir.glob("govuk-frontend*"):
    if item.is_dir():
        shutil.rmtree(item, ignore_errors=True)
    else:
        try:
            item.unlink()
        except Exception:
            pass

# Download the ZIP file
url = "https://github.com/alphagov/govuk-frontend/releases/download/v5.10.1/release-v5.10.1.zip"
print(f"Downloading GOV.UK Frontend from {url}")
urllib.request.urlretrieve(url, zip_path)

# Unzip to static directory
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(static_dir)

# Move contents of assets to static directory
if assets_dir.exists():
    for item in assets_dir.iterdir():
        dest = static_dir / item.name
        if item.is_dir():
            shutil.move(str(item), dest)
        else:
            shutil.move(str(item), str(dest))

# Cleanup
shutil.rmtree(assets_dir, ignore_errors=True)
try:
    (static_dir / "VERSION.txt").unlink()
except FileNotFoundError:
    pass

try:
    zip_path.unlink()
except FileNotFoundError:
    pass
