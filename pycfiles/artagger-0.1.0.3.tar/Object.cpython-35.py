# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/app/tagger/SCRDRlearner/Object.py
# Compiled at: 2017-01-18 02:22:01
# Size of source mod 2**32: 6136 bytes
import logging, copy

class Object:
    attributes = [
     'word',
     'tag',
     'prevWord2',
     'prevWord1',
     'nextWord1',
     'nextWord2',
     'prevTag2',
     'prevTag1',
     'nextTag1',
     'nextTag2',
     'suffixL2',
     'suffixL3',
     'suffixL4']
    code = 'def __init__(self'
    for att in attributes:
        code = code + ', ' + att + ' = None'

    code = code + '):\n'
    for att in attributes:
        code = code + '    self.' + att + '=' + att + '\n'

    exec(code)

    def toStr(self):
        res = '('
        for att in Object.attributes:
            boo = eval('isinstance(self. ' + att + ', str)')
            if not boo:
                res = res + str(eval('self.' + att))
            else:
                res = res + '"' + str(eval('self.' + att)) + '"'
            if att != Object.attributes[(len(Object.attributes) - 1)]:
                res = res + ','

        res += ')'
        return res


def getWordTag(wordTag):
    if wordTag == '///':
        return ('/', '/')
    index = wordTag.rfind('/')
    word = wordTag[:index].strip()
    tag = wordTag[index + 1:].strip()
    return (word, tag)


def getObject(wordTags, index):
    word, tag = getWordTag(wordTags[index])
    preWord1 = preTag1 = preWord2 = preTag2 = ''
    nextWord1 = nextTag1 = nextWord2 = nextTag2 = ''
    suffixL2 = suffixL3 = suffixL4 = ''
    decodedW = copy.copy(word)
    if len(decodedW) >= 4:
        suffixL3 = decodedW[-3:].encode('utf-8')
        suffixL2 = decodedW[-2:].encode('utf-8')
    if len(decodedW) >= 5:
        suffixL4 = decodedW[-4:].encode('utf-8')
    if index > 0:
        preWord1, preTag1 = getWordTag(wordTags[(index - 1)])
    if index > 1:
        preWord2, preTag2 = getWordTag(wordTags[(index - 2)])
    if index < len(wordTags) - 1:
        nextWord1, nextTag1 = getWordTag(wordTags[(index + 1)])
    if index < len(wordTags) - 2:
        nextWord2, nextTag2 = getWordTag(wordTags[(index + 2)])
    return Object(word, tag, preWord2, preWord1, nextWord1, nextWord2, preTag2, preTag1, nextTag1, nextTag2, suffixL2, suffixL3, suffixL4)


def getObjectDictionary(initializedCorpus, goldStandardCorpus):
    logger = logging.getLogger(__name__)
    goldStandardSens = open(goldStandardCorpus, 'r').readlines()
    initializedSens = open(initializedCorpus, 'r').readlines()
    objects = {}
    j = 0
    for i in xrange(len(initializedSens)):
        init = initializedSens[i].strip()
        if len(init) == 0:
            pass
        else:
            while j < len(goldStandardSens) and goldStandardSens[j].strip() == '':
                j += 1

            if j >= len(goldStandardSens):
                pass
            else:
                gold = goldStandardSens[j].strip()
                j += 1
                initWordTags = init.replace('“', "''").replace('”', "''").replace('"', "''").split()
                goldWordTags = gold.replace('“', "''").replace('”', "''").replace('"', "''").split()
                for k in xrange(len(initWordTags)):
                    initWord, initTag = getWordTag(initWordTags[k])
                    goldWord, correctTag = getWordTag(goldWordTags[k])
                    if initWord != goldWord:
                        logger.error('Raw texts extracted from the gold standard corpus and the initialized corpus are not the same!')
                        return
                    if initTag not in objects.keys():
                        objects[initTag] = {}
                        objects[initTag][initTag] = []
                    if correctTag not in objects[initTag].keys():
                        objects[initTag][correctTag] = []
                    objects[initTag][correctTag].append(getObject(initWordTags, k))

    return objects


class FWObject:
    __doc__ = '\n    RDRPOSTaggerV1.1: new implementation scheme\n    RDRPOSTaggerV1.2: add suffixes\n    '

    def __init__(self, check=False):
        self.context = [None, None, None, None, None, None, None, None, None, None, None, None, None]
        if check == True:
            i = 0
            while i < 10:
                self.context[i] = '<W>'
                self.context[i + 1] = '<T>'
                i = i + 2

            self.context[10] = '<SFX>'
            self.context[11] = '<SFX>'
            self.context[12] = '<SFX>'
        self.notNoneIds = []

    @staticmethod
    def getFWObject(startWordTags, index):
        object = FWObject(True)
        word, tag = getWordTag(startWordTags[index])
        object.context[4] = word
        object.context[5] = tag
        decodedW = copy.copy(word)
        if len(decodedW) >= 4:
            object.context[10] = decodedW[-2:].encode('utf-8')
            object.context[11] = decodedW[-3:].encode('utf-8')
        if len(decodedW) >= 5:
            object.context[12] = decodedW[-4:].encode('utf-8')
        if index > 0:
            preWord1, preTag1 = getWordTag(startWordTags[(index - 1)])
            object.context[2] = preWord1
            object.context[3] = preTag1
        if index > 1:
            preWord2, preTag2 = getWordTag(startWordTags[(index - 2)])
            object.context[0] = preWord2
            object.context[1] = preTag2
        if index < len(startWordTags) - 1:
            nextWord1, nextTag1 = getWordTag(startWordTags[(index + 1)])
            object.context[6] = nextWord1
            object.context[7] = nextTag1
        if index < len(startWordTags) - 2:
            nextWord2, nextTag2 = getWordTag(startWordTags[(index + 2)])
            object.context[8] = nextWord2
            object.context[9] = nextTag2
        return object