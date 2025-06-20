import subprocess
from pathlib import Path

# === Define pipeline order ===
pipeline_steps = [
    "/Users/benatwood/PycharmProjects/WhatsItCost/Scrapers/Behometh Injector.py",
    "/Users/benatwood/PycharmProjects/WhatsItCost/prepare_data.py",
    "/Users/benatwood/PycharmProjects/WhatsItCost/GPT_Tools/cluster_JSON_creator.py",
    "/Users/benatwood/PycharmProjects/WhatsItCost/Scrapers/execsummary.py"
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
    # === Only run Git push if everything succeeds ===
    print("📦 Committing changes to Git...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "🧠 Auto-sync: Behemoth + GPT JSONs updated"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Git push complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git push failed: {e}")

print("\n🎉 Full pipeline finished.")
