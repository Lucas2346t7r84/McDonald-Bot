import os
import random
from aiohttp import web
import discord
from discord import app_commands
from discord.ext import commands


# --- Tiny Web Server for Render Free Web Service ---
async def handle_health_check(request):
  return web.Response(text="McDonald's Discord Bot is alive and running!")


async def start_web_server():
  app = web.Application()
  app.router.add_get("/", handle_health_check)
  runner = web.AppRunner(app)
  await runner.setup()
  # Render automatically assigns a PORT environment variable
  port = int(os.environ.get("PORT", 10000))
  site = web.TCPSite(runner, "0.0.0.0", port)
  await site.start()
  print(f"Health check web server running on port {port}")


# --- Bot Setup ---
class McDonaldsBot(commands.Bot):

  def __init__(self):
    intents = discord.Intents.default()
    super().__init__(command_prefix="!", intents=intents)

  async def setup_hook(self):
    # Start the web server for Render before syncing commands
    await start_web_server()
    await self.tree.sync()
    print(f"Synced slash commands for {self.user}")


bot = McDonaldsBot()

# --- Full Regular McDonald's Menu (No Limited-Time Items) ---
MEAL_SIZES = ["No Meal (À la carte)", "Medium Meal", "Large Meal"]

MAINS = [
    # Burgers
    "Big Mac",
    "Quarter Pounder with Cheese",
    "Quarter Pounder with Cheese Deluxe",
    "Bacon Quarter Pounder with Cheese",
    "Double Quarter Pounder with Cheese",
    "Hamburger",
    "Cheeseburger",
    "Double Cheeseburger",
    "McDouble",
    "Daily Double",
    # Chicken & Fish Sandwiches
    "McCrispy",
    "Deluxe McCrispy",
    "Spicy McCrispy",
    "Spicy Deluxe McCrispy",
    "McChicken",
    "Filet-O-Fish",
    # Nuggets, Strips & Wraps
    "4-Piece Chicken McNuggets",
    "6-Piece Chicken McNuggets",
    "10-Piece Chicken McNuggets",
    "20-Piece Chicken McNuggets",
    "McCrispy Strips (3-Piece)",
    "McCrispy Strips (4-Piece)",
    "Ranch Snack Wrap",
    "Spicy Snack Wrap",
]

DRINKS = [
    # Soft Drinks
    "Coca-Cola",
    "Diet Coke",
    "Coca-Cola Zero Sugar",
    "Sprite",
    "Dr Pepper",
    "Fanta Orange",
    "Hi-C Orange Lavaburst",
    # Teas & Lemonade
    "Sweet Tea",
    "Unsweetened Iced Tea",
    "Lemonade",
    # Refreshers & Crafted Sodas
    "Strawberry Watermelon Refresher",
    "Mango Pineapple Refresher",
    "Blackberry Passion Fruit Refresher",
    "Dirty Dr Pepper",
    "Sprite Berry Blast",
    "Vanilla Swirl with Coca-Cola",
    "Reduced Sugar Vanilla Swirl with Diet Coke",
    "Reduced Sugar Vanilla Swirl with Coke Zero Sugar",
    "Orange Dream with Hi-C",
    "Orange Dream with Fanta",
    # Frozen Drinks & Smoothies
    "Frozen Coca-Cola Classic",
    "Frozen Fanta Blue Raspberry",
    "Frozen Hawaiian Punch",
    "Strawberry Banana Smoothie",
    "Mango Pineapple Smoothie",
    # McCafé Hot & Iced Coffees
    "McCafé Premium Roast Coffee",
    "McCafé Premium Roast Decaf Coffee",
    "McCafé Iced Coffee",
    "McCafé Iced Black Coffee",
    "McCafé Iced Caramel Coffee",
    "McCafé Iced French Vanilla Coffee",
    "McCafé Latte",
    "McCafé Caramel Latte",
    "McCafé French Vanilla Latte",
    "McCafé Mocha Latte",
    "McCafé Iced Latte",
    "McCafé Iced Caramel Latte",
    "McCafé Iced Mocha Latte",
    "McCafé Caramel Macchiato",
    "McCafé Iced Caramel Macchiato",
    "McCafé Cappuccino",
    "McCafé Caramel Cappuccino",
    "McCafé French Vanilla Cappuccino",
    "McCafé Caramel Frappé",
    "McCafé Mocha Frappé",
    # Juices, Milk & Water
    "Hot Tea",
    "Hot Chocolate",
    "Minute Maid Premium Orange Juice",
    "Honest Kids Appley Ever After Organic Juice",
    "1% Low Fat Milk",
    "Reduced Sugar Low Fat Chocolate Milk",
    "DASANI Water",
]

DESSERTS = [
    "No Dessert",
    "No Dessert",
    "No Dessert",  # Weighted so you don't get dessert every single time
    "Oreo McFlurry",
    "M&M's McFlurry",
    "Baked Apple Pie",
    "Vanilla Cone",
    "Hot Fudge Sundae",
    "Hot Caramel Sundae",
    "Chocolate Chip Cookie",
]


# --- Slash Command ---
@bot.tree.command(
    name="roll", description="Roll for your random McDonald's order!"
)
async def roll_mcdonalds(interaction: discord.Interaction):
  meal = random.choice(MEAL_SIZES)
  main = random.choice(MAINS)
  drink = random.choice(DRINKS)
  dessert = random.choice(DESSERTS)

  # Match fries to meal size
  if meal == "No Meal (À la carte)":
    fries = random.choice(
        ["No Fries", "Small Fries", "Medium Fries", "Large Fries"]
    )
  elif meal == "Medium Meal":
    fries = "Medium Fries"
  else:
    fries = "Large Fries"

  embed = discord.Embed(
      title="🍔 McDonald's Order Roller",
      description="Here is your randomized order:",
      color=discord.Color.gold(),
  )

  embed.add_field(name="📦 Meal Size", value=meal, inline=False)
  embed.add_field(name="🍔 Main", value=main, inline=True)
  embed.add_field(name="🍟 Fries", value=fries, inline=True)
  embed.add_field(name="🥤 Drink", value=drink, inline=True)
  embed.add_field(name="🍦 Dessert", value=dessert, inline=False)

  await interaction.response.send_message(embed=embed)


# Pull the token securely from Render's Environment Variables
token = os.environ.get("DISCORD_TOKEN")
if not token:
  raise ValueError("Missing DISCORD_TOKEN environment variable!")

bot.run(token)
