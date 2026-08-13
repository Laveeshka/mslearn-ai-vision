"""
Preflight check for the Wide World Importers visual analysis lab.

Each task in this lab can be completed on its own. Before you start a task,
run this script from the starter `Python` folder (the folder you opened in
VS Code) to confirm your .env file has everything that task needs:

    python ../setup/check_env.py --task 1

It never changes anything - it only reads your .env and tells you what (if
anything) is missing, so you can fix it before running the task.

Tasks and what they need:

    Task 1  (code)   OPENAI_ENDPOINT, MODEL_DEPLOYMENT_NAME
    Task 2  (code)   OPENAI_ENDPOINT, MODEL_DEPLOYMENT_NAME
    Task 3  (code)   CONTENT_UNDERSTANDING_ENDPOINT, ANALYZER_ID
"""

import argparse
import os
from pathlib import Path

try:
    from dotenv import dotenv_values
except ModuleNotFoundError:
    # python-dotenv is installed into the lab's virtual environment, but this
    # preflight check is meant to run BEFORE 'pip install -r requirements.txt'
    # (and possibly outside the venv). Fall back to a small stdlib parser so the
    # check still works on a clean interpreter.
    def dotenv_values(path):
        """Minimal .env reader: KEY=VALUE, honoring quotes and # comments."""
        values = {}
        with open(path, "r", encoding="utf-8-sig") as env_file:
            for raw_line in env_file:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[len("export "):].lstrip()
                key, separator, value = line.partition("=")
                if not separator:
                    # python-dotenv records a bare key with no "=" as None.
                    values[line] = None
                    continue
                key = key.strip()
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                    value = value[1:-1]
                else:
                    value = value.split(" #")[0].strip()
                values[key] = value
        return values

# Which .env keys each task needs to run on its own.
TASK_REQUIREMENTS = {
    1: ["OPENAI_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    2: ["OPENAI_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    3: ["CONTENT_UNDERSTANDING_ENDPOINT", "ANALYZER_ID"],
}

# Every key this lab might read, used when merging real environment variables.
ALL_KEYS = [
    "OPENAI_ENDPOINT",
    "MODEL_DEPLOYMENT_NAME",
    "CONTENT_UNDERSTANDING_ENDPOINT",
    "ANALYZER_ID",
]

# Placeholder text shipped in .env.example - present but not yet filled in.
PLACEHOLDERS = {
    "",
    "your_endpoint",
    "your_analyzer_id",
    "your_model_deployment",
    "https://your-resource-name.openai.azure.com/openai/v1/",
    "https://your-resource-name.services.ai.azure.com/",
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
    "MODEL_DEPLOYMENT_NAME": (
        "Set MODEL_DEPLOYMENT_NAME to the name of the multimodal chat model you "
        "deployed (for example, gpt-4o). You can see it in the Foundry portal under "
        "your project's Deployments page."
    ),
    "CONTENT_UNDERSTANDING_ENDPOINT": (
        "Task 3 uses Azure AI Content Understanding. Copy the resource endpoint from "
        "the Code Example tab of your analyzer in Content Understanding Studio - it "
        "looks like https://<your-resource-name>.services.ai.azure.com/ . This is NOT "
        "the Azure OpenAI endpoint."
    ),
    "ANALYZER_ID": (
        "Task 3 needs the name you gave your analyzer when you selected Build analyzer "
        "in Content Understanding Studio. You can see it in the analyzer list."
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
