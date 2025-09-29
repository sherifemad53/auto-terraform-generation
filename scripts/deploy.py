import os
import sys
import yaml
import json
import argparse
import subprocess
import shutil
from pathlib import Path

MAIN_HEADER = """terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region
}

"""

def generate_tf_project(yaml_file):
    with open(yaml_file, "r") as f:
        config = yaml.safe_load(f) or {}

    project_name = Path(yaml_file).stem
    project_dir = Path(project_name)
    project_dir.mkdir(exist_ok=True)

    region = config.get("region")
    modules = config.get("modules", {}) or {}

    print('Generating Terraform project............')


    # ---------------- main.tf ----------------
    main_tf = [MAIN_HEADER]
    
    # variables.tf initialized regardless of region presence
    variables_tf = []
    if region:
        variables_tf.append('variable "region" {')
        variables_tf.append('  type    = string')
        variables_tf.append(f'  default = "{region}"')
        variables_tf.append('}')

    # Add modules
    for mod_name, mod_conf in modules.items():
        source = mod_conf.get("source")
        if source is None:
            raise ValueError(f"Module '{mod_name}' is missing required 'source' key")
        # Write module block
        main_tf.append(f'module "{mod_name}" {{')
        main_tf.append(f'  source = "{source}"')
        for key in [k for k in mod_conf.keys() if k != "source"]:
            main_tf.append(f'  {key} = var.{mod_name}_{key}')
            variables_tf.append(f'variable "{mod_name}_{key}" {{}}')
        main_tf.append("}\n")

        # Copy or create module inside project/modules
        copy_or_create_module(project_dir / "modules" / mod_name, mod_conf)

    # ---------------- write files ----------------
    with open(project_dir / "main.tf", "w") as f:
        f.write("\n".join(main_tf))

    with open(project_dir / "variables.tf", "w") as f:
        f.write("\n".join(variables_tf))

    # Only write literal values to tfvars JSON; skip HCL expressions like module.*
    # def is_literal(val):
    #     return not (isinstance(val, str) and val.strip().startswith("module."))

    # flat_vars = {}
    # for mod, conf in modules.items():
    #     for key, val in conf.items():
    #         if key == "source":
    #             continue
    #         if is_literal(val):
    #             flat_vars[f"{mod}_{key}"] = val

    with open(project_dir / "terraform.tfvars.json", "w") as f:
        json.dump(flatten_vars(modules), f, indent=2)
    print(f"✅ Project '{project_name}' generated at {project_dir.absolute()}")
    return project_dir


def flatten_vars(modules: dict):
    """Flatten module variables to match var.<module>_<key> style"""
    flat = {}
    for mod, conf in modules.items():
        for key, val in conf.items():
            if key != "source":
                flat[f"{mod}_{key}"] = val
    return flat


def copy_or_create_module(target_dir: Path, mod_conf):
    """Copy module if exists, else create skeleton"""
    source_path = Path(mod_conf["source"])

    if source_path.exists():
        # Copy existing module into project
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_path, target_dir)
    else:
        # Create skeleton module
        target_dir.mkdir(parents=True, exist_ok=True)
        # main.tf placeholder
        (target_dir / "main.tf").write_text(
            f"""# {target_dir.name} module
# Define AWS resources for {target_dir.name} here
"""
        )
        # variables.tf
        lines = []
        for key in mod_conf:
            if key != "source":
                lines.append(f'variable "{key}" {{}}')
        (target_dir / "variables.tf").write_text("\n".join(lines) + "\n")

        # outputs.tf
        (target_dir / "outputs.tf").write_text(
            f"""# Outputs for {target_dir.name} module
# Example:
# output "{target_dir.name}_id" {{
#   value = aws_<resource>.this.id
# }}
"""
        )

def check_aws_credentials():
    """Check if AWS credentials are available via env vars or profile"""
    env_ok = os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY")
    profile_ok = os.getenv("AWS_PROFILE") is not None
    if not (env_ok or profile_ok):
        print("Error: AWS credentials not found. Set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY or AWS_PROFILE.")
        sys.exit(1)

def run_terraform_commands(project_dir, do_apply=False):
    """Run terraform init and plan/apply in the generated project directory"""
    cwd = os.getcwd()
    try:
        os.chdir(project_dir)
        subprocess.run(["terraform", "init"], check=True)
        if do_apply:
            subprocess.run(["terraform", "apply", "-auto-approve"], check=True)
        else:
            subprocess.run(["terraform", "plan"], check=True)
    finally:
        os.chdir(cwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Terraform project from YAML and run Terraform.")
    parser.add_argument("yaml", help="Path to YAML config file")
    parser.add_argument("--apply", action="store_true", help="Run 'terraform apply -auto-approve' instead of 'plan'")
    args = parser.parse_args()

    check_aws_credentials()
    yaml_file = args.yaml
    project_dir = generate_tf_project(yaml_file)
    run_terraform_commands(project_dir, do_apply=args.apply)
