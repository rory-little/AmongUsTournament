import dotenv
import os

import discord
from discord.ext import commands

from statistics import Statistics

DOTENV_PATH = ".env"
TOKEN_KEY = "DISCORD_TOKEN"

def make_finished_message(lobby, imps, win):
  return 0

class Tournament:
  def __init__(self):
    self.lobbies = []
    self.pending = {}
    self.queue = []
    self.statistics = Statistics()
  
  def find_lobby_by_players(self, players):
    for lobby in self.lobbies:
      if players < lobby:
        return lobby
  
  def start_game(self, lobby):
    self.lobbies.append(lobby)
  
  def conclude_game(self, lobby, imps, imp_win, id):
    # construct message here
    self.pending[id] = lobby
    self.lobbies.remove(lobby)


LOBBY_SIZE = 10

class Game(commands.Cog):
  def __init__(self, tournament):
    self.tournament = tournament

  @commands.command(name='start', aliases=['begin'])
  async def start(self, ctx):
    for channel in ctx.guild.voice_channels:
      if ctx.author in channel.members and len(channel.members) == LOBBY_SIZE:
        self.tournament.start_game(set(channel.members))


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
  t = Tournament()
  load_cogs(bot, t)
  bot.run(os.getenv(TOKEN_KEY))


if __name__ == '__main__':
  main()
