import json

# 🔁 Replace with your actual absolute file paths
file1_path = "/Users/mgangwal/Documents/synchrony/pluginValidation/nocasc-plugins.json"
file2_path = "/Users/mgangwal/Documents/synchrony/pluginValidation/union-plugins.json"

# Load plugin data from both files
with open(file1_path, 'r') as f1:
    plugins1 = json.load(f1)

with open(file2_path, 'r') as f2:
    plugins2 = json.load(f2)

# Extract plugin IDs
ids1 = {plugin["id"] for plugin in plugins1}
ids2 = {plugin["id"] for plugin in plugins2}

# Compute the difference: plugins in file1 but not in file2
diff_ids = ids1 - ids2

# Format the result
diff_plugins = [{"id": plugin_id} for plugin_id in sorted(diff_ids)]

# Write to diff-plugins.json
with open("diff-plugins.json", "w") as outfile:
    json.dump(diff_plugins, outfile, indent=4)

print("✅ Difference written to 'diff-plugins.json'")

