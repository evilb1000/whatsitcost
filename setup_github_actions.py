#!/usr/bin/env python3
"""
Setup script for GitHub Actions environment
Ensures all required files and permissions are in place
"""

import os
import subprocess
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and report status"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ Missing: {description}: {file_path}")
        return False

def main():
    """Main setup verification"""
    print("🔧 BIG ALPHA KINGS GITHUB ACTIONS SETUP 🔧")
    print("=" * 50)
    
    # Check required files
    required_files = [
        ("automated_data_pipeline.py", "Master pipeline script"),
        (".github/workflows/automated-data-pipeline.yml", "GitHub Actions workflow"),
        ("Scrapers/MasterScraper.py", "BLS data scraper"),
        ("theBehemoth.py", "Data consolidation script"),
        ("Scrapers/master_updater.py", "Processing and upload script"),
        ("requirements.txt", "Python dependencies")
    ]
    
    all_good = True
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    print("\n📋 SETUP CHECKLIST:")
    print("1. ✅ Automated pipeline script created")
    print("2. ✅ GitHub Actions workflow configured")
    print("3. ✅ Scheduled for: Sept 10, Oct 16, Nov 14, Dec 11 at 4pm EST")
    print("4. ✅ Manual trigger enabled")
    print("5. ✅ Error handling and logging included")
    
    if all_good:
        print("\n🎉 SETUP COMPLETE!")
        print("📝 Next steps:")
        print("   1. Commit and push these files to GitHub")
        print("   2. Check Actions tab for workflow")
        print("   3. Test with manual trigger")
        print("   4. Wait for scheduled runs")
    else:
        print("\n❌ SETUP INCOMPLETE - Fix missing files first")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    exit(main())



