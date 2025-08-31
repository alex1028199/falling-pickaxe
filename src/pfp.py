import os
import requests
from pathlib import Path

PFP_CACHE_DIR = Path(__file__).parent.parent / "pfp_cache"
PFP_CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_pfp(channel_id, pfp_url):
    """
    Downloads and caches a profile picture.
    Returns the path to the cached image.
    """
    cached_pfp_path = PFP_CACHE_DIR / f"{channel_id}.jpg"

    if cached_pfp_path.exists():
        return str(cached_pfp_path)

    try:
        response = requests.get(pfp_url, stream=True)
        response.raise_for_status()
        with open(cached_pfp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return str(cached_pfp_path)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading profile picture for {channel_id}: {e}")
        return None
