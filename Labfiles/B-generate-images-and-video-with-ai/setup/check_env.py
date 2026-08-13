"""
Preflight check for the Wide World Importers generative media lab.

Each task in this lab can be completed on its own. Before you start a task,
run this script to confirm your .env file has everything that task needs:

    python setup/check_env.py --task 1

It never changes anything - it only reads your .env and tells you what (if
anything) is missing, so you can fix it before running the task.

Tasks and what they need:

    Task 1  (code)   OPENAI_ENDPOINT, IMAGE_MODEL_DEPLOYMENT_NAME
    Task 2  (code)   OPENAI_ENDPOINT, VIDEO_MODEL_DEPLOYMENT_NAME
    Task 3  (code)   OPENAI_ENDPOINT, VIDEO_MODEL_DEPLOYMENT_NAME
"""

import argparse
import os
from pathlib import Path

from dotenv import dotenv_values

# Which .env keys each task needs to run on its own.
TASK_REQUIREMENTS = {
    1: ["OPENAI_ENDPOINT", "IMAGE_MODEL_DEPLOYMENT_NAME"],
    2: ["OPENAI_ENDPOINT", "VIDEO_MODEL_DEPLOYMENT_NAME"],
    3: ["OPENAI_ENDPOINT", "VIDEO_MODEL_DEPLOYMENT_NAME"],
}

# Every key this lab might read, used when merging real environment variables.
ALL_KEYS = [
    "OPENAI_ENDPOINT",
    "IMAGE_MODEL_DEPLOYMENT_NAME",
    "VIDEO_MODEL_DEPLOYMENT_NAME",
]

# Placeholder text shipped in .env.example - present but not yet filled in.
PLACEHOLDERS = {
    "",
    "your_image_model_deployment",
    "your_video_model_deployment",
    "https://your-resource-name.openai.azure.com/openai/v1/",
    "<your-openai-endpoint>",
    "<your-model-deployment-name>",
}

# How to fix each key, shown only when it's missing.
FIX_HINTS = {
    "OPENAI_ENDPOINT": (
        "Copy the Azure OpenAI endpoint for your Foundry resource from the project "
        "home page and add the '/openai/v1/' suffix, so it looks like "
        "https://<your-resource-name>.openai.azure.com/openai/v1/ . This is NOT the "
        "project endpoint."
    ),
    "IMAGE_MODEL_DEPLOYMENT_NAME": (
        "Task 1 needs an image generation model. Deploy gpt-image-2 in the Foundry "
        "portal and set IMAGE_MODEL_DEPLOYMENT_NAME to its deployment name."
    ),
    "VIDEO_MODEL_DEPLOYMENT_NAME": (
        "Tasks 2 and 3 need a video generation model. Deploy sora-2 in the Foundry "
        "portal and set VIDEO_MODEL_DEPLOYMENT_NAME to its deployment name. Access to "
        "video generation models is restricted - you may need to register your "
        "subscription first."
    ),
}


def find_env_file():
    """Return the .env next to the lab's Python folder, wherever this is run from."""
    here = Path(__file__).resolve().parent
    candidates = [
        Path.cwd() / ".env",
        here.parent / "Python" / ".env",
        here.parent / ".env",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    # Default to the Python-folder location even if it doesn't exist yet.
    return here.parent / "Python" / ".env"


def load_values(env_path):
    """Merge real environment variables over .env file values (env wins)."""
    values = {}
    if env_path.exists():
        values.update({k: v for k, v in dotenv_values(env_path).items() if v is not None})
    for key in ALL_KEYS:
        if os.environ.get(key):
            values[key] = os.environ[key]
    return values


def is_set(values, key):
    """A key counts as set if it's present and not a leftover placeholder."""
    value = (values.get(key) or "").strip()
    return bool(value) and value not in PLACEHOLDERS


def main():
    parser = argparse.ArgumentParser(
        description="Check that your .env has what a given lab task needs."
    )
    parser.add_argument(
        "--task",
        type=int,
        choices=sorted(TASK_REQUIREMENTS),
        required=True,
        help="Which task you're about to start (1-3).",
    )
    args = parser.parse_args()

    env_path = find_env_file()
    values = load_values(env_path)
    required = TASK_REQUIREMENTS[args.task]

    print(f"Checking readiness for Task {args.task}")
    print(f"Reading: {env_path}{'' if env_path.exists() else '  (not found yet)'}")
    print()

    missing = [key for key in required if not is_set(values, key)]

    for key in required:
        mark = "OK " if is_set(values, key) else "MISSING"
        print(f"  [{mark}] {key}")

    if not missing:
        print()
        print(f"You're ready to start Task {args.task}.")
        return 0

    print()
    print("Set the following before starting this task:")
    for key in missing:
        print(f"\n  {key}\n    {FIX_HINTS.get(key, 'Add this key to your .env file.')}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
