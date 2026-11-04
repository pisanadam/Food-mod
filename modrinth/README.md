# Modrinth yayın rehberi

Bu klasörde Modrinth sayfası için gereken her şey var. Modrinth'te **Create a project** deyip alanları aşağıdaki gibi doldurabilirsin.

## 1. Proje bilgileri

| Alan | Değer |
|---|---|
| **Name** | `World Foods` |
| **URL** | `world-foods` |
| **Project type** | Mod |
| **Summary** (en fazla 256 karakter) | `73 real-world dishes from 19 cuisines - döner, pizza, sushi, tacos, curry and more - plus 17 new crops to grow the ingredients. Vanilla-style cooking with crafting tables, furnaces and campfires.` |
| **Icon** | `modrinth/icon.png` (512×512) |
| **Categories** | `Food` (ana kategori). İstersen ek olarak `Game Mechanics` |
| **Client side** | Required |
| **Server side** | Required |
| **License** | MIT |
| **Source code** | `https://github.com/pisanadam/Food-mod` |
| **Issue tracker** | `https://github.com/pisanadam/Food-mod/issues` |

**Description** alanına `modrinth/description.md` dosyasının içeriğini olduğu gibi yapıştır (İngilizce + Türkçe).

## 2. Galeri

Modrinth'te **Gallery → Upload an image**. Her görsel için başlık ve açıklama:

| Dosya | Featured | Title | Description |
|---|---|---|---|
| `gallery/01-farm.png` | ✅ **Evet** (kapak görseli) | All 17 crops | A farm with every new crop fully grown: tomatoes, peppers, eggplants, corn, rice, garlic and more. |
| `gallery/02-farm-closeup.png` | | Ripe and ready | Eggplants, bell peppers, tomatoes and corn up close. |
| `gallery/03-turkish-dishes.png` | | Turkish cuisine | Döner, lahmacun, pide, köfte, şiş kebap, mantı, baklava, simit, Turkish tea and coffee... |
| `gallery/04-world-dishes.png` | | World cuisine | Pizza, burgers, sushi, ramen, tacos, curry, croissants, paella and more. |
| `gallery/05-creative-tab.png` | | Creative tab | Every item in its own World Foods creative tab. |
| `gallery/06-first-person.png` | | Hungry? | A hotbar full of food from around the world. |
| `gallery/07-farm-side.png` | | Growing season | Crops grow in 4 visible stages, with bone meal and Fortune support. |
| `gallery/08-dishes-1.png` | | Dishes (1/2) | All dishes with their Turkish names and how much hunger they restore. |
| `gallery/09-dishes-2.png` | | Dishes (2/2) | Asian, European, Middle Eastern and American dishes, desserts and drinks. |
| `gallery/10-crops.png` | | Crops & growth stages | Every crop with its seeds and growth stages. |
| `gallery/11-ingredients.png` | | Ingredients | Flour, dough, cheese, yogurt, minced meat, tortillas, tofu and other building blocks. |

## 3. Sürümleri yükle

Her Minecraft sürüm grubu için ayrı bir sürüm oluştur (**Versions → Create a version**). Jar dosyaları GitHub Actions'ta **build** iş akışının **Artifacts** bölümünde ya da yerelde `./gradlew build -Ptarget=<sürüm>` ile `build/libs/` içinde oluşur.

| Version number | Version title | Dosya | Game versions | Loader |
|---|---|---|---|---|
| `1.0.0+mc26.3` | World Foods 1.0.0 for 26.3 | `world-foods-1.0.0+mc26.3.jar` | 26.3 | Fabric |
| `1.0.0+mc26.2` | World Foods 1.0.0 for 26.2 | `world-foods-1.0.0+mc26.2.jar` | 26.2 | Fabric |
| `1.0.0+mc26.1` | World Foods 1.0.0 for 26.1 | `world-foods-1.0.0+mc26.1.jar` | 26.1, 26.1.1, 26.1.2 | Fabric |

Hepsi için:
- **Release channel:** Release
- **Dependencies:** `Fabric API` → **Required**
- `-sources.jar` dosyasını yükleme, sadece normal jar'ı yükle.

**Changelog** (üçü için aynı):

```markdown
First release! 🎉

- 73 real-world dishes from 19 cuisines
- 17 new crops with seeds that drop from grass
- 17 basic ingredients (flour, dough, cheese, yogurt, minced meat...)
- Raw dishes that are cooked in a furnace, smoker or campfire
- Bowls, bottles and sticks are returned after eating
- Special effects for Turkish coffee, Turkish tea, kimchi, curry, miso soup and more
- English and Turkish translations
```

## Görselleri yeniden üretmek

```sh
python3 tools/generate.py           # dokular ve mod simgesi
python3 tools/modrinth_assets.py    # logo + katalog görselleri (08-11)

# oyun içi ekran görüntüleri (01-07), Minecraft EULA'sını kabul eder:
WORLDFOODS_SHOWCASE=1 xvfb-run -a -s "-screen 0 1920x1080x24" \
  ./gradlew runClientGameTest -PclientTests -Ptarget=26.1
# çıktı: build/run/clientGameTest/screenshots/
```
