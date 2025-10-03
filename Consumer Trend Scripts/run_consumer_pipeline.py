#!/usr/bin/env python3
"""
Consumer Trends Pipeline - Master Script
Chains together: fred_batch_pull → calculate_metrics → upload_to_firestore
One script to rule them all! 🔥
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import os


def run_script(script_path: str, script_name: str, *args) -> bool:
    """Run a script and handle errors"""
    print(f"🚀 Running: {script_name}")
    
    cmd = [sys.executable, script_path] + list(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ {script_name} completed successfully")
        if result.stdout:
            print(f"📝 Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {script_name} failed with error code {e.returncode}")
        if e.stderr:
            print(f"📝 Error output: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error running {script_name}: {e}")
        return False


def main() -> int:
    """Main pipeline execution"""
    print("🔥 CONSUMER TRENDS PIPELINE - BIG ALPHA KING STYLE 🔥")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
    print("=" * 70)
    
    # Get the scripts directory
    scripts_dir = Path(__file__).parent.absolute()
    data_dir = scripts_dir.parent / "Consumer Trend Data"
    
    print(f"📁 Scripts directory: {scripts_dir}")
    print(f"📊 Data directory: {data_dir}")
    
    # Pipeline steps
    pipeline_steps = [
        {
            "script": scripts_dir / "fred_batch_pull.py",
            "name": "FRED Data Pull",
            "args": [
                "--api-key", "6af5cb112e0c7a9ac1a27238e7848047",
                "--start", "1980-01-01",
                "--outdir", str(data_dir)
            ]
        },
        {
            "script": scripts_dir / "calculate_metrics.py",
            "name": "Calculate Metrics",
            "args": ["--datadir", str(data_dir)]
        },
        {
            "script": scripts_dir / "upload_to_firestore.py",
            "name": "Upload to Firestore",
            "args": ["--datadir", str(data_dir)]
        }
    ]
    
    # Execute pipeline
    success_count = 0
    failed_step = None
    
    for step in pipeline_steps:
        if step["script"].exists():
            if run_script(step["script"], step["name"], *step["args"]):
                success_count += 1
                print()  # Add spacing between steps
            else:
                failed_step = step["name"]
                print(f"\n💥 Pipeline failed at: {step['name']}")
                break
        else:
            print(f"❌ Script not found: {step['script']}")
            failed_step = step["name"]
            break
    
    # Final status
    print("=" * 70)
    if success_count == len(pipeline_steps):
        print(f"🎉 PIPELINE COMPLETE! All {success_count} steps successful!")
        print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
        print("🚀 Consumer Spending Indicators are fresh and live!")
        return 0
    else:
        print(f"💥 PIPELINE FAILED at: {failed_step}")
        print(f"✅ Completed: {success_count}/{len(pipeline_steps)} steps")
        return 1


if __name__ == "__main__":
    sys.exit(main())
