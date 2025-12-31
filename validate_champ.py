#!/usr/bin/env python3
"""Validate CHAMP installation."""

import json
import os
import sys


def check_file(path, description):
    """Check if file exists."""
    if os.path.exists(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description} MISSING: {path}")
        return False


def validate_json(path):
    """Validate JSON file."""
    try:
        with open(path) as f:
            json.load(f)
        print(f"✅ Valid JSON: {path}")
        return True
    except Exception as e:
        print(f"❌ Invalid JSON in {path}: {e}")
        return False


def check_manifest(path):
    """Validate manifest.json specifically."""
    try:
        with open(path) as f:
            manifest = json.load(f)

        required_fields = ["domain", "name", "version", "config_flow"]
        missing = [f for f in required_fields if f not in manifest]

        if missing:
            print(f"❌ Manifest missing required fields: {missing}")
            return False

        if manifest["domain"] != "champ":
            print(f"❌ Manifest domain should be 'champ', got '{manifest['domain']}'")
            return False

        if not manifest.get("config_flow"):
            print("❌ config_flow should be true")
            return False

        print(f"✅ Manifest valid: domain={manifest['domain']}, version={manifest['version']}")
        return True

    except Exception as e:
        print(f"❌ Error validating manifest: {e}")
        return False


def main():
    """Run validation."""
    base_path = "custom_components/champ"

    print("🔍 Validating CHAMP Installation")
    print("=" * 50)
    print()

    all_good = True

    # Check directory exists
    if not os.path.isdir(base_path):
        print(f"❌ CHAMP directory not found: {base_path}")
        print(f"\nCurrent directory: {os.getcwd()}")
        print(f"Expected path: {os.path.abspath(base_path)}")
        return 1

    print(f"✅ CHAMP directory found: {base_path}\n")

    # Check required Python files
    print("Checking Python files:")
    print("-" * 50)
    required_files = [
        ("__init__.py", "Component initialization"),
        ("config_flow.py", "Configuration flow"),
        ("const.py", "Constants"),
        ("coordinator.py", "Data coordinator"),
        ("sensor.py", "Sensor platform"),
        ("switch.py", "Switch platform"),
    ]

    for filename, description in required_files:
        path = os.path.join(base_path, filename)
        if not check_file(path, description):
            all_good = False

    print()

    # Check JSON files
    print("Checking JSON files:")
    print("-" * 50)

    manifest_path = os.path.join(base_path, "manifest.json")
    if check_file(manifest_path, "Component manifest"):
        if not check_manifest(manifest_path):
            all_good = False
    else:
        all_good = False

    strings_path = os.path.join(base_path, "strings.json")
    if check_file(strings_path, "UI strings"):
        if not validate_json(strings_path):
            all_good = False
    else:
        all_good = False

    print()

    # Check translations
    print("Checking translations:")
    print("-" * 50)
    for lang in ["en", "de"]:
        path = os.path.join(base_path, "translations", f"{lang}.json")
        if check_file(path, f"{lang.upper()} translation"):
            if not validate_json(path):
                all_good = False
        else:
            all_good = False

    print()
    print("=" * 50)

    if all_good:
        print("✅ All validation checks passed!")
        print()
        print("📋 Next steps:")
        print("  1. Copy to Home Assistant: /config/custom_components/champ")
        print("  2. Restart Home Assistant")
        print("  3. Go to Settings → Devices & Services")
        print("  4. Click 'Add Integration' and search for 'CHAMP'")
        print("  5. Follow the setup wizard")
        print()
        print("📚 See INSTALL.md for detailed instructions")
        return 0
    else:
        print("❌ Validation failed - please fix errors above")
        print()
        print("💡 Tips:")
        print("  - Ensure you're running this from the project root")
        print("  - Check that all files were created correctly")
        print("  - Verify JSON files have valid syntax")
        return 1


if __name__ == "__main__":
    sys.exit(main())
