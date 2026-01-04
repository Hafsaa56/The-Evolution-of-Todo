#!/usr/bin/env python3
"""
Setup verification script for the Todo Application
Checks if all necessary files and configurations are in place
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print the result"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} - NOT FOUND")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists and print the result"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ {description}: {dirpath} - NOT FOUND")
        return False

def check_backend_files():
    """Check backend files"""
    print("\n🔍 Checking Backend Files...")
    backend_ok = True

    backend_ok &= check_directory_exists("backend", "Backend directory")

    if os.path.exists("backend"):
        backend_files = [
            ("backend/main.py", "Backend main application"),
            ("backend/requirements.txt", "Backend requirements"),
            ("backend/models", "Backend models directory"),
            ("backend/api", "Backend API directory"),
            ("backend/utils", "Backend utilities directory"),
            ("backend/.env.example", "Backend environment example"),
        ]

        for filepath, description in backend_files:
            backend_ok &= check_file_exists(filepath, description)

    return backend_ok

def check_frontend_files():
    """Check frontend files"""
    print("\n🔍 Checking Frontend Files...")
    frontend_ok = True

    frontend_ok &= check_directory_exists("frontend", "Frontend directory")

    if os.path.exists("frontend"):
        frontend_files = [
            ("frontend/package.json", "Frontend package configuration"),
            ("frontend/app", "Frontend app directory"),
            ("frontend/components", "Frontend components directory"),
            ("frontend/services", "Frontend services directory"),
            ("frontend/.env.example", "Frontend environment example"),
        ]

        for filepath, description in frontend_files:
            frontend_ok &= check_file_exists(filepath, description)

    return frontend_ok

def check_helper_files():
    """Check helper files"""
    print("\n🔍 Checking Helper Files...")
    helper_ok = True

    helper_files = [
        ("run_app.bat", "Windows run script"),
        ("run_app.sh", "Linux/Mac run script"),
        ("RUN_INSTRUCTIONS.md", "Run instructions"),
        ("SETUP_ENV.md", "Environment setup guide"),
        ("START_HERE.txt", "Quick start guide"),
    ]

    for filepath, description in helper_files:
        helper_ok &= check_file_exists(filepath, description)

    return helper_ok

def check_env_files():
    """Check if environment files exist"""
    print("\n🔍 Checking Environment Files...")
    env_ok = True

    # Check if .env files exist (they might not exist yet, which is okay)
    if os.path.exists("backend/.env"):
        print("✓ Backend .env file exists")
    else:
        print("? Backend .env file not found - you may need to create it from .env.example")
        env_ok = False  # Not critical, but good to have

    if os.path.exists("frontend/.env"):
        print("✓ Frontend .env file exists")
    else:
        print("? Frontend .env file not found - you may need to create it from .env.example")
        env_ok = False  # Not critical, but good to have

    return env_ok

def main():
    """Main function to run all checks"""
    print("🔧 Todo Application Setup Verification")
    print("=" * 50)

    print("This script checks if all necessary files for the Todo application are in place.")

    backend_ok = check_backend_files()
    frontend_ok = check_frontend_files()
    helper_ok = check_helper_files()
    env_ok = check_env_files()

    print("\n" + "=" * 50)
    print("📋 SUMMARY:")

    all_checks = [backend_ok, frontend_ok, helper_ok]

    if all(all_checks):
        print("✅ All critical files are in place!")
        if env_ok:
            print("✅ Environment files are configured!")
            print("\n🎉 You're ready to run the application!")
            print("   - For Windows: Double-click run_app.bat")
            print("   - For Linux/Mac: Run ./run_app.sh")
        else:
            print("⚠️  Environment files are missing but can be created from .env.example files")
            print("   - Follow SETUP_ENV.md instructions to create them")
    else:
        print("❌ Some files are missing. Please check the output above.")
        print("   - Make sure you're running this script from the main project directory")
        print("   - Check that all files were properly copied")

    print("\n📖 For detailed instructions, see RUN_INSTRUCTIONS.md")
    print("📖 For environment setup, see SETUP_ENV.md")

if __name__ == "__main__":
    main()