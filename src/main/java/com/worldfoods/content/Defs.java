package com.worldfoods.content;

import java.util.List;

import org.jspecify.annotations.Nullable;

import net.minecraft.core.Holder;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.item.Item;

/** Plain data types used by {@link GeneratedDefs}. */
public final class Defs {
	private Defs() {
	}

	/** What an item leaves behind once eaten. */
	public enum Container {
		NONE,
		BOWL,
		BOTTLE,
		STICK
	}

	/** A status effect applied when the food is eaten. */
	public record Effect(Holder<MobEffect> effect, int duration, int amplifier) {
	}

	/**
	 * An item definition. A nutrition of 0 means the item is a plain (non-edible) ingredient.
	 *
	 * @param craftRemainder item returned when this item is used in a crafting recipe (e.g. a bowl)
	 */
	public record FoodDef(String id, int nutrition, float saturation, Container container, List<Effect> effects,
			@Nullable Item craftRemainder) {
		public boolean edible() {
			return nutrition > 0;
		}
	}

	/** A crop: its block, the seeds that plant it and the item it produces. */
	public record CropDef(String block, String seeds, FoodDef produce) {
	}
}
