#!/usr/bin/env python3
import sys
import yaml

def read_yaml(file_path: str) -> dict:
    """Read a YAML file and return its content as a dictionary."""
    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
        return data
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python read_yaml.py <path-to-yaml>")
        sys.exit(1)

    yaml_file = sys.argv[1]
    config = read_yaml(yaml_file)

    print("✅ YAML content loaded successfully:\n")
    print(config)
