import json
import os
import requests

# Path to your JSON file
JSON_FILE = "merged_plugins.json"
# Output directory to save plugins
OUTPUT_DIR = "plugins_apr10"
# Jenkins plugin download URL template
PLUGIN_URL_TEMPLATE = "https://updates.jenkins.io/download/plugins/{name}/{version}/{name}.hpi"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load JSON data
with open(JSON_FILE, "r") as file:
    plugins = json.load(file)

# Download each plugin
for plugin_name, version in plugins.items():
    url = PLUGIN_URL_TEMPLATE.format(name=plugin_name, version=version)
    output_path = os.path.join(OUTPUT_DIR, f"{plugin_name}.hpi")

    print(f"Downloading {plugin_name} ({version})...")

    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✔ Saved to {output_path}")
    else:
        print(f"❌ Failed to download {plugin_name} ({version}). HTTP {response.status_code}")

