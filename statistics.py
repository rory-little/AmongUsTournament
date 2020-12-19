class PlayerStats:
  def __init__(self):
    self.crew_games = 0
    self.crew_wins = 0
    self.imp_games = 0
    self.imp_wins = 0
  
  def total_games(self):
    return self.crew_games + self.imp_games


BASE_WINRATE = 0.5
BASE_CREW_WINRATE = 0.65
BASE_IMP_WINRATE = 1 - BASE_CREW_WINRATE
BASE_CREW_VALUE = 1 / BASE_CREW_WINRATE
BASE_IMP_VALUE = 1 / BASE_IMP_WINRATE

MAX_GAMES = 5

WINRATE_GAME_THRESHOLD = 8

class Statistics:
  def __init__(self):
    self.total_games = 0
    self.crew_wins = 0
    self.players = {}

  def crew_winrate(self):
    return (self.crew_wins / self.total_games
            if self.total_games > 1
            else BASE_CREW_WINRATE)
  
  def imp_winrate(self):
    return 1 - self.crew_winrate()
  
  def crew_value(self):
    return (1 / (self.crew_winrate() if self.crew_winrate() != 0 else 0.1)
            if self.total_games > WINRATE_GAME_THRESHOLD
            else BASE_CREW_VALUE)

  def imp_value(self):
    return (1 / (self.imp_winrate() if self.imp_winrate() != 0 else 0.1)
            if self.total_games > WINRATE_GAME_THRESHOLD
            else BASE_IMP_VALUE)

  def crew_score(self, player):
    return self.crew_value() * player.crew_wins

  def imp_score(self, player):
    return self.imp_value() * player.imp_wins
  
  def score(self, player):
    return self.crew_score(player) + self.imp_score(player)

  def rating(self, player):
    return int(self.score(player) / player.total_games() * 1000
            if player.total_games() >= 1
            else -1.0)

  def get_player(self, id):
    # Inefficient, but it's python so we don't care about random object creation
    return self.players.setdefault(id, PlayerStats())

  def enter_result(self, result):
    self.total_games += 1
    self.crew_wins += 0 if result.imp_win else 1

    for member in result.players:
      player = self.get_player(member.id)

      if player.total_games() < MAX_GAMES:
        if member in result.imps:
          player.imp_games += 1
          player.imp_wins += 1 if result.imp_win else 0
        else:
          player.crew_games += 1
          player.crew_wins += 1 if not result.imp_win else 0
