import discord
from discord.ext import commands

import tournament
from config import Config

ACCEPT_EMOJI = "✅"
DENY_EMOJI = "❌"

ACCEPT_THRESHOLD = 6 # TODO
DENY_THRESHOLD = 2

async def make_declaring_message(ctx:commands.Context,
                           channel:discord.VoiceChannel,
                           players:set[discord.Member],
                           imps:set[discord.Member],
                           imp_win:bool):
  imp_str = ""
  for imp in imps:
    imp_str += f"{imp.mention} "

  player_str = ""
  for player in players:
    player_str += f"{player.mention} "
  
  result_str = "Imposters win!" if imp_win else "Crewmates win!"

  embed = discord.Embed(
      title=f"Game ended in {channel.name}",
      description="Please react to this message to complete the game"
    )
  embed.add_field(name="Players", value=player_str)
  embed.add_field(name="Imposters", value=imp_str)
  embed.add_field(name="Result", value=result_str)

  msg = await ctx.send(channel.mention, embed=embed)
  await msg.add_reaction(ACCEPT_EMOJI)
  await msg.add_reaction(DENY_EMOJI)
  return msg.id


class Game(commands.Cog):
  def __init__(self,
               tournament:tournament.Tournament,
               config:Config):
    self.tournament = tournament
    self.config = config


  async def __get_voice_channel(self,
                          ctx:commands.Context,
                          *channel:discord.VoiceChannel):
    user_channel = None
    for vc in ctx.guild.voice_channels:
      if ctx.author in vc.members:
        user_channel = vc

    if len(channel) == 0:
      channel = user_channel
    elif len(channel) >= 2:
      raise commands.BadArgument(message="Too many voice channels given")
    elif (channel != user_channel
          and ctx.author.top_role < self.config.get_mod()):
      await ctx.send(
          f"Only {self.config.get_mod().name} can start and end games "
          "they are not in"
        )
      return None
    else:
      channel = channel[0]

    if not channel:
      await ctx.send(
          "Please specify which game (ping the game's voice channel) or join "
          "that voice channel and retry this command"
        )

    return channel


  @commands.command(name='start', aliases=['begin'])
  async def start(self,
                  ctx:commands.Context,
                  *channel:commands.VoiceChannelConverter):
    channel = await self.__get_voice_channel(ctx, *channel)
    
    if not channel:
      return
    
    err = self.tournament.start_game(set(channel.members), channel.id)

    if not err:
      await ctx.send(f"Game started in {channel.mention}")
    else:
      await ctx.send(err)


  @commands.command(name='cancel')
  async def cancel(self,
                   ctx:commands.Context,
                   *channel:commands.VoiceChannelConverter):
    channel = await self.__get_voice_channel(ctx, *channel)

    if not channel:
      return
    
    if self.tournament.cancel_game(channel.id):
      await ctx.send("Game successfully cancelled")
    else:
      await ctx.send("No active game exists to cancel")


  async def __declare_result(self,
                       ctx:commands.Context,
                       imps:set[discord.Member],
                       imp_win:bool,
                       *channel:discord.VoiceChannel):
    channel = await self.__get_voice_channel(ctx, *channel)

    if not channel:
      return
    
    players = self.tournament.game_players(channel.id)

    if not players:
      await ctx.send(f"A game in {channel.mention} was not started, and so a "
                     "result cannot be declared")
      return

    msg_id = await make_declaring_message(ctx, channel, players, imps, imp_win)
    self.tournament.declare_game(channel.id, imps, imp_win, msg_id)


  @commands.command(name='impwin', aliases=['iw', 'crewlose', 'cl'])
  async def imp_win(self, ctx,
                    imp1:commands.MemberConverter,
                    imp2:commands.MemberConverter,
                    *channel:commands.VoiceChannelConverter):
    await self.__declare_result(ctx, {imp1, imp2}, True, *channel)


  @commands.command(name='implose', aliases=['il', 'crewwin', 'cw'])
  async def imp_lose(self, ctx,
                    imp1:commands.MemberConverter,
                    imp2:commands.MemberConverter,
                    *channel:commands.VoiceChannelConverter):
    await self.__declare_result(ctx, {imp1, imp2}, False, *channel)


  @commands.Cog.listener()
  async def on_reaction_add(self,
                            reaction:discord.Reaction,
                            user:discord.Member):
    if reaction.message.id in self.tournament.pending:
      if reaction.emoji == ACCEPT_EMOJI and reaction.count >= ACCEPT_THRESHOLD:
        self.tournament.confirm_result(reaction.message.id)
      elif reaction.emoji == DENY_EMOJI and reaction.count >= DENY_THRESHOLD:
        self.tournament.deny_result(reaction.message.id)

  @commands.Cog.listener()
  async def on_command_error(self,
                             ctx:commands.Context,
                             error):
    await ctx.send("Error in command, try consulting the documentation")
