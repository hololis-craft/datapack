import json
import os
from base64 import b64encode
import requests

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

loot_table = {
    "type": "minecraft:empty",
    "pools": [
        {
            "entries": [],
            "rolls": 1,
        }
    ],
}

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

        for skin in json_data["skins"]:
            skin_url = f"https://textures.minecraft.net/texture/{skin['hash']}"

            # Create texture JSON structure
            texture_json = {"textures": {"SKIN": {"url": skin_url}}}

            # Convert to base64
            texture_value = b64encode(json.dumps(texture_json).encode("utf-8")).decode(
                "utf-8"
            )

            # Create loot table
            player_head = {
                "type": "minecraft:item",
                "name": "minecraft:player_head",
                "functions": [
                    {
                        "function": "minecraft:set_components",
                        "components": {
                            "minecraft:profile": {
                                "properties": [
                                    {
                                        "name": "textures",
                                        "value": texture_value,
                                    }
                                ]
                            }
                        },
                    }
                ],
            }

            loot_table["pools"][0]["entries"].append(player_head)

            print(f"Added {name_tag} head with skin {skin['hash']} to loot table")

    except Exception as e:
        print(f"Error processing {name_tag}: {e}")

# Save loot table to file
with open("player_heads.json", "w") as f:
    json.dump(loot_table, f, indent=4)
print("Done creating loot tables")
