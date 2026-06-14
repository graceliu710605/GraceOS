import json

def search(keyword):

    with open(
        r"E:\知识库obsidian\02_Projects\graceos\09_Database\software_assets\software_inventory.json",
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    result = []

    for item in data:

        if keyword.lower() in item["raw"].lower():

            result.append(item["raw"])

    return result