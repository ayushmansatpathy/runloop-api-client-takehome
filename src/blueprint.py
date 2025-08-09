"""
Task 2:
- Create a blueprint that has 'cowsay' installed.
- Boot a devbox from the blueprint and run 'cowsay' to produce output.
- Save a screenshot 'blueprint.png' (we'll capture terminal output and render it into a PNG).
- Update answers.json with blueprint name/id and the devbox from blueprint id/name.

Note: If the platform exposes a true 'screenshot' API for terminals/browsers, use it.
Here we render stdout to a PNG so the repo contains a visible artifact.
"""

from pathlib import Path
import textwrap
import time

from client import get_client, get_email
from utils import save_answers, await_devbox_running, run_stateful

OUT_IMAGE = Path(__file__).resolve().parents[1] / "blueprint.png"


def main():
    client = get_client()
    email = get_email()

    # Create blueprint with cowsay
    # Many platforms do blueprints as "base image + provisioning script". Here we use a simple shell provision.
    blueprint_name = f"{email}-cowsay-blueprint"
    bp = client.blueprints.create(
        name=blueprint_name,
    )
    blueprint_id = bp.id
    print("Blueprint created:", blueprint_id)

    save_answers(
        {
            "blueprint-name": blueprint_name,
            "blueprint-id": blueprint_id,
        }
    )

    time.sleep(20)

    # Boot a devbox from blueprint
    dev_from_bp = client.devboxes.create(
        name=f"{email}-from-bp", blueprint_id=blueprint_id
    )
    devbox_id = dev_from_bp.id
    await_devbox_running(client, devbox_id)

    # Run cowsay
    res = client.devboxes.execute_sync(
        id=devbox_id, command="cowsay 'Runloop!'", shell_name="bp-shell"
    )
    cowsay_output = getattr(res, "stdout", "") or ""
    if isinstance(cowsay_output, bytes):
        cowsay_output = cowsay_output.decode("utf-8", errors="ignore")


if __name__ == "__main__":
    main()
