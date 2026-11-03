package com.worldfoods;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.worldfoods.compat.Compat;
import com.worldfoods.content.ModContent;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.storage.loot.LootTable;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.loot.v3.LootTableEvents;
import net.fabricmc.fabric.api.registry.VillagerInteractionRegistries;

public class WorldFoods implements ModInitializer {
	public static final String MOD_ID = "worldfoods";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	/** Chance that breaking grass drops one of the mod's seeds. */
	private static final float GRASS_SEED_CHANCE = 0.1f;

	private static final ResourceKey<LootTable> SHORT_GRASS = vanillaLoot("blocks/short_grass");
	private static final ResourceKey<LootTable> TALL_GRASS = vanillaLoot("blocks/tall_grass");
	private static final ResourceKey<LootTable> FERN = vanillaLoot("blocks/fern");

	public static Identifier id(String path) {
		return Identifier.fromNamespaceAndPath(MOD_ID, path);
	}

	private static ResourceKey<LootTable> vanillaLoot(String path) {
		return ResourceKey.create(Registries.LOOT_TABLE, Identifier.withDefaultNamespace(path));
	}

	@Override
	public void onInitialize() {
		ModContent.register();
		registerVillagerInteractions();
		registerGrassSeedDrops();
		LOGGER.info("World Foods loaded: {} items, {} crops", ModContent.ITEMS.size(), ModContent.CROP_BLOCKS.size());
	}

	private static void registerVillagerInteractions() {
		// Seeds are picked up and planted via the minecraft:villager_plantable_seeds tag.
		for (Item seeds : ModContent.SEEDS) {
			VillagerInteractionRegistries.registerCompostable(seeds);
		}
	}

	private static void registerGrassSeedDrops() {
		LootTableEvents.MODIFY.register((key, builder, source, registries) -> {
			if (!source.isBuiltin() || !(key.equals(SHORT_GRASS) || key.equals(TALL_GRASS) || key.equals(FERN))) {
				return;
			}

			builder.withPool(Compat.randomItemPool(ModContent.SEEDS, GRASS_SEED_CHANCE));
		});
	}
}
