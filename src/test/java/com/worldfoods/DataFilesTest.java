package com.worldfoods;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.stream.Stream;

import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import com.mojang.serialization.Codec;
import com.mojang.serialization.JsonOps;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import com.worldfoods.content.GeneratedDefs;

import net.minecraft.SharedConstants;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.data.registries.VanillaRegistries;
import net.minecraft.resources.RegistryOps;
import net.minecraft.server.Bootstrap;
import net.minecraft.world.item.crafting.Recipe;
import net.minecraft.world.level.storage.loot.LootTable;

/**
 * Decodes every generated recipe and loot table with the game's own codecs, so
 * malformed JSON or references to missing items fail the build instead of being
 * silently skipped when a world loads.
 */
class DataFilesTest {
	private static final Path DATA = Path.of("src/main/resources/data/worldfoods");

	/**
	 * Top-level fields that newer versions omit when re-encoding because they are defaults or no longer
	 * used (the recipe book category was removed for crafting recipes in 26.2). Keeping them is harmless.
	 */
	private static final Set<String> OPTIONAL_FIELDS = Set.of("/category", "/cookingtime");
	private static HolderLookup.Provider registries;

	@BeforeAll
	static void bootstrap() {
		SharedConstants.tryDetectVersion();
		Bootstrap.bootStrap();
		new WorldFoods().onInitialize();
		registries = vanillaLookup();
	}

	/** {@code VanillaRegistries} was reworked in 26.3, so look the factory method up reflectively. */
	private static HolderLookup.Provider vanillaLookup() {
		try {
			try {
				return (HolderLookup.Provider) VanillaRegistries.class.getMethod("createLookup").invoke(null);
			} catch (NoSuchMethodException e) {
				Object world = VanillaRegistries.class.getMethod("createWorldLookup").invoke(null);
				return (HolderLookup.Provider) VanillaRegistries.class
						.getMethod("createReloadableLookup", HolderLookup.Provider.class)
						.invoke(null, world);
			}
		} catch (ReflectiveOperationException e) {
			throw new IllegalStateException("Could not create vanilla registry lookup", e);
		}
	}

	@Test
	void modItemsRegistered() {
		int expected = GeneratedDefs.FOODS.size() + GeneratedDefs.CROPS.size() * 2;
		long actual = BuiltInRegistries.ITEM.keySet().stream().filter(id -> id.getNamespace().equals(WorldFoods.MOD_ID)).count();
		assertEquals(expected, actual, "registered item count");
	}

	@Test
	void recipesDecode() throws IOException {
		assertAllDecode(DATA.resolve("recipe"), Recipe.CODEC);
	}

	@Test
	void lootTablesDecode() throws IOException {
		Path compatData = Path.of("src", System.getProperty("worldfoods.compat"), "resources/data/worldfoods");
		assertAllDecode(compatData.resolve("loot_table"), LootTable.DIRECT_CODEC);
	}

	private static <T> void assertAllDecode(Path dir, Codec<T> codec) throws IOException {
		RegistryOps<JsonElement> ops = RegistryOps.create(JsonOps.INSTANCE, registries);
		List<String> errors = new ArrayList<>();
		int count = 0;

		try (Stream<Path> files = Files.walk(dir)) {
			for (Path file : files.filter(p -> p.toString().endsWith(".json")).toList()) {
				count++;
				try (Reader reader = Files.newBufferedReader(file)) {
					JsonElement json = JsonParser.parseReader(reader);
					String name = file.getFileName().toString();
					codec.parse(ops, json)
							.ifError(e -> errors.add(name + ": " + e.message()))
							// Re-encoding can fail for registry holders on some versions; decoding already succeeded then.
							.ifSuccess(value -> codec.encodeStart(ops, value)
									.ifSuccess(encoded -> checkNothingDropped(name, "", json, encoded, errors)));
				}
			}
		}

		assertTrue(count > 0, "no files found in " + dir);
		assertTrue(errors.isEmpty(), String.join("\n", errors));
	}

	/**
	 * Codecs silently ignore unknown fields, so a file written for a different Minecraft version can
	 * decode "successfully" while losing conditions or functions. Re-encoding the decoded value and
	 * checking that every field we wrote survived catches that.
	 */
	private static void checkNothingDropped(String file, String path, JsonElement original, JsonElement encoded, List<String> errors) {
		if (original.isJsonObject() && encoded.isJsonArray() && encoded.getAsJsonArray().size() == 1) {
			encoded = encoded.getAsJsonArray().get(0);
		} else if (original.isJsonArray() && original.getAsJsonArray().size() == 1 && !encoded.isJsonArray()) {
			original = original.getAsJsonArray().get(0);
		}

		if (original.isJsonObject()) {
			if (!encoded.isJsonObject()) {
				if (encoded.isJsonPrimitive() && original.getAsJsonObject().has("type")
						&& original.getAsJsonObject().size() == 1) {
					return; // e.g. {"type": "x"} encoded inline as "x"
				}
				errors.add(file + ": " + path + " changed shape: " + original + " -> " + encoded);
				return;
			}
			for (var entry : original.getAsJsonObject().entrySet()) {
				JsonElement other = encoded.getAsJsonObject().get(entry.getKey());
				if (other == null && OPTIONAL_FIELDS.contains(path + "/" + entry.getKey())) {
					continue;
				}
				if (other == null) {
					errors.add(file + ": field '" + path + "/" + entry.getKey() + "' was ignored by the game");
				} else {
					checkNothingDropped(file, path + "/" + entry.getKey(), entry.getValue(), other, errors);
				}
			}
		} else if (original.isJsonArray()) {
			if (!encoded.isJsonArray() || encoded.getAsJsonArray().size() != original.getAsJsonArray().size()) {
				errors.add(file + ": " + path + " changed: " + original + " -> " + encoded);
				return;
			}
			for (int i = 0; i < original.getAsJsonArray().size(); i++) {
				checkNothingDropped(file, path + "[" + i + "]", original.getAsJsonArray().get(i), encoded.getAsJsonArray().get(i), errors);
			}
		}
	}
}
