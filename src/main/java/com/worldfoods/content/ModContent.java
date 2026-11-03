package com.worldfoods.content;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

import com.worldfoods.WorldFoods;
import com.worldfoods.block.WorldFoodsCropBlock;
import com.worldfoods.compat.Compat;
import com.worldfoods.compat.Compost;
import com.worldfoods.content.Defs.Container;
import com.worldfoods.content.Defs.CropDef;
import com.worldfoods.content.Defs.FoodDef;

import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.component.Consumable;
import net.minecraft.world.item.component.Consumables;
import net.minecraft.world.item.consume_effects.ApplyStatusEffectsConsumeEffect;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;

import net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;

/** Registers every block, item and the creative tab. */
public final class ModContent {
	/** All items added by the mod, in creative tab order. */
	public static final Map<String, Item> ITEMS = new LinkedHashMap<>();
	public static final List<Block> CROP_BLOCKS = new ArrayList<>();
	public static final List<Item> SEEDS = new ArrayList<>();
	public static final List<Item> PRODUCE = new ArrayList<>();
	public static final List<Item> DISHES = new ArrayList<>();

	private ModContent() {
	}

	public static void register() {
		for (CropDef crop : GeneratedDefs.CROPS) {
			registerCrop(crop);
		}

		for (FoodDef food : GeneratedDefs.FOODS) {
			DISHES.add(registerFood(food, Compost.NONE));
		}

		CreativeModeTab tab = FabricCreativeModeTab.builder()
				.title(Component.translatable("itemGroup." + WorldFoods.MOD_ID))
				.icon(() -> new ItemStack(ITEMS.getOrDefault("doner", Items.BREAD)))
				.displayItems((params, output) -> ITEMS.values().forEach(output::accept))
				.build();
		Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, WorldFoods.id("main"), tab);
	}

	private static void registerCrop(CropDef crop) {
		ResourceKey<Block> blockKey = ResourceKey.create(Registries.BLOCK, WorldFoods.id(crop.block()));
		Item[] seedsHolder = new Item[1];
		Block block = new WorldFoodsCropBlock(BlockBehaviour.Properties.ofFullCopy(Blocks.WHEAT).setId(blockKey),
				() -> seedsHolder[0]);
		Registry.register(BuiltInRegistries.BLOCK, blockKey, block);
		CROP_BLOCKS.add(block);

		Item seeds = registerItem(crop.seeds(), Compost.LOW, props -> new BlockItem(block, props.useItemDescriptionPrefix()));
		seedsHolder[0] = seeds;
		SEEDS.add(seeds);

		PRODUCE.add(registerFood(crop.produce(), Compost.MEDIUM));
	}

	private static Item registerFood(FoodDef def, Compost compost) {
		return registerItem(def.id(), compost, props -> {
			if (def.craftRemainder() != null) {
				props.craftRemainder(def.craftRemainder());
			}

			if (def.edible()) {
				FoodProperties food = new FoodProperties.Builder()
						.nutrition(def.nutrition())
						.saturationModifier(def.saturation())
						.build();
				Consumable.Builder consumable = def.container() == Container.BOTTLE
						? Consumables.defaultDrink()
						: Consumables.defaultFood();

				if (!def.effects().isEmpty()) {
					List<MobEffectInstance> effects = def.effects().stream()
							.map(e -> new MobEffectInstance(e.effect(), e.duration(), e.amplifier()))
							.toList();
					consumable.onConsume(new ApplyStatusEffectsConsumeEffect(effects));
				}

				props.food(food, consumable.build());

				switch (def.container()) {
					case BOWL -> props.stacksTo(16).usingConvertsTo(Items.BOWL);
					case BOTTLE -> props.stacksTo(16).usingConvertsTo(Items.GLASS_BOTTLE);
					case STICK -> props.usingConvertsTo(Items.STICK);
					case NONE -> { }
				}
			}

			return new Item(props);
		});
	}

	private static Item registerItem(String name, Compost compost, Function<Item.Properties, Item> factory) {
		ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, WorldFoods.id(name));
		Item item = factory.apply(Compat.compostable(new Item.Properties().setId(key), compost));
		Registry.register(BuiltInRegistries.ITEM, key, item);
		Compat.afterItemRegistered(item, compost);
		ITEMS.put(name, item);
		return item;
	}
}
