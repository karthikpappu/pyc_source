# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\bogglesolver\test\integration_tests.py
# Compiled at: 2014-08-30 00:39:57
# Size of source mod 2**32: 12440 bytes
__doc__ = 'Integration tests for all boggle classes.'
import sys, unittest, os.path, time, sqlite3, os
from bogglesolver.load_english_dictionary import Edict
from bogglesolver.boggle_board import Boggle
from bogglesolver.solve_boggle import SolveBoggle
from bogglesolver.twl06 import WORD_LIST
from bogglesolver.twl06 import TEST_WORD_LIST

class test_solve_boggle(unittest.TestCase):
    """test_solve_boggle"""

    def test_init(self):
        """Test solve boggle."""
        columns = 5
        rows = 1
        array = ['w', 'a', 't', 'e', 'r']
        solve_game = SolveBoggle(True)
        solve_game.set_board(columns, rows, array)
        solve_game.edict.add_word('wata')
        solve_game.edict.add_word('wate')
        solve_game.edict.add_word('a')
        solve_game.edict.add_word('tear')
        solve_game.edict.add_word('tea')
        solve_game.edict.add_word('eat')
        solved = solve_game.solve()
        assert 'water' in solved
        assert 'a' not in solved
        assert 'wata' not in solved
        assert 'wate' in solved
        assert 'eat' not in solved
        assert 'tear' not in solved
        assert 'tea' not in solved
        solve_game.min_word_len = 0
        solved = solve_game.solve()
        assert 'a' in solved
        solved = solve_game.solve(normal_adj=False)
        assert 'water' in solved
        assert 'a' in solved
        assert 'wata' not in solved
        assert 'wate' in solved
        assert 'eat' in solved
        assert 'tea' in solved
        assert 'tear' in solved
        solve_game = SolveBoggle(True)
        solve_game.set_board(columns, rows, None)
        print('Columns are: %s, Rows are: %s' % (columns, rows))
        assert solve_game.boggle.is_full()


class test_everything(unittest.TestCase):
    """test_everything"""

    def test_generate_board(self):
        """Test generating the board."""
        game = Boggle(4, 4)
        game.generate_boggle_board()
        assert game.is_full()

    def test_solves_Boggle(self):
        """Test solving the boggle board."""
        columns = 4
        rows = 4
        array = 'a b c d e f g h i j k l m n o p'.split()
        assert len(array) == columns * rows
        solve_game = SolveBoggle()
        solve_game.set_board(columns, rows, array)
        known_words = [
         'knife', 'mino', 'bein', 'fink', 'nife', 'glop', 'polk', 'mink', 'fino', 'jink', 'nief', 'knop', 'ink', 'fin', 'jin', 'nim', 'kop', 'pol', 'fab', 'fie', 'nie', 'kon', 'lop', 'ab', 'ef', 'if', 'mi', 'be', 'jo', 'ch', 'on', 'lo', 'ae', 'ea', 'in', 'ba', 'fa', 'no', 'ko', 'op', 'po']
        for word in known_words:
            solve_game.edict.add_word(word)

        solve_game.min_word_len = 5
        solved = solve_game.solve()
        for word in known_words:
            if len(word) >= solve_game.min_word_len:
                if not word in solved:
                    raise AssertionError
            elif not word not in solved:
                raise AssertionError

        solve_game.min_word_len = 0
        solved = solve_game.solve()
        for word in known_words:
            if len(word) >= solve_game.min_word_len:
                if not word in solved:
                    raise AssertionError
            elif not word not in solved:
                raise AssertionError

    @unittest.skip('Skipping integration tests.')
    def test_search_speed_vs_raw_read(self):
        """Test search speed."""
        my_dict = Edict()
        my_dict.read_dictionary()
        test_words = TEST_WORD_LIST
        allwords = ' '.join(WORD_LIST)
        alllines = WORD_LIST
        num_slower_than_read = 0
        num_slower_than_readlines = 0
        time1 = time.time()
        time2 = time.time()
        for a_word in test_words:
            word = a_word
            lower = a_word.lower().strip()
            if not my_dict.is_word(lower):
                print(word)
            time1 = time.time()
            assert my_dict.is_word(lower)
            time2 = time.time()
            dict_time = time2 - time1
            time1 = time.time()
            if word not in allwords:
                assert False
            time2 = time.time()
            all_time = time2 - time1
            time1 = time.time()
            if word not in alllines:
                assert False
            time2 = time.time()
            line_time = time2 - time1
            if dict_time > all_time:
                num_slower_than_read += 1
            if dict_time > line_time:
                num_slower_than_readlines += 1
                continue

        assert num_slower_than_read <= 1
        assert num_slower_than_readlines <= 1

    def test_loads_all_words(self):
        """Test the dictionary can load all the words."""
        t0 = time.time()
        my_dict = Edict()
        my_dict.read_dictionary()
        t1 = time.time()
        for line in WORD_LIST:
            my_dict.is_word(line.lower())
            if not my_dict.is_word(line.lower()):
                raise AssertionError

    @unittest.skip('Skipping integration tests.')
    def test_against_my_sql(self):
        """Test searching in custom dictionary is faster than in my_sql."""
        my_dict = Edict()
        my_dict.read_dictionary()
        num_slower_than_sql = 0
        conn = sqlite3.connect('example.db')
        con = conn.cursor()
        con.execute('CREATE TABLE my_dict (word text)')
        for word in WORD_LIST:
            con.execute('INSERT INTO my_dict VALUES (?)', [word])

        conn.commit()
        test_words = TEST_WORD_LIST
        time1 = time.time()
        time2 = time.time()
        for word in test_words:
            time1 = time.time()
            my_dict.is_word(word)
            time2 = time.time()
            d_time = time2 - time1
            time1 = time.time()
            con.execute('SELECT * FROM my_dict WHERE word=?', [word])
            time2 = time.time()
            b_time = time2 - time1
            if d_time > b_time:
                num_slower_than_sql += 1
                print('D time is: ' + str(d_time))
                print('B time is: ' + str(b_time))
                continue

        con.close()
        conn.close()
        os.remove('example.db')
        assert num_slower_than_sql <= 1


class test_speed_against_other_libraries(unittest.TestCase):
    """test_speed_against_other_libraries"""

    def test_pypi_init_speeds(self):
        """Test how fast they load."""
        import boggleboard
        other_default_size = 4
        letters = ['i', 'r', 'e', 'e', 'r', 'i', 'u', 'c', 't', 's', 'i', 'e', 'a', 'n', 'i', 'a']
        t1 = time.time()
        their_boggle = boggleboard.BoggleBoard(other_default_size, letters)
        their_trie = boggleboard.Trie(WORD_LIST)
        t2 = time.time()
        their_time = t2 - t1
        t1 = time.time()
        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)
        t2 = time.time()
        my_time = t2 - t1
        print('My init time is: %s' % my_time)
        print('Their init time is: %s' % their_time)
        print('Mine is %s slower.' % (my_time / their_time))
        assert my_time / their_time < 2

    def test_pypi_4_by_4(self):
        """Test 4x4 against the current boggle board on pypi."""
        import boggleboard
        other_default_size = 4
        letters = ['i', 'r', 'e', 'e',
         'r', 'i', 'u', 'c',
         't', 's', 'i', 'e',
         'a', 'n', 'i', 'a']
        their_boggle = boggleboard.BoggleBoard(other_default_size, letters)
        their_trie = boggleboard.Trie(WORD_LIST)
        t1 = time.time()
        their_words = their_boggle.findWords(their_trie)
        t2 = time.time()
        their_solve_time = t2 - t1
        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)
        t1 = time.time()
        my_words = my_boggle.solve()
        t2 = time.time()
        my_solve_time = t2 - t1
        time_difference = my_solve_time / their_solve_time
        print('I found %s words.' % len(my_words))
        print('They found %s words.' % len(their_words))
        print('Mine is %s percent slower' % time_difference)
        print('My total time %s\nTheir total time %s' % (my_solve_time, their_solve_time))
        for word in their_words:
            if word not in my_words:
                print("I didn't find: %s" % word)
                if not my_boggle.edict.is_word(word):
                    raise AssertionError
                continue

        for word in my_words:
            if not word in their_words:
                raise AssertionError

        assert len(my_words) == len(their_words)
        assert time_difference < 1
        assert False

    def test_pypi_10_by_10(self):
        """Test 10x10 against the current boggle board on pypi."""
        import boggleboard
        other_default_size = 10
        letters = ['o', 'i', 's', 'r', 'l', 'm', 'i', 'e', 'a', 't',
         'g', 'e', 't', 'y', 'r', 'b', 'd', 's', 's', 'h',
         'f', 'r', 'h', 'r', 'a', 'e', 'd', 'g', 'l', 'u',
         'e', 'i', 'e', 'r', 's', 's', 'o', 'n', 'o', 'a',
         'o', 'd', 'e', 'g', 'a', 'o', 'e', 't', 's', 'm',
         'e', 'y', 's', 'e', 'e', 'b', 'i', 'd', 't', 'h',
         'y', 'm', 'i', 'r', 'p', 'c', 's', 'm', 'r', 'e',
         'b', 't', 'o', 'o', 'e', 'i', 'p', 's', 'r', 'u',
         's', 'l', 'w', 'o', 'k', 'l', 'c', 't', 's', 'l',
         'n', 'l', 'r', 'r', 'e', 'i', 'e', 's', 'g', 't']
        their_boggle = boggleboard.BoggleBoard(other_default_size, letters)
        their_trie = boggleboard.Trie(WORD_LIST)
        t1 = time.time()
        their_words = their_boggle.findWords(their_trie)
        t2 = time.time()
        their_solve_time = t2 - t1
        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)
        t1 = time.time()
        my_words = my_boggle.solve()
        t2 = time.time()
        my_solve_time = t2 - t1
        time_difference = my_solve_time / their_solve_time
        print('I found %s words.' % len(my_words))
        print('They found %s words.' % len(their_words))
        print('Mine is %s percent slower' % time_difference)
        print('My total time %s\nTheir total time %s' % (my_solve_time, their_solve_time))
        for word in their_words:
            if word not in my_words:
                print("I didn't find: %s" % word)
                if not my_boggle.edict.is_word(word):
                    raise AssertionError
                continue

        for word in my_words:
            if not word in their_words:
                raise AssertionError

        assert len(my_words) == len(their_words)
        assert time_difference < 1
        assert False

    def test_100x100_time(self):
        """Test 100x100 against the current boggle board on pypi."""
        import boggleboard
        other_default_size = 100
        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size)
        t1 = time.time()
        my_words = my_boggle.solve()
        t2 = time.time()
        my_solve_time = t2 - t1
        print('Found %s words.' % len(my_words))
        print('Took %s seconds to solve 100x100.' % my_solve_time)
        assert my_solve_time < 120
        assert False


if __name__ == '__main__':
    unittest.main()