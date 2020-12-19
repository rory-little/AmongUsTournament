import json
import discord

class Config:
  def __init__(self, client:discord.Client, path="config.json"):
    self.jcfg = json.load(open(path))
    self.client = client
    self.mod = None
  
  def __load_config(self,):
    for guild in self.client.guilds:
      if guild.name == self.jcfg['name']:
        for role in guild.roles:
          if role.name == self.jcfg['mod']:
            self.mod = role
    
    if not self.mod:
      raise Exception('config error: could not find moderator role in guild')
  
  def get_mod(self,):
    if not self.mod:
      self.__load_config()

    return self.mod

# def get_guild_config(name, cfg_data, client):
#   cfg = {}
#   for guild in cfg_data:
#     if guild['name'] == name:
#       for guild
