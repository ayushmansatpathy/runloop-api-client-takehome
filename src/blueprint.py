"""
Task 2:
- Create a blueprint that has 'cowsay' installed.
- Boot a devbox from the blueprint and run 'cowsay' to produce output.
- Update answers.json with blueprint name/id and the devbox from blueprint id/name.
- Take screenshot of devbox and upload it as blueprint.png
"""

from pathlib import Path
import time

from client import get_client, get_email
from utils import save_answers, await_devbox_running, run_stateful


def main():
    client = get_client()
    email = get_email()

    # create blueprint
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

    time.sleep(
        20
    )  # added delay to ensure blueprint was up and running, can have cleaner solution like await_devbox_running

    # Boot a devbox from blueprint
    dev_from_bp = client.devboxes.create(
        name=f"{email}-from-bp", blueprint_id=blueprint_id
    )
    devbox_id = dev_from_bp.id
    await_devbox_running(client, devbox_id)

    save_answers(
        {
            "devbox-from-blueprint-id": devbox_id,
            "devbox-from-blueprint-name": dev_from_bp.name,
        }
    )

    # Install cowsay
    res = client.devboxes.execute_sync(
        id=devbox_id, command="pip install cowsay", shell_name="bp-shell"
    )
    cowsay_output = getattr(res, "stdout", "") or ""
    if isinstance(cowsay_output, bytes):
        cowsay_output = cowsay_output.decode("utf-8", errors="ignore")


if __name__ == "__main__":
    main()
