package com.worldfoods.test;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.List;

import com.worldfoods.content.ModContent;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.inventory.CreativeModeInventoryScreen;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.decoration.ItemFrame;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.CropBlock;

import net.fabricmc.fabric.api.client.creativetab.v1.FabricCreativeModeInventoryScreen;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;

/**
 * Builds a few scenes and takes 1920x1080 screenshots for the mod page.
 * Only runs when the WORLDFOODS_SHOWCASE environment variable is set.
 */
public class ShowcaseScreenshots implements FabricClientGameTest {
	private static final List<String> TURKISH = List.of("doner", "lahmacun", "pide", "kofte", "shish_kebab", "menemen",
			"manti", "lentil_soup", "imam_bayildi", "stuffed_peppers", "cabbage_rolls", "cacik", "baklava", "simit",
			"kumpir", "ayran", "turkish_tea", "turkish_coffee", "flatbread", "yogurt", "cheese");
	private static final List<String> WORLD = List.of("pizza", "spaghetti_bolognese", "lasagna", "tiramisu", "hamburger",
			"cheeseburger", "hot_dog", "pancakes", "taco", "burrito", "nachos", "sushi", "onigiri", "ramen", "miso_soup",
			"fried_rice", "dumplings", "kimchi", "bibimbap", "chicken_curry", "naan", "pad_thai", "croissant", "baguette",
			"paella", "churros", "hummus", "falafel");

	@Override
	public void runTest(ClientGameTestContext ctx) {
		if (System.getenv("WORLDFOODS_SHOWCASE") == null) {
			return;
		}

		ctx.getInput().resizeWindow(1920, 1080);
		try (TestSingleplayerContext world = ctx.worldBuilder().create()) {
			TestServerContext server = world.getServer();
			server.runCommand("gamerule random_tick_speed 0");
			server.runCommand("time set 5000");
			server.runCommand("weather clear");
			BlockPos o = server.computeOnServer(s -> player(s).blockPosition());
			ctx.waitTicks(40);

			buildFarm(server, o);
			buildMenuWall(server, o.offset(0, 0, -20), TURKISH, 7);
			buildMenuWall(server, o.offset(30, 0, -20), WORLD, 7);
			ctx.waitTicks(40);

			// spectator: no gravity, no hand in view
			server.runCommand("gamemode spectator @a");
			ctx.getInput().pressKey(GLFW_KEY_F1); // hide HUD
			shot(ctx, server, o.offset(0, 9, -2), 0, 42, "01-farm");
			shot(ctx, server, o.offset(-29, 5, 0), -50, 25, "02-farm-side");
			shot(ctx, server, o.offset(-6, 3, 9), 0, 55, "03-farm-closeup");
			shot(ctx, server, o.offset(0, 2, -26), 0, 8, "04-turkish-dishes");
			shot(ctx, server, o.offset(30, 2, -26), 0, 8, "05-world-dishes");

			// first person with a hotbar full of food
			server.runOnServer(s -> {
				ServerPlayer p = player(s);
				p.getInventory().clearContent();
				List<String> hotbar = List.of("doner", "pizza", "sushi", "lentil_soup", "hamburger", "baklava", "taco",
						"turkish_tea", "ramen");
				for (int i = 0; i < hotbar.size(); i++) {
					p.getInventory().setItem(i, new ItemStack(ModContent.ITEMS.get(hotbar.get(i))));
				}
			});
			server.runCommand("gamemode creative @a");
			ctx.getInput().pressKey(GLFW_KEY_F1); // show HUD again
			ctx.waitTicks(220); // let the "game mode changed" chat message fade
			shot(ctx, server, o.offset(3, 0, -1), 20, 30, "06-first-person");

			// creative tab
			ctx.getInput().pressKey(options -> options.keyInventory);
			ctx.waitForScreen(CreativeModeInventoryScreen.class);
			ctx.runOnClient(mc -> ((FabricCreativeModeInventoryScreen) currentScreen(mc)).setSelectedTab(ModContent.TAB));
			ctx.getInput().setCursorPos(5, 5);
			ctx.waitTicks(20);
			ctx.takeScreenshot("worldfoods-showcase-07-creative-tab");
			ctx.setScreen(() -> null);
		}
	}

	private static final int GLFW_KEY_F1 = 290;

	/** The open screen; where it is stored changed between versions, so find it reflectively. */
	private static Screen currentScreen(Minecraft mc) {
		for (Object owner : new Object[] {mc, mc.gui}) {
			for (Class<?> c = owner.getClass(); c != null; c = c.getSuperclass()) {
				for (Field f : c.getDeclaredFields()) {
					if (Screen.class.isAssignableFrom(f.getType()) && !Modifier.isStatic(f.getModifiers())) {
						try {
							f.setAccessible(true);
							Object value = f.get(owner);
							if (value instanceof CreativeModeInventoryScreen) {
								return (Screen) value;
							}
						} catch (ReflectiveOperationException | RuntimeException e) {
							// keep looking
						}
					}
				}
			}
		}
		throw new IllegalStateException("No open screen found");
	}

	private static ServerPlayer player(MinecraftServer server) {
		return server.getPlayerList().getPlayers().getFirst();
	}

	private static void shot(ClientGameTestContext ctx, TestServerContext server, BlockPos pos, float yaw, float pitch, String name) {
		server.runCommand(String.format("tp @a %d %d %d %.1f %.1f", pos.getX(), pos.getY(), pos.getZ(), yaw, pitch));
		ctx.waitTicks(60);
		ctx.takeScreenshot("worldfoods-showcase-" + name);
	}

	/** Strips of every crop, fully grown, with water channels between them. */
	private static void buildFarm(TestServerContext server, BlockPos o) {
		server.runOnServer(s -> {
			ServerLevel level = player(s).level();
			List<Block> crops = ModContent.CROP_BLOCKS;
			int width = crops.size() * 3;
			int x0 = o.getX() - width / 2;
			int y = o.getY() - 1;
			for (int i = 0; i < crops.size(); i++) {
				CropBlock crop = (CropBlock) crops.get(i);
				for (int dz = 0; dz < 14; dz++) {
					int z = o.getZ() + 2 + dz;
					for (int dx = 0; dx < 2; dx++) {
						BlockPos ground = new BlockPos(x0 + i * 3 + dx, y, z);
						level.setBlockAndUpdate(ground, Blocks.FARMLAND.defaultBlockState());
						// a few younger plants at the front so the growth stages are visible
						int age = dz < 2 ? Math.min(crop.getMaxAge(), dz * 3 + dx * 2 + 1) : crop.getMaxAge();
						level.setBlockAndUpdate(ground.above(), crop.getStateForAge(age));
					}
					level.setBlockAndUpdate(new BlockPos(x0 + i * 3 + 2, y, z), Blocks.WATER.defaultBlockState());
				}
			}
			// border path
			for (int x = x0 - 1; x <= x0 + width; x++) {
				level.setBlockAndUpdate(new BlockPos(x, y, o.getZ() + 1), Blocks.DIRT_PATH.defaultBlockState());
				level.setBlockAndUpdate(new BlockPos(x, y + 1, o.getZ() + 16), Blocks.OAK_FENCE.defaultBlockState());
			}
		});
	}

	/** A spruce wall with item frames showing dishes, lanterns on top. */
	private static void buildMenuWall(TestServerContext server, BlockPos o, List<String> items, int cols) {
		server.runOnServer(s -> {
			ServerLevel level = player(s).level();
			int rows = (items.size() + cols - 1) / cols;
			int z = o.getZ();
			int x0 = o.getX() - cols / 2 - 1;
			int y0 = o.getY();
			for (int x = x0; x <= x0 + cols + 1; x++) {
				for (int y = y0 - 1; y <= y0 + rows + 1; y++) {
					boolean edge = x == x0 || x == x0 + cols + 1 || y == y0 - 1 || y == y0 + rows + 1;
					level.setBlockAndUpdate(new BlockPos(x, y, z), edge ? Blocks.STRIPPED_DARK_OAK_LOG.defaultBlockState()
							: Blocks.SPRUCE_PLANKS.defaultBlockState());
				}
				level.setBlockAndUpdate(new BlockPos(x, y0 + rows + 2, z), (x - x0) % 2 == 0
						? Blocks.LANTERN.defaultBlockState() : Blocks.AIR.defaultBlockState());
				for (int dz = 1; dz <= 6; dz++) {
					level.setBlockAndUpdate(new BlockPos(x, y0 - 1, z - dz), Blocks.SMOOTH_STONE.defaultBlockState());
				}
			}
			for (int i = 0; i < items.size(); i++) {
				BlockPos pos = new BlockPos(x0 + 1 + i % cols, y0 + rows - 1 - i / cols, z - 1);
				ItemFrame frame = new ItemFrame(level, pos, Direction.NORTH);
				frame.setItem(new ItemStack(ModContent.ITEMS.get(items.get(i))), false);
				level.addFreshEntity(frame);
			}
		});
	}
}
