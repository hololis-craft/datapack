import json
import os
from base64 import b64encode

name_tags = [
    "tokinosorach",
    "robocosan",
    "AZKi_",
    "sakuramiko35",
    "Suisei_HONMONO",
    "SUISEI_HOSIMATI",
    "yozoramel",
    "akirosenthal",
    "HAACHAMA810",
    "natsuiromatsuri",
    "murasakishion",
    "nakiriayame",
    "yuzukichoco",
    "oozorasubaru",
    "shirakamifubuki",
    "ookamimio",
    "okayu_nekoneko22",
    "nekomata_okayu",
    "inugamikorone",
    "Usadapekora",
    "shiranuiflare",
    "shiroganenoel",
    "houshou_marine",
    "uruharushia",
    "Amane_Kanata",
    "Tsunomakiwatame",
    "Towasama",
    "HimemoriLuna",
    "Lamy_Yukihana",
    "supernenechii",
    "botaaan",
    "omapol",
    "Laplus_sama",
    "takanelui61",
    "KoyoriHakui315",
    "matamatasakamata",
    "Kazama168",
    "Ayunda_Risu",
    "itsmoona",
    "imoonya",
    "IOFI15",
    "kureijiollie",
    "anyaaaaam3lfi",
    "reineeeee",
    "VestiaZeta_V7",
    "lakaela",
    "KobokanAer",
    "moricalliopeEN",
    "Kiara_HOLOEN",
    "NinoIna",
    "GaaoGura",
    "amwatson",
    "IRySuperGlue",
    "faunaceres",
    "ourkronii",
    "nana_mumei",
    "whatabae",
    "ShioriNyavella",
    "KosekiBijou",
    "RissaRavencroft",
    "fluffyFUWAWA",
    "fuzzyMOCOCO",
    "ERBloodflame",
    "gigigimurin",
    "imgreen1",
    "Raoraaa",
    "Hiodoshi_Ao",
    "Kanade_ReGLOSS",
    "Ichijou_Ririka",
    "juufuutei_raden",
    "todoroki_hajime",
    "isaki_riona",
    "koganei_niko",
    "mizumiya_su",
    "rindo_chihaya",
    "kikirara_vivi",
    "minatoaqua",
    "kiryucoco",
    "bigSANA",
    "achan_UGA",
]

SCRIPT_DIR = os.path.dirname(__file__)
DATAPACK_BASE_DIR = os.path.join(
    SCRIPT_DIR, "..", "datapacks", "hololis", "data", "hololis"
)
LOOT_TABLE_PATH = os.path.join(
    DATAPACK_BASE_DIR,
    "loot_table",
    "holomem",
    "player_heads.json",
)
ADVANCEMENT_PATH = os.path.join(
    DATAPACK_BASE_DIR,
    "advancement",
    "holoheads",
    "all_heads.json",
)
PLAYER_ADVANCEMENT_DIR = os.path.join(
    DATAPACK_BASE_DIR,
    "advancement",
    "holoheads",
    "player_heads",
)


def fetch_player_skins():
    import requests

    player_skins = {}
    for name_tag in name_tags:
        try:
            player_info = requests.get(
                f"https://crafty.gg/players/{name_tag}.json",
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                    "Cookie": "userid=7e6fe6ff-7ae3-4bb1-853a-72a7e62eec76; ph_phc_MikTdLzdbwMK2UQ1Gg7RDl8WQRIh4GgKl12Tyf2Igaq_posthog=%7B%22distinct_id%22%3A%220196cf35-9909-7e4e-804f-69e93ef2dcbe%22%2C%22%24sesid%22%3A%5B1747233390128%2C%220196cf35-990c-782a-a578-3cfb7f3b7253%22%2C1747233118476%5D%7D",
                },
            )
            if player_info.status_code != 200:
                print(f"Failed to fetch data for {name_tag}: {player_info.status_code}")
                continue

            json_data = json.loads(player_info.text)
            player_skins[name_tag] = json_data["skins"]
            print(f"Fetched {len(json_data['skins'])} skins for {name_tag}")

        except Exception as e:
            print(f"Error processing {name_tag}: {e}")

    return player_skins


def make_texture_value(skin_hash):
    skin_url = f"https://textures.minecraft.net/texture/{skin_hash}"
    texture_json = {"textures": {"SKIN": {"url": skin_url}}}
    return b64encode(json.dumps(texture_json).encode("utf-8")).decode("utf-8")


def make_loot_table(player_skins):
    loot_table = {
        "type": "minecraft:empty",
        "pools": [
            {
                "entries": [],
                "rolls": 1,
            }
        ],
    }

    for name_tag, skins in player_skins.items():
        try:
            for skin in skins:
                texture_value = make_texture_value(skin["hash"])

                player_head = {
                    "type": "minecraft:item",
                    "name": "minecraft:player_head",
                    "functions": [
                        {
                            "function": "minecraft:set_components",
                            "components": {
                                "minecraft:profile": {
                                    "name": name_tag,
                                    "properties": [
                                        {
                                            "name": "textures",
                                            "value": texture_value,
                                        }
                                    ],
                                }
                            },
                        }
                    ],
                }

                loot_table["pools"][0]["entries"].append(player_head)
                print(f"Added {name_tag} head with skin {skin['hash']} to loot table")

        except Exception as e:
            print(f"Error creating loot table entry for {name_tag}: {e}")

    return loot_table


def make_all_heads_advancement():
    criteria = {}
    requirements = []

    for name_tag in name_tags:
        criteria[name_tag] = {
            "trigger": "minecraft:inventory_changed",
            "conditions": {
                "items": [
                    {
                        "items": "minecraft:player_head",
                        "components": {
                            "minecraft:profile": {
                                "name": name_tag,
                            }
                        },
                    }
                ]
            },
        }
        requirements.append([name_tag])

    return {
        "display": {
            "title": {"translate": "頭コレクター"},
            "description": "すべてのホロメンの頭を集める",
            "icon": {
                "id": "minecraft:player_head",
                "components": {
                    "minecraft:profile": {"name": "supernenechii"},
                    "minecraft:enchantment_glint_override": True,
                },
            },
            "announce_to_chat": True,
            "show_toast": True,
        },
        "criteria": criteria,
        "requirements": requirements,
        "parent": "hololis:holomem/root",
    }


def make_unique_skin_hashes(skins):
    unique_hashes = []
    seen = set()
    for skin in skins:
        skin_hash = skin["hash"]
        if skin_hash in seen:
            continue
        seen.add(skin_hash)
        unique_hashes.append(skin_hash)
    return unique_hashes


def make_player_all_heads_advancement_from_texture_values(name_tag, texture_values):
    criteria = {}
    requirements = []

    if not texture_values:
        return None

    for i, texture_value in enumerate(texture_values, start=1):
        criterion_name = f"skin_{i:02}"
        criteria[criterion_name] = {
            "trigger": "minecraft:inventory_changed",
            "conditions": {
                "items": [
                    {
                        "items": "minecraft:player_head",
                        "components": {
                            "minecraft:profile": {
                                "name": name_tag,
                                "properties": [
                                    {
                                        "name": "textures",
                                        "value": texture_value,
                                    }
                                ],
                            }
                        },
                    }
                ]
            },
        }
        requirements.append([criterion_name])

    return {
        "display": {
            "title": {"text": name_tag},
            "description": f"{name_tag} の頭を全種類集める",
            "icon": {
                "id": "minecraft:player_head",
                "components": {
                    "minecraft:profile": {
                        "name": name_tag,
                        "properties": [
                            {
                                "name": "textures",
                                "value": texture_values[0],
                            }
                        ],
                    },
                    "minecraft:enchantment_glint_override": True,
                },
            },
            "announce_to_chat": True,
            "show_toast": True,
        },
        "criteria": criteria,
        "requirements": requirements,
        "parent": "hololis:holomem/root",
    }


def make_player_all_heads_advancement(name_tag, skins):
    unique_hashes = make_unique_skin_hashes(skins)
    texture_values = [make_texture_value(skin_hash) for skin_hash in unique_hashes]
    return make_player_all_heads_advancement_from_texture_values(
        name_tag, texture_values
    )


def write_player_advancements(player_skins):
    for name_tag, skins in player_skins.items():
        advancement = make_player_all_heads_advancement(name_tag, skins)
        if advancement is None:
            continue
        path = os.path.join(PLAYER_ADVANCEMENT_DIR, f"{name_tag}.json")
        write_json(path, advancement)
        print(f"Done creating player advancement: {path}")


def load_player_skins_from_loot_table(path):
    with open(path, "r", encoding="utf-8") as f:
        loot_table = json.load(f)

    player_skins = {}
    entries = loot_table.get("pools", [{}])[0].get("entries", [])

    for entry in entries:
        components = entry["functions"][0]["components"]
        profile = components["minecraft:profile"]
        name_tag = profile["name"]
        texture_value = profile["properties"][0]["value"]
        player_skins.setdefault(name_tag, []).append({"texture_value": texture_value})

    return player_skins


def make_player_all_heads_advancement_from_loot_table(name_tag, skins):
    unique_values = []
    seen = set()
    for skin in skins:
        texture_value = skin["texture_value"]
        if texture_value in seen:
            continue
        seen.add(texture_value)
        unique_values.append(texture_value)

    return make_player_all_heads_advancement_from_texture_values(
        name_tag, unique_values
    )


def write_player_advancements_from_loot_table(path):
    player_skins = load_player_skins_from_loot_table(path)
    for name_tag, skins in player_skins.items():
        advancement = make_player_all_heads_advancement_from_loot_table(name_tag, skins)
        if advancement is None:
            continue
        output_path = os.path.join(PLAYER_ADVANCEMENT_DIR, f"{name_tag}.json")
        write_json(output_path, advancement)
        print(f"Done creating player advancement: {output_path}")


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    player_skins = fetch_player_skins()
    loot_table = make_loot_table(player_skins)
    write_json(LOOT_TABLE_PATH, loot_table)
    print(f"Done creating loot table: {LOOT_TABLE_PATH}")

    advancement = make_all_heads_advancement()
    write_json(ADVANCEMENT_PATH, advancement)
    print(f"Done creating advancement: {ADVANCEMENT_PATH}")
    write_player_advancements(player_skins)


if __name__ == "__main__":
    main()
