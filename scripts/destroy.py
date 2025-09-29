import os
import sys
import argparse
import subprocess
from pathlib import Path


def ensure_project_dir(yaml_path: str) -> Path:
    project_dir = Path(yaml_path).with_suffix("").name
    return Path(project_dir)


def run_destroy(project_dir: Path):
    if not project_dir.exists():
        print(f"Error: project directory '{project_dir}' does not exist.")
        sys.exit(1)

    cwd = os.getcwd()
    try:
        os.chdir(project_dir)
        subprocess.run(["terraform", "init"], check=True)
        subprocess.run(["terraform", "destroy", "-auto-approve"], check=True)
    finally:
        os.chdir(cwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Destroy a generated Terraform project based on YAML file name.")
    parser.add_argument("yaml", help="Path to YAML config used to generate the project")
    args = parser.parse_args()

    project_dir = ensure_project_dir(args.yaml)
    run_destroy(project_dir)


