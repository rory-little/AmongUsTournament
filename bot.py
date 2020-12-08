import dotenv
import os

import discord
from discord.ext import commands

import tournament
from statistics import Statistics

DOTENV_PATH = ".env"
TOKEN_KEY = "DISCORD_TOKEN"

def make_finished_message(lobby, imps, win):
  return 0

class Game(commands.Cog):
  def __init__(self, tournament):
    self.tournament = tournament.Tournament()

  @commands.command(name='start', aliases=['begin'])
  async def start(self, ctx):
    lobby = self.tournament.find_lobby_by_players([ctx.author])

    if lobby:
      lobby, lobby_id = lobby
      self.tournament.start_game(lobby_id)
    else:
      pass
    for channel in ctx.guild.voice_channels:
      if lobby <= set(channel.members) and len(lobby) >= LOBBY_SIZE:


  @commands.command(name='impwin', aliases=['iw'])
  async def imp_win(self, ctx,
                    imp1:commands.MemberConverter,
                    imp2:commands.MemberConverter):
    imps = set([imp1, imp2])
    lobby = self.tournament.find_lobby_by_players(imps)
    self.tournament.conclude_game(lobby, imps, True)

def load_cogs(bot, tournament):
  pass

def main():
  dotenv.load_dotenv(dotenv_path=DOTENV_PATH)
  bot = commands.Bot(command_prefix="!")
  t = tournament.Tournament()
  load_cogs(bot, t)
  bot.run(os.getenv(TOKEN_KEY))


if __name__ == '__main__':
  main()
