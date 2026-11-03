#!/usr/bin/env python3
"""
Generates every asset, data file and the Java definition table for World Foods
from tools/content.py.

    python3 tools/generate.py

Requires Pillow (pip install pillow).
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import CROPS, FOODS, CUISINES  # noqa: E402
import textures  # noqa: E402

MODID = "worldfoods"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RES = os.path.join(ROOT, "src", "main", "resources")
ASSETS = os.path.join(RES, "assets", MODID)
DATA = os.path.join(RES, "data", MODID)
JAVA = os.path.join(ROOT, "src", "main", "java", "com", "worldfoods", "content", "GeneratedDefs.java")


VANILLA_TR = {
    "apple": "Elma", "baked_potato": "Fırınlanmış Patates", "beef": "Çiğ Sığır Eti", "beetroot": "Pancar",
    "bowl": "Kase", "bread": "Ekmek", "brown_mushroom": "Kahverengi Mantar", "carrot": "Havuç",
    "cocoa_beans": "Kakao Çekirdeği", "cod": "Çiğ Morina", "cooked_beef": "Biftek", "cooked_chicken": "Pişmiş Tavuk",
    "cooked_cod": "Pişmiş Morina", "cooked_mutton": "Pişmiş Koyun Eti", "cooked_porkchop": "Pişmiş Domuz Pirzolası",
    "dried_kelp": "Kurutulmuş Yosun", "egg": "Yumurta", "glass_bottle": "Cam Şişe", "honey_bottle": "Bal Şişesi",
    "melon_slice": "Karpuz Dilimi", "milk_bucket": "Süt Kovası", "mutton": "Çiğ Koyun Eti", "paper": "Kâğıt",
    "porkchop": "Çiğ Domuz Pirzolası", "potato": "Patates", "salmon": "Çiğ Somon", "snowball": "Kar Topu",
    "stick": "Çubuk", "sugar": "Şeker", "sweet_berries": "Tatlı Meyveler", "water_bucket": "Su Kovası",
    "wheat": "Buğday", "wheat_seeds": "Buğday Tohumu",
}


def ref(x):
    if x.startswith("wf:"):
        return f"{MODID}:{x[3:]}"
    if ":" in x:
        return x
    return f"minecraft:{x}"


def mix(a, b, t):
    """Blend two #rrggbb colours."""
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{int(x * t + y * (1 - t)):02x}" for x, y in zip(ca, cb))


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def clean():
    for p in (os.path.join(RES, "assets", MODID, "blockstates"),
              os.path.join(RES, "assets", MODID, "items"),
              os.path.join(RES, "assets", MODID, "models"),
              os.path.join(RES, "assets", MODID, "textures"),
              os.path.join(RES, "assets", MODID, "lang"),
              os.path.join(RES, "data"),
              os.path.join(ROOT, "src", "mc261", "resources", "data"),
              os.path.join(ROOT, "src", "mc263", "resources", "data")):
        if os.path.isdir(p):
            shutil.rmtree(p)


def crop_loot_tables(block, produce, seeds, lo, hi):
    """Returns {compat source set: loot table json} for a crop block."""
    blk = f"{MODID}:{block}"
    count = {"type": "minecraft:uniform", "min": lo, "max": hi}
    fortune_uniform = {"enchantment": "minecraft:fortune", "formula": "minecraft:uniform_bonus_count",
                       "parameters": {"bonusMultiplier": 1}}
    fortune_binomial = {"enchantment": "minecraft:fortune", "formula": "minecraft:binomial_with_bonus_count",
                        "parameters": {"extra": 1, "probability": 0.5714286}}

    # Minecraft 26.1 - 26.2
    age7 = [{"condition": "minecraft:block_state_property", "block": blk, "properties": {"age": "7"}}]
    legacy = {
        "type": "minecraft:block",
        "functions": [{"function": "minecraft:explosion_decay"}],
        "pools": [
            {"rolls": 1.0, "bonus_rolls": 0.0, "entries": [{"type": "minecraft:alternatives", "children": [
                {"type": "minecraft:item", "name": f"{MODID}:{produce}", "conditions": age7,
                 "functions": [{"function": "minecraft:set_count", "count": count},
                               {"function": "minecraft:apply_bonus", **fortune_uniform}]},
                {"type": "minecraft:item", "name": f"{MODID}:{seeds}"}]}]},
            {"rolls": 1.0, "bonus_rolls": 0.0, "conditions": age7, "entries": [
                {"type": "minecraft:item", "name": f"{MODID}:{seeds}",
                 "functions": [{"function": "minecraft:apply_bonus", **fortune_binomial}]}]},
        ],
        "random_sequence": f"{MODID}:blocks/{block}",
    }

    # Minecraft 26.3+
    ripe = {"type": "minecraft:match_block", "blocks": blk, "state": {"age": "7"}}
    modern = {
        "type": "minecraft:block",
        "modifier": {"type": "minecraft:explosion_decay"},
        "pools": [
            {"rolls": 1, "entries": [{"type": "minecraft:alternatives", "children": [
                {"type": "minecraft:item", "name": f"{MODID}:{produce}", "condition": ripe,
                 "modifier": [{"type": "minecraft:set_count", "count": count},
                              {"type": "minecraft:apply_bonus", **fortune_uniform}]},
                {"type": "minecraft:item", "name": f"{MODID}:{seeds}"}]}]},
            {"rolls": 1, "condition": ripe, "entries": [
                {"type": "minecraft:item", "name": f"{MODID}:{seeds}",
                 "modifier": {"type": "minecraft:apply_bonus", **fortune_binomial}}]},
        ],
        "random_sequence": f"{MODID}:blocks/{block}",
    }
    return {"mc261": legacy, "mc263": modern}


# ---------------------------------------------------------------------------
items = []          # (id, kind) in creative-tab order
lang_en = {}
lang_tr = {}
recipes = {}        # name -> json
shapeless_sets = {}
java_items = []     # java constructor strings
java_crops = []


def add_item_model(iid, style, colours, seed):
    write_json(f"{ASSETS}/items/{iid}.json", {"model": {"type": "minecraft:model", "model": f"{MODID}:item/{iid}"}})
    write_json(f"{ASSETS}/models/item/{iid}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MODID}:item/{iid}"}})
    os.makedirs(f"{ASSETS}/textures/item", exist_ok=True)
    textures.item_texture(style, colours, seed).save(f"{ASSETS}/textures/item/{iid}.png")


def add_shapeless(name, ingredients, result, count):
    key = tuple(sorted(ref(i) for i in ingredients))
    if key in shapeless_sets:
        raise SystemExit(f"Recipe conflict: {name} and {shapeless_sets[key]} use {key}")
    if len(ingredients) > 9:
        raise SystemExit(f"Too many ingredients in {name}")
    shapeless_sets[key] = name
    res = {"id": ref(result)}
    if count != 1:
        res["count"] = count
    recipes[name] = {"type": "minecraft:crafting_shapeless", "category": "misc",
                     "ingredients": [ref(i) for i in ingredients], "result": res}


def add_cooking(name, inp, result, xp, kinds=("smelting", "smoking", "campfire_cooking")):
    times = {"smelting": 200, "smoking": 100, "campfire_cooking": 600}
    for k in kinds:
        suffix = "" if k == "smelting" else "_from_" + ("smoking" if k == "smoking" else "campfire_cooking")
        recipes[name + suffix] = {"type": f"minecraft:{k}", "category": "food", "cookingtime": times[k],
                                  "experience": xp, "ingredient": ref(inp), "result": {"id": ref(result)}}


def java_str(s):
    return '"' + s.replace('"', '\\"') + '"'


def java_effects(effects):
    if not effects:
        return "List.of()"
    return "List.of(" + ", ".join(f"new Effect(MobEffects.{e}, {d}, {a})" for e, d, a in effects) + ")"


def java_food(iid, food, container="NONE", effects=None, remainder="null"):
    if food is None:
        return f"new FoodDef({java_str(iid)}, 0, 0f, Container.NONE, List.of(), null)"
    n, s = food
    return f"new FoodDef({java_str(iid)}, {n}, {s}f, Container.{container}, {java_effects(effects)}, {remainder})"


def main():
    clean()
    seed = 1

    # ---------------- crops ----------------
    seed_items = []
    produce_items = []
    for c in CROPS:
        cid = c["id"]
        block = f"{cid}_crop"
        seeds = f"{cid}_seeds"
        produce = c["produce"]
        seed_items.append(seeds)
        produce_items.append(produce)

        # names
        lang_en[f"block.{MODID}.{block}"] = c.get("crop_en", cid.replace("_", " ").title()) + " Crop"
        lang_tr[f"block.{MODID}.{block}"] = c["tr"].replace(" Çekirdeği", "").replace(" Yaprağı", "") + " Bitkisi"
        lang_en[f"item.{MODID}.{seeds}"] = c.get("seeds_en", c["en"] + " Seeds")
        lang_tr[f"item.{MODID}.{seeds}"] = c.get("seeds_tr", c["tr"] + " Tohumu")
        lang_en[f"item.{MODID}.{produce}"] = c["en"]
        lang_tr[f"item.{MODID}.{produce}"] = c["tr"]

        # blockstate & models (8 ages -> 4 visual stages, like potatoes)
        stage_of = [0, 0, 1, 1, 2, 2, 2, 3]
        write_json(f"{ASSETS}/blockstates/{block}.json",
                   {"variants": {f"age={a}": {"model": f"{MODID}:block/{block}_stage{stage_of[a]}"} for a in range(8)}})
        os.makedirs(f"{ASSETS}/textures/block", exist_ok=True)
        for st in range(4):
            write_json(f"{ASSETS}/models/block/{block}_stage{st}.json",
                       {"parent": "minecraft:block/crop", "textures": {"crop": f"{MODID}:block/{block}_stage{st}"}})
            textures.crop_texture(c["plant"], c["fruit"], st, seed).save(f"{ASSETS}/textures/block/{block}_stage{st}.png")

        # item models
        style, *cols = c["tex"]
        add_item_model(produce, style, cols, seed)
        add_item_model(seeds, "seeds", [c.get("seed_colour", mix(c["fruit"], "#b89a52", 0.45))], seed)
        seed += 1

        # loot table (format differs between 26.1-26.2 and 26.3+)
        lo, hi = c["drop"]
        for compat, table in crop_loot_tables(block, produce, seeds, lo, hi).items():
            write_json(f"{ROOT}/src/{compat}/resources/data/{MODID}/loot_table/blocks/{block}.json", table)

        # produce -> seeds
        add_shapeless(f"{seeds}_from_{produce}", [f"wf:{produce}"], f"wf:{seeds}", 1)

        java_crops.append(f"new CropDef({java_str(block)}, {java_str(seeds)}, {java_food(produce, c['food'], effects=c.get('effects'))})")

    # ---------------- foods ----------------
    food_items = []
    for f in FOODS:
        fid = f["id"]
        cont = f.get("c", "none").upper()
        rem = f.get("rem")
        rem_java = f"Items.{rem.upper()}" if rem else "null"
        style, *cols = f["tex"]

        if "raw" in f:
            raw_ings, raw_count, raw_tex = f["raw"]
            rid = f"raw_{fid}"
            lang_en[f"item.{MODID}.{rid}"] = "Raw " + f["en"]
            lang_tr[f"item.{MODID}.{rid}"] = "Çiğ " + f["tr"]
            add_item_model(rid, raw_tex[0], list(raw_tex[1:]), seed)
            add_shapeless(rid, raw_ings, f"wf:{rid}", raw_count)
            add_cooking(fid, f"wf:{rid}", f"wf:{fid}", 0.35)
            java_items.append(java_food(rid, None))
            food_items.append(rid)

        lang_en[f"item.{MODID}.{fid}"] = f["en"]
        lang_tr[f"item.{MODID}.{fid}"] = f["tr"]
        add_item_model(fid, style, cols, seed)
        seed += 1

        for i, r in enumerate(f.get("r", [])):
            name = fid if i == 0 else f"{fid}_{i + 1}"
            if r[0] == "shapeless":
                add_shapeless(name, r[1], f"wf:{fid}", r[2])
            elif r[0] == "cook":
                add_cooking(name, r[1], f"wf:{fid}", r[2])
            elif r[0] == "smelt":
                add_cooking(name, r[1], f"wf:{fid}", r[2], kinds=("smelting",))
        java_items.append(java_food(fid, f.get("food"), cont, f.get("effects"), rem_java))
        food_items.append(fid)

    for name, rec in recipes.items():
        write_json(f"{DATA}/recipe/{name}.json", rec)

    # ---------------- tags ----------------
    ids = lambda lst: [f"{MODID}:{x}" for x in lst]  # noqa: E731
    crop_blocks = [f"{c['id']}_crop" for c in CROPS]
    mc = os.path.join(RES, "data", "minecraft", "tags")
    common = os.path.join(RES, "data", "c", "tags")
    write_json(f"{mc}/block/crops.json", {"replace": False, "values": ids(crop_blocks)})
    write_json(f"{mc}/block/bee_growables.json", {"replace": False, "values": ids(crop_blocks)})
    write_json(f"{mc}/block/maintains_farmland.json", {"replace": False, "values": ids(crop_blocks)})
    write_json(f"{mc}/item/villager_plantable_seeds.json", {"replace": False, "values": ids(seed_items)})
    write_json(f"{mc}/item/chicken_food.json", {"replace": False, "values": ids(seed_items)})
    write_json(f"{mc}/item/parrot_food.json", {"replace": False, "values": ids(seed_items)})
    write_json(f"{common}/item/seeds.json", {"replace": False, "values": ids(seed_items)})
    write_json(f"{common}/item/crops.json", {"replace": False, "values": ids(produce_items)})
    edible = [c["produce"] for c in CROPS if c["food"]] + [f["id"] for f in FOODS if f.get("food")]
    write_json(f"{common}/item/foods.json", {"replace": False, "values": ids(edible)})
    write_json(f"{common}/block/crops.json", {"replace": False, "values": ids(crop_blocks)})

    # ---------------- lang ----------------
    lang_en[f"itemGroup.{MODID}"] = "World Foods"
    lang_tr[f"itemGroup.{MODID}"] = "Dünya Mutfağı"
    os.makedirs(f"{ASSETS}/lang", exist_ok=True)
    write_json(f"{ASSETS}/lang/en_us.json", dict(sorted(lang_en.items())))
    write_json(f"{ASSETS}/lang/tr_tr.json", dict(sorted(lang_tr.items())))

    textures.icon_texture().save(f"{ASSETS}/icon.png")

    # ---------------- java ----------------
    java = f"""// GENERATED FILE - DO NOT EDIT. Regenerate with: python3 tools/generate.py
package com.worldfoods.content;

import java.util.List;

import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.Items;

import static com.worldfoods.content.Defs.*;

public final class GeneratedDefs {{
\tprivate GeneratedDefs() {{
\t}}

\t/** Crops: block id, seeds id, produce definition. */
\tpublic static final List<CropDef> CROPS = List.of(
\t\t\t{(',' + chr(10) + chr(9) * 3).join(java_crops)}
\t);

\t/** Ingredients and dishes, in creative tab order. */
\tpublic static final List<FoodDef> FOODS = List.of(
\t\t\t{(',' + chr(10) + chr(9) * 3).join(java_items)}
\t);
}}
"""
    os.makedirs(os.path.dirname(JAVA), exist_ok=True)
    with open(JAVA, "w", encoding="utf-8") as fh:
        fh.write(java)

    # ---------------- README food table ----------------
    def tr_name(i):
        if i.startswith("wf:"):
            return lang_tr[f"item.{MODID}.{i[3:]}"]
        return VANILLA_TR.get(i, i)

    def recipe_text(f):
        parts = []
        if "raw" in f:
            ings, n, _ = f["raw"]
            parts.append(" + ".join(tr_name(i) for i in ings) + f" → Çiğ {f['tr']} → 🔥 pişir")
        for r in f.get("r", []):
            if r[0] == "shapeless":
                parts.append(" + ".join(tr_name(i) for i in r[1]) + (f" (×{r[2]})" if r[2] > 1 else ""))
            else:
                parts.append(f"🔥 {tr_name(r[1])} pişir")
        return " / ".join(parts)

    rows = []
    for f in FOODS:
        cu = CUISINES[f["cuisine"]] if "cuisine" in f else ("Other", "Diğer")
        hunger = f["food"][0] if f.get("food") else "–"
        rows.append(f"| {f['tr']} | {f['en']} | {cu[1]} | {hunger} | {recipe_text(f)} |")
    with open(os.path.join(ROOT, "tools", "food_table.md"), "w", encoding="utf-8") as fh:
        fh.write("| Türkçe | English | Mutfak | Açlık | Tarif (🔥 = fırın / tütsülük / kamp ateşi) |\n"
                 "|---|---|---|---|---|\n" + "\n".join(rows) + "\n")

    print(f"Generated {len(CROPS)} crops, {len(java_items) + 2 * len(CROPS)} items, {len(recipes)} recipes.")


if __name__ == "__main__":
    main()
