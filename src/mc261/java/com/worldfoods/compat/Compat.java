package com.worldfoods.compat;

import java.util.List;

import net.minecraft.world.item.Item;
import net.minecraft.world.level.storage.loot.LootPool;
import net.minecraft.world.level.storage.loot.entries.LootItem;
import net.minecraft.world.level.storage.loot.predicates.LootItemRandomChanceCondition;
import net.minecraft.world.level.storage.loot.providers.number.ConstantValue;

import net.fabricmc.fabric.api.registry.CompostableRegistry;

/** Version-specific code for Minecraft 26.1 - 26.2. */
public final class Compat {
	private Compat() {
	}

	/** Called while building the item's properties. Composting is registered after creation on this version. */
	public static Item.Properties compostable(Item.Properties props, Compost compost) {
		return props;
	}

	/** Called once the item is registered. */
	public static void afterItemRegistered(Item item, Compost compost) {
		if (compost != Compost.NONE) {
			CompostableRegistry.INSTANCE.add(item, compost.chance);
		}
	}

	/** A loot pool that drops one random item from {@code items} with the given chance. */
	public static LootPool.Builder randomItemPool(List<Item> items, float chance) {
		LootPool.Builder pool = LootPool.lootPool()
				.setRolls(ConstantValue.exactly(1))
				.when(LootItemRandomChanceCondition.randomChance(chance));
		items.forEach(item -> pool.add(LootItem.lootTableItem(item)));
		return pool;
	}
}
