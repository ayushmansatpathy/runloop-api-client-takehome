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
import time
from client import get_client, get_email
from utils import save_answers, upload_directory, await_devbox_running, run_stateful

RESOURCES_DIR = Path(__file__).resolve().parents[1] / "resources"
REMOTE_ROOT = "/workspace"
REMOTE_RESOURCES = f"resources"


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

    # Create a scenario with a basic “scoring contract”
    # If SDK expects you to upload code for scorer, you can inline a trivial spec.
    scenario = client.scenarios.create(
        name=f"{email}-ext-scenario",
        scoring_contract={
            "scoring_function_parameters": [
                {
                    "name": "resources_checker",
                    "scorer": {
                        "type": "bash_script_scorer",
                        "bash_script": """
                        if [ -f "resources/me.txt" ] && [ -f "resources/test.py" ] && [ -f "resources/test.js" ]; then
                          echo "1.0"
                        else
                          echo "0.0"
                        fi
                    """,
                    },
                    "weight": 1.0,
                }
            ]
        },
        input_context={
            "problem_statement": "Check presence of /resources and its files",
            "additional_context": {},
        },
    )

    # Start scenario run targeting our devbox
    run = client.scenarios.start_run(scenario_id=scenario.id)
    dev_id = run.devbox_id
    await_devbox_running(client, dev_id)

    # Copy resources to devbox & edit me.txt
    upload_directory(client, dev_id, RESOURCES_DIR, REMOTE_RESOURCES)
    client.devboxes.write_file_contents(
        id=dev_id,
        file_path=f"{REMOTE_RESOURCES}/me.txt",
        contents=email,
    )

    # Run test script (same as Task 1.b)
    run_stateful(
        client,
        dev_id,
        [
            f"mkdir -p {REMOTE_ROOT}",
            f"cd {REMOTE_ROOT}",
            f"python {REMOTE_RESOURCES}/test.py || node {REMOTE_RESOURCES}/test.js",
        ],
    )
    time.sleep(3)
    client.scenarios.runs.score(
        id=run.id,
    )
    time.sleep(3)
    complete_id = client.scenarios.runs.complete(id=run.id)

    save_answers({"ext-scenario-run-id": complete_id.id})


if __name__ == "__main__":
    main()
