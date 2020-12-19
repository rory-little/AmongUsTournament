import discord
from discord.ext import commands

from statistics import Statistics

class Viewer(commands.Cog):
  def __init__(self, client, stats):
    self.client = client
    self.stats = stats

  @commands.command(name='rating', aliases=['mmr', 'mr', 'me'])
  async def rating(self, ctx:commands.Context,
                   member:commands.MemberConverter):
    player = self.stats.get_player(member.id)
    embed = discord.Embed(title=f"Rating for {member.name}: ")
    embed.add_field(name="Rating", value=f"{self.stats.rating(player)}")
    embed.add_field(name="Imp Wins",
                    value=f"{player.imp_wins}/{player.imp_games}")
    embed.add_field(name="Crew Wins",
                    value=f"{player.crew_wins}/{player.crew_games}")
    await ctx.send("", embed=embed)
