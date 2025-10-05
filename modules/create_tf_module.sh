#!/bin/bash

# Script to scaffold a Terraform module with common files
# Usage: ./create_tf_module.sh <module_name>

set -e

if [ -z "$1" ]; then
  echo "❌ Please provide a module name"
  echo "👉 Example: ./create_tf_module.sh route_table"
  exit 1
fi

MODULE_NAME=$1
MODULE_DIR="./modules/${MODULE_NAME}"

# Check if module directory already exists
if [ -d "${MODULE_DIR}" ]; then
  echo "❌ Module directory ${MODULE_DIR} already exists!"
  exit 1
fi

# Create module directory
mkdir -p "${MODULE_DIR}"

# main.tf
cat > "${MODULE_DIR}/main.tf" <<EOF
# ${MODULE_NAME} module

resource "aws_${MODULE_NAME}" "this" {
  # TODO: add resource config
}
EOF

# variables.tf
cat > "${MODULE_DIR}/variables.tf" <<EOF
# Variables for ${MODULE_NAME} module
EOF

# outputs.tf
cat > "${MODULE_DIR}/outputs.tf" <<EOF
# Outputs for ${MODULE_NAME} module
EOF

# README.md
cat > "${MODULE_DIR}/README.md" <<EOF
# ${MODULE_NAME} Module

## Usage

\`\`\`hcl
module "${MODULE_NAME}" {
  source = "./modules/${MODULE_NAME}"

  name = "example"
  tags = {
    Environment = "dev"
  }
}
\`\`\`
EOF

echo "✅ Terraform module '${MODULE_NAME}' created at ${MODULE_DIR}"
