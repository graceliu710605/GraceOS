import json

def search(keyword):

    with open(
        r"E:\创业项目\GraceOS\09_Database\software_assets\software_inventory.json",
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    result = []

    for item in data:

        if keyword.lower() in item["raw"].lower():

            result.append(item["raw"])

    return result