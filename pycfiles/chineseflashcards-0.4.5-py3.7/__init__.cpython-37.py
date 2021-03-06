# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chineseflashcards/__init__.py
# Compiled at: 2018-09-30 16:12:49
# Size of source mod 2**32: 13471 bytes
import collections, functools, genanki, os.path, re, yaml
__version__ = '0.4.5'
CHINESE_NOTE_MODEL_ID = 2828301746
CEDICT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cedict.txt')
FIELDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fields.json')
TEMPLATES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates.yaml')
CSS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cards.css')
SCRIPT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'add_pinyin_diacritics_and_color.js')

class ChineseNote(genanki.Note):

    def __init__(self, **kwargs):
        (super().__init__)((load_chinese_note_model()), **kwargs)

    @property
    def guid(self):
        return genanki.guid_for(' '.join([
         'kerrick hsk',
         self.fields[0],
         self.fields[1],
         self.fields[2]]))


class CedictWord:

    def __init__(self, trad, simp, pinyin, tw_pinyin, defs, clfrs):
        self.trad = trad
        self.simp = simp
        self.pinyin = pinyin
        self.tw_pinyin = tw_pinyin
        self.defs = defs
        self.clfrs = clfrs

    def __repr__(self):
        return '{}({}, {}, {}, {}, {}, {})'.format(self.__class__.__name__, repr(self.trad), repr(self.simp), repr(self.pinyin), repr(self.tw_pinyin), repr(self.defs), repr(self.clfrs))


class Classifier:

    def __init__(self, trad, simp, pinyin):
        self.trad = trad
        self.simp = simp
        self.pinyin = pinyin

    @classmethod
    def parse(cls, s):
        if '|' in s:
            trad, rest = s.split('|')
            simp, rest = rest.split('[')
        else:
            trad, rest = s.split('[')
            simp = trad
        pinyin = rest.rstrip(']')
        return cls(trad, simp, pinyin)


def _parse_line(line):
    m = re.match('(.+?) (.+?) \\[(.+?)\\] /(.+)/', line.strip())
    defs = m.group(4).split('/')
    actual_defs = []
    clfrs = None
    tw_pinyin = None
    for def_ in defs:
        if def_.startswith('CL:'):
            pieces = def_.split(':', 2)[1].split(',')
            clfrs = [Classifier.parse(piece) for piece in pieces]
        elif def_.startswith('Taiwan pr. '):
            tw_pinyin = def_.split('[')[1].rstrip(']')
        else:
            actual_defs.append(def_)

    return CedictWord(m.group(1), m.group(2), m.group(3), tw_pinyin, actual_defs, clfrs)


DIACRITIC_VOWELS = [
 [
  'ā', 'á', 'ǎ', 'à', 'a'],
 [
  'ē', 'é', 'ě', 'è', 'e'],
 [
  'ī', 'í', 'ǐ', 'ì', 'i'],
 [
  'ō', 'ó', 'ǒ', 'ò', 'o'],
 [
  'ū', 'ú', 'ǔ', 'ù', 'u'],
 [
  'ǖ', 'ǘ', 'ǚ', 'ǜ', 'ü']]

def diacritic_vowel(vowel, tone):
    """
  :param str vowel: one of a e i o u ü
  :param int tone: one of 1 2 3 4 5
  :return str: the vowel with a diacritic added. For example, the args (a, 1) return ā, (i, 5) return i, and (ü, 3)
      return ǚ.
  """
    for row in DIACRITIC_VOWELS:
        if row[4] == vowel:
            return row[(tone - 1)]


def diacritic_syl(syl):
    """
  :param str syl: An ASCII representation of a pinyin syllable with the tone at the end, e.g. ni3, ge5, lu:4. If it's
      neutral tone, it must end in 5, and the two-character sequence u: is used to represent ü.
  :return str: The syllable with the diacritic applied, e.g. nǐ, ge, lǜ.
  """
    if syl == 'r':
        return syl
    rv = []
    tone = int(syl[(-1)])
    curr = syl[0]
    toned = False
    for next_ in syl[1:]:
        if curr == 'u':
            if next_ == ':':
                curr = 'ü'
                continue
        if not curr in 'ae' or toned:
            if not (curr == 'o' and next_ == 'u'):
                if not toned:
                    if not curr in 'aeiouü' or next_ not in 'aeiouü':
                        rv.append(diacritic_vowel(curr, tone))
                        toned = True
                else:
                    rv.append(curr)
                curr = next_

    return ''.join(rv)


def diacritic_syl_and_tone(syl):
    """
  Returns the syllable with a diacritic added and its tone as an int. If the syllable already has a diacritic, it's
  left unchanged and the tone is inferred from it.

  :param str syl: Either an ASCII representation of a pinyin syllable, like ni3, ge5, or lu:4, or a diacritic-based
      representation like nǐ, ge, or lǜ.
  :return (str, int): The syllable with a diacritic added and its tone. For example, both syl='ni3' and syl='nǐ' return
      ('nǐ', 3), both syl='ge5' and syl='ge' return ('ge', 5), and both syl='lu:4' and syl='lǜ' return ('lǜ', 4).
  """
    if syl in ('r', 'r5'):
        return ('r', 5)
    if syl[(-1)] in '12345':
        return (
         diacritic_syl(syl), int(syl[(-1)]))
    for i, vowel_group in enumerate(zip(*DIACRITIC_VOWELS)):
        if set(vowel_group) & set(syl):
            return (
             syl, i + 1)

    raise ValueError('diacritic_syl_and_tone got unexpected argument : {}'.format(syl))


def prettify_defs(defs):
    pieces = [
     '<ol>']
    for def_ in defs:
        pieces.append('<li>')
        pieces.append(def_)
        pieces.append('</li>')

    pieces.append('</ol>')
    return ''.join(pieces)


def prettify_pinyin(p, lower=False):
    """
  Apply diacritics to pinyin and wrap each syllable in <span class="toneN"> tags.

  :param str p: A series of pinyin characters separated by spaces, e.g. 'nu:3 ren2' or 'nǚ rén'.
  :param bool lower: If true, will convert the string to lowercase before processing.
  :return str: Pinyin string with diacritics and tone tags. For example, both p='nu:3 ren2' and p='nǚ rén' will return
      '<span class="tone3">nǚ</span> <span class="tone2">rén</span>'.
  """
    if lower:
        p = p.lower()
    rv = []
    for syl in p.split():
        toned, tone = diacritic_syl_and_tone(syl)
        if tone == 5:
            rv.append(toned)
        else:
            rv.append('<span class="tone{}">{}</span>'.format(tone, toned))

    rv = ' '.join(rv)
    return rv


def prettify_classifiers(clfrs, simp_first=False):
    if clfrs is None:
        return ''
    rv = []
    for clfr in clfrs:
        first, second = clfr.trad, clfr.simp
        if simp_first:
            first, second = second, first
        s = first
        if second != first:
            s += '|' + second
        s += '(' + prettify_pinyin(clfr.pinyin, True) + ')'
        rv.append(s)

    return ', '.join(rv)


def prettify_example_sentences(example_sentences):
    if not example_sentences:
        return ''
    sent = example_sentences[0]
    pieces = [sent.trad, sent.pinyin, sent.eng]
    if sent.simp:
        pieces.insert(1, sent.simp)
    pieces = [p.replace('\n', '<br/>') for p in pieces]
    pieces = ['<p>{}</p>'.format(p) for p in pieces]
    return '\n'.join(pieces)


@functools.lru_cache()
def load_cedict():
    rv = collections.defaultdict(list)
    with open(CEDICT_FILE, encoding='utf-8') as (inf):
        for line in inf:
            if line.startswith('#'):
                continue
            word = _parse_line(line)
            rv[word.trad].append(word)
            if word.simp != word.trad:
                rv[word.simp].append(word)

    return dict(rv)


@functools.lru_cache()
def load_chinese_note_model():
    with open(FIELDS_FILE, encoding='utf-8') as (fields):
        with open(TEMPLATES_FILE, encoding='utf-8') as (templates):
            with open(CSS_FILE, encoding='utf-8') as (css):
                with open(SCRIPT_FILE, encoding='utf-8') as (script):
                    templates_formatted = templates.read()
                    templates_formatted = templates_formatted.replace('CHARACTER', '{{#Traditional}}<span class="nobr">{{Traditional}}</span>|{{/Traditional}}<span class="nobr">{{Simplified}}</span>')
                    templates_formatted = templates_formatted.replace('PINYIN', '{{#Taiwan Pinyin}}{{Taiwan Pinyin}} | {{/Taiwan Pinyin}}{{Pinyin}}')
                    script_contents = []
                    for i, line in enumerate(script.read().splitlines()):
                        if 'BEGIN TESTS' in line:
                            break
                        if i > 0:
                            line = '      ' + line
                        script_contents.append(line)

                    script_contents.append('      main();')
                    script_contents = '\n'.join(script_contents)
                    templates_formatted = templates_formatted.replace('SCRIPT', script_contents)
                    return genanki.Model(CHINESE_NOTE_MODEL_ID,
                      'Chinese',
                      fields=(fields.read()),
                      templates=templates_formatted,
                      css=(css.read()))


class MultipleMatchingWordsException(Exception):
    pass


class NoMatchingWordsException(Exception):
    pass


class ChineseDeck(genanki.Deck):

    def __init__(self, deck_id=None, name=None):
        super().__init__(deck_id, name)
        self._cedict = load_cedict()
        self.preferred_words = {}

    def _lookup_word(self, word, alt_word, pinyin):
        if word in self.preferred_words:
            alt_word = self.preferred_words[word].get('alt_word')
            pinyin = self.preferred_words[word].get('pinyin')
        else:
            candidates = self._cedict.get(word, [])
            matching_candidates = []
            for candidate in candidates:
                if alt_word:
                    if sorted([candidate.simp, candidate.trad]) != sorted([word, alt_word]):
                        continue
                if pinyin not in [None, candidate.pinyin]:
                    continue
                matching_candidates.append(candidate)

            if len(matching_candidates) > 1:
                trimmed_candidates = []
                for candidate in matching_candidates:
                    if not candidate.defs[0].startswith('variant of'):
                        if candidate.defs[0].startswith('old variant of'):
                            continue
                        if re.match('see [^ ]+\\[[^\\]]+\\]', candidate.defs[0]):
                            continue
                        trimmed_candidates.append(candidate)

            else:
                trimmed_candidates = matching_candidates
            if len(trimmed_candidates) > 1:
                help_text = 'you need to disambiguate by passing '
                if alt_word is None and pinyin is None:
                    help_text += 'alt_word and/or pinyin'
                else:
                    if alt_word is None:
                        help_text += 'alt_word'
                    else:
                        help_text += 'pinyin'
                raise MultipleMatchingWordsException('multiple entries for word={} alt_word={} pinyin={}; {}: {}'.format(repr(word), repr(alt_word), repr(pinyin), help_text, matching_candidates))
            assert trimmed_candidates, 'no entries for word={} alt_word={} pinyin={}'.format(repr(word), repr(alt_word), repr(pinyin))
        return trimmed_candidates[0]

    def add_preferred_words(self, dict_):
        """
    :param dict_: A dict where each key is a word and each value is another dict with one or both of the
        keys `pinyin` and `alt_word`. If you add the word in a later call to `add_word`, these values will be used to
        disambiguate which CEDICT entry to use.

    For example, you can pass the dict

      {
        '年': {
          'alt_word': '年',
          'pinyin': 'nian2',
        },
        '听': {
          'pinyin': 'ting1',
        },
      }

    This means that the entry

      年 年 [nian2] /year/CL:個|个[ge4]/

    will be used for 年, instead of the entry

      秊 年 [nian2] /grain/harvest (old)/variant of 年[nian2]/

    or

      年 年 [Nian2] /surname Nian/

    Similarly, the more common meaning of 听 will be used.

    TODO: naming here is kinda meh, clean it up.
    TODO: need tests, there's some weird behavior depending on where you pass simp vs trad.
    """
        self.preferred_words.update(dict_)

    def add_preferred_words_yaml(self, yaml_):
        """
    Same as `add_preferred_words`, but takes a YAML string.
    :param yaml_: A YAML string representing preferred words to add.

    For example, you can pass the string

        '''
        年:
          pinyin: nian2
          alt_word: 年
        听:
          pinyin: ting1
        '''
    """
        self.add_preferred_words(yaml.load(yaml_))

    def add_preferred_words_yaml_from_file(self, path):
        """
    Same as add_preferred_words_yaml, but loads from a file.
    :param path: path to file.
    """
        with open(path, encoding='utf-8') as (h):
            self.add_preferred_words_yaml(h.read())

    def add_word(self, word, alt_word=None, pinyin=None, tags=None):
        """
    Add word by hanzi (e.g. pass word='你好' to add that word to the deck).

    Returns the Note that was added.
    """
        word = self._lookup_word(word, alt_word, pinyin)
        note = ChineseNote(fields=[
         word.simp,
         word.trad,
         prettify_pinyin(word.pinyin, True),
         prettify_defs(word.defs),
         prettify_classifiers(word.clfrs),
         prettify_pinyin(word.tw_pinyin or ''),
         '',
         '',
         '' if word.trad == word.simp else 'y',
         '' if word.trad == word.simp else 'y',
         'y' if word.trad == word.simp else ''],
          tags=tags)
        self.add_note(note)
        return note

    def add_vocab_list_word(self, vocab_word, tags=None):
        """
    Add a word from the chinese_vocab_list package.

    Returns the Note that was added.
    """
        note = ChineseNote(fields=[
         vocab_word.simp,
         vocab_word.trad,
         prettify_pinyin(vocab_word.pinyin, True),
         prettify_defs(vocab_word.defs),
         prettify_classifiers(vocab_word.clfrs),
         prettify_pinyin(vocab_word.tw_pinyin or ''),
         '',
         prettify_example_sentences(vocab_word.example_sentences),
         '' if vocab_word.trad == vocab_word.simp else 'y',
         '' if vocab_word.trad == vocab_word.simp else 'y',
         'y' if vocab_word.trad == vocab_word.simp else ''],
          tags=tags)
        self.add_note(note)
        return note