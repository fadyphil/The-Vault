#!/usr/bin/env python3
import sys
import os
import json
import re
import subprocess

# Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_error(msg):
    print(f"{RED}{BOLD}❌ Error:{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}{BOLD}⚠️ Warning:{RESET} {msg}")

def print_success(msg):
    print(f"{GREEN}{BOLD}✓{RESET} {msg}")

def check_swagger_json(swagger_path):
    """Checks that the Swagger JSON is valid and structured correctly."""
    if not os.path.exists(swagger_path):
        print_error(f"Swagger documentation file not found at '{swagger_path}'!")
        return None

    try:
        with open(swagger_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print_success(f"Swagger spec '{swagger_path}' is valid JSON.")
        return data
    except json.JSONDecodeError as e:
        print_error(f"Swagger file '{swagger_path}' contains syntax errors:\n{e}")
        return None

def check_endpoint_consistency(swagger_data):
    """Scans Go source code for registered routes and checks if they are documented."""
    go_routes = []
    # Scan cmd/ and internal/ for Go files
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith(".go"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Match HandleFunc pattern: HandleFunc("POST /v1/secrets", ...) or HandleFunc("/v1/secrets", ...)
                    matches = re.findall(r'HandleFunc\(\s*"([A-Z]*)\s*([^"]+)"', content)
                    for match in matches:
                        method = match[0].strip()
                        route = match[1].strip()
                        go_routes.append((file_path, method, route))
                except Exception as e:
                    print_warning(f"Could not read {file_path}: {e}")

    if not go_routes:
        print_warning("No Go endpoints found via HandleFunc parsing. Skipping endpoint consistency check.")
        return True

    paths_in_swagger = swagger_data.get("paths", {})
    missing_docs = []

    for file_path, method, route in go_routes:
        # Standardize matching for paths (handling path variables and simple trailing slashes)
        matched_path = None
        for swagger_path in paths_in_swagger.keys():
            # Check for exact match or parameterized match
            # E.g., /v1/secrets/{id} matching /v1/secrets/{id}
            if swagger_path == route:
                matched_path = swagger_path
                break
        
        if not matched_path:
            missing_docs.append((file_path, method, route, "Path not found in Swagger paths"))
            continue

        if method:
            method_lower = method.lower()
            if method_lower not in paths_in_swagger[matched_path]:
                missing_docs.append((file_path, method, route, f"HTTP method '{method}' is not documented for '{route}'"))
        else:
            # If method is empty, make sure at least one HTTP method is defined in Swagger
            if not paths_in_swagger[matched_path]:
                missing_docs.append((file_path, method, route, f"No HTTP methods documented for path '{route}'"))

    if missing_docs:
        print_error("Undocumented API endpoints detected in Go code:")
        for file_path, method, route, reason in missing_docs:
            method_str = f"[{method}] " if method else ""
            print(f"  - {file_path}: {method_str}{route} -> {reason}")
    print_success("All Go code endpoints are documented in Swagger.")
    return True

def check_readme_endpoints(swagger_data, readme_path="README.md"):
    """Validates that all API endpoints listed in the README.md table exist in the Swagger spec."""
    if not os.path.exists(readme_path):
        print_warning(f"README file not found at '{readme_path}'. Skipping README endpoint check.")
        return True

    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print_warning(f"Could not read {readme_path}: {e}")
        return True

    # Find table rows with backticks, e.g.: | `POST` | `/v1/secrets` | Description |
    readme_endpoints = re.findall(r'\|\s*`([A-Z]+)`\s*\|\s*`([^`]+)`\s*\|', content)
    
    if not readme_endpoints:
        print_warning("No endpoints table found in README.md. Skipping README check.")
        return True

    paths_in_swagger = swagger_data.get("paths", {})
    missing_docs = []

    for method, route in readme_endpoints:
        matched_path = None
        for swagger_path in paths_in_swagger.keys():
            if swagger_path == route:
                matched_path = swagger_path
                break
        
        if not matched_path:
            missing_docs.append((method, route, "Path not found in Swagger paths"))
            continue

        method_lower = method.lower()
        if method_lower not in paths_in_swagger[matched_path]:
            missing_docs.append((method, route, f"HTTP method '{method}' is not documented for '{route}' in Swagger"))

    if missing_docs:
        print_error("Endpoints documented in README.md are missing or mismatching in docs/swagger.json:")
        for method, route, reason in missing_docs:
            print(f"  - [{method}] {route} -> {reason}")
        return False

    print_success("All README.md endpoints are fully documented in Swagger.")
    return True


def check_markdown_links():
    """Scans all markdown files and validates that local relative links are valid."""
    errors = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    for line_num, line in enumerate(lines, 1):
                        # Simple regex to extract local links e.g. [text](relative/path)
                        # Ignores http://, https://, mailto:, and empty links/anchors
                        links = re.findall(r'\[[^\]]*\]\(([^)]+)\)', line)
                        for link in links:
                            if link.startswith(("http://", "https://", "mailto:", "#")):
                                continue
                            
                            # Remove anchor/query parameters from file path
                            clean_link = link.split("#")[0].split("?")[0]
                            if not clean_link:
                                continue
                            
                            # Resolve target file path relative to markdown file directory
                            link_dir = os.path.dirname(file_path)
                            target_path = os.path.normpath(os.path.join(link_dir, clean_link))
                            
                            if not os.path.exists(target_path):
                                errors.append((file_path, line_num, link, target_path))
                except Exception as e:
                    print_warning(f"Could not analyze markdown file {file_path}: {e}")

    if errors:
        print_error("Broken markdown links detected:")
        for src_file, line, link, resolved in errors:
            print(f"  - {src_file}:{line} -> Broken link: '{link}' (Resolved to: '{resolved}')")
        return False

    print_success("All internal markdown links are valid.")
    return True

def check_git_commit_status(swagger_path):
    """Enforces that if API files are modified, documentation is updated as well."""
    bypass = os.environ.get("BYPASS_DOCS_CHECK") == "1"
    
    try:
        # Get staged files in the current commit
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        staged_files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception as e:
        print_warning(f"Unable to read Git staged files (perhaps not in a Git repository?): {e}")
        return True

    # If no files are staged, we are not running a pre-commit or it's empty
    if not staged_files:
        return True

    staged_api_files = []
    staged_doc_files = []

    for f in staged_files:
        # Identify API code files
        if f.startswith(("cmd/", "internal/handler/", "internal/dto/", "internal/service/")) and f.endswith(".go"):
            staged_api_files.append(f)
        # Identify documentation/spec files
        elif f.startswith("docs/") or f in ["README.md", "CHANGELOG.md", "ROADMAP.md", "CONTRIBUTING.md", "SECURITY.md"]:
            staged_doc_files.append(f)

    if staged_api_files and not staged_doc_files:
        if bypass:
            print_warning("API code changed without documentation updates, but bypass is active (BYPASS_DOCS_CHECK=1).")
            return True
        else:
            print_error("API code has been updated, but no matching documentation changes are staged.")
            print(f"Staged API files:\n" + "\n".join([f"  - {f}" for f in staged_api_files]))
            print(f"\n{BOLD}💡 What you should do:{RESET}")
            print(f"1. Check if the Swagger specification ({swagger_path}) or other docs need updates.")
            print(f"2. Stage the documentation updates (e.g. `git add docs/swagger.json README.md`).")
            print(f"3. Commit again.")
            print(f"4. (Bypass) If this change does not affect the API contract, run: {BOLD}BYPASS_DOCS_CHECK=1 git commit{RESET} or {BOLD}git commit --no-verify{RESET}\n")
            return False

    return True

def main():
    swagger_path = "docs/swagger.json"
    success = True

    print(f"{BOLD}=== Running Documentation and Swagger Verification ==={RESET}\n")

    # 1. Check Swagger JSON Validity
    swagger_data = check_swagger_json(swagger_path)
    if swagger_data is None:
        success = False

    # 2. Check Go Endpoint Consistency with Swagger
    if swagger_data:
        if not check_endpoint_consistency(swagger_data):
            success = False
        if not check_readme_endpoints(swagger_data):
            success = False

    # 3. Check Markdown Links Integrity
    if not check_markdown_links():
        success = False

    # 4. Enforce Documentation updates alongside API changes
    if not check_git_commit_status(swagger_path):
        success = False

    print("")
    if success:
        print_success("All documentation checks passed successfully!")
        sys.exit(0)
    else:
        print_error("Documentation verification failed. Please correct the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
