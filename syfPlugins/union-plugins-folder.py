import os
import json

# Set the path to the folder containing JSON files
#folder_path = "path/to/your/folder"  # 🔁 Replace this with your actual folder path

# Initialize a set to hold all unique plugin IDs
plugin_ids = set()

# Loop through all JSON files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                plugins = json.load(f)
                plugin_ids.update(plugin["id"] for plugin in plugins)
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"⚠️ Skipping {filename} due to error: {e}")

# Format the result as required
union_plugins = [{"id": plugin_id} for plugin_id in sorted(plugin_ids)]

# Write the output to union-plugins.json
with open("union-plugins.json", "w", encoding="utf-8") as outfile:
    json.dump(union_plugins, outfile, indent=4)

print("✅ Union plugin list written to 'union-plugins.json'")

