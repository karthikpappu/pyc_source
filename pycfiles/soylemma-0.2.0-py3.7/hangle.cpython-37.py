# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soylemma/hangle.py
# Compiled at: 2019-09-27 13:55:26
# Size of source mod 2**32: 3194 bytes
import re
hangle_pattern = re.compile('[가-힣ㄱ-ㅎㅏ-ㅣ]+')
is_jaum = lambda c: 'ㄱ' <= c <= 'ㅎ'
is_moum = lambda c: 'ㅏ' <= c <= 'ㅣ'

def is_hangle(word):
    """
    Arguments
    ---------
    word : str

    Returns
    -------
    It returns True if all characters in the word are Hangle
    Else It returns False
    """
    match = hangle_pattern.match(word)
    if not match:
        return False
    span = match.span()
    return span[1] - span[0] == len(word)


def compose(cho, jung, jong):
    """
    Arguments
    ---------
    cho : str
        Chosung, length is 1
    jung : str
        Jungsung, length is 1
    jong : str
        Jongsung, length is 1

    Returns
    -------
    Composed hangle : str
    """
    cho_ = cho_to_idx.get(cho, -1)
    jung_ = jung_to_idx.get(jung, -1)
    jong_ = jong_to_idx.get(jong, -1)
    if cho_ < 0 or jung_ < 0 or jong_ < 0:
        return
    return chr(kor_begin + cho_base * cho_ + jung_base * jung_ + jong_)


def decompose(input, ensure_input=False):
    """
    Arguments
    ---------
    input : str
        Character, length is 1
    ensure_input : Boolean
        If True, pass length and hangle check

    Returns
    -------
    (cho, jung, jong) : tuple of str or None
        If input is hangle.
        Else it return None
    """
    if not ensure_input:
        return len(input) > 1 or is_hangle(input) or None
    if is_jaum(input):
        return (
         input, ' ', ' ')
    if is_moum(input):
        return (
         ' ', input, ' ')
    i = ord(input) - kor_begin
    cho = i // cho_base
    jung = (i - cho * cho_base) // jung_base
    jong = i - cho * cho_base - jung * jung_base
    return (chosungs[cho], jungsungs[jung], jongsungs[jong])


kor_begin = 44032
kor_end = 55203
cho_base = 588
jung_base = 28
jaum_begin = 12593
jaum_end = 12622
moum_begin = 12623
moum_end = 12643
chosungs = [
 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ',
 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ',
 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
jungsungs = [
 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ',
 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ',
 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
 'ㅣ']
jongsungs = [
 ' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ',
 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ',
 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ',
 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ',
 'ㅌ', 'ㅍ', 'ㅎ']
jaums = [
 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ',
 'ㄶ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㄺ',
 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ',
 'ㅀ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅄ',
 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
moums = [
 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ',
 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ',
 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
 'ㅣ']
cho_to_idx = {cho:idx for idx, cho in enumerate(chosungs)}
jung_to_idx = {jung:idx for idx, jung in enumerate(jungsungs)}
jong_to_idx = {jong:idx for idx, jong in enumerate(jongsungs)}