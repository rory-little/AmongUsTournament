from statistics import Statistics

LOBBY_SIZE = 10

class Result:
  def __init__(self, players, imps, imp_win):
    self.players = players
    self.imps = imps
    self.imp_win = imp_win


class Tournament:
  def __init__(self):
    # Queue of members waiting in queue channel
    self.queue = []

    # Active games, keyed by lobby id
    self.games = {}

    # Pending results keyed by result message id
    self.pending = {}

    # Games from which results have not yet been accepted, requiring mod action
    self.disputed = []

    # Results which have been accepted, as a queue
    self.history = []

    # Tournament data
    self.statistics = Statistics()

  def game_running(self, game_id):
    return game_id in self.games

  def game_players(self, game_id):
    return self.games.get(game_id)

  def start_game(self, players, game_id):
    if len(players) != LOBBY_SIZE:
      return "You need exactly 10 players to start a game"
    elif game_id in self.games:
      return "Game cannot be started, it is already running"
    else:
      self.games[game_id] = players
      return None

  def declare_game(self, game_id, imps, imp_win, result_id):
    players = self.games.pop(game_id, None)

    if players:
      self.pending[result_id] = Result(players, imps, imp_win)
      return True
    else:
      return False

  def cancel_game(self, game_id):
    return self.games.pop(game_id, None) != None
  
  def confirm_result(self, result_id):
    result = self.pending.pop(result_id, None)

    if result:
      self.statistics.enter_result(result)
      self.history.append(result)
      return True
    else:
      return False

  def deny_result(self, result_id):
    result = self.pending.pop(result_id, None)

    if result:
      self.disputed.append(result)
      return True
    else:
      return False
