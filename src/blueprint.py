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
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)  # pillow is optional; can vendor a minimal text->png if needed
import textwrap

from client import get_client, get_email
from utils import save_answers, await_devbox_running, run_stateful

OUT_IMAGE = Path(__file__).resolve().parents[1] / "blueprint.png"


def text_to_png(text: str, path: Path):
    lines = textwrap.dedent(text).splitlines()
    width = max((len(l) for l in lines), default=40)
    width_px = max(600, width * 10)
    height_px = max(200, (len(lines) + 2) * 18)

    img = Image.new("RGB", (width_px, height_px), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    y = 10
    for l in lines:
        draw.text((10, y), l, fill=(0, 0, 0), font=font)
        y += 18
    img.save(path)


def main():
    client = get_client()
    email = get_email()

    # Create blueprint with cowsay
    # Many platforms do blueprints as "base image + provisioning script". Here we use a simple shell provision.
    blueprint_name = f"{email}-cowsay-blueprint"
    bp = client.blueprints.create(
        name=blueprint_name,
        # If the SDK supports a 'provision_script' or 'on_boot' commands, we can specify apt install here.
        # Otherwise, some platforms expect a devbox->snapshot->convert-to-blueprint flow.
        provision_script="apt-get update && apt-get install -y cowsay",
    )
    blueprint_id = bp.id
    print("Blueprint created:", blueprint_id)

    save_answers(
        {
            "blueprint-name": blueprint_name,
            "blueprint-id": blueprint_id,
        }
    )

    # Boot a devbox from blueprint
    dev_from_bp = client.blueprints.devboxes.create(
        blueprint_id=blueprint_id, name=f"{email}-from-bp"
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

    # Turn the cowsay output into an image artifact for the repo
    text_to_png(cowsay_output.strip() or "cowsay output empty?", OUT_IMAGE)

    save_answers(
        {
            "devbox-from-blueprint-id": devbox_id,
            "devbox-from-blueprint-name": f"{email}-from-bp",
        }
    )
    print("Saved cowsay screenshot ->", OUT_IMAGE)


if __name__ == "__main__":
    main()
