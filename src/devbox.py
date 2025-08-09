"""
Task 1:
- Create a devbox named your email.
- Copy resources/ into the devbox.
- Edit resources/me.txt in the devbox to contain your email.
- Execute test.js or test.py inside the devbox.
- Snapshot the devbox.
- Update answers.json.
"""

import os
from pathlib import Path
from client import get_client, get_email
from utils import save_answers, upload_directory, await_devbox_running, run_stateful

RESOURCES_DIR = Path(__file__).resolve().parents[1] / "resources"
REMOTE_ROOT = "/workspace"
REMOTE_RESOURCES = f"resources"


def main():
    client = get_client()
    email = get_email()

    # 1.a: Create devbox named your email
    dev = client.devboxes.create(name=email)
    devbox_id = dev.id
    print("Created devbox:", devbox_id)
    await_devbox_running(client, devbox_id)

    # Record api-key (from env), devbox-name, devbox-id
    save_answers(
        {
            "devbox-name": email,
            "devbox-id": devbox_id,
        }
    )
    print(RESOURCES_DIR)
    # 1.b: Copy resources/ to devbox under /workspace/resources
    upload_directory(client, devbox_id, RESOURCES_DIR, REMOTE_RESOURCES)

    # Replace email in me.txt
    client.devboxes.write_file_contents(
        id=devbox_id,
        file_path=f"{REMOTE_RESOURCES}/me.txt",
        contents=email,
    )

    # Execute one of the test scripts (prefer Python; fallback to Node)
    cmds = [
        f"mkdir -p {REMOTE_ROOT}",
        f"cd {REMOTE_ROOT}",
        # Try python first
        f"python {REMOTE_RESOURCES}/test.py || node {REMOTE_RESOURCES}/test.js",
    ]
    run_stateful(client, devbox_id, cmds)

    # 1.c: Snapshot the devbox
    snap = client.devboxes.snapshot_disk(id=devbox_id)
    snap_id = snap.id
    print("Snapshot id:", snap_id)
    save_answers({"snapshot-id": snap_id})


if __name__ == "__main__":
    main()
