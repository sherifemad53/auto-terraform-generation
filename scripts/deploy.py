import os
import sys
import yaml
import json
import argparse
import subprocess
import shutil
from pathlib import Path


# ---------------- Provider templates ----------------
PROVIDER_TEMPLATE = """terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region  = var.region
#   profile = var.profile
}
"""

# ---------------- MAIN SCRIPT ----------------
def generate_tf_project(yaml_file):
    with open(yaml_file, "r") as f:
        config = yaml.safe_load(f) or {}

    project_name = Path(yaml_file).stem
    base_dir = Path("./generated-projects")
    # project_dir = base_dir / project_name
    project_dir = Path(project_name)

    # ✅ Ensure the base folder exists
    base_dir.mkdir(exist_ok=True)

    # ✅ Ensure the specific project folder exists
    project_dir.mkdir(exist_ok=True)

    modules = config.get("modules", {}) or {}

    print(f"Generating Terraform project for AWS ............")

    # Select modules path
    MODULE_PATHS = {
        mod: f"./modules/{mod}"
        for mod in modules.keys()
    }

    # ---------------- main.tf ----------------
    main_tf = [PROVIDER_TEMPLATE]
    variables_tf = ['variable "region" {type = string}']

    # ---- Other modules ----
    for mod_name, mod_conf in modules.items():
        source = MODULE_PATHS.get(mod_name)
        if not source:
            print(f"⚠️ Skipping unknown module '{mod_name}'")
            continue

        main_tf.append(f'module "{mod_name}" {{')
        main_tf.append(f'  source = "{source}"')

        for key, val in mod_conf.items():
            # If it's a Terraform expression, write it literally
            if isinstance(val, str) and val.startswith("module."):
                main_tf.append(f'  {key} = {val}')
            else:
                main_tf.append(f'  {key} = var.{mod_name}_{key}')
                variables_tf.append(f'variable "{mod_name}_{key}" {{}}')

        main_tf.append("}\n")
        copy_or_create_module(project_dir / "modules" / mod_name, mod_conf, source)

    # Write files
    (project_dir / "main.tf").write_text("\n".join(main_tf))
    (project_dir / "variables.tf").write_text("\n".join(variables_tf))

    flat_vars = flatten_vars(config)
    (project_dir / "terraform.tfvars.json").write_text(json.dumps(flat_vars, indent=2))

    print(f"✅ Project '{project_name}' generated for AWS at {project_dir.absolute()}")
    return project_dir


def flatten_vars(config: dict):
    """
    Flatten only real Terraform variables — not module references.
    Skips entire `modules` section except for primitive + list vars.
    """
    flat = {}

    # --- top-level vars like region, profile ---
    for key, val in config.items():
        if key == "modules":
            continue
        if not isinstance(val, dict):
            flat[key] = val

    # --- modules vars ---
    modules = config.get("modules", {}) or {}
    for mod, conf in modules.items():
        for key, val in conf.items():
            # Skip expressions like "module.vpc.vpc_id"
            if isinstance(val, str) and val.startswith("module."):
                continue
            flat[f"{mod}_{key}"] = val

    return flat



def copy_or_create_module(target_dir: Path, mod_conf, source: str):
    source_path = Path(source)
    if source_path.exists():
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_path, target_dir)
    else:
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "main.tf").write_text(f"# {target_dir.name} module placeholder\n")
        (target_dir / "variables.tf").write_text(
            "\n".join([f'variable "{k}" {{}}' for k in mod_conf.keys()])
        )


def check_aws_credentials():
    if not (os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY")):
        print("❌ Missing AWS credentials. Export AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
        sys.exit(1)

def run_terraform_commands(project_dir, do_apply=False):
    cwd = os.getcwd()
    try:
        os.chdir(project_dir)

        # Add backend dynamically
        backend_block = get_backend_config(project_dir)
        if backend_block:
            with open("backend.tf", "w") as f:
                f.write(backend_block)

        subprocess.run(["terraform", "init"], check=True)
        if do_apply:
            subprocess.run(["terraform", "apply", "-auto-approve"], check=True)
        else:
            subprocess.run(["terraform", "plan"], check=True)
    finally:
        os.chdir(cwd)

def get_backend_config(project_dir):
    project_name = project_dir.name
    return f"""terraform {{
  backend "s3" {{
    bucket = "my-terraform-states-konecta"
    key    = "{project_name}/terraform.tfstate"
    region = "us-east-1"
  }}
}}
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and deploy Terraform project for AWS or GCP.")
    parser.add_argument("yaml", help="Path to YAML config file")
    parser.add_argument("--apply", action="store_true", help="Run terraform apply -auto-approve")
    args = parser.parse_args()

    yaml_file = args.yaml
    project_dir = generate_tf_project(yaml_file)
    get_backend_config(project_dir)
    # check_aws_credentials()
    # run_terraform_commands(project_dir, do_apply=args.apply)
