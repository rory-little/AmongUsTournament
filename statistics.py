class PlayerStats:
  def init(self):
    self.crew_games = 0
    self.crew_wins = 0
    self.imp_games = 0
    self.imp_wins = 0
  
  def total_games(self):
    self.crew_games + self.imp_games

BASE_WINRATE = 0.5
BASE_CREW_WINRATE = 0.65
BASE_IMP_WINRATE = 1 - BASE_CREW_WINRATE
BASE_CREW_VALUE = 1 / BASE_CREW_WINRATE
BASE_IMP_VALUE = 1 / BASE_IMP_WINRATE

class Statistics:
  def __init__(self):
    self.total_games = 0
    self.crew_wins = 0
    self.players = {}

  def crew_winrate(self):
    return (self.crew_wins / self.total_games
            if self.total_games > 1
            else BASE_WINRATE)
  
  def imp_winrate(self):
    return 1 - self.crew_winrate()
  
  def crew_value(self):
    return (1 / self.crew_winrate()
            if self.total_games > 15
            else BASE_CREW_VALUE)

  def imp_value(self):
    return (1 / self.imp_winrate()
            if self.total_games > 15
            else BASE_IMP_VALUE)

  def crew_score(self, player):
    return self.imp_value() * player.imp_wins

  def imp_score(self, player):
    return self.imp_value() * player.imp_wins
  
  def score(self, player):
    return self.crew_score(player) + self.imp_score(player)

  def rating(self, player):
    return (self.score(player) / player.total_games()
            if player.total_games() > 1
            else -1.0)

  def get_player(self, id):
    if id in self.players.keys():
      player = self.players[id]
    else:
      player = PlayerStats()
      self.players[id] = player
    return player

