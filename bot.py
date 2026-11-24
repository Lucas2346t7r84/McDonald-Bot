import os
from aiohttp import web
import discord
from discord.ext import commands


async def _healthcheck(request: web.Request) -> web.Response:
  return web.Response(text="OK")


async def _start_web_server() -> None:
  app = web.Application()
  app.router.add_get("/", _healthcheck)
  runner = web.AppRunner(app)
  await runner.setup()
  port = int(os.environ.get("PORT", 10000))
  site = web.TCPSite(runner, "0.0.0.0", port)
  await site.start()


class ExistingBot(commands.Bot):

  def __init__(self):
    intents = discord.Intents.default()
    # Enable message_content only if your existing bot uses prefix commands
    super().__init__(command_prefix="!", intents=intents)

  async def setup_hook(self):
    await _start_web_server()
    await self.load_extension("cogs.mcdonalds")
    # Load any other cogs your bot already has here
    await self.tree.sync()


bot = ExistingBot()

token = os.environ.get("DISCORD_TOKEN")
if not token:
  raise RuntimeError("Set DISCORD_TOKEN in Render's Environment settings.")

bot.run(token)
