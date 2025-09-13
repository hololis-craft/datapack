import yaml
from mojangson import parse
from pprint import pprint
import csv


with open("base.yaml", "r") as file:
    data = yaml.safe_load(file)


def item_id_to_type(item_id: str) -> str:
    if "helmet" in item_id:
        return "(頭)"
    elif "chestplate" in item_id:
        return "(胴)"
    elif "leggings" in item_id:
        return "(脚)"
    elif "boots" in item_id:
        return "(足)"

    return item_id


def trim_mc(id: str | None) -> str | None:
    if id is None:
        return None
    return id.replace("minecraft:", "")


# Read mapping.csv
with open("mapping.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    mapping = {rows[0]: rows[1] for rows in reader}

final_items = []

for item_key in data["items_for_sale"].keys():
    value = data["items_for_sale"][item_key]
    container = value["item"]["components"]["minecraft:container"]
    container_parsed = parse(container)
    for shulker in container_parsed["value"]["value"]:
        custom_name = shulker["item"]["value"]["components"]["value"][
            "minecraft:custom_name"
        ]["value"]
        costume_items = shulker["item"]["value"]["components"]["value"][
            "minecraft:container"
        ]["value"]["value"]
        # print(f"Custom Name: {custom_name}")
        # print("Costume Items:")
        for costume_item in costume_items:
            item_id = costume_item["item"]["value"]["id"]["value"]
            item_count = costume_item["item"]["value"]["count"]["value"]
            item_type = item_id_to_type(item_id)
            components = (
                costume_item["item"]["value"].get("components", {}).get("value", {})
            )

            dyed_color = components.get("minecraft:dyed_color", {}).get("value")
            trim = components.get("minecraft:trim", {}).get("value", {})
            trim_material = trim.get("material", {}).get("value")
            trim_pattern = trim.get("pattern", {}).get("value")
            print(custom_name)
            # print(
            #     f"  - Item ID: {item_id}, Count: {item_count}, Type: {item_type}, Dyed Color: {dyed_color}, Trim Material: {trim_material}, Trim Pattern: {trim_pattern}"
            # )
            final_name = f"{custom_name} {item_type}"
            mapped_mcid = mapping.get(custom_name)
            final_items.append(
                {
                    "name": final_name,
                    "base_item": trim_mc(item_id),
                    # "count": item_count,
                    "dyed_color": dyed_color,
                    "trim_material": trim_mc(trim_material),
                    "trim_pattern": trim_mc(trim_pattern),
                    "mcid": mapped_mcid,
                }
            )
    # break


# Write to CSV

with open("costume_items.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = [
        "name",
        "base_item",
        # "count",
        "dyed_color",
        "trim_material",
        "trim_pattern",
        "mcid",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in final_items:
        writer.writerow(item)
