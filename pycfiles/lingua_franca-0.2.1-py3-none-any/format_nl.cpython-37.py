# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/format_nl.py
# Compiled at: 2019-12-13 05:20:21
# Size of source mod 2**32: 12237 bytes
from .format_common import convert_to_mixed_fraction
from math import floor
months = [
 'januari', 'februari', 'maart', 'april', 'mei', 'juni',
 'juli', 'augustus', 'september', 'oktober', 'november',
 'december']
NUM_STRING_NL = {0:'nul', 
 1:'één', 
 2:'twee', 
 3:'drie', 
 4:'vier', 
 5:'vijf', 
 6:'zes', 
 7:'zeven', 
 8:'acht', 
 9:'negen', 
 10:'tien', 
 11:'elf', 
 12:'twaalf', 
 13:'dertien', 
 14:'veertien', 
 15:'vijftien', 
 16:'zestien', 
 17:'zeventien', 
 18:'actien', 
 19:'negentien', 
 20:'twintig', 
 30:'dertig', 
 40:'veertig', 
 50:'vijftig', 
 60:'zestig', 
 70:'zeventig', 
 80:'tachtig', 
 90:'negentig', 
 100:'honderd'}
NUM_POWERS_OF_TEN = [
 '', 'duizend', 'miljoen', 'miljard', 'biljoen', 'biljard', 'triljoen',
 'triljard']
FRACTION_STRING_NL = {2:'half', 
 3:'derde', 
 4:'vierde', 
 5:'vijfde', 
 6:'zesde', 
 7:'zevende', 
 8:'achtste', 
 9:'negende', 
 10:'tiende', 
 11:'elfde', 
 12:'twaalfde', 
 13:'dertiende', 
 14:'veertiende', 
 15:'vijftiende', 
 16:'zestiende', 
 17:'zeventiende', 
 18:'achttiende', 
 19:'negentiende', 
 20:'twintigste'}
EXTRA_SPACE = ''

def nice_number_nl(number, speech, denominators=range(1, 21)):
    """ Dutch helper for nice_number
    This function formats a float to human understandable functions. Like
    4.5 becomes "4 einhalb" for speech and "4 1/2" for text
    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        return str(round(number, 3)).replace('.', ',')
    else:
        whole, num, den = result
        if not speech:
            if num == 0:
                return str(whole)
                return '{} {}/{}'.format(whole, num, den)
                if num == 0:
                    return str(whole)
                den_str = FRACTION_STRING_NL[den]
                if whole == 0:
                    if num == 1:
                        return_string = 'één {}'.format(den_str)
            else:
                return_string = '{} {}'.format(num, den_str)
        elif num == 1:
            return_string = '{} en één {}'.format(whole, den_str)
        else:
            return_string = '{} en {} {}'.format(whole, num, den_str)
    return return_string


def pronounce_number_nl(num, places=2):
    """
    Convert a number to its spoken equivalent
    For example, '5.2' would return 'five point two'
    Args:
        num(float or int): the number to pronounce (set limit below)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number

    """

    def pronounce_triplet_nl(num):
        result = ''
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                result += NUM_STRING_NL[hundreds] + EXTRA_SPACE + 'honderd' + EXTRA_SPACE
                num -= hundreds * 100
        if num == 0:
            result += ''
        else:
            if num <= 20:
                result += NUM_STRING_NL[num]
            else:
                if num > 20:
                    ones = num % 10
                    tens = num - ones
                    if ones > 0:
                        result += NUM_STRING_NL[ones] + EXTRA_SPACE
                        if tens > 0:
                            result += 'en' + EXTRA_SPACE
                    if tens > 0:
                        result += NUM_STRING_NL[tens] + EXTRA_SPACE
        return result

    def pronounce_fractional_nl(num, places):
        result = ''
        place = 10
        while places > 0:
            result += ' ' + NUM_STRING_NL[(int(num * place) % 10)]
            if int(num * place) % 10 == 1:
                result += ''
            place *= 10
            places -= 1

        return result

    def pronounce_whole_number_nl(num, scale_level=0):
        if num == 0:
            return ''
        num = floor(num)
        result = ''
        last_triplet = num % 1000
        if last_triplet == 1:
            if scale_level == 0:
                if result != '':
                    result += 'één'
                else:
                    result += 'één'
            elif scale_level == 1:
                result += 'één' + EXTRA_SPACE + 'duizend' + EXTRA_SPACE
            else:
                result += 'één ' + NUM_POWERS_OF_TEN[scale_level] + ' '
        elif last_triplet > 1:
            result += pronounce_triplet_nl(last_triplet)
            if scale_level == 1:
                result += 'duizend' + EXTRA_SPACE
            if scale_level >= 2:
                result += ' ' + NUM_POWERS_OF_TEN[scale_level] + ' '
            if scale_level >= 2:
                if scale_level % 2 == 0:
                    result += ''
                result += ''
        num = floor(num / 1000)
        scale_level += 1
        return pronounce_whole_number_nl(num, scale_level) + result + ''

    result = ''
    if abs(num) >= 1000000000000000000000000:
        return str(num)
    if num == 0:
        return str(NUM_STRING_NL[0])
    if num < 0:
        return 'min ' + pronounce_number_nl(abs(num), places)
    if num == int(num):
        return pronounce_whole_number_nl(num)
    whole_number_part = floor(num)
    fractional_part = num - whole_number_part
    result += pronounce_whole_number_nl(whole_number_part)
    if places > 0:
        result += ' komma'
        result += pronounce_fractional_nl(fractional_part, places)
    return result


def pronounce_ordinal_nl(num):
    ordinals = [
     'nulste', 'eerste', 'tweede', 'derde', 'vierde', 'vijfde',
     'zesde', 'zevende', 'achtste']
    if num < 0 or num != int(num):
        return num
    if num < 4:
        return ordinals[num]
    if num < 8:
        return pronounce_number_nl(num) + 'de'
    if num < 9:
        return pronounce_number_nl(num) + 'ste'
    if num < 20:
        return pronounce_number_nl(num) + 'de'
    return pronounce_number_nl(num) + 'ste'


def nice_time_nl(dt, speech=True, use_24hour=False, use_ampm=False):
    """
    Format a time to a comfortable human format

    For example, generate 'five thirty' for speech or '5:30' for
    text display.

    Args:
        dt (datetime): date to format (assumes already in local timezone)
        speech (bool): format for speech (default/True) or display (False)=Fal
        use_24hour (bool): output in 24-hour/military or 12-hour format
        use_ampm (bool): include the am/pm for 12-hour format
    Returns:
        (str): The formatted time string
    """
    if use_24hour:
        string = dt.strftime('%H:%M')
    else:
        if use_ampm:
            string = dt.strftime('%I:%M %p')
        else:
            string = dt.strftime('%I:%M')
        if string[0] == '0':
            string = string[1:]
        else:
            return speech or string
        speak = ''
        if use_24hour:
            speak += pronounce_number_nl(dt.hour)
            speak += ' uur'
            if not dt.minute == 0:
                speak += ' ' + pronounce_number_nl(dt.minute)
            return speak
        if dt.hour == 0:
            if dt.minute == 0:
                return 'Middernacht'
        hour = dt.hour % 12
        if dt.minute == 0:
            hour = fix_hour(hour)
            speak += pronounce_number_nl(hour)
            speak += ' uur'
        else:
            if dt.minute == 30:
                speak += 'half '
                hour += 1
                hour = fix_hour(hour)
                speak += pronounce_number_nl(hour)
            else:
                if dt.minute == 15:
                    speak += 'kwart over '
                    hour = fix_hour(hour)
                    speak += pronounce_number_nl(hour)
                else:
                    if dt.minute == 45:
                        speak += 'kwart voor '
                        hour += 1
                        hour = fix_hour(hour)
                        speak += pronounce_number_nl(hour)
                    else:
                        if dt.minute > 30:
                            speak += pronounce_number_nl(60 - dt.minute)
                            speak += ' voor '
                            hour += 1
                            hour = fix_hour(hour)
                            speak += pronounce_number_nl(hour)
                        else:
                            speak += pronounce_number_nl(dt.minute)
                            speak += ' over '
                            hour = fix_hour(hour)
                            speak += pronounce_number_nl(hour)
        if use_ampm:
            speak += nice_part_of_day_nl(dt)
        return speak


def fix_hour(hour):
    hour = hour % 12
    if hour == 0:
        hour = 12
    return hour


def nice_part_of_day_nl(dt):
    if dt.hour < 6:
        return " 's nachts"
    if dt.hour < 12:
        return " 's ochtends"
    if dt.hour < 18:
        return " 's middags"
    if dt.hour < 24:
        return " 's avonds"
    raise Exception('dt.hour is bigger than 24')


def nice_response_nl(text):
    words = text.split()
    for idx, word in enumerate(words):
        if word.lower() in months:
            text = nice_ordinal_nl(text)
        if word == '^':
            wordNext = words[(idx + 1)] if idx + 1 < len(words) else ''
            if wordNext.isnumeric():
                words[idx] = 'tot de macht'
                text = ' '.join(words)

    return text


def nice_ordinal_nl(text):
    normalized_text = text
    words = text.split()
    for idx, word in enumerate(words):
        wordNext = words[(idx + 1)] if idx + 1 < len(words) else ''
        wordPrev = words[(idx - 1)] if idx > 0 else ''
        if word[:-1].isdecimal():
            if wordNext.lower() in months:
                if wordPrev == 'de':
                    word = pronounce_ordinal_nl(int(word))
                else:
                    word = pronounce_number_nl(int(word))
            words[idx] = word

    normalized_text = ' '.join(words)
    return normalized_text