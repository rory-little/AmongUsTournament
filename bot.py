import dotenv
import os

import discord
from discord.ext import commands

import tournament
from game import Game
from viewer import Viewer
from config import Config


DOTENV_PATH = ".env"
TOKEN_KEY = "DISCORD_TOKEN"

def get_intents():
  intents = discord.Intents.default()
  intents.members = True
  intents.emojis = True
  intents.voice_states = True

  return intents

def load_cogs(bot, tournament):
  bot.add_cog(Game(tournament, Config(bot)))
  bot.add_cog(Viewer(bot, tournament.statistics))

def main():
  dotenv.load_dotenv(dotenv_path=DOTENV_PATH)
  bot = commands.Bot(command_prefix="!", intents=get_intents())
  t = tournament.Tournament()
  load_cogs(bot, t)
  bot.run(os.getenv(TOKEN_KEY))

if __name__ == '__main__':
  main()
