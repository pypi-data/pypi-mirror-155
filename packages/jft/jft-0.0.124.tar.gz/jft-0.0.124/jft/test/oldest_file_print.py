from jft.directory.list_testables import f as list_testables
from os.path import getmtime
from jft.pickle.load_if_exists import f as load_pickle
from jft.file.remove import f as remove
from jft.pickle.save import f as save
from jft.test.make_Π_to_test import f as make_Π_t
from jft.dict.test_durations.to_tuple_list_sorted_by_duration import f as srt

def f(Π=None):
  Π = list_testables()
  try: prev = load_pickle('./last_modified.pickle') or set()
  except EOFError as eofe: remove('./last_modified.pickle'); prev = set()
  last_mods = {py_filename: getmtime(py_filename) for py_filename in Π}
  save(last_mods, './last_modified.pickle')
  Π_fail = set()
  _A = [_[0] for _ in srt(last_mods)[::-1]]
  _B = set(make_Π_t(Π, True, prev, last_mods) + list(Π_fail))
  Π_t = [a for a in _A if a in _B]
  print(f'Oldest file: {Π_t[-1]}')

def t(): return True # TODO
