import random
import discord
from discord import app_commands
from discord.ext import commands


class McDonalds(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot

    self.meal_sizes = [
        "No Meal (À la carte)",
        "Medium Meal",
        "Large Meal",
    ]

    self.mains = [
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

    self.drinks = [
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

    self.desserts = [
        "No Dessert",
        "No Dessert",
        "No Dessert",
        "Oreo McFlurry",
        "M&M's McFlurry",
        "Baked Apple Pie",
        "Vanilla Cone",
        "Hot Fudge Sundae",
        "Hot Caramel Sundae",
        "Chocolate Chip Cookie",
    ]

  @app_commands.command(
      name="roll", description="Roll for your random McDonald's order!"
  )
  async def roll(self, interaction: discord.Interaction):
    meal = random.choice(self.meal_sizes)
    main = random.choice(self.mains)
    drink = random.choice(self.drinks)
    dessert = random.choice(self.desserts)

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


async def setup(bot: commands.Bot):
  await bot.add_cog(McDonalds(bot))
