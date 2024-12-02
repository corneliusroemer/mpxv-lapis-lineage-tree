# %%
import os
import pathlib
from typing import Any

import yaml
from git import Repo

# %%

REPO_URL = "https://github.com/mpxv-lineages/lineage-designation"
LOCAL_DIR = "./lineage-designation/"
try:
    repo = Repo.clone_from(REPO_URL, LOCAL_DIR)
except:
    print("Repo already cloned")

# %%

# Folder containing lineage YAML files
# input_folder = LOCAL_DIR / "lineages"
input_folder = pathlib.Path(LOCAL_DIR) / "lineages"
output_file = "lineage_dag.yaml"

# Dictionary to store the DAG
lineage_dag = {}

# Iterate through each YAML file in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".yml") or filename.endswith(".yaml"):
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r") as file:
            lineage_data: dict[str, Any] = yaml.safe_load(file)
            name = lineage_data.get("name")
            parent = lineage_data.get("parent")
            alias = lineage_data.get("alias")
            unaliased_name = lineage_data.get("unaliased_name")

            # Ensure name entry exists in DAG
            if name not in lineage_dag:
                lineage_dag[name] = {
                    "parents": [],
                    "aliases": [],
                }

            # Add parent if available
            if parent and parent != "None":
                lineage_dag[name]["parents"].append(parent)

            # Add aliases
            if alias:
                lineage_dag[name]["aliases"].append(alias)
            if unaliased_name and unaliased_name != name:
                lineage_dag[name]["aliases"].append(unaliased_name)

# Add some extra fields like None
lineage_dag["None"] = {
    "parents": [],
    "aliases": ["Unknown", "Unassigned", "Outgroup"],
}

# Write the DAG to a consolidated YAML file
with open(output_file, "w") as output:
    yaml.dump(lineage_dag, output, default_flow_style=False)

print(f"Lineage DAG written to {output_file}")

# %%
