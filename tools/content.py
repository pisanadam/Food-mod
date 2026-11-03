"""
World Foods - content definitions.

Everything the mod adds (crops, ingredients, dishes, recipes, translations and
texture styles) is declared here. Run `python3 tools/generate.py` to regenerate
all JSON assets/data, textures and the Java definition table.

Ingredient references: "wf:x" -> worldfoods:x, anything else -> minecraft:x.
"""

# ---------------------------------------------------------------------------
# CROPS
# ---------------------------------------------------------------------------
# id, produce id, EN name, TR name, (EN seeds, TR seeds), nutrition, saturation,
# produce texture style, colours, plant style, drop count (min, max), effects
CROPS = [
    dict(id="tomato", produce="tomato", en="Tomato", tr="Domates",
         food=(2, 0.3), tex=("round", "#d83a2b", "#3f8f2f"), plant="bush", fruit="#d83a2b", drop=(1, 3)),
    dict(id="lettuce", produce="lettuce", en="Lettuce", tr="Marul",
         food=(2, 0.2), tex=("leafy", "#7cc652", "#4f9a35"), plant="head", fruit="#8fd65c", drop=(1, 2)),
    dict(id="onion", produce="onion", en="Onion", tr="Soğan",
         food=(1, 0.1), tex=("bulb", "#c9874b", "#e9c48f"), plant="bulb", fruit="#c9874b", drop=(1, 3)),
    dict(id="garlic", produce="garlic", en="Garlic", tr="Sarımsak",
         food=None, tex=("bulb", "#eee6d2", "#c9bfa5"), plant="bulb", fruit="#eee6d2", drop=(1, 3)),
    dict(id="rice", produce="rice", en="Rice", tr="Pirinç",
         food=None, tex=("grains", "#f3efe0", "#d8d0b4"), plant="grass", fruit="#e8d9a0", drop=(2, 4)),
    dict(id="corn", produce="corn", en="Corn", tr="Mısır",
         food=(2, 0.3), tex=("cob", "#f2c62e", "#6aa83a"), plant="grass", fruit="#f2c62e", drop=(1, 2)),
    dict(id="bell_pepper", produce="bell_pepper", en="Bell Pepper", tr="Dolmalık Biber",
         food=(2, 0.3), tex=("pepper", "#e0412f", "#3c8a2c"), plant="bush", fruit="#e0412f", drop=(1, 3)),
    dict(id="chili_pepper", produce="chili_pepper", en="Chili Pepper", tr="Acı Biber",
         food=(1, 0.1), tex=("chili", "#c8221a", "#3c8a2c"), plant="bush", fruit="#c8221a", drop=(1, 3),
         effects=[("FIRE_RESISTANCE", 100, 0)]),
    dict(id="eggplant", produce="eggplant", en="Eggplant", tr="Patlıcan",
         food=None, tex=("long", "#5b2a6e", "#3c8a2c"), plant="bush", fruit="#5b2a6e", drop=(1, 2)),
    dict(id="cucumber", produce="cucumber", en="Cucumber", tr="Salatalık",
         food=(2, 0.3), tex=("long", "#3f8f2f", "#5fae45"), plant="bush", fruit="#3f8f2f", drop=(1, 3)),
    dict(id="soybean", produce="soybeans", en="Soybeans", tr="Soya Fasulyesi", seeds_en="Soybean Seeds", seeds_tr="Soya Tohumu",
         food=None, tex=("grains", "#d9c27a", "#b59f58"), plant="bush", fruit="#9bbf4a", drop=(2, 4)),
    dict(id="chickpea", produce="chickpeas", en="Chickpeas", tr="Nohut", seeds_en="Chickpea Seeds", seeds_tr="Nohut Tohumu",
         food=None, tex=("grains", "#e3c38a", "#c4a066"), plant="bush", fruit="#c9d27a", drop=(2, 4)),
    dict(id="cabbage", produce="cabbage", en="Cabbage", tr="Lahana",
         food=(2, 0.3), tex=("leafy", "#b8dc8a", "#86b85c"), plant="head", fruit="#b8dc8a", drop=(1, 2)),
    dict(id="strawberry", produce="strawberry", en="Strawberry", tr="Çilek",
         food=(2, 0.3), tex=("berry", "#e2263a", "#3c8a2c"), plant="bush", fruit="#e2263a", drop=(1, 3)),
    dict(id="lentil", produce="lentils", en="Lentils", tr="Mercimek", seeds_en="Lentil Seeds", seeds_tr="Mercimek Tohumu",
         food=None, tex=("grains", "#e27b37", "#bb5c22"), plant="bush", fruit="#c7b25a", drop=(2, 4)),
    dict(id="coffee", produce="coffee_beans", en="Coffee Beans", tr="Kahve Çekirdeği", seeds_en="Coffee Seeds", seeds_tr="Kahve Tohumu",
         food=None, tex=("grains", "#b8322a", "#7a1d18"), plant="bush", fruit="#b8322a", drop=(1, 3)),
    dict(id="tea", produce="tea_leaves", en="Tea Leaves", tr="Çay Yaprağı", seeds_en="Tea Seeds", seeds_tr="Çay Tohumu",
         food=None, tex=("leaves", "#3d7a2a", "#5fa03f"), plant="bush", fruit="#4d9a33", drop=(1, 3)),
]

# ---------------------------------------------------------------------------
# FOODS / INGREDIENTS
# ---------------------------------------------------------------------------
# Fields:
#   id, en, tr
#   food: (nutrition, saturation) or None for non-edible ingredients
#   c: container: none | bowl | bottle | stick
#   tex: (style, colour1, colour2, colour3)
#   r: list of recipes:
#        ("shapeless", [ingredients], count)
#        ("cook", input, xp)             -> smelting + smoking + campfire
#        ("smelt", input, xp)            -> smelting only
#   raw: if present, an extra "raw_<id>" item is generated which is crafted with
#        raw=(ingredients, count, (style, colours...)) and then cooked into this
#        item (smelting + smoking + campfire).
#   effects: [(MobEffects field, duration ticks, amplifier)]
#   rem: crafting remainder item (e.g. "bowl")
#   cuisine: used only for the README / tooltip grouping
FOODS = [
    # ---------------- basic ingredients ----------------
    dict(id="flour", en="Flour", tr="Un", tex=("sack", "#f4f1e8", "#d9d2c0"),
         r=[("shapeless", ["wheat"], 1)]),
    dict(id="dough", en="Dough", tr="Hamur", tex=("blob", "#f1dfb5", "#d8c08f"),
         r=[("shapeless", ["wf:flour", "wf:flour", "wf:flour", "water_bucket"], 3)]),
    dict(id="pasta", en="Pasta", tr="Makarna", tex=("noodles", "#f2d77e", "#d8b85a"),
         r=[("shapeless", ["wf:dough", "wf:dough"], 3)]),
    dict(id="cheese", en="Cheese", tr="Peynir", food=(3, 0.5), tex=("wedge", "#f5c842", "#d9a92a"),
         r=[("shapeless", ["milk_bucket"], 3)]),
    dict(id="yogurt", en="Yogurt", tr="Yoğurt", food=(3, 0.4), c="bowl", rem="bowl", tex=("bowl", "#f7f5ee", "#e9e4d6", "#ffffff"),
         r=[("shapeless", ["milk_bucket", "bowl", "bowl"], 2)]),
    dict(id="minced_meat", en="Minced Meat", tr="Kıyma", food=(1, 0.1), tex=("mince", "#c0473f", "#e07a70"),
         r=[("shapeless", ["beef"], 2), ("shapeless", ["mutton"], 2)]),
    dict(id="cooked_rice", en="Cooked Rice", tr="Pilav", food=(4, 0.4), tex=("grains", "#ffffff", "#e8e4d8"),
         r=[("cook", "wf:rice", 0.1)]),
    dict(id="cornmeal", en="Cornmeal", tr="Mısır Unu", tex=("sack", "#f2d14b", "#d4b030"),
         r=[("shapeless", ["wf:corn", "wf:corn"], 2)]),
    dict(id="tortilla", en="Tortilla", tr="Tortilla", food=(2, 0.3), tex=("flat", "#efd9a0", "#d2b673", "#c49c58"),
         r=[("cook", "wf:cornmeal", 0.1)]),
    dict(id="flatbread", en="Flatbread", tr="Lavaş", food=(4, 0.5), tex=("flat", "#e6c58b", "#c9a062", "#b58848"),
         r=[("cook", "wf:dough", 0.1)]),
    dict(id="tofu", en="Tofu", tr="Tofu", food=(2, 0.4), tex=("cube", "#f4f0e2", "#d9d3bd"),
         r=[("shapeless", ["wf:soybeans", "wf:soybeans", "wf:soybeans", "water_bucket"], 2)]),
    dict(id="roasted_coffee", en="Roasted Coffee", tr="Kavrulmuş Kahve", tex=("grains", "#5a3420", "#3a1f12"),
         r=[("smelt", "wf:coffee_beans", 0.2)]),
    dict(id="chocolate", en="Chocolate Bar", tr="Çikolata", food=(3, 0.3), tex=("bar", "#6b3d23", "#4a2816"),
         r=[("shapeless", ["cocoa_beans", "cocoa_beans", "sugar", "milk_bucket"], 3)]),
    dict(id="tomato_sauce", en="Tomato Sauce", tr="Domates Sosu", food=(2, 0.2), c="bowl", rem="bowl",
         tex=("bowl", "#c8281c", "#e0412f", "#a01d14"),
         r=[("shapeless", ["wf:tomato", "wf:tomato", "wf:garlic", "bowl"], 1)]),
    dict(id="sausage", en="Sausage", tr="Sosis", food=(5, 0.6), tex=("sausage", "#a3432a", "#7c2e1c"),
         raw=(["porkchop", "wf:minced_meat"], 2, ("sausage", "#e48a83", "#c2665e"))),
    dict(id="beef_patty", en="Beef Patty", tr="Hamburger Köftesi", food=(6, 0.7), tex=("patty", "#6e3b22", "#4e2614"),
         raw=(["wf:minced_meat", "wf:minced_meat"], 1, ("patty", "#c75a52", "#a2403a"))),
    dict(id="french_fries", en="French Fries", tr="Patates Kızartması", food=(4, 0.4), tex=("fries", "#f5d14a", "#d82e24"),
         r=[("shapeless", ["baked_potato", "baked_potato"], 3)]),

    # ---------------- Turkish cuisine ----------------
    dict(id="doner", en="Doner Kebab", tr="Döner", food=(10, 0.8), tex=("wrap", "#e6c58b", "#8b4a28", "#5fae45"), cuisine="tr",
         r=[("shapeless", ["wf:flatbread", "cooked_beef", "wf:tomato", "wf:onion", "wf:lettuce"], 1)]),
    dict(id="lahmacun", en="Lahmacun", tr="Lahmacun", food=(7, 0.6), tex=("flat", "#e6b77a", "#b8402c", "#5fae45"), cuisine="tr",
         raw=(["wf:dough", "wf:minced_meat", "wf:tomato", "wf:onion", "wf:bell_pepper"], 2, ("flat", "#f1dfb5", "#d0605a", "#5fae45"))),
    dict(id="pide", en="Pide", tr="Pide", food=(9, 0.7), tex=("boat", "#d9a55e", "#f5c842", "#8b4a28"), cuisine="tr",
         raw=(["wf:dough", "wf:cheese", "wf:minced_meat", "egg"], 1, ("boat", "#f1dfb5", "#f5e08a", "#c75a52"))),
    dict(id="kofte", en="Kofte (Turkish Meatballs)", tr="Köfte", food=(7, 0.7), tex=("balls", "#7a3f22", "#5a2c16"), cuisine="tr",
         raw=(["wf:minced_meat", "wf:onion", "wf:flour"], 2, ("balls", "#c75a52", "#a2403a"))),
    dict(id="shish_kebab", en="Shish Kebab", tr="Şiş Kebap", food=(9, 0.8), c="stick", tex=("skewer", "#7a3f22", "#3f8f2f", "#e0412f"), cuisine="tr",
         r=[("shapeless", ["stick", "cooked_mutton", "wf:bell_pepper", "wf:onion", "wf:tomato"], 1)]),
    dict(id="menemen", en="Menemen", tr="Menemen", food=(7, 0.6), c="bowl", tex=("bowl", "#e0552f", "#f5c842", "#3f8f2f"), cuisine="tr",
         r=[("shapeless", ["egg", "egg", "wf:tomato", "wf:bell_pepper", "wf:onion", "bowl"], 1)]),
    dict(id="manti", en="Manti", tr="Mantı", food=(9, 0.7), c="bowl", tex=("bowl", "#f7f5ee", "#f1dfb5", "#c8281c"), cuisine="tr",
         r=[("shapeless", ["wf:dough", "wf:minced_meat", "wf:yogurt", "wf:garlic", "bowl"], 1)]),
    dict(id="lentil_soup", en="Lentil Soup", tr="Mercimek Çorbası", food=(7, 0.6), c="bowl", tex=("bowl", "#e88a2f", "#f0a24a", "#c86a1a"), cuisine="tr",
         r=[("shapeless", ["wf:lentils", "wf:lentils", "wf:onion", "carrot", "bowl"], 1)]),
    dict(id="imam_bayildi", en="Imam Bayildi", tr="İmam Bayıldı", food=(7, 0.6), c="bowl", tex=("bowl", "#5b2a6e", "#e0412f", "#f5d14a"), cuisine="tr",
         r=[("shapeless", ["wf:eggplant", "wf:onion", "wf:tomato", "wf:garlic", "bowl"], 1)]),
    dict(id="stuffed_peppers", en="Stuffed Peppers (Dolma)", tr="Biber Dolması", food=(6, 0.6), tex=("pepper", "#4c9a36", "#f3efe0", "#2e6b22"), cuisine="tr",
         r=[("shapeless", ["wf:bell_pepper", "wf:cooked_rice", "wf:minced_meat", "wf:onion"], 2)]),
    dict(id="cabbage_rolls", en="Cabbage Rolls (Sarma)", tr="Lahana Sarması", food=(6, 0.6), tex=("rolls", "#b8dc8a", "#86b85c", "#f3efe0"), cuisine="tr",
         r=[("shapeless", ["wf:cabbage", "wf:cooked_rice", "wf:onion"], 3)]),
    dict(id="cacik", en="Cacik", tr="Cacık", food=(4, 0.4), c="bowl", tex=("bowl", "#f7f5ee", "#5fae45", "#ffffff"), cuisine="tr",
         r=[("shapeless", ["wf:yogurt", "wf:cucumber", "wf:garlic", "bowl"], 1)]),
    dict(id="baklava", en="Baklava", tr="Baklava", food=(6, 0.5), tex=("pastry", "#d9a03c", "#f2c75e", "#6aa83a"), cuisine="tr",
         raw=(["wf:dough", "wf:dough", "sugar", "honey_bottle"], 4, ("pastry", "#f1dfb5", "#f8ecc8", "#9bbf4a"))),
    dict(id="simit", en="Simit", tr="Simit", food=(5, 0.5), tex=("ring", "#b8692e", "#f3e6c0"), cuisine="tr",
         raw=(["wf:dough", "sugar", "wheat_seeds"], 2, ("ring", "#f1dfb5", "#ffffff"))),
    dict(id="kumpir", en="Kumpir", tr="Kumpir", food=(10, 0.7), tex=("kumpir", "#b8864a", "#f5c842", "#e0412f"), cuisine="tr",
         r=[("shapeless", ["baked_potato", "wf:cheese", "wf:corn", "wf:sausage"], 1)]),
    dict(id="ayran", en="Ayran", tr="Ayran", food=(3, 0.4), c="bottle", tex=("bottle", "#f7f5ee"), cuisine="tr",
         r=[("shapeless", ["wf:yogurt", "glass_bottle", "glass_bottle"], 2)]),
    dict(id="turkish_tea", en="Turkish Tea", tr="Türk Çayı", food=(2, 0.2), c="bottle", tex=("tea_glass", "#a5351d"), cuisine="tr",
         effects=[("REGENERATION", 100, 0)],
         r=[("shapeless", ["wf:tea_leaves", "glass_bottle"], 1)]),
    dict(id="turkish_coffee", en="Turkish Coffee", tr="Türk Kahvesi", food=(2, 0.2), c="bottle", tex=("cup", "#3a1f12"), cuisine="tr",
         effects=[("SPEED", 600, 0), ("HASTE", 600, 0)],
         r=[("shapeless", ["wf:roasted_coffee", "sugar", "glass_bottle"], 1)]),

    # ---------------- Italian ----------------
    dict(id="pizza", en="Pizza Margherita", tr="Margarita Pizza", food=(10, 0.7), tex=("pizza", "#d9a55e", "#c8281c", "#f5e08a"), cuisine="it",
         raw=(["wf:dough", "wf:tomato_sauce", "wf:cheese"], 1, ("pizza", "#f1dfb5", "#d0605a", "#fff3c0"))),
    dict(id="spaghetti_bolognese", en="Spaghetti Bolognese", tr="Bolonez Soslu Spagetti", food=(10, 0.8), c="bowl", tex=("bowl", "#f2d77e", "#c8281c", "#7a3f22"), cuisine="it",
         r=[("shapeless", ["wf:pasta", "wf:tomato_sauce", "wf:minced_meat", "bowl"], 1)]),
    dict(id="lasagna", en="Lasagna", tr="Lazanya", food=(12, 0.9), tex=("slice", "#f2d77e", "#c8281c", "#f5c842"), cuisine="it",
         raw=(["wf:pasta", "wf:pasta", "wf:tomato_sauce", "wf:minced_meat", "wf:cheese"], 2, ("slice", "#f8ecc8", "#d0605a", "#fff3c0"))),
    dict(id="risotto", en="Mushroom Risotto", tr="Mantarlı Risotto", food=(8, 0.7), c="bowl", tex=("bowl", "#f3e8c8", "#a07850", "#f5e08a"), cuisine="it",
         r=[("shapeless", ["wf:cooked_rice", "wf:cheese", "brown_mushroom", "wf:onion", "bowl"], 1)]),
    dict(id="tiramisu", en="Tiramisu", tr="Tiramisu", food=(7, 0.6), tex=("slice", "#f3e6c8", "#6b3d23", "#8b5a3a"), cuisine="it",
         r=[("shapeless", ["wf:roasted_coffee", "wf:cheese", "sugar", "egg", "cocoa_beans"], 2)]),
    dict(id="mac_and_cheese", en="Mac and Cheese", tr="Peynirli Makarna", food=(8, 0.6), c="bowl", tex=("bowl", "#f5c842", "#f2d77e", "#e0a82a"), cuisine="us",
         r=[("shapeless", ["wf:pasta", "wf:cheese", "milk_bucket", "bowl"], 1)]),

    # ---------------- American ----------------
    dict(id="hamburger", en="Hamburger", tr="Hamburger", food=(11, 0.8), tex=("burger", "#d9963e", "#5a2c16", "#5fae45"), cuisine="us",
         r=[("shapeless", ["bread", "wf:beef_patty", "wf:lettuce", "wf:tomato", "wf:onion"], 1)]),
    dict(id="cheeseburger", en="Cheeseburger", tr="Çizburger", food=(12, 0.85), tex=("burger", "#d9963e", "#5a2c16", "#f5c842"), cuisine="us",
         r=[("shapeless", ["bread", "wf:beef_patty", "wf:cheese", "wf:lettuce", "wf:tomato"], 1)]),
    dict(id="hot_dog", en="Hot Dog", tr="Sosisli Sandviç", food=(8, 0.6), tex=("hotdog", "#e0a85a", "#a3432a", "#f5d14a"), cuisine="us",
         r=[("shapeless", ["bread", "wf:sausage", "wf:onion"], 1)]),
    dict(id="popcorn", en="Popcorn", tr="Patlamış Mısır", food=(3, 0.2), tex=("popcorn", "#fff8e0", "#d82e24"), cuisine="us",
         r=[("smelt", "wf:corn", 0.1)]),
    dict(id="pancakes", en="Pancakes", tr="Pankek", food=(7, 0.5), tex=("stack", "#e0a85a", "#b8732e", "#f2c62e"), cuisine="us",
         r=[("shapeless", ["wf:flour", "egg", "milk_bucket", "sugar"], 3)]),
    dict(id="apple_pie", en="Apple Pie", tr="Elmalı Turta", food=(8, 0.5), tex=("pie", "#d9963e", "#b8692e", "#c8281c"), cuisine="us",
         r=[("shapeless", ["apple", "apple", "sugar", "wf:dough", "egg"], 1)]),

    # ---------------- Mexican ----------------
    dict(id="taco", en="Taco", tr="Tako", food=(7, 0.6), tex=("taco", "#efd9a0", "#7a3f22", "#5fae45"), cuisine="mx",
         r=[("shapeless", ["wf:tortilla", "cooked_beef", "wf:lettuce", "wf:tomato", "wf:cheese"], 1)]),
    dict(id="burrito", en="Burrito", tr="Burrito", food=(10, 0.8), tex=("wrap", "#efd9a0", "#f3efe0", "#e0412f"), cuisine="mx",
         r=[("shapeless", ["wf:tortilla", "wf:cooked_rice", "cooked_chicken", "wf:cheese", "wf:bell_pepper"], 1)]),
    dict(id="nachos", en="Nachos", tr="Nachos", food=(6, 0.4), tex=("nachos", "#f2c62e", "#f5a82a", "#c8221a"), cuisine="mx",
         r=[("shapeless", ["wf:tortilla", "wf:tortilla", "wf:cheese", "wf:chili_pepper"], 1)]),
    dict(id="quesadilla", en="Quesadilla", tr="Quesadilla", food=(8, 0.6), tex=("taco", "#e8c47a", "#f5c842", "#e0412f"), cuisine="mx",
         r=[("shapeless", ["wf:tortilla", "wf:cheese", "wf:cheese", "cooked_chicken"], 1)]),

    # ---------------- Japanese ----------------
    dict(id="sushi", en="Sushi", tr="Suşi", food=(4, 0.6), tex=("sushi", "#ffffff", "#f07a4a", "#1f2a1a"), cuisine="jp",
         r=[("shapeless", ["wf:cooked_rice", "dried_kelp", "salmon"], 3), ("shapeless", ["wf:cooked_rice", "dried_kelp", "cod"], 3)]),
    dict(id="onigiri", en="Onigiri", tr="Onigiri", food=(5, 0.6), tex=("onigiri", "#ffffff", "#1f2a1a"), cuisine="jp",
         r=[("shapeless", ["wf:cooked_rice", "wf:cooked_rice", "dried_kelp"], 2)]),
    dict(id="ramen", en="Ramen", tr="Ramen", food=(11, 0.8), c="bowl", tex=("bowl", "#e8b96a", "#f2d77e", "#f5f0e0"), cuisine="jp",
         r=[("shapeless", ["wf:pasta", "egg", "cooked_porkchop", "dried_kelp", "bowl"], 1)]),
    dict(id="miso_soup", en="Miso Soup", tr="Miso Çorbası", food=(6, 0.6), c="bowl", tex=("bowl", "#c9a35a", "#f4f0e2", "#3f8f2f"), cuisine="jp",
         effects=[("WATER_BREATHING", 600, 0)],
         r=[("shapeless", ["wf:tofu", "wf:soybeans", "dried_kelp", "bowl"], 1)]),

    # ---------------- Chinese ----------------
    dict(id="fried_rice", en="Fried Rice", tr="Kızarmış Pilav", food=(9, 0.7), c="bowl", tex=("bowl", "#f0dc9a", "#f5c842", "#e8762a"), cuisine="cn",
         r=[("shapeless", ["wf:cooked_rice", "egg", "carrot", "wf:onion", "bowl"], 1)]),
    dict(id="dumplings", en="Dumplings", tr="Çin Mantısı (Dumpling)", food=(5, 0.6), tex=("dumplings", "#f4ecd6", "#d9cba8"), cuisine="cn",
         raw=(["wf:dough", "wf:minced_meat", "wf:cabbage", "wf:garlic"], 3, ("dumplings", "#f8f2e2", "#e6dcc4"))),
    dict(id="spring_rolls", en="Spring Rolls", tr="Çin Böreği", food=(4, 0.5), tex=("rolls", "#e0a85a", "#b8732e", "#5fae45"), cuisine="cn",
         raw=(["wf:dough", "wf:cabbage", "carrot", "wf:soybeans"], 3, ("rolls", "#f1dfb5", "#d8c08f", "#5fae45"))),

    # ---------------- Korean ----------------
    dict(id="kimchi", en="Kimchi", tr="Kimçi", food=(5, 0.5), c="bowl", tex=("bowl", "#e0552f", "#f0a070", "#b8dc8a"), cuisine="kr",
         effects=[("RESISTANCE", 200, 0)],
         r=[("shapeless", ["wf:cabbage", "wf:chili_pepper", "wf:garlic", "bowl"], 1)]),
    dict(id="bibimbap", en="Bibimbap", tr="Bibimbap", food=(12, 0.9), c="bowl", tex=("bowl", "#ffffff", "#f5c842", "#e8762a"), cuisine="kr",
         r=[("shapeless", ["wf:cooked_rice", "egg", "cooked_beef", "carrot", "wf:lettuce", "bowl"], 1)]),

    # ---------------- Indian ----------------
    dict(id="chicken_curry", en="Chicken Curry", tr="Tavuk Köri", food=(12, 0.85), c="bowl", tex=("bowl", "#e8a02a", "#f5d080", "#ffffff"), cuisine="in",
         effects=[("FIRE_RESISTANCE", 400, 0)],
         r=[("shapeless", ["cooked_chicken", "wf:cooked_rice", "wf:chili_pepper", "wf:onion", "wf:garlic", "bowl"], 1)]),
    dict(id="dal", en="Dal", tr="Dal (Hint Mercimeği)", food=(7, 0.6), c="bowl", tex=("bowl", "#f0b03a", "#e88a2f", "#3f8f2f"), cuisine="in",
         r=[("shapeless", ["wf:lentils", "wf:lentils", "wf:garlic", "wf:chili_pepper", "bowl"], 1)]),
    dict(id="naan", en="Naan", tr="Naan Ekmeği", food=(5, 0.6), tex=("flat", "#efd09a", "#c9963e", "#8b5a2b"), cuisine="in",
         raw=(["wf:dough", "wf:yogurt", "wf:garlic"], 2, ("flat", "#f8ecc8", "#f1dfb5", "#d8c08f"))),
    dict(id="samosa", en="Samosa", tr="Samosa", food=(5, 0.5), tex=("triangle", "#d9963e", "#b8732e"), cuisine="in",
         raw=(["wf:dough", "potato", "wf:chickpeas", "wf:chili_pepper"], 2, ("triangle", "#f1dfb5", "#d8c08f"))),

    # ---------------- Thai ----------------
    dict(id="pad_thai", en="Pad Thai", tr="Pad Thai", food=(10, 0.7), c="bowl", tex=("bowl", "#f0c070", "#f4f0e2", "#c8221a"), cuisine="th",
         r=[("shapeless", ["wf:pasta", "wf:tofu", "egg", "wf:chili_pepper", "bowl"], 1)]),

    # ---------------- French ----------------
    dict(id="croissant", en="Croissant", tr="Kruvasan", food=(5, 0.5), tex=("crescent", "#d9963e", "#a8642a"), cuisine="fr",
         raw=(["wf:dough", "wf:dough", "egg", "sugar"], 3, ("crescent", "#f1dfb5", "#d8c08f"))),
    dict(id="baguette", en="Baguette", tr="Baget Ekmek", food=(6, 0.6), tex=("loaf", "#d9963e", "#a8642a"), cuisine="fr",
         raw=(["wf:dough", "wf:dough", "wf:dough"], 2, ("loaf", "#f1dfb5", "#d8c08f"))),
    dict(id="ratatouille", en="Ratatouille", tr="Ratatuy", food=(9, 0.7), c="bowl", tex=("bowl", "#c8281c", "#5b2a6e", "#3f8f2f"), cuisine="fr",
         r=[("shapeless", ["wf:eggplant", "wf:tomato", "wf:bell_pepper", "wf:cucumber", "wf:onion", "bowl"], 1)]),
    dict(id="crepe", en="Chocolate Crepe", tr="Çikolatalı Krep", food=(6, 0.5), tex=("crepe", "#efc884", "#6b3d23"), cuisine="fr",
         r=[("shapeless", ["wf:flour", "egg", "milk_bucket", "wf:chocolate"], 2)]),
    dict(id="french_onion_soup", en="French Onion Soup", tr="Fransız Soğan Çorbası", food=(8, 0.6), c="bowl", tex=("bowl", "#a8642a", "#f5c842", "#d9963e"), cuisine="fr",
         r=[("shapeless", ["wf:onion", "wf:onion", "bread", "wf:cheese", "bowl"], 1)]),

    # ---------------- Spanish ----------------
    dict(id="paella", en="Paella", tr="Paella", food=(13, 0.9), c="bowl", tex=("bowl", "#f2c62e", "#e0552f", "#3f8f2f"), cuisine="es",
         r=[("shapeless", ["wf:cooked_rice", "cooked_chicken", "cooked_cod", "wf:bell_pepper", "wf:garlic", "bowl"], 1)]),
    dict(id="gazpacho", en="Gazpacho", tr="Gazpaço", food=(5, 0.5), c="bowl", tex=("bowl", "#d83a2b", "#e86a4a", "#5fae45"), cuisine="es",
         r=[("shapeless", ["wf:tomato", "wf:tomato", "wf:cucumber", "wf:bell_pepper", "wf:garlic", "bowl"], 1)]),
    dict(id="churros", en="Churros", tr="Churros", food=(4, 0.4), tex=("sticks", "#d9963e", "#a8642a"), cuisine="es",
         raw=(["wf:dough", "sugar"], 3, ("sticks", "#f1dfb5", "#d8c08f"))),

    # ---------------- Greek / Middle Eastern ----------------
    dict(id="greek_salad", en="Greek Salad", tr="Yunan Salatası", food=(6, 0.5), c="bowl", tex=("bowl", "#3f8f2f", "#e0412f", "#ffffff"), cuisine="gr",
         r=[("shapeless", ["wf:tomato", "wf:cucumber", "wf:onion", "wf:cheese", "bowl"], 1)]),
    dict(id="hummus", en="Hummus", tr="Humus", food=(6, 0.6), c="bowl", tex=("bowl", "#e3c38a", "#d4a960", "#c8221a"), cuisine="me",
         r=[("shapeless", ["wf:chickpeas", "wf:chickpeas", "wf:garlic", "bowl"], 1)]),
    dict(id="falafel", en="Falafel", tr="Falafel", food=(4, 0.5), tex=("balls", "#9a6a2a", "#6e4a1a"), cuisine="me",
         raw=(["wf:chickpeas", "wf:chickpeas", "wf:onion", "wf:garlic", "wf:flour"], 3, ("balls", "#c9b26a", "#a8924a"))),

    # ---------------- British / European ----------------
    dict(id="fish_and_chips", en="Fish and Chips", tr="Fish and Chips", food=(11, 0.8), tex=("plate", "#d9963e", "#f5d14a", "#ffffff"), cuisine="gb",
         r=[("shapeless", ["cooked_cod", "wf:french_fries", "paper"], 1)]),
    dict(id="full_breakfast", en="Full English Breakfast", tr="İngiliz Kahvaltısı", food=(13, 0.9), tex=("plate", "#a3432a", "#f5c842", "#ffffff"), cuisine="gb",
         r=[("shapeless", ["egg", "wf:sausage", "bread", "wf:tomato", "brown_mushroom"], 1)]),
    dict(id="borscht", en="Borscht", tr="Borş Çorbası", food=(8, 0.6), c="bowl", tex=("bowl", "#9a1e3a", "#c8325a", "#ffffff"), cuisine="ua",
         r=[("shapeless", ["beetroot", "beetroot", "wf:cabbage", "wf:onion", "bowl"], 1)]),
    dict(id="pierogi", en="Pierogi", tr="Pierogi", food=(4, 0.5), tex=("dumplings", "#f0d8a0", "#c9a868"), cuisine="pl",
         raw=(["wf:dough", "potato", "wf:onion", "wf:cheese"], 3, ("dumplings", "#f8f2e2", "#e6dcc4"))),
    dict(id="goulash", en="Goulash", tr="Gulaş", food=(11, 0.8), c="bowl", tex=("bowl", "#a8321c", "#7a3f22", "#f5c842"), cuisine="hu",
         r=[("shapeless", ["cooked_beef", "potato", "wf:bell_pepper", "wf:onion", "bowl"], 1)]),
    dict(id="waffles", en="Waffles", tr="Waffle", food=(7, 0.5), tex=("waffle", "#e0a85a", "#b8732e"), cuisine="be",
         r=[("shapeless", ["wf:flour", "egg", "milk_bucket", "honey_bottle"], 2)]),

    # ---------------- Americas ----------------
    dict(id="poutine", en="Poutine", tr="Poutine", food=(9, 0.6), c="bowl", tex=("bowl", "#f5d14a", "#8b5a2b", "#ffffff"), cuisine="ca",
         r=[("shapeless", ["wf:french_fries", "wf:cheese", "bowl"], 1)]),

    # ---------------- Salads, desserts & drinks ----------------
    dict(id="caesar_salad", en="Caesar Salad", tr="Sezar Salata", food=(9, 0.7), c="bowl", tex=("bowl", "#7cc652", "#f5e8c8", "#d9963e"), cuisine="it",
         r=[("shapeless", ["wf:lettuce", "cooked_chicken", "bread", "wf:cheese", "bowl"], 1)]),
    dict(id="fruit_salad", en="Fruit Salad", tr="Meyve Salatası", food=(6, 0.5), c="bowl", tex=("bowl", "#e2263a", "#f2c62e", "#7cc652"),
         r=[("shapeless", ["apple", "wf:strawberry", "melon_slice", "sweet_berries", "bowl"], 1)]),
    dict(id="cheesecake", en="Strawberry Cheesecake", tr="Çilekli Cheesecake", food=(7, 0.6), tex=("slice", "#f8f0d8", "#e2263a", "#d9963e"),
         r=[("shapeless", ["wf:cheese", "wf:cheese", "sugar", "egg", "wf:strawberry", "wheat"], 2)]),
    dict(id="strawberry_ice_cream", en="Strawberry Ice Cream", tr="Çilekli Dondurma", food=(5, 0.4), c="bowl", tex=("bowl", "#f7a8b8", "#ffd0dc", "#e2263a"),
         r=[("shapeless", ["snowball", "milk_bucket", "sugar", "wf:strawberry", "bowl"], 1)]),
    dict(id="hot_chocolate", en="Hot Chocolate", tr="Sıcak Çikolata", food=(4, 0.4), c="bottle", tex=("cup", "#6b3d23"),
         effects=[("ABSORPTION", 600, 0)],
         r=[("shapeless", ["wf:chocolate", "milk_bucket", "glass_bottle"], 1)]),
    dict(id="strawberry_milkshake", en="Strawberry Milkshake", tr="Çilekli Milkshake", food=(4, 0.4), c="bottle", tex=("bottle", "#f7a8b8"),
         r=[("shapeless", ["wf:strawberry", "wf:strawberry", "milk_bucket", "sugar", "glass_bottle"], 1)]),
    dict(id="latte", en="Caffe Latte", tr="Kafe Latte", food=(3, 0.3), c="bottle", tex=("cup", "#c8a070"),
         effects=[("SPEED", 400, 0)],
         r=[("shapeless", ["wf:roasted_coffee", "milk_bucket", "glass_bottle"], 1)]),
]

CUISINES = {
    "tr": ("Turkish", "Türk"), "it": ("Italian", "İtalyan"), "us": ("American", "Amerikan"),
    "mx": ("Mexican", "Meksika"), "jp": ("Japanese", "Japon"), "cn": ("Chinese", "Çin"),
    "kr": ("Korean", "Kore"), "in": ("Indian", "Hint"), "th": ("Thai", "Tayland"),
    "fr": ("French", "Fransız"), "es": ("Spanish", "İspanyol"), "gr": ("Greek", "Yunan"),
    "me": ("Middle Eastern", "Orta Doğu"), "gb": ("British", "İngiliz"), "ua": ("Ukrainian", "Ukrayna"),
    "pl": ("Polish", "Polonya"), "hu": ("Hungarian", "Macar"), "be": ("Belgian", "Belçika"),
    "ca": ("Canadian", "Kanada"),
}
