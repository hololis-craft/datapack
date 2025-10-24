from typing import Dict, List, Literal
from google.oauth2.service_account import Credentials
import gspread
from jinja2 import Environment, FileSystemLoader
import hashlib
from yaml import safe_dump
import datetime

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/10czE4OoQ-3k_SK0TGciAh9-b14DudNp1JeHLyQRd80g/edit#gid=0"
ITEM_OUTPUT = "./pack/Items/generated-outfit-items.yml"
DISGUISE_SKILL_OUTPUT = "./pack/Skills/generated-disguise.yml"
MARKET_OUTPUT = "./pack/generated-vm-items.yml"

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = Credentials.from_service_account_file(
    "../google-credentials.json", scopes=scopes
)

gc = gspread.authorize(credentials)


def is_valid_entry(entry):
    return (
        entry.get("No") not in (None, "")
        and entry.get("基礎アイテム") not in (None, "")
        and entry.get("装備名 (MiniMessage)") not in (None, "")
        and entry.get("耐久値") not in (None, "")
    )


spreadsheet = gc.open_by_url(SPREADSHEET_URL)
all_entries = spreadsheet.get_worksheet(0).get_all_records()
all_entries = [e for e in all_entries if is_valid_entry(e)]

ordered_groups = []
grouped_entries: Dict[str, List[dict]] = {}

for entry in all_entries:
    group_name = str(entry.get("内部グループ名"))
    if group_name in (None, "", "None"):
        continue
    if group_name not in grouped_entries:
        grouped_entries[group_name] = []
        ordered_groups.append(group_name)
    grouped_entries[group_name].append(entry)

env = Environment(loader=FileSystemLoader("./templates"), autoescape=False)
item_template = env.get_template("outfit-item.yml.j2")
disguise_skill_template = env.get_template("disguise-skill.yml.j2")

# {'No': 34,
#  '内部グループ名': '夜空メル概念衣装',
#  '装備名 (MiniMessage)': '夜空メル概念衣装 (胴)',
#  '基礎アイテム': 'leather_chestplate',
#  '耐久値': 532,
#  '染色(皮装備)': 14207412,
#  '装飾アイテム': 'netherite',
#  '装飾パターン': 'wayfinder',
#  '(変身) MCID': 'yozoramel',
#  '(変身) テクスチャHash': ''


def villager_market_slot_id(
    offset: int, type: Literal["Helmet", "Chestplate", "Leggings", "Boots"]
) -> int:
    type_index = {
        "Helmet": 0,
        "Chestplate": 9,
        "Leggings": 9 * 2,
        "Boots": 9 * 3,
    }[type]
    page = int(offset / 9)
    base_slot = page * 5 * 9 + (offset % 9)
    return base_slot + type_index


# Hash化されたグループ名を返す
def group_key(entry):
    return hashlib.sha1(entry["内部グループ名"].encode("utf-8")).hexdigest()[:10]


def get_kind_from_item(
    item_name,
) -> Literal["Helmet", "Chestplate", "Leggings", "Boots", "Unknown"]:
    if "helmet" in item_name:
        return "Helmet"
    elif "chestplate" in item_name:
        return "Chestplate"
    elif "leggings" in item_name:
        return "Leggings"
    elif "boots" in item_name:
        return "Boots"
    else:
        return "Unknown"


def group_has_disguise(group_name):
    entries = grouped_entries[group_name]
    for entry in entries:
        if "(変身) MCID" not in entry and "(変身) テクスチャHash" not in entry:
            return False
    group_kinds = set(
        [
            get_kind_from_item(str(e["基礎アイテム"]).lower())
            for e in grouped_entries[group_name]
        ]
    )
    if group_kinds == {"Helmet", "Chestplate", "Leggings", "Boots"}:
        return True
    return False


def has_disguise(entry):
    # 内部グループ名が未記入なら変身スキルを生成しない
    if "内部グループ名" not in entry or entry["内部グループ名"] == "":
        return False
    # 内部グループ名が一致するアイテムが4つ揃っている + 種類がHelmet, Chestplate, Leggings, Bootsの4種類である
    group_name = entry["内部グループ名"]
    if group_has_disguise(group_name):
        return True
    return False


items_list = []
disguise_skills_list = []
market_items = {}


def create_market_item(entry):
    return {
        "item": {
            "==": "org.bukkit.inventory.ItemStack",
            "DataVersion": 4440,
            "id": "minecraft:paper",
            "count": 1,
            "components": {
                "minecraft:custom_data": f'{{PublicBukkitValues:{{"mythicmobs:type":"Outfit-{entry["No"]}"}}}}'
            },
            "schema_version": 1,
        },
        "amount": 1,
        "trade_amount": 0,
        "price": float(1),
        "buy_price": float(1),
        "mode": "SELL",
        "buy_limit": 0,
        "command": [],
        "server_trades": 0,
        "limit_mode": "PLAYER",
        "cooldown": "never",
        "discount": {"amount": 0, "end": 0},
        "allow_custom_amount": True,
        "next_reset": 0,
    }


def color_int_to_rgb(color_int):
    if color_int is None or color_int == "":
        return None
    color_int = int(color_int)
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return f"{r},{g},{b}"


def minify_yaml(text: str) -> str:
    # Remove comments and empty lines
    lines = text.splitlines()
    minified_lines = []
    for line in lines:
        stripped_line = line.split("#", 1)[0].rstrip()  # Remove comments
        if stripped_line:  # Only add non-empty lines
            minified_lines.append(stripped_line)
    return "\n".join(minified_lines)


def create_item(entry):
    kind = get_kind_from_item(str(entry["基礎アイテム"]).lower())
    item_data = {
        "num": entry["No"],
        "base_item": entry["基礎アイテム"],
        "max_durability": entry["耐久値"],
        "display_name": entry["装備名 (MiniMessage)"],
        "kind": kind,
        "generation_unixtime": int(datetime.datetime.now().timestamp()),
    }
    if entry.get("染色(皮装備)") not in (None, ""):
        item_data["color_code"] = color_int_to_rgb(entry["染色(皮装備)"])
    if entry.get("装飾アイテム") not in (None, "") and entry.get(
        "装飾パターン"
    ) not in (None, ""):
        item_data["trim_material"] = entry["装飾アイテム"]
        item_data["trim_pattern"] = entry["装飾パターン"]
    if has_disguise(entry):
        item_data["has_disguise"] = True
    if "内部グループ名" in entry and entry["内部グループ名"] != "":
        item_data["group_name"] = entry["内部グループ名"]
        item_data["group_key"] = group_key(entry)

    return minify_yaml(item_template.render(item_data))


previous_index = 0
previous_group = None
previous_gen = None
for entry in all_entries:
    items_list.append(create_item(entry))
    if "内部グループ名" not in entry or entry["内部グループ名"] == "":
        continue
    kind = get_kind_from_item(str(entry["基礎アイテム"]).lower())
    if kind == "Unknown":
        continue
    group_name = entry.get("内部グループ名", "")

    current_gen = entry.get("期生", None)

    if current_gen is not None and current_gen != "":
        if previous_gen is not None and current_gen != previous_gen:
            previous_index += 8 - (previous_index % 9)
        previous_gen = current_gen

    if group_name != previous_group and previous_group is not None:
        previous_index += 1

    previous_group = group_name

    market_slot = str(villager_market_slot_id(previous_index, kind))
    market_items[market_slot] = create_market_item(entry)

for group_name, entries in grouped_entries.items():
    if group_has_disguise(group_name):
        mcid = entries[0].get("(変身) MCID", "")
        texture_hash = entries[0].get("(変身) テクスチャHash", "")

        item_nums = {}
        for entry in entries:
            kind = get_kind_from_item(str(entry["基礎アイテム"]).lower())
            item_nums[kind] = entry["No"]
        skill_data = {
            "group_key": group_key(entries[0]),
            "head_item": item_nums.get("Helmet", ""),
            "chest_item": item_nums.get("Chestplate", ""),
            "legs_item": item_nums.get("Leggings", ""),
            "feet_item": item_nums.get("Boots", ""),
            "disguise_name": group_name,
            "disguise_skin": mcid,
        }
        disguise_skills_list.append(
            minify_yaml(disguise_skill_template.render(skill_data))
        )

with open(ITEM_OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(items_list))

with open(DISGUISE_SKILL_OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(disguise_skills_list))

with open(MARKET_OUTPUT, "w", encoding="utf-8") as f:
    f.write(safe_dump({"items_for_sale": market_items}, sort_keys=False))
