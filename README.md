# Auto Terraform Generation (AWS)

This repository provides a Terraform-based framework to provision common AWS infrastructure components, and includes helper scripts to generate per-project Terraform from YAML and run Terraform commands.

## Features
- VPC creation with public/private subnets
- Internet Gateway, Elastic IP, and NAT Gateway
- Public and private route tables
- Security Group with customizable ingress/egress rules
- EC2 instance
- S3 bucket
- Application Load Balancer (ALB)
- YAML-driven project generation via `scripts/deploy.py`

## Repository Structure

```
/ (repo root)
├── main.tf                # Root Terraform using AWS modules in ./modules
├── variables.tf           # Input variables for root
├── terraform.tfvars       # Example variable values
├── modules/               # Reusable Terraform modules (vpc, subnet, sg, ec2, s3, alb, igw, nat, rt, eip)
├── scripts/
│   ├── deploy.py          # Generate a per-project folder from YAML and run init/plan
│   └── destroy.py         # Placeholder for destroy helper
├── configs/
│   ├── project-requirments.yaml  # Example full configuration for root
│   └── test1.yaml                # Example for generator flow
├── test1/                 # Example generated project (by script)
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars.json
└── app-requirenemts.md    # Project requirements and context
```

## Prerequisites
- Terraform >= 1.5
- AWS credentials exported in your environment (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and optionally `AWS_DEFAULT_REGION`)
- Python 3.9+

## Quick Start (Root Stack)
1. Review and update `terraform.tfvars` as needed (region, CIDRs, AMI, etc.).
2. Initialize providers and modules:
   ```bash
   terraform init
   ```
3. Review the plan:
   ```bash
   terraform plan
   ```
4. Apply:
   ```bash
   terraform apply
   ```

## YAML-driven Generation (scripts/deploy.py)
The generator reads a YAML config and creates a project directory named after the YAML file (without extension). It writes:
- `main.tf` and `variables.tf` with module stubs
- `terraform.tfvars.json` with flattened variables
Then it runs `terraform init` and `terraform plan` in the generated directory.

Example config (`configs/test1.yaml`):
```yaml
region: "us-east-1"
modules:
  vpc:
    source: "./modules/vpc"
    vpc_name: "my-vpc"
    vpc_cidr: "10.0.0.0/16"
  sg:
    source: "./modules/sg"
    vpc_id: "module.vpc.vpc_id"
    name: "main-sg"
    ingress_rules:
      - { from_port: 22, to_port: 22, protocol: "tcp", cidr_blocks: ["0.0.0.0/0"] }
    egress_rules:
      - { from_port: 0, to_port: 0, protocol: "-1", cidr_blocks: ["0.0.0.0/0"] }
```

Run the generator:
```bash
python scripts/deploy.py configs/test1.yaml
```
This creates a folder `test1/` with Terraform files and runs `terraform init` and `terraform plan` inside it.

### Notes and Limitations
- The generator currently expects each module block to include a `source` key. All other keys become variables named `var.<module>_<key>` in the generated `variables.tf`.
- Values like references (`module.vpc.vpc_id`) are serialized literally into `terraform.tfvars.json`. You may need to replace those with proper wiring in the generated `main.tf` if Terraform evaluation fails.
- The generator adds a `variable "region"` line only if `region` is provided in the YAML. Review generated `variables.tf` for correctness.

## Modules Overview
Each module in `modules/` encapsulates a specific AWS resource pattern. For details, read each module’s `variables.tf` and `output(s).tf`. Example for route tables:

```startLine:endLine:modules/rt/README.md
# rt Module

## Usage

```hcl
module "rt" {
  source = "./modules/rt"

  name = "example"
  tags = {
    Environment = "dev"
  }
}
```
```

## Inputs
See `variables.tf` in the root and within each module. Common inputs include:
- `region`, `vpc_name`, `vpc_cidr`, `subnets`
- Security group `name`, `ingress_rules`, `egress_rules`
- EC2 `ami`, `instance_type`, `key_name`, `instance_name`
- S3 `bucket_name`, ALB `name`

## Outputs
Inspect each module’s `output.tf` to discover IDs and ARNs exposed, such as `vpc_id`, `subnet_ids`, `sg_id`, and more.

## Security Considerations
- `terraform.tfvars` allows SSH and HTTP/HTTPS from `0.0.0.0/0` for convenience. Restrict these CIDRs in production.
- Manage state securely (e.g., remote backend like S3 + DynamoDB) if collaborating.

## Cleaning Up
If you applied from the root, you can destroy resources:
```bash
terraform destroy
```
For generated projects, run destroy in that project directory.

## Roadmap
- Improve variable generation and expression support in `deploy.py`
- Implement `scripts/destroy.py` to auto-destroy generated projects based on YAML
- Add CI workflow and linting
