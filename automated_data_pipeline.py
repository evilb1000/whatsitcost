#!/usr/bin/env python3
"""
Big Alpha Kings Automated Data Pipeline
Chains together: MasterScraper → theBehemoth → master_updater
Runs on scheduled dates to keep AI data fresh
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import os

def run_script(script_path, script_name):
    """Run a script and handle errors"""
    print(f"🚀 Running: {script_name}")
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {script_name} completed successfully")
        if result.stdout:
            print(f"📝 Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {script_name} failed with error code {e.returncode}")
        print(f"📝 Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error running {script_name}: {e}")
        return False

def main():
    """Main pipeline execution"""
    print("🔥 BIG ALPHA KINGS AUTOMATED DATA PIPELINE 🔥")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
    print("=" * 60)
    
    # Get the repository root directory
    repo_root = Path(__file__).parent.absolute()
    print(f"📁 Working directory: {repo_root}")
    
    # Define the pipeline steps
    pipeline_steps = [
        {
            "script": repo_root / "Scrapers" / "MasterScraper.py",
            "name": "MasterScraper (BLS Data Download)"
        },
        {
            "script": repo_root / "theBehemoth.py", 
            "name": "theBehemoth (Data Consolidation)"
        },
        {
            "script": repo_root / "Scrapers" / "master_updater.py",
            "name": "master_updater (Process + Upload + Git)"
        }
    ]
    
    # Execute pipeline
    success_count = 0
    for step in pipeline_steps:
        if step["script"].exists():
            if run_script(step["script"], step["name"]):
                success_count += 1
            else:
                print(f"💥 Pipeline failed at: {step['name']}")
                sys.exit(1)
        else:
            print(f"❌ Script not found: {step['script']}")
            sys.exit(1)
    
    # Final success message
    print("=" * 60)
    print(f"🎉 PIPELINE COMPLETE! All {success_count}/{len(pipeline_steps)} steps successful!")
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
    print("🚀 AI data is now fresh and deployed!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())


