import os
from typing import Optional
from runloop_api_client import Runloop

BASE_URL = os.environ.get("RUNLOOP_BASE_URL", "https://api.runloop.pro")
API_KEY = os.environ.get("RUNLOOP_API_KEY")
RUNLOOP_EMAIL = "asatpathy@umass.edu"


def get_client() -> Runloop:
    if not API_KEY:
        raise RuntimeError("RUNLOOP_API_KEY not set.")
    return Runloop(base_url=BASE_URL, bearer_token=API_KEY)


def get_email() -> str:
    email = RUNLOOP_EMAIL
    if not email:
        raise RuntimeError("RUNLOOP_EMAIL not set.")
    return email


def ensure_shell_name(name: Optional[str]) -> str:
    return name or "default-shell"
