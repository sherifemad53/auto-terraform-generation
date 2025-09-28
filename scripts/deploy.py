import os
import sys
import yaml
import json
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
        config = yaml.safe_load(f)

    project_name = Path(yaml_file).stem
    project_dir = Path(project_name)
    project_dir.mkdir(exist_ok=True)

    region = config.get("region",{})
    modules = config.get("modules", {})

    print('Generating Terraform project............')


    # ---------------- main.tf ----------------
    main_tf = [MAIN_HEADER]
    
    # # Add region variable default if provided
    if region:
        variables_tf = ['variable "region" { type = string,defualt= "${region}"} ']

    # Add modules
    for mod_name, mod_conf in modules.items():
        source = mod_conf.pop("source")
        # Write module block
        main_tf.append(f'module "{mod_name}" {{')
        main_tf.append(f'  source = "{source}"')
        for key in mod_conf.keys():
            main_tf.append(f'  {key} = var.{mod_name}_{key}')
            variables_tf.append(f'variable "{mod_name}_{key}" {{}}')
        main_tf.append("}\n")

    # ---------------- write files ----------------
    with open(project_dir / "main.tf", "w") as f:
        f.write("\n".join(main_tf))

    with open(project_dir / "variables.tf", "w") as f:
        f.write("\n".join(variables_tf))

    with open(project_dir / "terraform.tfvars.json", "w") as f:
        json.dump(flatten_vars(modules), f, indent=2)
    print(f"✅ Project '{project_name}' generated at {project_dir.absolute()}")


def flatten_vars(modules: dict):
    """Flatten module variables to match var.<module>_<key> style"""
    flat = {}
    for mod, conf in modules.items():
        for key, val in conf.items():
            if key != "source":
                flat[f"{mod}_{key}"] = val
    return flat

def check_aws_credentials():
    """Check if AWS credentials are set in environment variables"""
    if not (os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY")):
        print("Error: AWS credentials not found in environment variables.")
        print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
        sys.exit(1)

def run_terraform_commands(project_dir):
    """Run terraform init and plan in the generated project directory"""
    os.chdir(project_dir)
    os.system("terraform init")
    os.system("terraform plan")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_tf_project.py <config.yaml>")
        sys.exit(1)

    check_aws_credentials()
    yaml_file = sys.argv[1]
    generate_tf_project(yaml_file)
    project_name = Path(yaml_file).stem
    run_terraform_commands(project_name)
