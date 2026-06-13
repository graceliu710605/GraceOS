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
        # Search across all fields: name, id, publisher
        search_str = " ".join(str(v) for v in [item.get("name",""), item.get("id",""), item.get("publisher","")])
        if keyword.lower() in search_str.lower():
            result.append(item.get("name", str(item)))

    return result