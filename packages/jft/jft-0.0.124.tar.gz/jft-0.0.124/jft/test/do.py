from time import time
from jft.test.handle_pass import f as hp
from jft.dict.test_durations.to_tuple_list_sorted_by_duration import f as srt
from jft.directory.list_testables import f as list_testables
from os.path import getmtime
from jft.test.make_Π_to_test import f as make_Π_t
from jft.pickle.load_if_exists import f as load_pickle
from jft.file.remove import f as remove
from jft.pickle.save import f as save
from jft.strings.pyfiles.to_dict import f as pyfiles_to_dict
from jft.string.contains.function.test import f as has_t
from jft.string.contains.function.run import f as has_f
from jft.test.π_test_failed import f as π_test_failed
from jft.test.handle_fail import f as hf
from jft.text_colours.danger import f as danger
from jft.text_colours.warning import f as warn
"""
from jft.file.load import f as load
from jft.text_colours.success import f as success
from jft.pf import f as pf
def check_line_lengths(Π=None):
  print('Checking line lengths...', end='\r')
  Π = list_testables() or Π
  for π in Π:
    ignore_line_lengths = False
    for line_index, line in enumerate(load(π).split('\n')):
      if 'ignore_overlength_lines' in line: ignore_line_lengths = True
      if len(line) > 80 and not ignore_line_lengths: return pf([
        f'{π}:{line_index+1}',
        danger(line)
      ])
  print(f"{success('PASS')} Line Lengths "+' '*20)
def check_final_line(Π=None):
  print('Checking final lines...', end='\r')
  Π = list_testables() or Π
  for π in Π:
    _lines = load(π).split('\n')
    _last_line_index = len(_lines)-1
    _line = _lines[_last_line_index]
    if _line != '': return pf([
      f'{π}:{_last_line_index}',
      danger([_line])
    ])
  print(f"{success('PASS')} Final lines "+' '*20)
def print_oldest_file(Π=None):
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
def check_return_false(Π=None):
  print('Checking for return False lines...', end='\r')
  Π = list_testables() or Π
  for π in Π:
    for line_index, line in enumerate(load(π).split('\n')):
      if 'return False' in line.strip(): return pf([
        f'{π}:{line_index+1:<40}', danger(line)
      ])
  print(f"{success('PASS')} Return False check "+' '*20)
"""
def f(test_all=False, t_0=time()):
  Π = list_testables()
  try: prev = load_pickle('./last_modified.pickle') or set()
  except EOFError as eofe: remove('./last_modified.pickle'); prev = set()
  last_mods = {py_filename: getmtime(py_filename) for py_filename in Π}
  save(last_mods, './last_modified.pickle')
  Π_fail = set()
  _A = [_[0] for _ in srt(last_mods)[::-1]]
  _B = set(make_Π_t(Π, test_all, prev, last_mods) + list(Π_fail))
  Π_t = [a for a in _A if a in _B]
  pyfile_data = pyfiles_to_dict(Π_t)
  max_len = 0
  for π_index, π in enumerate(Π_t):
    content = pyfile_data[π]
    _m = ' '.join([
      f'[{(100*(π_index+1)/len(Π_t)):> 6.2f} % of',
      f'{π_index+1}/{len(Π_t)} files.] Checking {π}'
    ])
    max_len = max(max_len, len(_m))
    # print(f'{_m:<{max_len}}', end='\r')
    print(f'{_m:<{max_len}}')
    if not has_t(content): return hf(Π_fail, π, danger(" has no ")+warn('t()'))
    if not has_f(content): return hf(Π_fail, π, danger(" has no ")+warn('f()'))
    if π_test_failed(π): return hf(Π_fail, π, '')
  return hp(t_0, Π_t)
