"""
Task 3 (extension):
- Create a custom scenario with a scorer that checks presence of 'resources' (folder + files).
- Copy scenario folder 'resources' to the devbox.
- Execute the script from step 1.b to edit 'me.txt' and run one of the tests.
- Score and complete the scenario run (1 if resources present; 0 otherwise).
- Record 'ext-scenario-run-id' in answers.json.

Notes:
- Some Runloop installs model scenarios as general 'benchmarks.scenarios' while others expose 'scenarios.*'.
- The code below uses a generic 'scenarios' surface; rename methods to match your SDK.
"""

import os
from pathlib import Path
from client import get_client, get_email
from utils import save_answers, upload_directory, await_devbox_running, run_stateful

RESOURCES_DIR = Path(__file__).resolve().parents[1] / "resources"
REMOTE_ROOT = "/workspace"
REMOTE_RESOURCES = f"{REMOTE_ROOT}/resources"


def resources_exist(client, devbox_id: str) -> bool:
    # Minimal “existence” check: read back both files
    try:
        me = client.devboxes.read_file_contents(
            id=devbox_id, file_path=f"{REMOTE_RESOURCES}/me.txt"
        )
        py = client.devboxes.read_file_contents(
            id=devbox_id, file_path=f"{REMOTE_RESOURCES}/test.py"
        )
        js = client.devboxes.read_file_contents(
            id=devbox_id, file_path=f"{REMOTE_RESOURCES}/test.js"
        )
        return bool(me and py and js)
    except Exception:
        return False


def main():
    client = get_client()
    email = get_email()

    # Create a fresh devbox for the scenario
    dev = client.devboxes.create(name=f"{email}-scenario")
    devbox_id = dev.id
    await_devbox_running(client, devbox_id)

    # Copy resources to devbox & edit me.txt
    upload_directory(client, devbox_id, RESOURCES_DIR, REMOTE_RESOURCES)
    client.devboxes.write_file_contents(
        id=devbox_id,
        file_path=f"{REMOTE_RESOURCES}/me.txt",
        contents=(email + "\n").encode("utf-8"),
    )

    # Run test script (same as Task 1.b)
    run_stateful(
        client,
        devbox_id,
        [
            f"mkdir -p {REMOTE_ROOT}",
            f"cd {REMOTE_ROOT}",
            f"python {REMOTE_RESOURCES}/test.py || node {REMOTE_RESOURCES}/test.js",
        ],
    )

    # Create a scenario with a basic “scoring contract”
    # If SDK expects you to upload code for scorer, you can inline a trivial spec.
    scenario = client.scenarios.create(
        name=f"{email}-ext-scenario",
        description="Checks for presence of /workspace/resources and its files.",
        # Arbitrary metadata; adjust based on SDK
        scoring_contract="presence_check_resources",
    )

    # Start scenario run targeting our devbox
    run = client.scenarios.runs.create(
        scenario_id=scenario.id,
        target_devbox_id=devbox_id,
    )

    # Compute local score (simple presence check) and submit to platform
    score = 1.0 if resources_exist(client, devbox_id) else 0.0

    client.scenarios.runs.submit_score(
        run_id=run.id,
        score=score,
        details={
            "reason": (
                "Found required files in /workspace/resources"
                if score == 1.0
                else "Missing files"
            )
        },
    )

    # Mark scenario run complete (some SDKs combine score+complete)
    client.scenarios.runs.complete(run_id=run.id)

    save_answers({"ext-scenario-run-id": run.id})
    print("Scenario run id:", run.id, "score:", score)


if __name__ == "__main__":
    main()
