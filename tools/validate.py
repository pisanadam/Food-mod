#!/usr/bin/env python3
"""Static checks for generated resources.

    python3 tools/validate.py <minecraft-client-jar>

Verifies that every item/block referenced by recipes, loot tables and tags
exists either in vanilla (read from the client jar) or in the mod, and that
every item/block model points at an existing texture.
"""
import glob
import json
import os
import sys
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RES = os.path.join(ROOT, "src", "main", "resources")
MOD = "worldfoods"

jar = zipfile.ZipFile(sys.argv[1])
vanilla_items = {"minecraft:" + os.path.basename(n)[:-5] for n in jar.namelist()
                 if n.startswith("assets/minecraft/items/") and n.endswith(".json")}
mod_items = {f"{MOD}:" + os.path.basename(p)[:-5] for p in glob.glob(f"{RES}/assets/{MOD}/items/*.json")}
mod_blocks = {f"{MOD}:" + os.path.basename(p)[:-5] for p in glob.glob(f"{RES}/assets/{MOD}/blockstates/*.json")}
known = vanilla_items | mod_items
errors = []


def check_item(i, where):
    if i.startswith("#"):
        return
    if i not in known:
        errors.append(f"{where}: unknown item {i}")


for p in glob.glob(f"{RES}/data/{MOD}/recipe/*.json"):
    r = json.load(open(p))
    w = os.path.basename(p)
    for i in r.get("ingredients", []):
        check_item(i, w)
    if "ingredient" in r:
        check_item(r["ingredient"], w)
    check_item(r["result"]["id"], w)
    if r["result"]["id"].startswith(MOD + ":") is False:
        errors.append(f"{w}: result not a mod item")

for p in glob.glob(f"{ROOT}/src/mc26*/resources/data/{MOD}/loot_table/blocks/*.json"):
    t = json.load(open(p))
    w = os.path.basename(p)
    blk = f"{MOD}:{w[:-5]}"
    if blk not in mod_blocks:
        errors.append(f"{w}: no such block")

    def walk(o):
        if isinstance(o, dict):
            if o.get("type") == "minecraft:item":
                check_item(o["name"], w)
            ref_blk = o.get("block", o.get("blocks"))
            if isinstance(ref_blk, str) and ref_blk != blk:
                errors.append(f"{w}: condition references {ref_blk}")
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(t)

for p in glob.glob(f"{RES}/data/*/tags/item/*.json"):
    for v in json.load(open(p))["values"]:
        if v.startswith(MOD):
            check_item(v, p)
for p in glob.glob(f"{RES}/data/*/tags/block/*.json"):
    for v in json.load(open(p))["values"]:
        if v.startswith(MOD) and v not in mod_blocks:
            errors.append(f"{p}: unknown block {v}")

for p in glob.glob(f"{RES}/assets/{MOD}/models/**/*.json", recursive=True):
    for tex in json.load(open(p)).get("textures", {}).values():
        ns, path = tex.split(":")
        if ns == MOD and not os.path.exists(f"{RES}/assets/{MOD}/textures/{path}.png"):
            errors.append(f"{p}: missing texture {tex}")
for p in glob.glob(f"{RES}/assets/{MOD}/items/*.json"):
    m = json.load(open(p))["model"]["model"].split(":")[1]
    if not os.path.exists(f"{RES}/assets/{MOD}/models/{m}.json"):
        errors.append(f"{p}: missing model {m}")
for p in glob.glob(f"{RES}/assets/{MOD}/blockstates/*.json"):
    for v in json.load(open(p))["variants"].values():
        m = v["model"].split(":")[1]
        if not os.path.exists(f"{RES}/assets/{MOD}/models/{m}.json"):
            errors.append(f"{p}: missing model {m}")

lang = {}
for l in ("en_us", "tr_tr"):
    lang[l] = json.load(open(f"{RES}/assets/{MOD}/lang/{l}.json"))
for i in mod_items:
    for l, d in lang.items():
        if f"item.{i.replace(':', '.')}" not in d:
            errors.append(f"{l}: missing name for {i}")

# every mod item should be obtainable by crafting/cooking or loot
results = set()
for p in glob.glob(f"{RES}/data/{MOD}/recipe/*.json"):
    results.add(json.load(open(p))["result"]["id"])
for p in glob.glob(f"{ROOT}/src/mc26*/resources/data/{MOD}/loot_table/blocks/*.json"):
    results.update(x for x in open(p).read().split('"') if x.startswith(MOD + ":"))
for i in sorted(mod_items - results):
    errors.append(f"{i} is not obtainable")

print(f"{len(vanilla_items)} vanilla items, {len(mod_items)} mod items, {len(mod_blocks)} mod blocks")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("OK")
