import sublime, sublime_plugin
from sys import maxint
import subprocess

def score_for_string(dick, dildo):
  # compare the dick to the dildo, find the one closest to the real thing
  if dick == dildo:
    return maxint

  dick_len = len(dick)
  score = 0
  score_increment = 1
  dick_index = 0
  last_match = False

  for dildo_char in dildo:
    if dick_index >= dick_len:
      break

    dick_char = dick[dick_index]
    dick_range = range(dick_index, dick_len)

    if len(dick_range) is 0:
      break

    for idx in dick_range:
      if dick_char is dildo_char:
        if not last_match:
          score = 1

        score += score_increment
        score_increment += 2
        dick_index += 1

        last_match = True

        break

      last_match = False

  return score
  # after-thought: WHY

def sorted_string_score_pairs(pairs):
  def compare(l, r):
    if r['score'] < l['score']:
      return -1
    elif r['score'] > l['score']:
      return 1
    return 0

  sortlist = sorted(pairs, compare)
  uniquelist = []

  for item in sortlist:
    # skip items we've already scanned and assigned
    if item['checked']:
      continue

    item_name = item['entry'][0]
    item_desc = item['entry'][1]

    is_dupe = False

    for uniq in uniquelist:
      if item_name == uniq['entry'][0]:
        is_dupe = True
        uniq['entry'].append(item_desc)
        item['checked'] = True
        break

    if not is_dupe:
      item['checked'] = True
      uniquelist.append(item)

  return (item['entry'] for item in uniquelist)

def query_manpages(keyword, use_apropos=False):
  cmd = 'whatis'

  if use_apropos:
    cmd = 'apropos'

  proc = subprocess.Popen([cmd, keyword], stdout = subprocess.PIPE)
  outs = proc.communicate()[0]

  queries = []

  if outs:
    splits = (line.split(" - ", 1) for line in outs.splitlines())
    for split in splits:
      if len(split) != 2:
        continue

      desc = split[1]
      names = (name.strip() for name in split[0].split(", "))
      for name in names:
        name_sans_sect = name[:name.index('(')]
        score = score_for_string(keyword, name_sans_sect)
        queries.append({
            'score': score,
            'entry': [name, desc],
            'checked': False
          })

  return queries

def manpage_for_query(query):
  # expects query in form 'memcpy(3)'
  name = query[:query.index('(')]
  sect = query[query.index('(')+1:query.index(')')]

  manproc = subprocess.Popen(['man', sect, name], stdout=subprocess.PIPE)
  colproc = subprocess.Popen(['col', '-b'], stdin=manproc.stdout, stdout=subprocess.PIPE)
  manproc.stdout.close()

  page = colproc.communicate()[0]

  return page

class OpenManPageCommand(sublime_plugin.WindowCommand):
  def queries_for_view(self, view):
    results = []

    for region in view.sel():
      if region.empty():
        region = view.word(region)

      query = str(view.substr(region)).strip()
      if len(query) is 0:
        continue

      results += query_manpages(str(query))

    results = sorted_string_score_pairs(results)

    self.choose_from_results(results)


  def get_query_input(self, input):
    if input is None or input == '':
      return

    results = sorted_string_score_pairs(query_manpages(str(query), False))
    self.choose_from_results(results)

  def run(self, source):
    if source == 'input':
      self.window.show_input_panel('man query', '', self.get_query_input, None, None)
    elif source == 'view':
      self.queries_for_view(self.window.active_view())
    else:
      print "open_man_page: Incorrect source provided"

  def choose_from_results(self, queries):
    self.entries = list(queries)
    if len(self.entries) is 0:
      return
    elif len(self.entries) is 1:
      self.entry_selected(1)
    else:
      self.window.show_quick_panel(self.entries, self.entry_selected)

  def entry_selected(self, index):
    if index is -1:
      return
    entry = self.entries[index]
    page = manpage_for_query(entry[0])
    self.open_view_with_string(entry[0], page)

  def open_view_with_string(self, name, page):
    view = self.window.new_file()
    view.set_name(name)
    view.set_scratch(True)
    edit = view.begin_edit()
    region = sublime.Region(0, view.size())
    view.insert(edit, 0, page)
    view.end_edit(edit)