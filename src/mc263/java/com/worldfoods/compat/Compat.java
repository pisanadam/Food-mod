package com.worldfoods.compat;

import java.util.List;

import net.minecraft.core.Holder;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.storage.loot.LootPool;
import net.minecraft.world.level.storage.loot.entries.LootItem;
import net.minecraft.world.level.storage.loot.predicates.LootItemRandomChanceCondition;
import net.minecraft.world.level.storage.loot.providers.number.ints.ConstantValue;
import net.minecraft.world.level.storage.loot.providers.number.ints.ContextIntProviders;

/** Version-specific code for Minecraft 26.3+. */
public final class Compat {
	private Compat() {
	}

	/** Composting is a data component of the item since 26.3. */
	public static Item.Properties compostable(Item.Properties props, Compost compost) {
		return switch (compost) {
			case LOW -> props.compostable(ContextIntProviders.COMPOSTABLE_LOW);
			case MEDIUM -> props.compostable(ContextIntProviders.COMPOSTABLE_MEDIUM);
			case NONE -> props;
		};
	}

	public static void afterItemRegistered(Item item, Compost compost) {
	}

	/** A loot pool that drops one random item from {@code items} with the given chance. */
	public static LootPool.Builder randomItemPool(List<Item> items, float chance) {
		LootPool.Builder pool = LootPool.lootPool()
				.setRolls(Holder.direct(new ConstantValue(1)))
				.when(Holder.direct(LootItemRandomChanceCondition.randomChance(chance).build()));
		items.forEach(item -> pool.add(LootItem.lootTableItem(item)));
		return pool;
	}
}
