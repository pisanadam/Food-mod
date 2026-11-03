package com.worldfoods.block;

import java.util.function.Supplier;

import net.minecraft.world.item.Item;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.block.CropBlock;

/** A standard 8-stage crop that drops/clones its own seeds item. */
public class WorldFoodsCropBlock extends CropBlock {
	private final Supplier<Item> seeds;

	public WorldFoodsCropBlock(Properties properties, Supplier<Item> seeds) {
		super(properties);
		this.seeds = seeds;
	}

	@Override
	protected ItemLike getBaseSeedId() {
		return seeds.get();
	}
}
