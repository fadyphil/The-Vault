#!/bin/bash
set -e

# setup-hooks.sh installs the doc-checking pre-commit hook.

HOOK_DIR=".git/hooks"
HOOK_FILE="$HOOK_DIR/pre-commit"

# Ensure we are in a git repository
if [ ! -d ".git" ]; then
  echo "❌ Error: .git directory not found. Make sure to run this script from the repository root."
  exit 1
fi

# Create hook directory if it doesn't exist
mkdir -p "$HOOK_DIR"

echo "⚙️  Installing pre-commit hook..."

# Write hook contents
cat << 'EOF' > "$HOOK_FILE"
#!/bin/bash
# Git pre-commit hook to verify documentation and Swagger API consistency.

# Execute the check-docs validation script
python3 scripts/check-docs.py
EOF

# Make hook executable
chmod +x "$HOOK_FILE"

echo "✅ Pre-commit hook installed successfully at: $HOOK_FILE"
echo "The hook will verify your Swagger JSON, Go routing consistency, and markdown links on every commit."
echo "If you ever need to bypass it for a non-API change, commit with:"
echo "  BYPASS_DOCS_CHECK=1 git commit"
echo "  or: git commit --no-verify"
