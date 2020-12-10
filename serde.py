import json

from statistics import Statistics, PlayerStats

class StatsEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, Statistics):
      return o.__dict__ | {'__statistics__': True}
    elif isinstance(o, PlayerStats):
      return o.__dict__ | {'__player__': True}
    else:
      return json.JSONEncoder.default(self, o)

def as_stats_object(dct:dict):
  if '__statistics__' in dct:
    dct.pop('__statistics__')
    stats = Statistics()
    stats.__dict__ = dct
    return stats
  elif '__player__' in dct:
    dct.pop('__player__')
    stats = PlayerStats()
    stats.__dict__ = dct
    return stats
  else:
    return dct

def serialize_stats(stats):
  return json.dumps(stats, cls=StatsEncoder)

def deserialize_stats(j):
  return json.loads(j, object_hook=as_stats_object)
