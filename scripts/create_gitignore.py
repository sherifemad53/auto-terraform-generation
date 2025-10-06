from pathlib import Path

def create_gitignore(target_dir, content=None):
    """Create a .gitignore file inside target_dir with default or custom content."""
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    gitignore_path = target_dir / ".gitignore"

    default_content = """
# Terraform
*.tfstate
*.tfstate.*
.terraform/
crash.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Logs
*.log

# Python
__pycache__/
*.pyc

# OS files
.DS_Store
Thumbs.db
"""

    # Use custom content if provided
    gitignore_content = content or default_content.strip()

    gitignore_path.write_text(gitignore_content)
    print(f"✅ .gitignore created at: {gitignore_path.absolute()}")

# Example usage
if __name__ == "__main__":
    create_gitignore("./generated-projects/my-project")
