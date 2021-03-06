# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/capture-the-flag/capture-the-flag/ctf/pieces.py
# Compiled at: 2020-04-25 13:55:25
# Size of source mod 2**32: 1573 bytes
"""Pieces used in Capture The Flag (Ctf) game."""

class Piece(object):

    def __init__(self, idx, team, position):
        """This class initializes the storage of standard attributes,
        shared amongst the other pieces.

        Args:
            idx (:obj:`int`): Index of Piece.
            team (:obj:`int`): The team this piece belongs to.
            position (:obj:`tuple`): Location of the piece on the board.

        """
        self.idx = idx
        self.team = team
        self.position = position


class Unit(Piece):

    def __init__(self, idx, team, position, has_flag=False, in_jail=False):
        """Unit piece, representing a controllable character on the board.

        Args:
            has_flag (:obj:`bool`, optional): Whether or not the unit has the
                flag. Defaults to `False`.
            in_jail (:obj:`bool`, optional): Whether or not the unit is in
                jail. Defaults to `False`.

        """
        super().__init__(idx, team, position)
        self.has_flag = has_flag
        self.in_jail = in_jail


class Flag(Piece):

    def __init__(self, idx, team, position, grounded=True):
        """Flag piece, representing one of the team's flags.

        Args:
            grounded (:obj:`bool`, optional): Whether or not this flag is on
                the ground. `True` meaning this flag is on the ground,
                `False` meaning a unit is currently carrying this flag.
                Defaults to `True`.

        """
        super().__init__(idx, team, position)
        self.grounded = grounded