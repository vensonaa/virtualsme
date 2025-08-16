#!/usr/bin/env python3
"""
Quick fix for missing numpy and other dependencies
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Install missing dependencies"""
    print("🔧 Fixing Missing Dependencies")
    print("=" * 40)
    
    # Critical dependencies that might be missing
    critical_packages = [
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "scikit-learn>=1.0.0",
        "transformers>=4.20.0"
    ]
    
    print("📦 Installing critical packages...")
    failed = []
    
    for package in critical_packages:
        if not install_package(package):
            failed.append(package)
    
    if failed:
        print(f"\n⚠️  Failed to install {len(failed)} packages:")
        for package in failed:
            print(f"  - {package}")
        print("\nPlease try installing them manually:")
        for package in failed:
            print(f"  pip install {package}")
    else:
        print("\n🎉 All critical dependencies installed!")
        print("\nNow try running your script again:")
        print("python add_sample_data.py")

if __name__ == "__main__":
    main()
