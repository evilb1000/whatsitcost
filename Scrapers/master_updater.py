import subprocess
from pathlib import Path
from datetime import datetime
import os

# === Define pipeline order ===
pipeline_steps = [
    "/Users/benatwood/PycharmProjects/WhatsItCost/Scrapers/Behometh Injector.py",
    "/Users/benatwood/PycharmProjects/WhatsItCost/prepare_data.py",
    "/Users/benatwood/PycharmProjects/WhatsItCost/GPT_Tools/cluster_JSON_creator.py",
    "/Users/benatwood/PycharmProjects/WhatsItCost/Scrapers/execsummary.py",
    "/Users/benatwood/PycharmProjects/WhatsItCost/frontend/updateFirestor.py"  # 🔥 Auto-sync to Firestore
]

print("🚀 Starting full sync pipeline...\n")

for script in pipeline_steps:
    name = Path(script).stem
    print(f"🔧 Running: {name}")
    try:
        subprocess.run(["python3", script], check=True)
        print(f"✅ {name} complete\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ {name} failed with error code {e.returncode}")
        break
else:
    # === Git push block only runs if all scripts succeeded ===
    print("📦 Committing changes to Git...")

    try:
        # === Move to actual Git repo root dynamically
        repo_root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip())
        os.chdir(repo_root)

        # === Detect Git branch
        branch = subprocess.check_output(["git", "branch", "--show-current"]).decode().strip()

        # === Define tracked files
        tracked_files = [
            "AIBrain/theBehemoth.csv",
            "AIBrain/JSONS/material_trendlines.json",
            "AIBrain/JSONS/material_trends.json",
            "AIBrain/JSONS/material_spikes.json",
            "AIBrain/JSONS/material_rolling.json",
            "AIBrain/JSONS/material_rolling_12mo.json",
            "AIBrain/JSONS/material_rolling_3yr.json",
            "AIBrain/JSONS/material_correlations.json",
            "AIBrain/JSONS/latest_snapshot.json",
            "AIBrain/JSONS/cluster_data.json"
        ]

        # === Print what will be staged
        print("🗂 Staging files:")
        for f in tracked_files:
            print("  -", f)

        # === Stage all tracked files
        subprocess.run(["git", "add", *tracked_files], check=True)

        # === Commit + Push
        snapshot_tag = datetime.now().strftime("auto-sync-%Y%m%d-%H%M")
        commit_msg = f"🧠 Auto-sync: BLS JSONs + Exec Summary + Firestore [{snapshot_tag}]"

        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", branch], check=True)

        print("✅ Git push complete.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Git push failed: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error during Git operations: {e}")

print("\n🎉 Full pipeline finished.")
