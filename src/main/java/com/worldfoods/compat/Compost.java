package com.worldfoods.compat;

/** Composter chance tiers (matching vanilla's 30% and 65% tiers). */
public enum Compost {
	NONE(0f),
	LOW(0.3f),
	MEDIUM(0.65f);

	public final float chance;

	Compost(float chance) {
		this.chance = chance;
	}
}
