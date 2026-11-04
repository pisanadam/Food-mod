# World Foods / Dünya Mutfağı 🍲

Minecraft **26.1 – 26.3** (en son sürüm) için bir **Fabric** modu. Dünyanın dört bir yanından
**73 gerçek yemek**, bu yemekler için **17 yeni ekin** ve
un, hamur, peynir, yoğurt, kıyma gibi ara malzemeler ekler.

*A Fabric mod for Minecraft 26.1 – 26.3 that adds dozens of real-world dishes, 17 new crops and the
ingredients needed to cook them. English and Turkish translations included.*

## Sürümler / Versions

| Minecraft | Jar | Fabric API |
|---|---|---|
| 26.1, 26.1.1, 26.1.2 | `world-foods-<sürüm>+mc26.1.jar` | 0.145.1+26.1 veya üstü |
| 26.2 | `world-foods-<sürüm>+mc26.2.jar` | 0.161.0+26.2 veya üstü |
| 26.3 | `world-foods-<sürüm>+mc26.3.jar` | 0.165.2+26.3 veya üstü |

Gereken: Fabric Loader 0.20.1+, Fabric API ve Java 25.

Minecraft 26.3'te bazı API'ler ve loot tablosu formatı değiştiği için her sürüm grubunun kendi jar'ı vardır.
Jar'lar GitHub Actions tarafından her push'ta otomatik üretilir (**Actions → build → Artifacts**).

## Nasıl oynanır? / How to play

1. **Tohum bul:** Çimen, uzun çimen ve eğrelti otu kırınca %10 ihtimalle rastgele bir mod tohumu düşer.
   Hasat edilen her ürün de üretim masasında tekrar tohuma çevrilebilir.
2. **Ek:** Tohumlar buğday gibi tarım toprağına ekilir, kemik tozuyla büyütülebilir ve
   tamamen büyüyünce 1–4 ürün + tohum verir (Servet büyüsü işe yarar). Köylüler de bu tohumları ekebilir.
3. **Pişir:** Malzemeleri üretim masasında birleştir. "Çiğ" ile başlayan ürünleri (çiğ pizza, çiğ köfte...)
   fırında, tütsülükte ya da kamp ateşinde pişir.
4. Tüm eşyalar yaratıcı modda **Dünya Mutfağı** sekmesindedir; tüm tarifler aşağıdaki tablodadır.

Kase yemekleri yendikten sonra kaseyi, içecekler şişeyi, şiş kebap da çubuğu geri verir.
Bazı yemeklerin özel etkileri vardır: Türk kahvesi (Hız + Acele), Türk çayı (Yenilenme),
kimçi (Direnç), tavuk köri ve acı biber (Ateş Direnci), miso çorbası (Su Altında Nefes),
sıcak çikolata (Emilim), latte (Hız).

## Ekinler / Crops

| Ürün | Crop | Tohum |
|---|---|---|
| Domates | Tomato | Domates Tohumu |
| Marul | Lettuce | Marul Tohumu |
| Soğan | Onion | Soğan Tohumu |
| Sarımsak | Garlic | Sarımsak Tohumu |
| Pirinç | Rice | Pirinç Tohumu |
| Mısır | Corn | Mısır Tohumu |
| Dolmalık Biber | Bell Pepper | Dolmalık Biber Tohumu |
| Acı Biber | Chili Pepper | Acı Biber Tohumu |
| Patlıcan | Eggplant | Patlıcan Tohumu |
| Salatalık | Cucumber | Salatalık Tohumu |
| Soya Fasulyesi | Soybeans | Soya Tohumu |
| Nohut | Chickpeas | Nohut Tohumu |
| Lahana | Cabbage | Lahana Tohumu |
| Çilek | Strawberry | Çilek Tohumu |
| Mercimek | Lentils | Mercimek Tohumu |
| Kahve Çekirdeği | Coffee Beans | Kahve Tohumu |
| Çay Yaprağı | Tea Leaves | Çay Tohumu |

## Malzemeler ve yemekler / Ingredients and dishes

İlk satırlar temel malzemelerdir (un, hamur, peynir...), ardından mutfaklara göre yemekler gelir.

| Türkçe | English | Mutfak | Açlık | Tarif (🔥 = fırın / tütsülük / kamp ateşi) |
|---|---|---|---|---|
| Un | Flour | Diğer | – | Buğday |
| Hamur | Dough | Diğer | – | Un + Un + Un + Su Kovası (×3) |
| Makarna | Pasta | Diğer | – | Hamur + Hamur (×3) |
| Peynir | Cheese | Diğer | 3 | Süt Kovası (×3) |
| Yoğurt | Yogurt | Diğer | 3 | Süt Kovası + Kase + Kase (×2) |
| Kıyma | Minced Meat | Diğer | 1 | Çiğ Sığır Eti (×2) / Çiğ Koyun Eti (×2) |
| Pilav | Cooked Rice | Diğer | 4 | 🔥 Pirinç pişir |
| Mısır Unu | Cornmeal | Diğer | – | Mısır + Mısır (×2) |
| Tortilla | Tortilla | Diğer | 2 | 🔥 Mısır Unu pişir |
| Lavaş | Flatbread | Diğer | 4 | 🔥 Hamur pişir |
| Tofu | Tofu | Diğer | 2 | Soya Fasulyesi + Soya Fasulyesi + Soya Fasulyesi + Su Kovası (×2) |
| Kavrulmuş Kahve | Roasted Coffee | Diğer | – | 🔥 Kahve Çekirdeği pişir |
| Çikolata | Chocolate Bar | Diğer | 3 | Kakao Çekirdeği + Kakao Çekirdeği + Şeker + Süt Kovası (×3) |
| Domates Sosu | Tomato Sauce | Diğer | 2 | Domates + Domates + Sarımsak + Kase |
| Sosis | Sausage | Diğer | 5 | Çiğ Domuz Pirzolası + Kıyma → Çiğ Sosis → 🔥 pişir |
| Hamburger Köftesi | Beef Patty | Diğer | 6 | Kıyma + Kıyma → Çiğ Hamburger Köftesi → 🔥 pişir |
| Patates Kızartması | French Fries | Diğer | 4 | Fırınlanmış Patates + Fırınlanmış Patates (×3) |
| Döner | Doner Kebab | Türk | 10 | Lavaş + Biftek + Domates + Soğan + Marul |
| Lahmacun | Lahmacun | Türk | 7 | Hamur + Kıyma + Domates + Soğan + Dolmalık Biber → Çiğ Lahmacun → 🔥 pişir |
| Pide | Pide | Türk | 9 | Hamur + Peynir + Kıyma + Yumurta → Çiğ Pide → 🔥 pişir |
| Köfte | Kofte (Turkish Meatballs) | Türk | 7 | Kıyma + Soğan + Un → Çiğ Köfte → 🔥 pişir |
| Şiş Kebap | Shish Kebab | Türk | 9 | Çubuk + Pişmiş Koyun Eti + Dolmalık Biber + Soğan + Domates |
| Menemen | Menemen | Türk | 7 | Yumurta + Yumurta + Domates + Dolmalık Biber + Soğan + Kase |
| Mantı | Manti | Türk | 9 | Hamur + Kıyma + Yoğurt + Sarımsak + Kase |
| Mercimek Çorbası | Lentil Soup | Türk | 7 | Mercimek + Mercimek + Soğan + Havuç + Kase |
| İmam Bayıldı | Imam Bayildi | Türk | 7 | Patlıcan + Soğan + Domates + Sarımsak + Kase |
| Biber Dolması | Stuffed Peppers (Dolma) | Türk | 6 | Dolmalık Biber + Pilav + Kıyma + Soğan (×2) |
| Lahana Sarması | Cabbage Rolls (Sarma) | Türk | 6 | Lahana + Pilav + Soğan (×3) |
| Cacık | Cacik | Türk | 4 | Yoğurt + Salatalık + Sarımsak + Kase |
| Baklava | Baklava | Türk | 6 | Hamur + Hamur + Şeker + Bal Şişesi → Çiğ Baklava → 🔥 pişir |
| Simit | Simit | Türk | 5 | Hamur + Şeker + Buğday Tohumu → Çiğ Simit → 🔥 pişir |
| Kumpir | Kumpir | Türk | 10 | Fırınlanmış Patates + Peynir + Mısır + Sosis |
| Ayran | Ayran | Türk | 3 | Yoğurt + Cam Şişe + Cam Şişe (×2) |
| Türk Çayı | Turkish Tea | Türk | 2 | Çay Yaprağı + Cam Şişe |
| Türk Kahvesi | Turkish Coffee | Türk | 2 | Kavrulmuş Kahve + Şeker + Cam Şişe |
| Margarita Pizza | Pizza Margherita | İtalyan | 10 | Hamur + Domates Sosu + Peynir → Çiğ Margarita Pizza → 🔥 pişir |
| Bolonez Soslu Spagetti | Spaghetti Bolognese | İtalyan | 10 | Makarna + Domates Sosu + Kıyma + Kase |
| Lazanya | Lasagna | İtalyan | 12 | Makarna + Makarna + Domates Sosu + Kıyma + Peynir → Çiğ Lazanya → 🔥 pişir |
| Mantarlı Risotto | Mushroom Risotto | İtalyan | 8 | Pilav + Peynir + Kahverengi Mantar + Soğan + Kase |
| Tiramisu | Tiramisu | İtalyan | 7 | Kavrulmuş Kahve + Peynir + Şeker + Yumurta + Kakao Çekirdeği (×2) |
| Peynirli Makarna | Mac and Cheese | Amerikan | 8 | Makarna + Peynir + Süt Kovası + Kase |
| Hamburger | Hamburger | Amerikan | 11 | Ekmek + Hamburger Köftesi + Marul + Domates + Soğan |
| Çizburger | Cheeseburger | Amerikan | 12 | Ekmek + Hamburger Köftesi + Peynir + Marul + Domates |
| Sosisli Sandviç | Hot Dog | Amerikan | 8 | Ekmek + Sosis + Soğan |
| Patlamış Mısır | Popcorn | Amerikan | 3 | 🔥 Mısır pişir |
| Pankek | Pancakes | Amerikan | 7 | Un + Yumurta + Süt Kovası + Şeker (×3) |
| Elmalı Turta | Apple Pie | Amerikan | 8 | Elma + Elma + Şeker + Hamur + Yumurta |
| Tako | Taco | Meksika | 7 | Tortilla + Biftek + Marul + Domates + Peynir |
| Burrito | Burrito | Meksika | 10 | Tortilla + Pilav + Pişmiş Tavuk + Peynir + Dolmalık Biber |
| Nachos | Nachos | Meksika | 6 | Tortilla + Tortilla + Peynir + Acı Biber |
| Quesadilla | Quesadilla | Meksika | 8 | Tortilla + Peynir + Peynir + Pişmiş Tavuk |
| Suşi | Sushi | Japon | 4 | Pilav + Kurutulmuş Yosun + Çiğ Somon (×3) / Pilav + Kurutulmuş Yosun + Çiğ Morina (×3) |
| Onigiri | Onigiri | Japon | 5 | Pilav + Pilav + Kurutulmuş Yosun (×2) |
| Ramen | Ramen | Japon | 11 | Makarna + Yumurta + Pişmiş Domuz Pirzolası + Kurutulmuş Yosun + Kase |
| Miso Çorbası | Miso Soup | Japon | 6 | Tofu + Soya Fasulyesi + Kurutulmuş Yosun + Kase |
| Kızarmış Pilav | Fried Rice | Çin | 9 | Pilav + Yumurta + Havuç + Soğan + Kase |
| Çin Mantısı (Dumpling) | Dumplings | Çin | 5 | Hamur + Kıyma + Lahana + Sarımsak → Çiğ Çin Mantısı (Dumpling) → 🔥 pişir |
| Çin Böreği | Spring Rolls | Çin | 4 | Hamur + Lahana + Havuç + Soya Fasulyesi → Çiğ Çin Böreği → 🔥 pişir |
| Kimçi | Kimchi | Kore | 5 | Lahana + Acı Biber + Sarımsak + Kase |
| Bibimbap | Bibimbap | Kore | 12 | Pilav + Yumurta + Biftek + Havuç + Marul + Kase |
| Tavuk Köri | Chicken Curry | Hint | 12 | Pişmiş Tavuk + Pilav + Acı Biber + Soğan + Sarımsak + Kase |
| Dal (Hint Mercimeği) | Dal | Hint | 7 | Mercimek + Mercimek + Sarımsak + Acı Biber + Kase |
| Naan Ekmeği | Naan | Hint | 5 | Hamur + Yoğurt + Sarımsak → Çiğ Naan Ekmeği → 🔥 pişir |
| Samosa | Samosa | Hint | 5 | Hamur + Patates + Nohut + Acı Biber → Çiğ Samosa → 🔥 pişir |
| Pad Thai | Pad Thai | Tayland | 10 | Makarna + Tofu + Yumurta + Acı Biber + Kase |
| Kruvasan | Croissant | Fransız | 5 | Hamur + Hamur + Yumurta + Şeker → Çiğ Kruvasan → 🔥 pişir |
| Baget Ekmek | Baguette | Fransız | 6 | Hamur + Hamur + Hamur → Çiğ Baget Ekmek → 🔥 pişir |
| Ratatuy | Ratatouille | Fransız | 9 | Patlıcan + Domates + Dolmalık Biber + Salatalık + Soğan + Kase |
| Çikolatalı Krep | Chocolate Crepe | Fransız | 6 | Un + Yumurta + Süt Kovası + Çikolata (×2) |
| Fransız Soğan Çorbası | French Onion Soup | Fransız | 8 | Soğan + Soğan + Ekmek + Peynir + Kase |
| Paella | Paella | İspanyol | 13 | Pilav + Pişmiş Tavuk + Pişmiş Morina + Dolmalık Biber + Sarımsak + Kase |
| Gazpaço | Gazpacho | İspanyol | 5 | Domates + Domates + Salatalık + Dolmalık Biber + Sarımsak + Kase |
| Churros | Churros | İspanyol | 4 | Hamur + Şeker → Çiğ Churros → 🔥 pişir |
| Yunan Salatası | Greek Salad | Yunan | 6 | Domates + Salatalık + Soğan + Peynir + Kase |
| Humus | Hummus | Orta Doğu | 6 | Nohut + Nohut + Sarımsak + Kase |
| Falafel | Falafel | Orta Doğu | 4 | Nohut + Nohut + Soğan + Sarımsak + Un → Çiğ Falafel → 🔥 pişir |
| Fish and Chips | Fish and Chips | İngiliz | 11 | Pişmiş Morina + Patates Kızartması + Kâğıt |
| İngiliz Kahvaltısı | Full English Breakfast | İngiliz | 13 | Yumurta + Sosis + Ekmek + Domates + Kahverengi Mantar |
| Borş Çorbası | Borscht | Ukrayna | 8 | Pancar + Pancar + Lahana + Soğan + Kase |
| Pierogi | Pierogi | Polonya | 4 | Hamur + Patates + Soğan + Peynir → Çiğ Pierogi → 🔥 pişir |
| Gulaş | Goulash | Macar | 11 | Biftek + Patates + Dolmalık Biber + Soğan + Kase |
| Waffle | Waffles | Belçika | 7 | Un + Yumurta + Süt Kovası + Bal Şişesi (×2) |
| Poutine | Poutine | Kanada | 9 | Patates Kızartması + Peynir + Kase |
| Sezar Salata | Caesar Salad | İtalyan | 9 | Marul + Pişmiş Tavuk + Ekmek + Peynir + Kase |
| Meyve Salatası | Fruit Salad | Diğer | 6 | Elma + Çilek + Karpuz Dilimi + Tatlı Meyveler + Kase |
| Çilekli Cheesecake | Strawberry Cheesecake | Diğer | 7 | Peynir + Peynir + Şeker + Yumurta + Çilek + Buğday (×2) |
| Çilekli Dondurma | Strawberry Ice Cream | Diğer | 5 | Kar Topu + Süt Kovası + Şeker + Çilek + Kase |
| Sıcak Çikolata | Hot Chocolate | Diğer | 4 | Çikolata + Süt Kovası + Cam Şişe |
| Çilekli Milkshake | Strawberry Milkshake | Diğer | 4 | Çilek + Çilek + Süt Kovası + Şeker + Cam Şişe |
| Kafe Latte | Caffe Latte | Diğer | 3 | Kavrulmuş Kahve + Süt Kovası + Cam Şişe |

## Geliştirme / Development

Tüm içerik `tools/content.py` içinde tanımlıdır. JSON dosyaları, dokular, çeviriler ve
`GeneratedDefs.java` buradan üretilir:

```sh
pip install pillow
python3 tools/generate.py          # içeriği yeniden üret
./gradlew build                    # Minecraft 26.1 için derle + test et
./gradlew build -Ptarget=26.3      # başka bir sürüm için derle
```

Oyun içi testler gerçek bir Minecraft istemcisi açar, dünya oluşturur ve ekinlerin büyümesini,
kompostu, yemek yemeyi (kase/şişe geri dönüşü ve efektler dahil) kontrol edip ekran görüntüsü alır.
Bu komut Minecraft EULA'sını kabul eder:

```sh
./gradlew runClientGameTest -PclientTests -Ptarget=26.1   # ekranı olmayan Linux'ta: xvfb-run -a ...
```

`./gradlew test`, üretilen her tarifi ve loot tablosunu oyunun kendi codec'leriyle çözümler; hatalı
ya da o sürümde yok sayılacak bir alan varsa derleme başarısız olur.

Sürüme özel kod `src/mc261` (26.1–26.2) ve `src/mc263` (26.3+) klasörlerindedir; hangisinin
kullanılacağı `versions/<sürüm>.properties` dosyasındaki `compat` değeriyle seçilir.

## Lisans / License

MIT
