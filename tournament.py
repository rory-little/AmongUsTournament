from statistics import Statistics

LOBBY_WAITING = 0
LOBBY_ACTIVE = 1

LOBBY_SIZE = 10

class Lobby:
  def __init__(self):
    self.players = {}
    self.state = LOBBY_WAITING

  def is_ready(self):
    return len(self.players) == 10 and  self.state == LOBBY_WAITING


class Result:
  def __init__(self, players, imps, imp_win):
    self.players = players
    self.imps = imps
    self.imp_win = imp_win


class Tournament:
  def __init__(self):
    # Queue of members waiting in queue channel
    self.queue = []

    # Lobbies, keyed by channel id
    self.lobbies = {}

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


  def find_lobby_by_players(self, players):
    for id in self.lobbies.keys():
      lobby = self.lobbies[id]
      if players < lobby.players:
        return (lobby, id)
    return None

  def find_lobby_by_id(self, id):
    return self.lobbies.get(id)

  def start_game(self, id):
    lobby = self.lobbies[id]

    # if the lobby is ready, start the game
    if lobby.is_ready():
      self.games[id] = lobby.players
      lobby.state = LOBBY_ACTIVE
      return True
    else:
      return False

  def declare_game(self, lobby, imps, imp_win, id):
    result = Result(self.games[lobby.id], imps, imp_win)
    self.pending[id] = result
    lobby.state = LOBBY_WAITING

  def cancel_game(self, lobby):
    self.games.pop(lobby.id, None)
    lobby.state = LOBBY_WAITING
  
  def confirm_result(self, id):
    result = self.pending.pop(id, None)

    if result:
      self.statistics.enter_result(result)
      return True
    else:
      return False

  def deny_result(self, id):
    result = self.pending.pop(id, None)

    if result:
      self.history.append(result)
      return True
    else:
      return False
