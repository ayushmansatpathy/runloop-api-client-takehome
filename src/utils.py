import io
import json
import os
import time
from pathlib import Path
from typing import Dict, Iterable

ANSWERS_PATH = Path(__file__).resolve().parents[1] / "answers.json"


def load_answers() -> Dict:
    if ANSWERS_PATH.exists():
        return json.loads(ANSWERS_PATH.read_text())
    return {
        "api-key": "",
        "devbox-name": "",
        "devbox-id": "",
        "snapshot-id": "",
        "blueprint-name": "",
        "blueprint-id": "",
        "devbox-from-blueprint-id": "",
        "devbox-from-blueprint-name": "",
        "ext-scenario-run-id": "",
    }


def save_answers(update: Dict) -> None:
    data = load_answers()
    data.update(update)
    ANSWERS_PATH.write_text(json.dumps(data, indent=2))


def upload_directory(client, devbox_id: str, local_dir: Path, remote_root: str) -> None:
    """
    Recursively uploads `local_dir` into devbox under `remote_root`.
    """
    for path in local_dir.rglob("*"):
        rel = path.relative_to(local_dir)
        remote_path = f"{remote_root}/{rel.as_posix()}"
        if path.is_dir():
            # For many SDKs, writing a directory isn't necessary; ensure parents by 'mkdir -p'
            client.devboxes.execute_sync(
                id=devbox_id,
                command=f"mkdir -p '{remote_path}'",
                shell_name="upload-shell",
            )
            continue
        # write file
        contents = path.read_bytes()
        # ensure parent dir exists
        parent = "/".join(remote_path.split("/")[:-1])
        client.devboxes.execute_sync(
            id=devbox_id, command=f"mkdir -p '{parent}'", shell_name="upload-shell"
        )
        client.devboxes.write_file_contents(
            id=devbox_id, file_path=remote_path, contents=contents
        )


def await_devbox_running(client, devbox_id: str, timeout_s: int = 180) -> None:
    t0 = time.time()
    while True:
        view = client.devboxes.retrieve(devbox_id)
        if getattr(view, "status", None) == "running":
            return
        if time.time() - t0 > timeout_s:
            raise TimeoutError("Devbox did not reach 'running' state in time.")
        time.sleep(2)


def run_stateful(
    client, devbox_id: str, commands: Iterable[str], shell_name: str = "stateful"
):
    for cmd in commands:
        res = client.devboxes.execute_sync(
            id=devbox_id, command=cmd, shell_name=shell_name
        )
        code = getattr(res, "exit_code", 0)
        if code != 0:
            out = getattr(res, "stdout", b"")
            err = getattr(res, "stderr", b"")
            raise RuntimeError(
                f"Command failed ({code}): {cmd}\nSTDOUT:\n{out}\nSTDERR:\n{err}"
            )
