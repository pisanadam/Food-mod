package com.worldfoods.test;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.worldfoods.content.Defs.Container;
import com.worldfoods.content.Defs.FoodDef;
import com.worldfoods.content.GeneratedDefs;
import com.worldfoods.content.ModContent;

import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.ComposterBlock;
import net.minecraft.world.level.block.CropBlock;
import net.minecraft.world.level.block.state.BlockState;

import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;

/**
 * Runs inside a real Minecraft client with a singleplayer world:
 * crops grow, composting works, food can be eaten (with containers and effects) and screenshots are taken.
 */
public class WorldFoodsClientGameTest implements FabricClientGameTest {
	private final List<String> failures = new ArrayList<>();

	@Override
	public void runTest(ClientGameTestContext ctx) {
		try (TestSingleplayerContext world = ctx.worldBuilder().create()) {
			waitForChunksRender(world);
			TestServerContext server = world.getServer();
			server.runCommand("gamerule random_tick_speed 0");
			server.runCommand("time set noon");
			server.runCommand("weather clear");

			BlockPos origin = server.computeOnServer(s -> player(s).blockPosition());

			testCropsGrow(ctx, server, origin);
			testComposting(ctx, server, origin);
			testEatingWithInput(ctx, server);
			testAllFoodsEdible(server);
			takeInventoryScreenshot(ctx, server);
		}

		if (!failures.isEmpty()) {
			throw new AssertionError("World Foods in-game test failures:\n - " + String.join("\n - ", failures));
		}
	}

	/** {@code getClientLevel()} was renamed to {@code getConnection()} in newer Fabric API versions. */
	private static void waitForChunksRender(TestSingleplayerContext world) {
		for (String getter : List.of("getClientLevel", "getConnection")) {
			try {
				Object client = TestSingleplayerContext.class.getMethod(getter).invoke(world);
				client.getClass().getMethod("waitForChunksRender").invoke(client);
				return;
			} catch (NoSuchMethodException e) {
				// try the next name
			} catch (ReflectiveOperationException e) {
				throw new IllegalStateException(e);
			}
		}
		throw new IllegalStateException("No way to wait for chunk rendering");
	}

	private static ServerPlayer player(MinecraftServer server) {
		return server.getPlayerList().getPlayers().getFirst();
	}

	private void check(boolean ok, String message) {
		System.out.println("[worldfoods-test] " + (ok ? "PASS " : "FAIL ") + message);
		if (!ok) {
			failures.add(message);
		}
	}

	/** Plants every crop (plus vanilla wheat as a control) in front of the player and lets random ticks grow them. */
	private void testCropsGrow(ClientGameTestContext ctx, TestServerContext server, BlockPos origin) {
		List<Block> crops = new ArrayList<>(ModContent.CROP_BLOCKS);
		crops.add(Blocks.WHEAT);
		int z = origin.getZ() + 4;
		int y = origin.getY() - 1;

		server.runOnServer(s -> {
			ServerLevel level = player(s).level();
			player(s).teleportTo(origin.getX() + 0.5, origin.getY(), origin.getZ() + 0.5);
			for (int i = 0; i < crops.size(); i++) {
				int x = origin.getX() - crops.size() / 2 + i;
				level.setBlockAndUpdate(new BlockPos(x, y, z - 1), Blocks.WATER.defaultBlockState());
				level.setBlockAndUpdate(new BlockPos(x, y, z), Blocks.FARMLAND.defaultBlockState());
				level.setBlockAndUpdate(new BlockPos(x, y + 1, z), crops.get(i).defaultBlockState());
				// a second row frozen at different ages, for the screenshot
				level.setBlockAndUpdate(new BlockPos(x, y, z + 1), Blocks.FARMLAND.defaultBlockState());
				CropBlock crop = (CropBlock) crops.get(i);
				level.setBlockAndUpdate(new BlockPos(x, y + 1, z + 1), crop.getStateForAge(i % 8));
				level.setBlockAndUpdate(new BlockPos(x, y, z + 2), Blocks.FARMLAND.defaultBlockState());
				level.setBlockAndUpdate(new BlockPos(x, y + 1, z + 2), crop.getStateForAge(crop.getMaxAge()));
			}
		});

		ctx.waitTicks(5);
		server.runCommand("gamerule random_tick_speed 1000");
		// Growth is random: wait until everything is ripe (or give up after 1200 ticks).
		Map<String, Boolean> grown = Map.of();
		for (int waited = 0; waited < 1200; waited += 50) {
			ctx.waitTicks(50);
			grown = cropStates(server, crops, origin, y, z);
			if (!grown.containsValue(false)) {
				break;
			}
		}
		server.runCommand("gamerule random_tick_speed 0");
		grown.forEach((id, ok) -> check(ok, id + " grows to max age"));

		// Look at the field and take a screenshot.
		server.runOnServer(s -> player(s).teleportTo(origin.getX() + 0.5, origin.getY() + 2, origin.getZ() + 0.5));
		ctx.runOnClient(mc -> {
			mc.player.setYRot(0);
			mc.player.setXRot(40);
		});
		ctx.waitTicks(20);
		ctx.takeScreenshot("worldfoods-crops");
	}

	private static Map<String, Boolean> cropStates(TestServerContext server, List<Block> crops, BlockPos origin, int y, int z) {
		return server.computeOnServer(s -> {
			ServerLevel level = player(s).level();
			Map<String, Boolean> result = new java.util.LinkedHashMap<>();
			for (int i = 0; i < crops.size(); i++) {
				int x = origin.getX() - crops.size() / 2 + i;
				BlockState state = level.getBlockState(new BlockPos(x, y + 1, z));
				Block block = crops.get(i);
				result.put(BuiltInRegistries.BLOCK.getKey(block).toString(),
						state.is(block) && ((CropBlock) block).isMaxAge(state));
			}
			return result;
		});
	}

	private void testComposting(ClientGameTestContext ctx, TestServerContext server, BlockPos origin) {
		BlockPos composter = origin.offset(-12, 0, -3);
		BlockPos control = origin.offset(-14, 0, -3);
		server.runOnServer(s -> {
			ServerLevel level = player(s).level();
			for (BlockPos pos : List.of(composter, control)) {
				level.setBlockAndUpdate(pos, Blocks.COMPOSTER.defaultBlockState());
				level.setBlockAndUpdate(pos.above(), Blocks.HOPPER.defaultBlockState());
			}
		});
		server.runCommand(String.format("item replace block %d %d %d container.0 with worldfoods:tomato 64",
				composter.getX(), composter.getY() + 1, composter.getZ()));
		server.runCommand(String.format("item replace block %d %d %d container.0 with worldfoods:tomato_seeds 64",
				control.getX(), control.getY() + 1, control.getZ()));
		ctx.waitTicks(100);

		int[] levels = server.computeOnServer(s -> new int[] {
				player(s).level().getBlockState(composter).getValue(ComposterBlock.LEVEL),
				player(s).level().getBlockState(control).getValue(ComposterBlock.LEVEL)});
		check(levels[0] > 0, "tomatoes can be composted (composter level " + levels[0] + ")");
		check(levels[1] > 0, "seeds can be composted (composter level " + levels[1] + ")");
	}

	/** Eats food with real mouse input, like a player would. */
	private void testEatingWithInput(ClientGameTestContext ctx, TestServerContext server) {
		server.runOnServer(s -> {
			ServerPlayer p = player(s);
			p.setGameMode(GameType.SURVIVAL);
			p.removeAllEffects();
			p.getFoodData().setFoodLevel(4);
			p.getInventory().clearContent();
			p.getInventory().setItem(0, new ItemStack(ModContent.ITEMS.get("lentil_soup")));
			p.getInventory().setItem(1, new ItemStack(ModContent.ITEMS.get("turkish_coffee")));
		});
		ctx.runOnClient(mc -> mc.player.getInventory().setSelectedSlot(0));
		ctx.waitTicks(5);
		ctx.getInput().holdKeyFor(options -> options.keyUse, 50);
		ctx.waitTicks(10);

		ctx.runOnClient(mc -> mc.player.getInventory().setSelectedSlot(1));
		ctx.waitTicks(5);
		ctx.getInput().holdKeyFor(options -> options.keyUse, 50);
		ctx.waitTicks(10);

		server.runOnServer(s -> {
			ServerPlayer p = player(s);
			int food = p.getFoodData().getFoodLevel();
			check(food >= 4 + 7 + 2, "eating lentil soup + turkish coffee restores hunger (food level " + food + ")");
			check(p.getInventory().getItem(0).is(Items.BOWL), "lentil soup leaves a bowl (" + p.getInventory().getItem(0) + ")");
			check(p.getInventory().getItem(1).is(Items.GLASS_BOTTLE), "turkish coffee leaves a glass bottle (" + p.getInventory().getItem(1) + ")");
			check(p.hasEffect(MobEffects.SPEED) && p.hasEffect(MobEffects.HASTE), "turkish coffee gives speed + haste");
		});
	}

	/** Every edible item restores hunger and leaves the right container. */
	private void testAllFoodsEdible(TestServerContext server) {
		List<FoodDef> foods = new ArrayList<>(GeneratedDefs.FOODS);
		GeneratedDefs.CROPS.forEach(c -> foods.add(c.produce()));

		server.runOnServer(s -> {
			ServerPlayer p = player(s);
			int edible = 0;
			for (FoodDef def : foods) {
				if (!def.edible()) {
					continue;
				}
				edible++;
				Item item = ModContent.ITEMS.get(def.id());
				p.getFoodData().setFoodLevel(0);
				p.getFoodData().setSaturation(0);
				ItemStack rest = new ItemStack(item).finishUsingItem(p.level(), p);
				int food = p.getFoodData().getFoodLevel();
				Item expected = switch (def.container()) {
					case BOWL -> Items.BOWL;
					case BOTTLE -> Items.GLASS_BOTTLE;
					case STICK -> Items.STICK;
					case NONE -> Items.AIR;
				};
				boolean containerOk = def.container() == Container.NONE ? rest.isEmpty() : rest.is(expected);
				if (food != def.nutrition() || !containerOk) {
					check(false, def.id() + ": food " + food + "/" + def.nutrition() + ", left " + rest);
				}
			}
			check(true, edible + " edible items checked");
		});
	}

	private void takeInventoryScreenshot(ClientGameTestContext ctx, TestServerContext server) {
		server.runOnServer(s -> {
			ServerPlayer p = player(s);
			p.getInventory().clearContent();
			List<Item> items = new ArrayList<>(ModContent.ITEMS.values());
			for (int i = 0; i < 36 && i < items.size(); i++) {
				p.getInventory().setItem(i, new ItemStack(items.get(items.size() - 1 - i)));
			}
		});
		ctx.waitTicks(5);
		var clientPlayer = ctx.computeOnClient(mc -> mc.player);
		ctx.setScreen(() -> new InventoryScreen(clientPlayer));
		ctx.waitTicks(10);
		ctx.takeScreenshot("worldfoods-inventory");
		ctx.setScreen(() -> null);
	}
}
